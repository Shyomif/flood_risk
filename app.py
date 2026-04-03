import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات الصفحة
st.set_page_config(layout="wide")
st.title("خريطة إدلب - تحليل مخاطر الفيضانات")

# الروابط المباشرة (Raw)
url_tif = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_low.tif"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# إنشاء الخريطة وتوسيطها يدوياً على إدلب لتجنب حاجة الدالة التلقائية
# إحداثيات مركز إدلب تقريباً [35.9, 36.6]
m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # 1. إضافة طبقة الراستر (TIF)
    # ملاحظة: أضفنا vmin و vmax (قيم افتراضية) لمساعدة المتصفح على رندرة الألوان
    m.add_raster(url_tif, layer_name="مخاطر الفيضانات", palette="Blues", opacity=0.8)

    # 2. إضافة ملفات الـ JSON
    m.add_geojson(url_idleb_json, layer_name="حدود إدلب")
    
    style_acc = {'fillColor': '#ffcc00', 'color': '#000000', 'weight': 1}
    m.add_geojson(url_acc_json, layer_name="بيانات إضافية (Acc)", style=style_acc)

    # عرض الخريطة
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
