import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة والعنوان
st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات - إدلب")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #1E88E5;'>نظام تحليل مخاطر الفيضانات التفاعلي</h1>
        <p style='font-size: 1.2em;'>منطقة الدراسة: محافظة إدلب - سوريا</p>
    </div>
    """, unsafe_allow_html=True)

# 2. وظيفة تحميل البيانات من Google Drive
@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        # الرابط المباشر للتحميل
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output, quiet=False)
    return output

# 3. معرفات الملفات (المعرف الجديد للملف الصغير + ملف الحدود)
TIF_ID = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' 
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    # تحميل الملفات إلى سيرفر Streamlit
    with st.spinner('جاري جلب البيانات الجغرافية...'):
        tif_path = download_data(TIF_ID, "flood_risk_final.tif")
        json_path = download_data(JSON_ID, "idleb_boundary.json")

    # 4. معالجة حدود المنطقة (Vector Data)
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # 5. إنشاء الخريطة التفاعلية
    # نستخدم خلفية قمر صناعي (Satellite) لتوضيح التضاريس
    m = leafmap.Map(
        google_map="SATELLITE", 
        center=[35.9, 36.6], 
        zoom=10
    )

    # 6. إضافة طبقة الخطر (Raster Data)
    # التعديلات: تدرج لوني RdYlGn_r، إخفاء القيم 0، شفافية 80%
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى خطورة الفيضان", 
        opacity=0.8
    )

    # 7. إضافة حدود محافظة إدلب
    m.add_gdf(
        gdf, 
        layer_name="حدود منطقة الدراسة", 
        style={'color': '#00FFFF', 'weight': 2, 'fillOpacity': 0}
    )

    # 8. إضافة أسماء المدن والقرى كطبقة علوية
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # 9. عرض الخريطة في تطبيق Streamlit
    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=750)

    # إضافة وسيلة إيضاح بسيطة
    st.info("💡 الألوان تتدرج من الأخضر (خطر منخفض) إلى الأحمر (خطر مرتفع).")

except Exception as e:
    st.error
