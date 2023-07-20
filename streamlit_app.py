import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time

# 獲取用戶選擇的語言設置，預設為英文
language = st.session_state.get('language', 'en')

# 設置語言選項
def set_language():
    global language
    st.write("目前語言：" + ("中文" if language == "zh" else "English"))

    if language == 'en':
        if st.button("中文"):
            language = 'zh'
    else:
        if st.button("English"):
            language = 'en'

    st.session_state.language = language

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
            with st.expander(translate_text("Banner Setting", "Banner 設置")):
                # 指定背景顏色
                background_color = form.color_picker(translate_text("Choose Background Color", "選擇背景顏色"), "#ffffff")
                # 指定圖片位置
                banner_width = form.slider(translate_text("Banner Width", "Banner 寬度"), 100, 1500, 1500)
                banner_height = form.slider(translate_text("Banner Height", "Banner 高度"), 100, 500, 500)

            with st.expander(translate_text("Image Setting", "圖片設置")):
                # 根據banner_size調整position的最大值和最小值
                position_x = form.slider(translate_text("Image Position(X)", "圖片位置(X)"), -banner_height, banner_width, 100)
                position_y = form.slider(translate_text("Image Position(Y)", "圖片位置(Y)"), -banner_height, banner_height, 50)
                position = (position_x, -position_y)

            with st.expander(translate_text("Text Setting", "文字設置")):
                # 指定Banner文字
                text = form.text_input(translate_text("Input Banner Text", "輸入Banner文字"), "比特幣青蛙")
                # 指定Banner文字顏色
                text_color = form.color_picker(translate_text("Text Color", "文字顏色"), "#ffffff")
                # 指定Banner文字大小
                text_size = form.slider(translate_text("Text Size", "文字大小"), 8, 240, 120)
                # 指定Banner文字位置
                text_position_x = form.slider(translate_text("Text Position(X)", "文字位置(X)"), -banner_width, banner_width, 0)
                text_position_y = form.slider(translate_text("Text Position(Y)", "文字位置(Y)"), -banner_height, banner_height, 0)
                text_position = (text_position_x, -text_position_y)

            submit_button = form.form_submit_button(translate_text("Apply Settings", "套用設置"))
    with col2:
        if uploaded_file is not None and submit_button:
            # 指定Banner尺寸
            banner_size = (banner_width, banner_height)

            with st.spinner(translate_text('Image processing, please wait...', '正在處理圖片，請稍等...')):
                # 處理圖片並顯示進度
                # 生成Banner圖片
                banner_image = fix_image(uploaded_file, position, background_color, text, banner_size, text_size, text_color, text_position, alpha_matting_custom)

            # 顯示Banner圖片
            st.image(banner_image)

            # 下載完成的圖片
            buffered = BytesIO()
            banner_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            download_text = translate_text("Click to Download", "點擊下載")
            href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">{download_text}</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
