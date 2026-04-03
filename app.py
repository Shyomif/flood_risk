import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات الصفحة
st.set_page_config(layout="wide")
st.title("خريطة إدلب - تحليل مخاطر الفيضانات")

# الرابط الجديد بصيغة Raw (الخام)
# لاحظ تغيير "github.com" إلى "raw.githubusercontent.com" وحذف كلمة "blob"
url_tif = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_low.tif"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# إنشاء الخريطة وتوسيطها مبدئياً
m = leafmap.Map(center=[35.9, 36.6], zoom=9)

try:
    # 1. إضافة طبقة الراستر (الرابط الجديد)
    # استخدمنا palette="terrain" أو "Blues" لإظهار القيم بشكل لوني واضح
    m.add_raster(url_tif, layer_name="مخاطر الفيضانات (الجديد)", palette="Blues", opacity=0.8)

    # 2. إضافة ملفات الـ JSON (الحدود والبيانات)
    m.add_geojson(url_idleb_json, layer_name="حدود إدلب")
    
    style_acc = {'fillColor': '#ffcc00', 'color': '#000000', 'weight': 1}
    m.add_geojson(url_acc_json, layer_name="بيانات إضافية (Acc)", style=style_acc)

    # سطر هام: الانتقال التلقائي لموقع طبقة الراستر للتأكد من ظهورها
    m.zoom_to_raster(url_tif)

    # عرض الخريطة في Streamlit
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
    st.info("تأكد من أن الملفات عامة (Public) على GitHub.")

# شريط جانبي للمعلومات
st.sidebar.success("تم تحديث رابط ملف التيف بنجاح.")
st.sidebar.write(f"اسم الملف الحالي: `flood_low.tif`")
