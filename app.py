import streamlit as st
import leafmap.foliumap as leafmap

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="خريطة مخاطر الفيضان")
st.title("خريطة خطر الفيضانات")

# 2. الروابط من GitHub
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# 3. إنشاء الخريطة
m = leafmap.Map(center=[35.9, 36.6], zoom=10)
m.add_basemap("Esri.WorldImagery")

try:
    # أ. حدود إدلب العامة (أبيض شفاف)
    m.add_geojson(
        url_idleb_json,
        layer_name="حدود إدلب",
        style={'color': '#000000', 'weight': 1.2, 'fillOpacity': 0}
    )

    # ب. حدود منطقة ACC (أصفر مقطع)
    m.add_geojson(
        url_acc_json,
        layer_name="مجرى النهر ACC",
        style={'color': '#0000ff', 'weight': 3, 'fillOpacity': 0, 'dashArray': '7, 7'}
    )

    # ج. طبقة المخاطر - ألوان مخصصة تشبه صورة الفيضان
    m.add_data(
        url_flood_json,
        column="DN",
        colors=[
            "#70a800",   # 1 - أخضر فاتح (خطر منخفض)
            "#fc8d59",   # 2 - أصفر (خطر متوسط)
            "#a8a800",   # 3 - برتقالي (خطر عالي)
            "#a8a800",   # 4 - برتقالي-أحمر
            "#a80000"    # 5 - أحمر غامق (خطر مرتفع جداً)
        ],
        layer_name="مستويات الخطر",
        scheme="Quantiles",
        k=5,
        legend_title="درجة الخطورة (منخفض → مرتفع)",
        fill_opacity=0.65,
        style_kwds={
            'weight': 0.8,
            'color': '#333333',      # لون الحدود بين المناطق
            'opacity': 0.6
        }
    )

    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ: {e}")

# 4. شريط جانبي محدث ومصحح
st.sidebar.markdown("""
### مفتاح الألوان (طبقة الفيضان):

- 🟢 **#91cf60** — خطر منخفض (آمن نسبيًا)  
- 🟡 **#fee08b** — خطر متوسط  
- 🟠 **#fc8d59** — خطر عالي  
- 🟠🔴 **#ef6548** — خطر مرتفع  
- 🔴 **#d7301f** — خطر مرتفع جداً (مناطق غمر شديد)

---

### عناصر الخريطة الأخرى:

- **حدود إدلب**: `#000000` (أسود) — خط رفيع  
- **حدود منطقة ACC**: `#00bfff` (أزرق سماوي) — خط مقطع  
- **الخلفية**: Esri World Imagery

---
**ملاحظة:**  
من عمل فريق Geo_Team
""")
