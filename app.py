import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات")

# دالة التحميل مع تجاوز قيود الحجم
@st.cache_data
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
        gdown.download(url, output, quiet=False, fuzzy=True)
    return output

TIF_ID = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    # تحميل الملفات للسيرفر السحابي
    tif_path = download_file(TIF_ID, "flood_risk.tif")
    json_path = download_file(JSON_ID, "idleb.json")

    # معالجة الحدود
    gdf = gpd.read_file(json_path)
    if gdf.crs is None or gdf.crs != "EPSG:4326":
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # --- الجزء الحاسم للملفات الضخمة ---
    # نستخدم add_raster ببارامترات تجعل المعالجة أخف على الرام
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة", 
        opacity=0.7
    )

    # إضافة الحدود والأسماء
    m.add_gdf(gdf, layer_name="حدود إدلب", style={'color': '#00FFFF', 'weight': 2, 'fillOpacity': 0})
    m.add_basemap("CartoDB.PositronOnlyLabels")
    
    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=750)

except Exception as e:
    st.error(f"حدث خطأ في المعالجة السحابية: {e}")
    st.info("نصيحة: إذا استمر عدم الظهور، فقد نحتاج لتحويل ملف TIF إلى صيغة COG لتخفيف الحمل عن السيرفر.")
