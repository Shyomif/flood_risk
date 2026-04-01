import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات - إدلب")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>خارطة مخاطر الفيضانات (ملفات ضخمة)</h2>", unsafe_allow_html=True)

# وظيفة متطورة لتحميل الملفات الكبيرة وتجاوز تحذير الفيروسات في درايف
@st.cache_data
def download_large_file(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}&confirm=t' # إضافة confirm=t للملفات الكبيرة
        gdown.download(url, output, quiet=False, fuzzy=True)
    return output

# معرفات الملفات الخاصة بك
TIF_ID = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    # تحميل الملفات (مع التعامل مع الحجم الكبير 300MB)
    with st.spinner('جاري تحميل بيانات الراستر الضخمة (300MB).. قد يستغرق دقيقة...'):
        tif_path = download_large_file(TIF_ID, "flood_risk.tif")
        json_path = download_large_file(JSON_ID, "idleb.json")

    # معالجة حدود المنطقة
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # إضافة طبقة الخطر
    # أضفنا ترسيم حدود القيم (vmin) وإخفاء الأصفار (nodata)
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة (النهر)", 
        opacity=0.8
    )

    # إضافة حدود المنطقة
    m.add_gdf(
        gdf, 
        layer_name="حدود إدلب", 
        style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0}
    )

    # إضافة أسماء المناطق فوق الطبقات
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # التركيز التلقائي
    m.zoom_to_gdf(gdf)

    # عرض الخريطة
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"فشل تحميل البيانات الضخمة: {e}")
    st.warning("تلميح: تأكد من أن ملف الـ TIF في Google Drive متاح لـ 'Anyone with the link'.")
