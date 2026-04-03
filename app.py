import streamlit as st
import leafmap.foliumap as leafmap
import requests
import os

st.set_page_config(layout="wide")
st.title("محلل مخاطر الفيضانات - إدلب والساحل")

# 1. الروابط المباشرة (Raw)
RASTER_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_risk_low.tif"
RIVERS_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
IDLEB_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# 2. تحميل الملف محلياً (ضروري جداً لضمان القراءة)
local_tif = "hazard_layer.tif"
if not os.path.exists(local_tif):
    with st.spinner("جاري جلب بيانات الخطر من السيرفر..."):
        r = requests.get(RASTER_URL)
        with open(local_tif, "wb") as f:
            f.write(r.content)

# 3. إعداد الخريطة
# تأكد من أن الإحداثيات [35.9, 36.6] هي مركز منطقة الدراسة فعلاً
m = leafmap.Map(center=[35.9, 36.6], zoom=10, google_map="HYBRID")

# 4. إضافة الطبقات المتجهية أولاً (للتأكد من أن الخريطة تعمل)
m.add_geojson(RIVERS_URL, layer_name="شبكة الأنهار", style={'color': 'blue', 'weight': 1.5})
m.add_geojson(IDLEB_URL, layer_name="حدود إدلب", style={'color': 'red', 'fillOpacity': 0, 'weight': 2})

# 5. محاولة إضافة الراستر بطريقة مستقرة
try:
    # نستخدم localtileserver لعرض الملف المحلي
    m.add_raster(
        local_tif, 
        layer_name="مستوى الخطر", 
        colormap="terrain", 
        opacity=0.7,
        nodata=0 # تجاهل القيم الصفرية إذا كانت تغطي الخريطة
    )
except Exception as e:
    st.error(f"فشل عرض طبقة الراستر: {e}")
    st.info("نصيحة: تأكد أن نظام إحداثيات الملف هو EPSG:4326")

# 6. عرض الخريطة
m.to_streamlit(height=700)
