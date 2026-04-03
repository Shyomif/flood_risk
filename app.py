import streamlit as st
import leafmap.foliumap as leafmap
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# 1. تحميل الملف ومعالجته برمجياً للتأكد من القيم
url_tif = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_low.tif"

m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # إضافة الطبقة مع تحديد vmin و vmax 
    # (إذا كانت قيم الفيضانات بين 0 و 1 مثلاً)
    m.add_raster(url_tif, layer_name="Flood Risk", palette="Blues", opacity=0.8, vmin=0, vmax=1)
    
    # إضافة الحدود للتأكد أن الخريطة في إدلب
    m.add_geojson("https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json", layer_name="إدلب")
    
    m.to_streamlit(height=700)
except:
    st.warning("الطبقة لم تظهر عبر الرابط المباشر، جرب الحل رقم 2 أدناه.")
