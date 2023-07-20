import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time

# 獲取用戶選擇的語言設置，預設為英文
language = st.session_state.get('language', 'en')

# 切換語言
def switch_language():
    global language
    language = 'zh' if language == 'en' else 'en'
    st.session_state.language = language

# 設置語言選項
def set_language():
    global language
    st.write("目前語言：" + ("中文" if language == "zh" else "English"))

    if st.button(translate_text("Switch Language", "切換語言")):
        switch_language()

# 中英文文字切換
def translate_text(text_en, text_zh):
    return text_zh if language == 'zh' else text_en

# Streamlit App
def main():
    global language

    st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    set_language()

    st.title(translate_text("Banner Generator", "橫幅生成器"))

    uploaded_file = st.file_uploader(translate_text("Upload Image", "上傳圖片"), type=['jpg', 'jpeg', 'png'])
    col1, col2 = st.columns([3, 7])
    with col1:
        form = st.form("processing_form")
        if uploaded_file is not None:
            # 添加選擇框來選擇處理選項
            processing_option = form.selectbox(translate_text("Choose Processing Option", "選擇處理選項"), ("預設", "自定義"))

            if processing_option == "自定義":
                # 添加滑動條以進行自定義設置
                with st.expander(translate_text("Remove Background Setting", "移除背景設置")):
                    alpha_matting_custom = {
                        "foreground_threshold": form.slider(translate_text("Alpha Matting Foreground Threshold", "Alpha Matting 前景閾值"), 0, 20, 9),
                        "background_threshold": form.slider(translate_text("Alpha Matting Background Threshold", "Alpha Matting 背景閾值"), 0, 20, 3),
                        "erode_size": form.slider(translate_text("Alpha Matting Erode Size", "Alpha Matting 侵蝕大小"), 0, 50, 17)
                    }
            else:
                alpha_matting_custom = None
            with st.expander
