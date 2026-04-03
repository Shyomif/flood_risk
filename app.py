import streamlit as st
import ee
import leafmap.foliumap as leafmap

# دالة لتهيئة Earth Engine سحابياً
def init_gee():
    if 'ee_initialized' not in st.session_state:
        try:
            # جلب المفاتيح من إعدادات Streamlit Secrets
            info = dict(st.secrets["gcp_service_account"])
            credentials = ee.ServiceAccountCredentials(info['client_email'], key_data=info['private_key'])
            ee.Initialize(credentials)
            st.session_state['ee_initialized'] = True
        except Exception as e:
            st.error(f"فشل الاتصال بـ Earth Engine: {e}")

init_gee()

# الآن يمكن لـ "المستخدم" إكمال بقية كود الخريطة والطبقات
m = leafmap.Map(center=[35.9, 36.6], zoom=10)
# ... أضف طبقات GitHub و GEE هنا
m.to_streamlit(height=700)
