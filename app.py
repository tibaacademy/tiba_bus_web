import streamlit as st
import streamlit.components.v1 as components
import base64
import os

page_icon_path = "Logo_3.jpg" if os.path.exists("Logo_3.jpg") else None

st.set_page_config(
    page_title="TIBA Languages Academy — Transportation System",
    page_icon=page_icon_path,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header[data-testid='stHeader'], section[data-testid='stSidebar'] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

def img_to_b64(filename, mime="image/jpeg"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_src = img_to_b64("Logo_3.jpg", "image/jpeg")
building_src = img_to_b64("IMG_0166.JPG", "image/jpeg")

with open("ui.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace("{{LOGO_SRC}}", logo_src)
html_code = html_code.replace("{{BUILDING_SRC}}", building_src)

# Inject the 9 Alexandria panoramic header images (1.png .. 9.png)
for i in range(1, 10):
    h_src = img_to_b64(f"{i}.png", "image/png")
    html_code = html_code.replace(f"{{{{HEADER_{i}}}}}", h_src)

components.html(html_code, height=980, scrolling=True)
