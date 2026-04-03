import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("محلل مخاطر الفيضانات - إدلب")

# الروابط المباشرة (Raw) التي تم استخراجها من مستودع المستخدم
RASTER_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_risk_low.tif"
RIVERS_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
IDLEB_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

m = leafmap.Map(center=[35.9, 36.6], zoom=10, google_map="HYBRID")

# إضافة طبقة الراستر باستخدام بروتوكول vsi
# استخدام محرك TiTiler الخارجي لمعالجة الرابط
# هذا الخيار هو الأضمن لظهور الملفات المرفوعة على GitHub
try:
    m.add_raster(
        RASTER_URL, 
        layer_name="مستوى الخطر", 
        colormap="Reds", 
        opacity=0.7
    )
except Exception as e:
    st.error(f"خطأ في عرض الطبقة: {e}")

# إضافة الطبقات المتجهية
m.add_geojson(RIVERS_URL, layer_name="شبكة الأنهار", style={'color': 'blue', 'weight': 1.5})
m.add_geojson(IDLEB_URL, layer_name="حدود إدلب", style={'color': 'red', 'fillOpacity': 0, 'weight': 2})

m.to_streamlit(height=700)
