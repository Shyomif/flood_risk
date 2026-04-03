import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات الصفحة
st.set_page_config(layout="wide")
st.title("خريطة إدلب - مخاطر الفيضانات والبيانات الجغرافية")

# --- تحويل روابط GitHub العادية إلى روابط Raw لتعمل برمجياً ---
# قمت بتعديل الروابط التي أرسلتها لتصبح روابط مباشرة (Raw)
url_tif = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_risk_low.tif"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# إنشاء الخريطة وتوسيطها على إدلب
m = leafmap.Map(center=[35.9, 36.6], zoom=9)

try:
    # 1. إضافة طبقة الراستر (TIF)
    # ملاحظة: إذا كان الملف ضخماً قد يستغرق ثوانٍ للتحميل
    m.add_raster(url_tif, layer_name="مخاطر الفيضانات (TIF)", colormap="Blues")

    # 2. إضافة طبقة idleb.json (غالباً حدود المنطقة)
    m.add_geojson(url_idleb_json, layer_name="حدود إدلب (JSON)")

    # 3. إضافة طبقة acc.json (البيانات الإضافية)
    # تخصيص لون مختلف لتمييزها
    style_acc = {'fillColor': '#ffcc00', 'color': '#ffcc00', 'fillOpacity': 0.5}
    m.add_geojson(url_acc_json, layer_name="بيانات Acc (JSON)", style=style_acc)

    # عرض الخريطة في Streamlit
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"خطأ في تحميل البيانات: {e}")
    st.info("تأكد من أن الملفات عامة (Public) على GitHub وأن حجم الـ TIF ليس ضخماً جداً.")

# إضافة معلومات في الشريط الجانبي
st.sidebar.info(f"""
**مكونات المشروع:**
- ملف الراستر: `flood_risk_low.tif`
- ملفات الحدود: `idleb.json` و `acc.json`
- المنطقة: إدلب، سوريا.
""")
