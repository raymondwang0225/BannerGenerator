import streamlit as st
import cv2
import numpy as np

def process_image(image):
    # 將圖片轉換為BGR格式
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    
    # 計算各個顏色的像素數量
    unique_colors, counts = np.unique(image.reshape(-1, 3), axis=0, return_counts=True)
    
    # 找到佔比最大的顏色
    max_color = unique_colors[np.argmax(counts)]
    
    # 將該顏色設置為透明
    image[np.where((image == max_color).all(axis=2))] = [0, 0, 0, 0]
    
    # 將圖片轉換為RGBA格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    
    return image

def main():
    st.title("圖片處理應用")
    
    # 上傳圖片
    uploaded_file = st.file_uploader("選擇一張圖片", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # 讀取上傳的圖片
        image = np.array(cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1))
        
        # 顯示原始圖片
        st.image(image, caption="原始圖片", use_column_width=True)
        
        # 處理圖片
        processed_image = process_image(image)
        
        # 顯示處理後的圖片
        st.image(processed_image, caption="處理後的圖片", use_column_width=True)

if __name__ == "__main__":
    main()
