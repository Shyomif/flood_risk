import streamlit as st
import leafmap.foliumap as leafmap

# إعدادات الصفحة
st.set_page_config(layout="wide")
st.title("تحليل هجين لمخاطر الفيضانات - إدلب")

# 1. تعريف الروابط
# رابط GeoJSON للمخاطر (GitHub)
url_flood_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"
# رابط GeoJSON لطبقة الحدود acc (GitHub)
url_acc_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
# رابط ملف الـ TIF من Google Drive (رابط تنزيل مباشر)
file_id = "1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw"
url_tif = f"https://docs.google.com/uc?export=download&id={file_id}"

# إنشاء الخريطة
m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # أ. إضافة طبقة الـ TIF الأصلية من Google Drive كخلفية (بكسلات)
    # ملاحظة: تعتمد سرعة ظهورها على حجم الملف وسرعة اتصال السيرفر
    m.add_raster(url_tif, layer_name="خريطة الراستر الأصلية (TIF)", opacity=0.4)

    # ب. إضافة طبقة الحدود acc (باللون الأسود أو الرمادي لتمييزها)
    style_acc = {
        "color": "#333333", 
        "weight": 2, 
        "fillOpacity": 0.1, 
        "dashArray": "5, 5" # خط مقطع للحدود
    }
    m.add_geojson(url_acc_json, layer_name="حدود منطقة ACC", style=style_acc)

    # ج. إضافة طبقة المخاطر بتدرج من الأخضر (آمن) إلى الأحمر (خطر)
    # نستخدم 'RdYlGn_r' لتعكس الألوان (Red-Yellow-Green Reversed)
    m.add_data(
        url_flood_json,
        column="DN",               # تأكد أن هذا هو اسم الحقل في ملف الـ JSON الخاص بك
        cmap="RdYlGn_r",           # التدرج المطلوب: الأحمر للمرتفع والأخضر للمنخفض
        layer_name="مستويات الخطر (متجه)",
        scheme="Quantiles",        # يتطلب مكتبة mapclassify
        k=5,                       # تقسيم الخطر إلى 5 درجات
        legend_title="درجة خطورة الفيضان",
        fill_opacity=0.7
    )

    # عرض الخريطة
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ في تحميل البيانات: {e}")
    st.info("تأكد من تثبيت المكتبات اللازمة: pip install mapclassify leafmap streamlit")

st.sidebar.markdown("""
### دليل الألوان:
- **الأخضر:** مخاطر منخفضة جداً.
- **الأصفر:** مخاطر متوسطة.
- **الأحمر:** مخاطر عالية جداً.
""")
