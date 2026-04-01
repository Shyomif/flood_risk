import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="محلل الفيضانات - إدلب")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>نظام تحليل مخاطر الفيضانات وشبكة الأنهار</h2>", unsafe_allow_html=True)

@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        # إضافة confirm=t لتجاوز فحص الفيروسات للملفات الكبيرة
        url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
        try:
            gdown.download(url, output, quiet=False, fuzzy=True)
        except Exception as e:
            st.error(f"فشل تحميل الملف {output}. تأكد من صلاحيات الرابط في درايف.")
            return None
    return output

# 2. معرفات الملفات الصحيحة
# ملاحظة: يجب استبدال ID_ACC بالمعرف الحقيقي لملف الأنهار من قوقل درايف
ID_FLOOD = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' 
ID_ACC = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy' # تأكد من هذا المعرف لملف الأنهار (acc)
ID_IDLEB = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI'

try:
    # تحميل الملفات
    flood_path = download_data(ID_FLOOD, "flood_risk.tif")
    acc_path = download_data(ID_ACC, "rivers_acc.tif")
    idleb_path = download_data(ID_IDLEB, "idleb_boundary.json")

    # إنشاء الخريطة
    m = leafmap.Map(google_map="SATELLITE")

    # 3. إضافة طبقة "صور الخطر" (تدرج أحمر-أصفر-أخضر)
    if flood_path:
        m.add_raster(
            flood_path, 
            palette="RdYlGn_r", 
            nodata=0, 
            vmin=1, 
            layer_name="مستوى الخطر", 
            opacity=0.7
        )

    # 4. إضافة طبقة "الأنهار" (تراكم الجريان باللون الأزرق)
    if acc_path:
        m.add_raster(
            acc_path, 
            palette="Blues", 
            nodata=0, 
            layer_name="شبكة الأنهار", 
            opacity=0.9
        )

    # 5. إضافة "الحدود"
    if idleb_path:
        gdf = gpd.read_file(idleb_path)
        m.add_gdf(
            gdf, 
            layer_name="حدود إدلب", 
            style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0}
        )

    # إضافة الأسماء
    m.add_basemap("CartoDB.PositronOnlyLabels")

    if idleb_path:
        m.zoom_to_gdf(gdf)
    
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ غير متوقع: {e}")
