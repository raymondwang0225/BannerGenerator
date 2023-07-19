import streamlit as st
import cv2
import numpy as np

def process_image(image, tolerance):
    # 將圖片轉換為RGBA格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    
    # 將圖片轉換為灰度圖像
    gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    
    # 執行二值化處理，將圖像轉換為二值圖像
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # 找到圖像中的輪廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 找到面積最大的輪廓
    max_contour = max(contours, key=cv2.contourArea)
    
    # 創建一個與原始圖像相同大小的遮罩
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # 在遮罩上繪製面積最大的輪廓
    cv2.drawContours(mask, [max_contour], -1, 255, thickness=cv2.FILLED)
    
    # 使用形態學操作對遮罩進行膨脹，填充輪廓周圍的區域
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    mask = cv2.dilate(mask, kernel)
    
    # 應用遮罩以僅保留面積最大的區域
    image = cv2.bitwise_and(image, image, mask=mask)
    
    # 計算各個顏色的像素數量
    unique_colors, counts = np.unique(image.reshape(-1, 4), axis=0, return_counts=True)
    
    # 找到佔比最大的顏色
    max_color = unique_colors[np.argmax(counts)]
    
    # 將該顏色設置為透明
    mask = np.all(np.abs(image - max_color) <= tolerance, axis=2)
    image[mask] = [0, 0, 0, 0]
    
    return image

def main():
    st.title("圖片處理應用")
    
    # 上傳圖片
    uploaded_file = st.file_uploader("選擇一張圖片", type=["jpg", "jpeg", "png"])
    
    # 容忍度滑桿
    tolerance = st.slider("容忍度", min_value=0, max_value=500, value=10)
    
    if uploaded_file is not None:
        # 讀取上傳的圖片
        image = np.array(cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1))
        
        # 顯示原始圖片
        #st.image(image, caption="原始圖片", use_column_width=True)
        
        # 處理圖片，傳遞容忍度參數
        processed_image = process_image(image, tolerance)
        
        # 顯示處理後的圖片
        st.image(processed_image, caption="處理後的圖片", use_column_width=True)

if __name__ == "__main__":
    main()
