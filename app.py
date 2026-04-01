import streamlit as st
import leafmap.foliumap as leafmap
import gdown
import os
import geopandas as gpd

# 1. إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام تحليل الفيضانات - إدلب")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #1E88E5;'>نظام تحليل مخاطر الفيضانات وشبكة الأنهار</h1>
        <p style='font-size: 1.1em;'>منطقة الدراسة: محافظة إدلب - سوريا</p>
    </div>
    """, unsafe_allow_html=True)

# 2. وظيفة تحميل البيانات مع تجاوز قيود الحجم (316MB)
@st.cache_data
def download_data(file_id, output):
    if not os.path.exists(output):
        # إضافة confirm=t ضرورية جداً للملفات الأكبر من 100MB لتجاوز تحذير قوقل
        url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
        try:
            gdown.download(url, output, quiet=False, fuzzy=True)
        except Exception as e:
            st.error(f"خطأ في تحميل {output}: {e}")
            return None
    return output

# 3. معرفات الملفات (المعرفات التي أرسلتها في الروابط)
ID_FLOOD = '1UNugklEQgWia_nSf-6KeWMkNlwG0AnKw' # صور الخطر (الملف الصغير)
ID_ACC = '15HLwgjj99QyErLu_BXacfKxDe0JxyKBy'   # شبكة الأنهار (الملف 316MB)
ID_IDLEB = '15XmVHfx3kiuomBxDqx19qry8qoH2m9bI' # حدود إدلب (JSON)

try:
    # تحميل الملفات إلى السيرفر
    with st.spinner('جاري جلب الطبقات الجغرافية (قد يستغرق وقتاً للملفات الضخمة)...'):
        flood_path = download_data(ID_FLOOD, "flood_risk_low.tif")
        acc_path = download_data(ID_ACC, "rivers_acc.tif")
        idleb_path = download_data(ID_IDLEB, "idleb.json")

    # 4. إنشاء الخريطة التفاعلية
    m = leafmap.Map(google_map="SATELLITE")

    # 5. إضافة طبقة "صور الخطر" (تدرج من الأخضر للأحمر)
    if flood_path:
        m.add_raster(
            flood_path, 
            palette="RdYlGn_r", 
            nodata=0, 
            vmin=1, 
            layer_name="مستوى الخطر", 
            opacity=0.7
        )

    # 6. إضافة طبقة "شبكة الأنهار" (تراكم الجريان باللون الأزرق)
    if acc_path:
        m.add_raster(
            acc_path, 
            palette="Blues", 
            nodata=0, 
            layer_name="شبكة الأنهار", 
            opacity=0.9
        )

    # 7. إضافة "الحدود" (بخط فوسفوري واضح)
    if idleb_path:
        gdf = gpd.read_file(idleb_path)
        if gdf.crs is None or gdf.crs != "EPSG:4326":
            gdf = gdf.set_crs("EPSG:4326", allow_override=True)
        
        m.add_gdf(
            gdf, 
            layer_name="حدود إدلب", 
            style={'color': '#00FFFF', 'weight': 3, 'fillOpacity': 0}
        )
        m.zoom_to_gdf(gdf)

    # 8. إضافة أسماء المناطق كطبقة علوية
    m.add_basemap("CartoDB.PositronOnlyLabels")

    # عرض الخريطة
    m.to_streamlit(height=800)

except Exception as e:
    st.error(f"حدث خطأ غير متوقع في بناء الخريطة: {e}")

st.info("💡 يمكنك التحكم في ظهور الطبقات من أيقونة الطبقات في أعلى يمين الخريطة.")
