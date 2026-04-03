import streamlit as st
import ee

def init_gee():
    if 'ee_initialized' not in st.session_state:
        try:
            # التحقق من وجود القسم الرئيسي
            if "gcp_service_account" in st.secrets:
                # تحويل Secrets إلى قاموس عادي لقراءته
                info = dict(st.secrets["gcp_service_account"])
                
                # التأكد من تنظيف المفتاح الخاص
                private_key = info['private_key'].replace("\\n", "\n").strip()
                
                credentials = ee.ServiceAccountCredentials(
                    info['client_email'], 
                    key_data=private_key
                )
                ee.Initialize(credentials)
                st.session_state['ee_initialized'] = True
                st.success("تم الاتصال بـ Earth Engine!")
            else:
                st.error("خطأ: لم يتم العثور على [gcp_service_account] في الإعدادات.")
        except Exception as e:
            st.error(f"فشل الاتصال: {e}")

init_gee()
