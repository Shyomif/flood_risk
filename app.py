import streamlit as st
import leafmap.foliumap as leafmap
import requests

st.set_page_config(layout="wide")
st.title("تطبيق هجين: بيانات شبكية (TIF) ومتجهة (JSON)")

# 1. روابط الملفات
# رابط الـ GeoJSON من GitHub (المتجه)
url_json = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/flood_decimal.json"

# رابط ملف الـ TIF من Google Drive 
# ملاحظة: تم تحويل الرابط لصيغة التنزيل المباشر
file_id = "1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw"
url_tif = f"https://docs.google.com/uc?export=download&id={file_id}"

m = leafmap.Map(center=[35.9, 36.6], zoom=10)

try:
    # إضافة الطبقة الشبكية (Raster) من درايف كخلفية دقيقة
    # ملاحظة: قد يتطلب عرض الـ TIF مباشرة وجود مكتبة localtileserver
    m.add_raster(url_tif, layer_name="خريطة المخاطر الأصلية (TIF)", opacity=0.5)

    # إضافة الطبقة المتجهة (Vector) من جيت هاب للتفاعل والتلوين
    m.add_data(
        url_json,
        column="DN",
        cmap="RdYlGn_r",
        layer_name="تحليل المضلعات (JSON)",
        legend_title="مستوى الخطر"
    )

    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"تنبيه: عرض ملف الـ TIF مباشرة من الرابط قد يحتاج لإعدادات COG.")
    st.info("يفضل تحويل الـ TIF إلى COG ورفعه على GitHub إذا كان الحجم صغيراً.")
