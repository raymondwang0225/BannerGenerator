import cv2
import numpy as np
from PIL import Image
import streamlit as st

def remove_background(image, threshold):
    # 将图像转换为OpenCV的BGR格式
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # 应用阈值处理来创建二值图像
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 使用形态学操作进行背景去除
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 将图像转换为PIL格式
    result = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    result.putalpha(128)

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
        removed_background = remove_background(image, threshold)

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(removed_background)


if __name__ == "__main__":
    main()
