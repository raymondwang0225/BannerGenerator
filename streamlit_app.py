import cv2
import numpy as np
import streamlit as st

def find_largest_color_region(image):
    # 转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 设定颜色范围
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 40])
    
    # 创建颜色掩码
    mask = cv2.inRange(hsv_image, lower_black, upper_black)
    
    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 找到最大面积的轮廓
    max_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour
    
    # 创建黑色背景图像
    background = np.zeros_like(image)
    
    # 将最大面积的轮廓绘制到黑色背景图像上
    cv2.drawContours(background, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)
    
    # 计算最大面积的轮廓内的颜色平均值
    color = np.mean(image[largest_contour.squeeze()], axis=0)
    
    return background, color

def remove_background(image, target_color, threshold):
    # 转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 设定颜色范围
    color_lower = np.array([target_color[0] - threshold, 0, 0])
    color_upper = np.array([target_color[0] + threshold, 255, 255])
    
    # 创建背景掩码
    background_mask = np.zeros_like(image)
    cv2.inRange(hsv_image, color_lower, color_upper, background_mask)
    
    # 创建结果图像
    result = np.copy(image)
    
    # 将背景外的区域设为透明
    result[background_mask == 0] = [0, 0, 0, 0]
    
    return result

def main():
    st.title("背景去除")
    
    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # 读取上传的图像
        image = cv2.imread(uploaded_file)
        
        # 查找最大颜色区域并获取目标颜色
        background, target_color = find_largest_color_region(image)
        
        # 显示最大颜色区域和目标颜色
        st.subheader("最大颜色区域")
        st.image(background)
        
        st.subheader("目标颜色")
        st.write(target_color)
        
        # 指定背景去除的阈值
        threshold = st.slider("背景去除强度", 0, 255, 160)
        
        # 进行背景去除
        removed_background = remove_background(image, target_color, threshold)
        
        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(removed_background)

if __name__ == "__main__":
    main()
