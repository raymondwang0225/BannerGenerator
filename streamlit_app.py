import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time

# 获取用户选择的语言设置，预设为英文
language = st.session_state.get('language', 'en')

# 切换语言
def switch_language(selected_language):
    global language
    language = selected_language
    st.session_state.language = language

# 设置语言选项
def set_language():
    global language
   

    # 使用 st.selectbox 来选择语言
    selected_language = st.selectbox("選擇語言 / Select Language", ("English", "中文"))

    if selected_language != language:
        switch_language(selected_language)

# 中英文文字切换
def translate_text(text_en, text_zh):
    return text_zh if language == '中文' else text_en



def fix_image(upload, position, background_color, text, banner_size, text_size, text_color, text_position, alpha_matting_custom):
    image = Image.open(upload)

    if alpha_matting_custom:
        # 使用自定义参数来处理图像
        fixed = remove(
            image,
            alpha_matting=True,
            alpha_matting_foreground_threshold=alpha_matting_custom["foreground_threshold"],
            alpha_matting_background_threshold=alpha_matting_custom["background_threshold"],
            alpha_matting_erode_size=alpha_matting_custom["erode_size"]
        )
    else:
        # 使用预设参数来处理图像
        fixed = remove(image)

    # 缩放fixed图像至banner尺寸并保持比例
    fixed.thumbnail(banner_size)

    # 创建 Banner 图片
    banner_image = Image.new('RGBA', banner_size, background_color)
    banner_image.paste(fixed, position, fixed)

    # 在 Banner 图片上添加文字
    draw = ImageDraw.Draw(banner_image)
    font = ImageFont.truetype("Pixels.ttf", text_size)
    text_width, text_height = draw.textsize(text, font=font)
    text_position_x = text_position[0] - text_width / 2
    text_position_y = text_position[1] - text_height / 2
    draw.text((text_position_x, text_position_y), text, fill=text_color, font=font)

    return banner_image




# Streamlit App
def main():
    global language

    st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    scol1, scol2 = st.columns([3, 7])
    with scol1:
        set_language()
    

    st.title(translate_text("Banner Generator", "横幅生成器"))
    uploaded_file = st.file_uploader(translate_text("Upload Image", "上载图像"), type=['jpg', 'jpeg', 'png'])


    col1, col2 = st.columns([3, 7])
    with col1:
        
        if uploaded_file is not None:
            # 添加选择框来选择处理选项
            processing_option = st.selectbox(translate_text("Choose Processing Option", "选择处理选项"), (translate_text("Default", "预设"), translate_text("Custom", "自定义")))

            if processing_option == translate_text("Custom", "自定义"):
                # 添加滑动条以进行自定义设置
                with st.expander(translate_text("Remove Background Setting", "去除背景设置")):
                    alpha_matting_custom = {
                        "foreground_threshold": st.slider(translate_text("Alpha Matting Foreground Threshold", "Alpha合成前景阈值"), 0, 20, 9),
                        "background_threshold": st.slider(translate_text("Alpha Matting Background Threshold", "Alpha合成背景阈值"), 0, 20, 3),
                        "erode_size": st.slider(translate_text("Alpha Matting Erode Size", "Alpha合成边界"), 0, 50, 17)
                    }
            else:
                alpha_matting_custom = None
            with st.expander(translate_text("Banner Setting", "Banner设置")):
                # 指定背景颜色
                background_color = st.color_picker(translate_text("Choose Background Color", "选择背景颜色"), "#ffffff")
                # 指定图片位置
                banner_width = st.slider(translate_text("Banner Width", "Banner宽度"), 100, 1500, 1500)
                banner_height = st.slider(translate_text("Banner Height", "Banner高度"), 100, 500, 500)

            with st.expander(translate_text("Image Setting", "图片设置")):
                # 根据banner_size调整position的最大值和最小值
                position_x = st.slider(translate_text("Image Position(X)", "图片位置(X)"), -banner_height, banner_width, 100)
                position_y = st.slider(translate_text("Image Position(Y)", "图片位置(Y)"), -banner_height, banner_height, 50)
                position = (position_x, -position_y)

            with st.expander(translate_text("Text Setting", "文字设置")):
                # 指定Banner文字
                text = st.text_input(translate_text("Input Banner Text", "输入Banner文字"), "Bitcoin Frogs")
                # 指定Banner文字颜色
                text_color = st.color_picker(translate_text("Text Color", "文字颜色"), "#ffffff")
                # 指定Banner文字大小
                text_size = st.slider(translate_text("Text Size", "文字大小"), 8, 240, 120)
                # 指定Banner文字位置
                text_position_x = st.slider(translate_text("Text Position(X)", "文字位置(X)"), -banner_width, banner_width, 0)
                text_position_y = st.slider(translate_text("Text Position(Y)", "文字位置(Y)"), -banner_height, banner_height, 0)
                text_position = (text_position_x, -text_position_y)

            
    with col2:
        if uploaded_file is not None:
            # 指定Banner尺寸
            banner_size = (banner_width, banner_height)

            with st.spinner(translate_text('Image processing, please wait...', '图像处理中，请稍候...')):
                # 处理图像并显示进度
                # 生成Banner图像
                banner_image = fix_image(uploaded_file, position, background_color, text, banner_size, text_size, text_color, text_position, alpha_matting_custom)

            # 显示Banner图像
            st.image(banner_image)

            # 下载完成的图像
            buffered = BytesIO()
            banner_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            download_text = translate_text("Click to Download", "点击下载")
            href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">{download_text}</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
