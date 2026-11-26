import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 1. إعداد الصفحة
st.set_page_config(
    page_title="TIBA Language Academy - Bus Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الاتصال بقاعدة البيانات
def init_connection() -> Client:
    url = "https://mpxpysulrjcpqgrbrpah.supabase.co"
    key = "sb_publishable_F4BMccrJCjHVo9vyD_pRkw_yvKdIajE"
    return create_client(url, key)

supabase = init_connection()

# 3. إدارة الجلسة والمظهر (النهاري / الليلي)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# تنسيق CSS الرسمي
def apply_custom_css():
    bg_color = "#0f172a" if st.session_state.dark_mode else "#f8fafc"
    card_bg = "#1e293b" if st.session_state.dark_mode else "#ffffff"
    text_color = "#f1f5f9" if st.session_state.dark_mode else "#1e293b"
    border_color = "#334155" if st.session_state.dark_mode else "#cbd5e1"
    header_bg = "#1e3a8a" if not st.session_state.dark_mode else "#020617"

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            direction: rtl;
            text-align: right;
        }}
        .official-header {{
            background-color: {header_bg};
            color: #ffffff;
            padding: 18px 25px;
            border-radius: 6px;
            border-bottom: 4px solid #d97706;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .official-header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .official-header p {{
            margin: 4px 0 0 0;
            font-size: 14px;
            color: #e2e8f0;
        }}
        .stat-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-right: 4px solid #1
