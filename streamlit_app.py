import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont

def fix_image(upload, position, background_color, text, banner_size, text_size, text_color, text_position):
    image = Image.open(upload)
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
    st.title("Banner Generator")

    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png'])

    # 指定图片位置
    banner_width = st.slider("Banner宽度", 100, 1000, 500)
    banner_height = st.slider("Banner高度", 100, 1000, 200)

    # 指定背景颜色
    background_color = st.color_picker("选择背景颜色", "#ffffff")

    # 指定Banner文字
    text = st.text_input("输入Banner文字")

    # 指定Banner文字大小
    text_size = st.slider("文字大小", 8, 120, 24)

    # 指定Banner文字颜色
    text_color = st.color_picker("文字颜色", "#000000")

    # 指定Banner文字位置
    text_position_x = st.slider("文字位置 (X)", -banner_width, banner_width, 0)
    text_position_y = st.slider("文字位置 (Y)", -banner_height, banner_height, 0)
    text_position = (text_position_x, -text_position_y)

    if uploaded_file is not None:
        # 指定Banner尺寸
        banner_size = (banner_width, banner_height)

        # 生成Banner图片
        banner_image = fix_image(uploaded_file, (0, 0), background_color, text, banner_size, text_size, text_color, text_position)

        # 使用st.columns来排列元素
        col1, col2 = st.columns(2)
        col1.image(banner_image)

        # 下载完成的图片
        buffered = BytesIO()
        banner_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">点击下载</a>'
        col2.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
