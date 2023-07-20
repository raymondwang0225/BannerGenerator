import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time


def fix_image(upload, position, background_color, text, banner_size, text_size, text_color, text_position, alpha_matting_custom, progress):
    image = Image.open(upload)

    if alpha_matting_custom:
        # 使用自訂參數來處理圖像
        fixed = remove(
            image,
            alpha_matting=True,
            alpha_matting_foreground_threshold=alpha_matting_custom["foreground_threshold"],
            alpha_matting_background_threshold=alpha_matting_custom["background_threshold"],
            alpha_matting_erode_size=alpha_matting_custom["erode_size"]
        )
    else:
        # 使用預設參數來處理圖像
        fixed = remove(image)

    # 縮放fixed圖像至banner尺寸並保持比例
    fixed.thumbnail(banner_size)

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

    return banner_image


# Streamlit App
def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    st.title("Banner Generator")

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    col1,col2 = st.columns([3,7])
    if uploaded_file is not None:
        banner_width = 1500
        banner_height = 500
        with col1:
            # Add a selectbox for processing options
            processing_option = st.selectbox("Choose Processing Option", ("default", "customize"))

            if processing_option == "customize":
                with st.expander("Remove Background Setting"):
                    # Add sliders for custom settings
                    alpha_matting_custom = {
                        "foreground_threshold": st.slider("Alpha Matting Foreground Threshold", 0, 20, 9),
                        "background_threshold": st.slider("Alpha Matting Background Threshold", 0, 20, 3),
                        "erode_size": st.slider("Alpha Matting Erode Size", 0, 50, 17)
                    }
            else:
                alpha_matting_custom = None
            with st.expander("Banner Setting"):
                # 指定背景顏色
                background_color = st.color_picker("Choose Background Color", "#ffffff")
                # 指定圖片位置
                banner_width = st.slider("Banner Width", 100, 1500, 1500)
                banner_height = st.slider("Banner Height", 100, 500, 500)

            with st.expander("Image Setting"):
                # 根據banner_size調整position的最大值和最小值
                position_x = st.slider("Image Position(X)", -banner_height, banner_width, 100)
                position_y = st.slider("Image Position(Y)", -banner_height, banner_height, 50)
                position = (position_x, -position_y)

            with st.expander("Text Setting"):
                # 指定Banner文字
                text = st.text_input("Input Banner Text", "Bitcoin Frogs")
                # 指定Banner文字顏色
                text_color = st.color_picker("Text Color", "#ffffff")
                # 指定Banner文字大小
                text_size = st.slider("Text Size", 8, 240, 120)
                # 指定Banner文字位置
                text_position_x = st.slider("Text Position(X)", -banner_width, banner_width, 0)
                text_position_y = st.slider("Text Position(Y)", -banner_height, banner_height, 0)
                text_position = (text_position_x, -text_position_y)
        with col2:
            # 指定Banner尺寸
            banner_size = (banner_width, banner_height)

            progress_placeholder = st.empty()

            with st.spinner('Image processing, please wait...'):
                # 处理图片并显示进度
                # 生成Banner圖片
                banner_image = fix_image(uploaded_file, position, background_color, text, banner_size, text_size, text_color, text_position, alpha_matting_custom, progress_placeholder)

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
