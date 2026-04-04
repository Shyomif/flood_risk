import streamlit as st
import leafmap.foliumap as leafmap

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="خريطة مخاطر إدلب")
st.title("تحليل مخاطر الفيضانات - إدلب (تدرج أخضر-أحمر)")

# 2. الروابط من GitHub
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# 3. إنشاء الخريطة
m = leafmap.Map(center=[35.9, 36.6], zoom=10)
m.add_basemap("Esri.WorldImagery")

try:
    # أ. حدود إدلب العامة
    m.add_geojson(
        url_idleb_json, 
        layer_name="حدود إدلب", 
        style={'color': '#ffffff', 'weight': 1.2, 'fillOpacity': 0}
    )

    # ب. حدود منطقة ACC (أصفر مقطع)
    m.add_geojson(
        url_acc_json, 
        layer_name="حدود منطقة ACC", 
        style={'color': '#ffff00', 'weight': 3, 'fillOpacity': 0, 'dashArray': '7, 7'}
    )

    # ج. طبقة المخاطر: تم إلغاء الأزرق باستخدام RdYlGn_r
    # يبدأ من الأخضر (قيم منخفضة) -> أصفر -> أحمر (قيم مرتفعة)
    m.add_data(
        url_flood_json,
        column="DN", 
        cmap="RdYlGn_r", 
        layer_name="مستويات الخطر",
        scheme="Quantiles", 
        k=5, 
        legend_title="درجة الخطورة",
        fill_opacity=0.7
    )

    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ: {e}")

# 4. شريط جانبي محدث
st.sidebar.markdown("""
### مفتاح الألوان الجديد:
- 🟢 **أخضر:** خطر منخفض (آمن).
- 🟡 **أصفر:** خطر متوسط.
- 🟠 **برتقالي:** خطر عالٍ.
- 🔴 **أحمر:** خطر مرتفع جداً.
---
*تم إزالة اللون الأزرق بناءً على الطلب.*
""")
