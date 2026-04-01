import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات - نسخة خفيفة")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>خارطة مخاطر الفيضانات التفاعلية (إدلب)</h2>", unsafe_allow_html=True)

# 2. وظيفة تحميل الملفات
@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output, quiet=False)
    return output

# معرفات الملفات (تم تحديث ملف الخطر للملف الصغير)
TIF_ID = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' 
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    with st.spinner('جاري تحميل الطبقات...'):
        tif_path = download_data(TIF_ID, "flood_risk_low.tif")
        json_path = download_data(JSON_ID, "idleb.json")

    # 3. قراءة الحدود
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # 4. إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # 5. إضافة طبقة الخطر (تدرج من الأخضر للأحمر مع إخفاء الصفر)
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة", 
        opacity=0.8
    )

    # 6. إضافة الحدود والأسماء
    m.add_gdf(gdf, layer_name="حدود إدلب", style={'color': '#00FFFF', 'weight': 2, 'fillOpacity': 0})
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # 7. ضبط الكاميرا والعرض
    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=750)

    st.success("✅ تم تحميل الطبقات بنجاح باستخدام النسخة الخفيفة.")

except Exception as e:
    st.error(f"حدث خطأ: {e}")
