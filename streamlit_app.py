import cv2
import numpy as np
import streamlit as st
from PIL import Image


def remove_background(image, threshold):
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用阈值处理将图像转换为二值图像
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个掩码图像，用于绘制物体轮廓
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # 绘制物体轮廓到掩码图像
    cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

    # 反转掩码图像，使主体区域为黑色，背景区域为白色
    mask = cv2.bitwise_not(mask)

    # 将图像转换为带有透明通道的RGBA格式
    result = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

    # 使用掩码图像将背景区域设为透明
    result[mask == 255] = [0, 0, 0, 0]

    return result


def fill_color(image):
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 寻找轮廓
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大面积的轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 创建一个与图像形状相同的掩码图像
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # 绘制最大面积轮廓到掩码图像
    cv2.drawContours(mask, [max_contour], -1, 255, thickness=cv2.FILLED)

    # 使用掩码图像将除黑色像素和最大面积相同颜色的像素外，其余像素设为黑色
    result = image.copy()
    result[np.logical_and(mask != 0, result != [0, 0, 0])] = [0, 0, 0]

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

        # 指定背景去除的阈值
        threshold = st.slider("背景去除阈值", 0, 255, 160)

        # 进行背景去除
        removed_background = remove_background(cv_image, threshold)

        # 填充其他颜色为黑色
        filled_image = fill_color(removed_background)

        # 将去除背景并填充颜色后的图像转换为PIL格式
        result_image = Image.fromarray(filled_image)

        # 显示去除背景并填充颜色后的图像
        st.subheader("去除背景并填充颜色后的图像")
        st.image(result_image)


if __name__ == "__main__":
    main()
