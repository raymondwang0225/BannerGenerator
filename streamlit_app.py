import cv2
import numpy as np
import streamlit as st
from PIL import Image


def find_largest_color_region(image):
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用阈值处理将图像转换为二值图像
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大的非黑色区域
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # 创建一个掩码图像，用于绘制最大非黑色区域
    mask = np.zeros_like(image)
    cv2.drawContours(mask, [max_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # 提取最大非黑色区域的颜色
    color = np.mean(image[mask == 255], axis=0)

    return color.astype(np.uint8)


def remove_background(image, target_color, threshold):
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

    # 创建一个背景范围的蒙版
    background_mask = np.zeros_like(image)

    # 将背景范围设定为与目标颜色接近的范围
    color_lower = target_color - threshold
    color_upper = target_color + threshold
    cv2.inRange(image, color_lower, color_upper, background_mask)

    # 将原始图像与背景范围蒙版进行按位与操作，仅保留指定颜色范围内的像素
    result = cv2.bitwise_and(image, background_mask)

    # 将掩码图像转换为灰度图像
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # 将掩码图像的灰度值作为透明度，将图像转换为带有透明通道的RGBA格式
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
    result[:, :, 3] = mask_gray

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

        # 找到除黑色区域之外的最大面积纯色
        target_color = find_largest_color_region(cv_image)

        # 指定背景去除的阈值
        threshold = st.slider("背景去除强度", 0, 255, 160)

        # 进行背景去除
        removed_background = remove_background(cv_image, target_color, threshold)

        # 将去除背景后的图像转换为PIL格式
        result_image = Image.fromarray(removed_background)

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(result_image)


if __name__ == "__main__":
    main()
