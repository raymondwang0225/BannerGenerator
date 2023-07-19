import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import cv2
import numpy as np


def process_license_image(img):
    hh, ww = img.shape[:2]

    # 剪切掉周围的3个像素以去除外部白色边框
    img = img[3:hh-3, 3:ww-3]

    # 在周围添加3个黑色像素，并添加额外的10个像素作为后续形态学处理的缓冲区
    img = cv2.copyMakeBorder(img, 13, 13, 13, 13, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # 应用形态学操作以去除小的黑色斑点
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    hh2, ww2 = thresh.shape[:2]

    # 剪切掉周围的10个像素
    thresh = thresh[10:hh2-10, 10:ww2-10]

    # 获取最大的外轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big_contour = max(contours, key=cv2.contourArea)

    # 在黑色背景上绘制填充的轮廓
    mask = np.zeros_like(thresh)
    cv2.drawContours(mask, [big_contour], -1, (255), cv2.FILLED)

    # 使用遮罩将阈值化的许可证外部变为白色
    result = thresh.copy()
    result[mask == 0] = 255

    # 返回处理结果
    return thresh, mask, result

def fix_image(upload, position, background_color, text, banner_size, text_size, text_color, text_position):
    # 读取上传的图像
    img = cv2.imdecode(np.frombuffer(upload.read(), np.uint8), cv2.IMREAD_COLOR)

    # 进行背景去除
    thresh_image, _, _ = process_license_image(img)

    # 缩放上传的图像至banner尺寸并保持比例
    img = cv2.resize(img, banner_size)

    # 创建 Banner 图片
    banner_image = Image.new('RGB', banner_size, background_color)
    banner_image.paste(Image.fromarray(img), position, Image.fromarray(img))

    # 在 Banner 图片上添加文字
    draw = ImageDraw.Draw(banner_image)
    font = ImageFont.truetype("Pixels.ttf", text_size)
    text_width, text_height = draw.textsize(text, font=font)
    text_position_x = text_position[0] - text_width / 2
    text_position_y = text_position[1] - text_height / 2
    draw.text((text_position_x, text_position_y), text, fill=text_color, font=font)

    # 将背景去除后的图像覆盖到Banner上
    banner_image.paste(Image.fromarray(thresh_image), position, Image.fromarray(thresh_image))

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

    if uploaded_file is not None:
        col1, col2,col3 = st.columns(3,gap="large")
        with col1:
            st.subheader("Banner")
            # 指定背景颜色
            background_color = st.color_picker("Choose Background Color", "#ffffff")
            # 指定图片位置
            banner_width = st.slider("Banner Width", 100, 1000, 500)
            banner_height = st.slider("Banner Height", 100, 1000, 200)
            
        with col2:
            st.subheader("Image")
            # 根据banner_size调整position的最大值和最小值
            position_x = st.slider("Image Position(X)", -banner_height, banner_width, 100)
            position_y = st.slider("Image Position(Y)", -banner_height, banner_height, 50)
            position = (position_x, -position_y)

        with col3:
            st.subheader("Text")
            # 指定Banner文字
            text = st.text_input("Input Banner Text")
             # 指定Banner文字颜色
            text_color = st.color_picker("Text Color", "#000000")

            # 指定Banner文字大小
            text_size = st.slider("Text Size", 8, 120, 24)

            # 指定Banner文字位置
            text_position_x = st.slider("Text Position(X)", -banner_width, banner_width, 0)
            text_position_y = st.slider("Text Position(Y)", -banner_height, banner_height, 0)
            text_position = (text_position_x, -text_position_y)

        # 指定Banner尺寸
        banner_size = (banner_width, banner_height)

        # 生成Banner图片
        banner_image = fix_image(uploaded_file, position, background_color, text, banner_size, text_size, text_color, text_position)

        # 显示Banner图片
        st.image(banner_image)

        # 下载完成的图片
        buffered = BytesIO()
        banner_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">点击下载</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
