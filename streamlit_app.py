import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np

def remove_background(image, background_color):
    # 将图像转换为NumPy数组
    image_array = np.array(image)

    # 获取图像的宽度和高度
    width, height = image.size

    # 将图像转换为RGBA模式，以支持透明度
    image = image.convert("RGBA")

    # 获取图像中的每个像素
    data = image.getdata()

    # 创建一个新的像素列表，根据背景颜色去除背景
    new_data = []
    for item in data:
        # 判断像素颜色是否与背景颜色完全匹配
        if item[:3] == background_color:
            # 将匹配的像素设置为透明
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    # 创建新的图像并返回
    new_image = Image.new("RGBA", (width, height))
    new_image.putdata(new_data)

    return new_image

# Streamlit App
def main():
    st.title("背景去除")

    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)

        # 显示图像和滴管工具
        background_color = st.image(image, use_column_width=True, caption="使用滴管工具选择背景颜色")
        background_color_picker = st.color_picker("选择背景颜色", value="#ffffff")

        # 当选择颜色后执行背景去除操作
        if st.button("去除背景"):
            # 获取选择的背景颜色
            selected_color = tuple(int(background_color_picker.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

            # 去除背景
            removed_background = remove_background(image, selected_color)

            # 显示去除背景后的图像
            st.subheader("去除背景后的图像")
            st.image(removed_background)

if __name__ == "__main__":
    main()
