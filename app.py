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
    brand_primary = "#1e3a8a"
    brand_accent = "#d97706"
    bus_title_col = "#60a5fa" if dark else brand_primary

    css = (
        f"<style>"
        f"@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');"
        f"html, body, [class*='css'] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }}"
        f".stApp {{ background-color: {bg_main}; color: {text_primary}; }}"
        f"#MainMenu, footer, header[data-testid='stHeader'] {{ visibility: hidden; height: 0; }}"
        f"section[data-testid='stSidebar'] {{ display: none !important; }}"
        f".block-container {{ padding-top: 1.2rem !important; padding-bottom: 2rem !important; max-width: 1380px !important; }}"
        f".top-navbar {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: #ffffff; padding: 18px 28px; border-radius: 12px; border-bottom: 4px solid {brand_accent}; box-shadow: 0 4px 20px rgba(0,0,0,0.12); display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}"
        f".top-navbar h1 {{ margin: 0; font-size: 22px; font-weight: 800; color: #ffffff; }}"
        f".top-navbar p {{ margin: 2px 0 0 0; font-size: 13px; color: #cbd5e1; }}"
        f".user-badge {{ background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 13px; color: #f8fafc; }}"
        f".kpi-card {{ background-color: {surface}; border: 1px solid {border_col}; border-top: 4px solid {brand_primary}; border-radius: 10px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s ease; }}"
        f".kpi-card:hover {{ transform: translateY(-2px); }}"
        f".kpi-title {{ font-size: 13px; color: {text_secondary}; font-weight: 600; margin-bottom: 4px; }}"
        f".kpi-value {{ font-size: 26px; font-weight: 800; color: {text_primary}; }}"
        f".bus-card {{ background-color: {surface}; border: 1px solid {border_col}; border-radius: 12px; overflow: hidden; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}"
        f".bus-card-header {{ background-color: {surface_alt}; border-bottom: 1px solid {border_col}; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; }}"
        f".bus-title {{ font-size: 17px; font-weight: 800; color: {bus_title_col}; }}"
        f".bus-meta {{ font-size: 13px; color: {text_secondary}; font-weight: 600; }}"
        f"div.stButton > button {{ border-radius: 8px !important; font-weight: 700 !important; border: 1px solid {border_col} !important; transition: all 0.2s ease !important; padding: 0.45rem 1rem !important; }}"
        f"
