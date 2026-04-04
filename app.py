import streamlit as st
import leafmap.foliumap as leafmap

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="خريطة إدلب الهجينة - Esri Satellite")
st.title("تحليل مخاطر الفيضانات فوق صور الأقمار الصناعية (Esri)")

# 2. روابط الملفات من GitHub
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# 3. إنشاء الخريطة وتغيير الـ Basemap لأزري
m = leafmap.Map(center=[35.9, 36.6], zoom=10)
m.add_basemap("Esri.WorldImagery") # إضافة خرائط Esri القمرية

try:
    # أ. إضافة طبقة حدود إدلب (خط رفيع أبيض ليظهر فوق الصور الفضائية)
    m.add_geojson(
        url_idleb_json, 
        layer_name="حدود إدلب", 
        style={'color': '#ffffff', 'weight': 1.5, 'fillOpacity': 0}
    )

    # ب. إضافة طبقة حدود acc (بخط أصفر متوهج للتمييز)
    style_acc = {
        "color": "#ffff00", 
        "weight": 3, 
        "fillOpacity": 0, 
        "dashArray": "7, 7" 
    }
    m.add_geojson(url_acc_json, layer_name="حدود منطقة ACC", style=style_acc)

    # ج. إضافة طبقة المخاطر بتدرج من الأخضر للأحمر
    # تم تقليل الشفافية قليلاً (0.6) لتسمح برؤية معالم الأرض تحتها
    m.add_data(
        url_flood_json,
        column="DN", 
        cmap="RdYlGn_r", 
        layer_name="مستويات الخطر",
        scheme="Quantiles", 
        k=5, 
        legend_title="درجة الخطورة",
        fill_opacity=0.6
    )

    # 4. عرض الخريطة
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ: {e}")

# شريط جانبي
st.sidebar.info("الخلفية المستخدمة الآن هي Esri World Imagery لتقديم تفاصيل جغرافية واقعية.")
