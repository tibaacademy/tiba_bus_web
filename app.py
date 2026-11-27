import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from PIL import Image, ImageDraw

def get_clean_circular_favicon(filename="Logo_3.jpg"):
    if not os.path.exists(filename):
        return None
    try:
        im = Image.open(filename).convert("RGBA")
        w, h = im.size
        # Find bounding box of non-white pixels (the navy outer circle of the logo)
        pixels = im.load()
        min_x, min_y, max_x, max_y = w, h, 0, 0
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if not (r > 235 and g > 235 and b > 235):
                    if x < min_x: min_x = x
                    if y < min_y: min_y = y
                    if x > max_x: max_x = x
                    if y > max_y: max_y = y
        if max_x > min_x and max_y > min_y:
            im = im.crop((min_x, min_y, max_x + 1, max_y + 1))
        size = min(im.size)
        im = im.resize((size, size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size - 1, size - 1), fill=255)
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.paste(im, (0, 0), mask)
        return out
    except Exception:
        return filename

st.set_page_config(
    page_title="TIBA Language Academy — Transportation System",
    page_icon=get_clean_circular_favicon("Logo_3.jpg"),
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
