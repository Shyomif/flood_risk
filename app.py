import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("خريطة إدلب - تدرج مخاطر الفيضانات")

# الروابط RAW
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # 1. طبقة حدود إدلب
    m.add_geojson(url_idleb_json, layer_name="حدود إدلب", style={'color': 'gray', 'weight': 1, 'fillOpacity': 0})

    # 2. طبقة ACC (باللون الأصفر)
    m.add_geojson(url_acc_json, layer_name="طبقة ACC", style={'fillColor': 'yellow', 'color': 'orange', 'fillOpacity': 0.4})

    # 3. طبقة المخاطر بتدرج من الأخضر للأحمر
    # استخدمنا 'RdYlGn_r' (الأحمر للقيم العالية والأخضر للمنخفضة)
    m.add_data(
        url_flood_json,
        column="DN", 
        cmap="RdYlGn_r", 
        layer_name="مستويات الخطر",
        scheme="Quantiles", # هذا يتطلب مكتبة mapclassify
        k=5, 
        legend_title="درجة الخطورة"
    )

    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"خطأ: {e}")
    st.info("تأكد من تثبيت 'pip install mapclassify' في بيئة العمل.")
