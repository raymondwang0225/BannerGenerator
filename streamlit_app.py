import cv2
import numpy as np
import streamlit as st
from PIL import Image


def remove_background(image):
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用阈值处理将图像转换为二值图像
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个掩码图像，用于绘制物体轮廓
    mask = np.zeros_like(image)

    # 绘制物体轮廓到掩码图像
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # 使用掩码图像将背景置为白色
    result = cv2.bitwise_and(image, mask)

    return result


# Streamlit App
def main():
    st.title("物体轮廓提取和背景去除")

    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)

        # 将图像转换为OpenCV的BGR格式
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 进行背景去除
        removed_background = remove_background(cv_image)

        # 将去除背景后的图像转换为PIL格式
        result_image = Image.fromarray(cv2.cvtColor(removed_background, cv2.COLOR_BGR2RGB))

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(result_image)


if __name__ == "__main__":
    main()
