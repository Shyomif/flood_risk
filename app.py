import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'> خريطة خطر الفيضانات</h2>", unsafe_allow_html=True)
st.markdown("---")

# 2. وظيفة تحميل الملفات
@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output, quiet=False)
    return output

TIF_ID = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    with st.spinner('جاري تحضير الطبقات والأسماء...'):
        tif_path = download_data(TIF_ID, "flood_risk.tif")
        json_path = download_data(JSON_ID, "idleb.json")

    # 3. معالجة الحدود
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # 4. إنشاء الخريطة بخلفية محايدة (أو قمر صناعي بدون أسماء)
    # استخدمنا 'SATELLITE' هنا لإظهار الأرض فقط بدون كتابة
    m = leafmap.Map(google_map="SATELLITE")

    # 5. إضافة طبقة الخطر (مع إخفاء الصفر "الأسود")
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة (النهر)", 
        opacity=0.8
    )

    # 6. إضافة حدود المحافظة
    m.add_gdf(
        gdf, 
        layer_name="حدود إدلب", 
        style={'color': '#00FFFF', 'weight': 2, 'fillOpacity': 0}
    )

    # 7. الإضافة السحرية: طبقة أسماء المناطق فقط (Labels Only)
    # هذه الطبقة ستضع أسماء المدن والقرى فوق طبقة الخطر
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # 8. ضبط الكاميرا
    m.zoom_to_gdf(gdf)

    # 9. عرض الخريطة
    m.to_streamlit(height=750)

    st.info("ℹ️ تم دمج أسماء المناطق فوق طبقة التحليل لسهولة التحديد المكاني.")

except Exception as e:
    st.error(f"حدث خطأ: {e}")
