import streamlit as st
import leafmap.foliumap as leafmap
import ee
import json

# دالة لتهيئة Earth Engine باستخدام Secrets
def initialize_ee():
    try:
        # جلب البيانات من Secrets
        credentials_dict = dict(st.secrets["gcp_service_account"])
        credentials = ee.ServiceAccountCredentials(credentials_dict['client_email'], key_data=credentials_dict['private_key'])
        ee.Initialize(credentials)
        return True
    except Exception as e:
        st.error(f"خطأ في الاتصال بـ GEE: {e}")
        return False

if initialize_ee():
    st.success("تم الاتصال بـ Google Earth Engine بنجاح!")
    
    # إعداد الخريطة
    m = leafmap.Map(center=[35.9, 36.6], zoom=10)

    # --- سحب طبقة من GEE (مثلاً نموذج الارتفاع الرقمي لـ إدلب) ---
    dem = ee.Image('USGS/SRTMGL1_003')
    vis_params = {'min': 0, 'max': 1000, 'palette': ['blue', 'green', 'red']}
    m.add_ee_layer(dem, vis_params, "GEE Elevation (SRTM)")

    # --- سحب البيانات الأخرى من GitHub ---
    RIVERS_URL = "https://raw.githubusercontent.com/Shyomif/flood_risk/main/acc.json"
    m.add_geojson(RIVERS_URL, layer_name="شبكة الأنهار (GitHub)")

    m.to_streamlit(height=700)
