import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TIBA Language Academy | Transportation System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def init_connection() -> Client:
    url = "https://mpxpysulrjcpqgrbrpah.supabase.co"
    key = "sb_publishable_F4BMccrJCjHVo9vyD_pRkw_yvKdIajE"
    return create_client(url, key)

supabase = init_connection()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "كشوف الباصات"

def inject_modern_ui():
    dark = st.session_state.dark_mode
    bg_main = "#0b1120" if dark else "#f1f5f9"
    surface = "#1e293b" if dark else "#ffffff"
    surface_alt = "#0f172a" if dark else "#f8fafc"
    text_primary = "#f8fafc" if dark else "#0f172a"
    text_secondary = "#94a3b8" if dark else "#475569"
    border_col = "#334155" if dark else "#e2e8f0"
    bus_title_col = "#60a5fa" if dark else "#1e3a8a"

    css_lines = [
        "<style>",
        "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');",
        "html, body, [class*='css'] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }",
        ".stApp { background-color: " + bg_main + "; color: " + text_primary + "; }",
        "#MainMenu, footer, header[data-testid='stHeader'] { visibility: hidden; height: 0; }",
        "section[data-testid='stSidebar'] { display: none !important; }",
        ".block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; max-width: 1380px
