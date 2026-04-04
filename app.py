import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات الصفحة
st.set_page_config(layout="wide")
st.title("خريطة تحليل مخاطر الفيضانات - إدلب")

# الروابط المباشرة (Raw) من GitHub
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# إنشاء الخريطة وتوسيطها على إدلب
m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # 1. إضافة طبقة حدود إدلب (للخلفية)
    m.add_geojson(url_idleb_json, layer_name="حدود إدلب", style={'color': '#aaaaaa', 'weight': 1, 'fillOpacity': 0})

    # 2. إضافة طبقة acc (باللون الأصفر مثلاً)
    style_acc = {'fillColor': '#ffff00', 'color': '#ffcc00', 'weight': 1, 'fillOpacity': 0.5}
    m.add_geojson(url_acc_json, layer_name="طبقة ACC", style=style_acc)

    # 3. إضافة طبقة مخاطر الفيضانات وتلوينها (من الأخضر للأحمر)
    # السر هنا في استخدام m.add_data وتحديد العمود واللوحة اللونية
    m.add_data(
        url_flood_json,
        column="DN",               # اسم الحقل الذي يحتوي على القيم الجغرافية (تأكد من اسمه في QGIS)
        cmap="RdYlGn_r",         # لوحة ألوان: Red-Yellow-Green (المعكوسة _r لتكون الأحمر للمرتفع)
        layer_name="مستويات خطر الفيضانات",
        k=5,                      # عدد التصنيفات الللونية (يمكنك زيادتها لدقة أكبر)
        legend_title="مستوى الخطر",
        fill_opacity=0.7
    )

    # عرض الخريطة في Streamlit
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الطبقات: {e}")
    st.info("تأكد من أن ملف `flood_decimal.json` يحتوي على حقل قيم (مثل DN) ومن أن الرابط يعمل.")

# شريط جانبي للمعلومات
st.sidebar.info("تم تحديث الخريطة لتشمل طبقة ACC وتلوين المخاطر بتدرج خطر.")
