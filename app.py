import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

st.set_page_config(layout="wide", page_title="محلل مخاطر الفيضانات")

@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, output, quiet=False)
    return output

# الروابط المحدثة (الملف الصغير والحدود)
TIF_ID = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' 
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    tif_path = download_data(TIF_ID, "flood_risk_small.tif")
    json_path = download_data(JSON_ID, "idleb.json")

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # إضافة طبقة الخطر (استخدام الطريقة الأكثر استقراراً للسحاب)
    m.add_raster(
        tif_path, 
        palette="RdYlGn_r", 
        nodata=0, 
        vmin=1, 
        layer_name="مستوى الخطورة"
    )

    # إضافة الحدود
    gdf = gpd.read_file(json_path)
    m.add_gdf(gdf, layer_name="حدود إدلب", style={'color': '#00FFFF', 'weight': 2, 'fillOpacity': 0})
    
    # إضافة الأسماء
    m.add_basemap("CartoDB.PositronOnlyLabels")

    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"خطأ تقني: {e}")
