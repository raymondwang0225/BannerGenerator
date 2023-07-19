import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import streamlit as st


def remove_background(image_path, threshold):
    # 读取图像
    img = cv2.imread(image_path)

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 进行阈值处理来创建二值图像
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 使用形态学操作进行背景去除
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 将图像转换为PIL格式
    result = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    result.putalpha(mask)

    return result


# Streamlit App
def main():
    st.title("背景去除")

    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)

        # 指定背景去除的阈值
        threshold = st.slider("背景去除强度", 0, 255, 100)

        # 进行背景去除
        removed_background = remove_background(np.array(image), threshold)

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(removed_background)

        # 下载去除背景后的图像
        buffered = BytesIO()
        removed_background.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="removed_background.png">点击下载</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
