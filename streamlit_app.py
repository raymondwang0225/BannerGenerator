import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont




def replace_white_with_transparent(image):
    # 将图像转换为RGBA模式，以支持透明度
    image = image.convert("RGBA")

    # 获取图像的像素数据
    data = image.getdata()

    # 创建一个新的像素列表，将白色像素替换为透明
    new_data = []
    for item in data:
        # 如果像素是白色，将其替换为透明
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))  # 设置透明度为0
        else:
            new_data.append(item)

    # 更新图像的像素数据
    image.putdata(new_data)

    return image


# Streamlit App
def main():
    st.title("Replace White with Transparent")

    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)

        # 替换白色为透明
        replaced_image = replace_white_with_transparent(image)

        # 显示替换后的图像
        st.subheader("替换后的图像")
        st.image(replaced_image)


if __name__ == "__main__":
    main()
