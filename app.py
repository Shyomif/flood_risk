import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="محلل الفيضانات - إدلب")

st.title("نظام تحليل مخاطر الفيضانات وشبكة الأنهار")

@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
        gdown.download(url, output, quiet=False, fuzzy=True)
    return output

# المعرفات المستخرجة من سجلاتك (Logs)
ID_FLOOD = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' # ملف الخطر الصغير
ID_ACC = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'   # ملف الأنهار (316MB)
ID_IDLEB = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI' # ملف الحدود

try:
    # تحميل الملفات
    with st.spinner('جاري تحميل البيانات الجغرافية...'):
        flood_path = download_data(ID_FLOOD, "flood_risk_small.tif")
        acc_path = download_data(ID_ACC, "rivers_acc.tif")
        idleb_path = download_data(ID_IDLEB, "idleb.json")

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # 1. إضافة طبقة الخطر (الصغيرة)
    m.add_raster(flood_path, palette="RdYlGn_r", nodata=0, vmin=1, layer_name="مستوى الخطر", opacity=0.7)

    # 2. إضافة طبقة الأنهار (الكبيرة)
    # ملاحظة: قد تستغرق وقتاً للظهور بسبب حجمها (316MB)
    m.add_raster(acc_path, palette="Blues", nodata=0, layer_name="شبكة الأنهار", opacity=0.9)

    # 3. إضافة الحدود
    gdf = gpd.read_file(idleb_path)
    m.add_gdf(gdf, layer_name="حدود إدلب", style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0})

    # إضافة الأسماء
    m.add_basemap("CartoDB.PositronOnlyLabels")
    
    m.zoom_to_gdf(gdf)
    
    # عرض الخريطة باستخدام الطريقة الموصى بها في السجلات
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ: {e}")
