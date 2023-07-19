import cv2
import numpy as np
from PIL import Image
import streamlit as st

def find_largest_color_region(image, color):
    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    # 指定颜色的HSV范围（例如，蓝色）
    lower_color = np.array([h, s, v])  # 替换为所需颜色的下限阈值
    upper_color = np.array([h, s, v])  # 替换为所需颜色的上限阈值
    
    # 根据颜色范围创建掩码
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    # 使用形态学操作对掩码进行处理，去除噪点
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 查找图像中的轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 找到最大面积的轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 创建与原始图像相同大小的掩码图像
        region_mask = np.zeros_like(mask)
        
        # 将最大面积的轮廓填充到掩码图像中
        cv2.drawContours(region_mask, [largest_contour], -1, 255, cv2.FILLED)
        
        # 将掩码应用于原始图像，提取相同颜色区域
        color_region = cv2.bitwise_and(image, image, mask=region_mask)
        
        return color_region
    
    return None


def remove_background(image, color):
    # 将图像转换为OpenCV的BGR格式
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 根据颜色找到最大区域
    color_region = find_largest_color_region(cv_image, color)

    if color_region is not None:
        # 将图像转换回PIL格式
        result = Image.fromarray(cv2.cvtColor(color_region, cv2.COLOR_BGR2RGB))
        return result

    return None


# Streamlit App
def main():
    st.title("背景去除")
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)
        
        # 指定要去除的颜色（例如，蓝色）
        color = (h, s, v)  # 替换为所需颜色的HSV值
        
        # 进行背景去除
        removed_background = remove_background(image, color)
        
        if removed_background is not None:
            # 显示去除背景后的图像
            st.subheader("去除背景后的图像")
            st.image(removed_background)
        else:
            st.write("未找到指定颜色的区域")
    

if __name__ == "__main__":
    main()
