import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات واجهة الموقع
st.set_page_config(layout="wide")
st.title("لوحة تحكم البيانات الجغرافية - منطقة إدلب")

# --- روابط الملفات من GitHub (استبدل الروابط بروابطك الحقيقية) ---
# ملاحظة: يجب أن تبدأ الروابط بـ raw.githubusercontent.com
url_tif = "https://raw.githubusercontent.com/username/repo/main/flood_risk_low.tif"
url_json1 = "https://raw.githubusercontent.com/username/repo/main/layer1.json"
url_json2 = "https://raw.githubusercontent.com/username/repo/main/layer2.json"

# إنشاء الخريطة وتحديد المركز (إحداثيات إدلب تقريباً)
m = leafmap.Map(center=[35.9, 36.6], zoom=10)

# إضافة الطبقات بترتيب معين
try:
    # 1. إضافة طبقة الراستر (TIF) أولاً لتكون في الأسفل
    m.add_raster(url_tif, layer_name="مخاطر الفيضانات (Raster)", colormap="terrain")

    # 2. إضافة طبقة GeoJSON الأولى (مثلاً حدود المناطق)
    m.add_geojson(url_json1, layer_name="الطبقة المتجهة 1 (JSON)")

    # 3. إضافة طبقة GeoJSON الثانية (مثلاً نقاط أو مساحات معينة)
    # يمكنك تخصيص الألوان هنا
    style = {'fillColor': '#ff0000', 'color': '#ff0000'} 
    m.add_geojson(url_json2, layer_name="الطبقة المتجهة 2 (JSON)", style=style)

    # عرض الخريطة في Streamlit
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل إحدى الطبقات: {e}")
    st.info("تأكد من صحة روابط الـ Raw وحجم الملفات.")

# إضافة قائمة جانبية للمعلومات
st.sidebar.header("معلومات المشروع")
st.sidebar.write("هذا التطبيق يعرض بيانات التربة ومخاطر الفيضانات لمنطقة إدلب.")
