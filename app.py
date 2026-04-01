import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import gdown
import os

st.set_page_config(layout="wide")

# معرفات الملفات
TIF_ID = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'
JSON_ID = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

@st.cache_data
def get_file(file_id, name):
    url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
    if not os.path.exists(name):
        gdown.download(url, name, quiet=False)
    return name

try:
    # تحميل الحدود فقط (لأنها خفيفة)
    json_path = get_file(JSON_ID, "idleb.json")
    tif_path = get_file(TIF_ID, "flood_risk.tif") # سيحمله السيرفر في الخلفية

    m = leafmap.Map(google_map="SATELLITE")

    # الطريقة البديلة: استخدام محرك محلي للرندر (Local Tile Server)
    # هذه الإضافة تجعل السيرفر يعالج الملف كأجزاء صغيرة جداً
    m.add_raster(
        tif_path,
        palette="RdYlGn_r",
        nodata=0,
        vmin=1,
        layer_name="خطر الفيضان",
        opacity=0.8
    )

    # إضافة الحدود والأسماء
    gdf = gpd.read_file(json_path)
    m.add_gdf(gdf, layer_name="الحدود", style={'color': 'cyan', 'weight': 2, 'fillOpacity': 0})
    m.add_basemap("CartoDB.PositronOnlyLabels")

    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=750)

except Exception as e:
    st.error(f"خطأ: {e}")
