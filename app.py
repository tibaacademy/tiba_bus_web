import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TIBA Language Academy", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu, footer, header[data-testid='stHeader'], section[data-testid='stSidebar'] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

with open("ui.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=980, scrolling=True)
