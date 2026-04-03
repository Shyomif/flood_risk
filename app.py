import streamlit as st
import ee

def init_gee():
    if 'ee_initialized' not in st.session_state:
        try:
            # الوصول المباشر للقسم المحدد في Secrets
            if "gcp_service_account" in st.secrets:
                info = st.secrets["gcp_service_account"]
                
                # التحقق من وجود البريد الإلكتروني والمفتاح
                if "client_email" in info and "private_key" in info:
                    credentials = ee.ServiceAccountCredentials(
                        info["client_email"], 
                        key_data=info["private_key"]
                    )
                    ee.Initialize(credentials)
                    st.session_state['ee_initialized'] = True
                else:
                    st.error("المفاتيح 'client_email' أو 'private_key' مفقودة داخل Secrets")
            else:
                st.error("قسم [gcp_service_account] غير موجود في إعدادات Secrets")
        except Exception as e:
            st.error(f"خطأ في الاتصال بـ GEE: {e}")

init_gee()
