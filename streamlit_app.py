import cv2
import numpy as np
import streamlit as st
from PIL import Image


def find_largest_color_region(image):
    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 计算颜色直方图
    hist = cv2.calcHist([hsv_image], [0, 1], None, [180, 256], [0, 180, 0, 256])

    # 寻找最大直方图值对应的颜色
    h, s = np.unravel_index(np.argmax(hist), hist.shape)[:2]

    # 返回最大区域的颜色（HSV值）
    return h, s


def remove_background(image, threshold):
    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 获取最大区域的颜色（背景颜色）
    h, s = find_largest_color_region(hsv_image)

    # 设定颜色范围
    lower_color = np.array([h - threshold, 0, 0])
    upper_color = np.array([h + threshold, 255, 255])

    # 创建颜色遮罩
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # 对原始图像应用颜色遮罩
    result = cv2.bitwise_and(image, image, mask=mask)

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
        threshold = st.slider("背景去除强度", 0, 50, 10)

        # 将图像转换为OpenCV的BGR格式
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 进行背景去除
        removed_background = remove_background(cv_image, threshold)

        # 将去除背景后的图像转换为PIL格式
        result_image = Image.fromarray(cv2.cvtColor(removed_background, cv2.COLOR_BGR2RGB))

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(result_image)


if __name__ == "__main__":
    main()
