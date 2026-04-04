import streamlit as st
import leafmap.foliumap as leafmap

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="خريطة إدلب - تدرج خطر الفيضانات")
st.title("تحليل مخاطر الفيضانات في إدلب (نسخة الألوان المخصصة)")

# 2. روابط الملفات الخام (Raw) من GitHub
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
url_idleb_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/idleb.json"

# 3. إنشاء الخريطة وتغيير الـ Basemap لأزري
m = leafmap.Map(center=[35.9, 36.6], zoom=10)
m.add_basemap("Esri.WorldImagery") # إضافة خرائط Esri القمرية

try:
    # أ. إضافة حدود إدلب العامة (خلفية بيضاء رفيعة)
    m.add_geojson(
        url_idleb_json, 
        layer_name="حدود إدلب", 
        style={'color': '#ffffff', 'weight': 1.5, 'fillOpacity': 0}
    )

    # ب. إضافة طبقة الحدود acc (بخط أصفر مقطع)
    style_acc = {
        "color": "#ffff00", 
        "weight": 3, 
        "fillOpacity": 0, 
        "dashArray": "7, 7" 
    }
    m.add_geojson(url_acc_json, layer_name="حدود منطقة ACC", style=style_acc)

    # ج. إضافة طبقة المخاطر مع تدرج الألوان المخصص (نسخ من الصورة)
    # السر هنا في استخدام 'add_data' وتحديد لوحة ألوان مخصصة
    # [السماوي، الأخضر، الأصفر، البرتقالي، الأحمر]
    custom_palette = ['#00FF00', '#FFFF00', '#FFA500', '#FF0000']
    
    m.add_data(
        url_flood_json,
        column="DN",               # حقل القيم (تأكد من اسمه في الملف)
        cmap=custom_palette,       # استخدام اللوحة اللونية المخصصة
        layer_name="مستويات الخطر (التدرج المخصص)",
        scheme="Quantiles",        # يتطلب mapclassify
        k=5,                       # تقسيم الخطر لـ 5 درجات
        legend_title="درجة الخطورة",
        fill_opacity=0.7
    )

    # 4. عرض الخريطة
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ: {e}")
    st.info("تأكد من تثبيت 'mapclassify' و 'leafmap' و 'streamlit' و 'geopandas'.")

# 5. شريط جانبي لشرح الألوان
st.sidebar.markdown(f"""
### مفتاح الألوان (نسخ من الصورة):
- 🟢 **أخضر:** خطر منخفض.
- 🟡 **أصفر:** خطر متوسط.
- 🟠 **برتقالي:** خطر عالٍ.
- 🔴 **أحمر:** خطر مرتفع جداً.
- **الخط المقطع الأصفر:** حدود منطقة **ACC**.
""")
