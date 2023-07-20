import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time


def fix_image(upload,scale_ratio, position, background_color, text, banner_size, text_size, text_color, text_position,progress):
    image = Image.open(upload)
    fixed = remove(image, alpha_matting=True, alpha_matting_foreground_threshold=9, alpha_matting_background_threshold=3, alpha_matting_erode_size=17)

    # 縮放fixed圖像至banner尺寸並保持比例
    fixed.thumbnail(banner_size)
     # Resize the image proportionally based on the scale_ratio
    new_width = int(fixed.width * scale_ratio)
    new_height = int(fixed.height * scale_ratio)
    fixed = fixed.resize((new_width, new_height))
    # 創建 Banner 圖片
    banner_image = Image.new('RGBA', banner_size, background_color)
    banner_image.paste(fixed, position, fixed)

    # 在 Banner 圖片上添加文字
    draw = ImageDraw.Draw(banner_image)
    font = ImageFont.truetype("Pixels.ttf", text_size)
    text_width, text_height = draw.textsize(text, font=font)
    text_position_x = text_position[0] - text_width / 2
    text_position_y = text_position[1] - text_height / 2
    draw.text((text_position_x, text_position_y), text, fill=text_color, font=font)

     # 模拟图片处理过程
    for i in range(1, 6):
        progress.progress(i * 20)  # 更新进度条，每次增加20%
        time.sleep(0.5)

    return banner_image


# Streamlit App
def main():
    #st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title("Banner Generator")

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    #if uploaded_file is not None:
    with st.expander("Banner Setting"):
        #st.sidebar.subheader("Banner")
        # 指定背景顏色
        background_color = st.sidebar.color_picker("Choose Background Color", "#ffffff")
        # 指定圖片位置
        banner_width = st.sidebar.slider("Banner Width", 100, 1500, 1500)
        banner_height = st.sidebar.slider("Banner Height", 100, 500, 500)
    
    with st.expander("Image Setting"):
        #st.sidebar.subheader("Image")
        image_scale = st.sidebar.slider("Image Scale Ratio", 0.1, 3.0, 1.0)
        # 根據banner_size調整position的最大值和最小值
        position_x = st.sidebar.slider("Image Position(X)", -banner_height, banner_width, 100)
        position_y = st.sidebar.slider("Image Position(Y)", -banner_height, banner_height, 50)
        position = (position_x, -position_y)

    with st.expander("Text Setting"):
        #st.sidebar.subheader("Text")
        # 指定Banner文字
        text = st.sidebar.text_input("Input Banner Text","Bitcoin Frogs")
        # 指定Banner文字顏色
        text_color = st.sidebar.color_picker("Text Color", "#ffffff")

        # 指定Banner文字大小
        text_size = st.sidebar.slider("Text Size", 8, 240, 120)

        # 指定Banner文字位置
        text_position_x = st.sidebar.slider("Text Position(X)", -banner_width, banner_width, 0)
        text_position_y = st.sidebar.slider("Text Position(Y)", -banner_height, banner_height, 0)
        text_position = (text_position_x, -text_position_y)

    # 指定Banner尺寸
    banner_size = (banner_width, banner_height)

    

    

    progress_placeholder = st.empty()
    
    with st.spinner('Image processing, please wait...'):
        # 处理图片并显示进度
        # 生成Banner圖片
        banner_image = fix_image(uploaded_file, image_scale, position, background_color, text, banner_size, text_size, text_color, text_position,progress_placeholder)
    # 顯示Banner圖片
    st.image(banner_image)

    # 下載完成的圖片
    buffered = BytesIO()
    banner_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">Click to Download</a>'
    st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
