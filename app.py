import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات")

st.markdown("<h2 style='text-align: center;'>خارطة مخاطر الفيضانات - إدلب</h2>", unsafe_allow_html=True)

# دالة محسنة للتحميل من قوقل درايف لضمان العمل على السحاب
@st.cache_data
def download_data(file_id, output):
    url = f'https://drive.google.com/uc?id={file_id}'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False, fuzzy=True)
    return output

# معرفات الملفات (تأكد أنها عامة Anyone with the link في درايف)
TIF_ID = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    # تحميل الملفات
    tif_path = download_data(TIF_ID, "flood_risk.tif")
    json_path = download_data(JSON_ID, "idleb.json")

    # قراءة الحدود والتأكد من الإحداثيات
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # إضافة طبقة الخطر (تأكد من استخدام nodata=0 لإخفاء الأسود)
    # ملاحظة: استخدمنا طريقة add_raster المستقرة للسحاب
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة", 
        opacity=0.8
    )

    # إضافة الحدود بلون واضح جداً
    m.add_gdf(
        gdf, 
        layer_name="حدود إدلب", 
        style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0}
    )

    # إضافة الأسماء فوق كل شيء
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # التركيز على المنطقة
    m.zoom_to_gdf(gdf)

    # عرض الخريطة
    m.to_streamlit(height=750)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الطبقات: {e}")
    st.info("تأكد من أن ملفات Google Drive منضبطة على خيار 'Anyone with the link'")
