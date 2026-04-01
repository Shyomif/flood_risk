import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="محلل الفيضانات - إدلب")

st.markdown("<h2 style='text-align: center;'>نظام تحليل مخاطر الفيضانات وشبكة الأنهار</h2>", unsafe_allow_html=True)

@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output, quiet=False)
    return output

# 2. معرفات الملفات (تأكد من وضع الـ IDs الصحيحة من درايف هنا)
ID_FLOOD = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' # ملف صور الخطر
ID_ACC = 'ضع_هنا_ID_ملف_الأنهار'              # ملف الأنهار (acc)
ID_IDLEB = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI' # ملف الحدود

try:
    # تحميل الملفات
    flood_path = download_data(ID_FLOOD, "flood_risk.tif")
    acc_path = download_data(ID_ACC, "rivers_acc.tif")
    idleb_path = download_data(ID_IDLEB, "idleb_boundary.json")

    # 3. إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # 4. إضافة طبقة "صور الخطر" (تدرج أحمر-أصفر-أخضر)
    m.add_raster(
        flood_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطر", 
        opacity=0.7
    )

    # 5. إضافة طبقة "الأنهار" (باللون الأزرق لتمييزها)
    m.add_raster(
        acc_path, 
        palette="Blues", 
        nodata=0, 
        layer_name="شبكة الأنهار (التراكم)", 
        opacity=0.9
    )

    # 6. إضافة "الحدود" (بخط فوسفوري واضح)
    gdf = gpd.read_file(idleb_path)
    m.add_gdf(
        gdf, 
        layer_name="حدود إدلب", 
        style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0}
    )

    # 7. إضافة الأسماء فوق كل شيء
    m.add_basemap("CartoDB.PositronOnlyLabels")

    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الطبقات: {e}")
