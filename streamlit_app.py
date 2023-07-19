import streamlit as st
import cv2
import numpy as np

def process_image(image, color_tolerance):
    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 计算图像中每个颜色的像素数
    hist = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])
    
    # 找到颜色频次最高的色相
    dominant_color_hue = np.argmax(hist)
    
    # 根据色相和容差计算颜色范围
    lower_color = np.array([dominant_color_hue - color_tolerance, 100, 100])
    upper_color = np.array([dominant_color_hue + color_tolerance, 255, 255])
    
    # 创建一个掩码来标记在颜色范围内的像素
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    # 计算掩码中最大连通区域的面积和位置
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour = max(contours, key=cv2.contourArea)
    _, _, width, height = cv2.boundingRect(max_contour)
    max_area = width * height
    
    # 根据最大连通区域的位置创建一个新的掩码
    new_mask = np.zeros_like(mask)
    cv2.drawContours(new_mask, [max_contour], 0, (255), -1)
    
    # 将新的掩码应用于图像，将最大连通区域以外的像素设置为透明
    image[new_mask == 0, :] = [0, 0, 0, 0]  # 设置透明像素的颜色






    
    return image

def main():
    st.title("图像处理")
    
    # 创建一个上传文件的组件
    uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # 读取上传的图像
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        
        # 显示原始图像
        #st.image(image, channels="BGR", caption="原始图像")
        
        # 创建一个滑动条，用于控制容差
        color_tolerance = st.slider("容差", 0, 50, 10)
        
        # 处理图像
        processed_image = process_image(image, color_tolerance)
        
        # 显示处理后的图像
        st.image(processed_image, channels="BGR", caption="处理后的图像")

if __name__ == "__main__":
    main()
