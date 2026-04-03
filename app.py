import streamlit as st
import leafmap.foliumap as leafmap
import requests
import os

# التأكد من وجود المكتبات الأساسية
try:
    import psutil
    import localtileserver
except ImportError:
    st.error("يرجى تثبيت psutil و localtileserver عبر pip install")

st.set_page_config(layout="wide")

# الروابط الصحيحة (Raw)
RASTER_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_risk_low.tif"

# تحميل الملف لضمان استقرار العرض
local_tif = "hazard_layer.tif"
if not os.path.exists(local_tif):
    response = requests.get(RASTER_URL)
    with open(local_tif, "wb") as f:
        f.write(response.content)

m = leafmap.Map(center=[35.9, 36.6], zoom=10)

# عرض الراستر
try:
    m.add_raster(local_tif, layer_name="نطاق الخطر", colormap="RdYlGn_r", opacity=0.7)
except Exception as e:
    st.error(f"فشل عرض الراستر: {e}")

m.to_streamlit(height=700)
