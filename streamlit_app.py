import streamlit as st
from PIL import Image
from PIL import ImageOps
from io import BytesIO
import base64
import cv2
import numpy as np

def remove_background(image):
    # 將圖像轉換為 NumPy 數組
    np_image = np.array(image)

    # 定義背景顏色（紅色）的閾值範圍
    lower_threshold = np.array([200, 0, 0], dtype=np.uint8)
    upper_threshold = np.array([255, 100, 100], dtype=np.uint8)

    # 創建遮罩，將背景顏色標記為白色（255），前景顏色標記為黑色（0）
    mask = cv2.inRange(np_image, lower_threshold, upper_threshold)

    # 將遮罩應用於原始圖像，保留前景區域
    foreground = cv2.bitwise_and(np_image, np_image, mask=mask)

    # 將前景圖像轉換回 PIL 圖像
    foreground_image = Image.fromarray(foreground)

    return foreground_image

def generate_banner(image, position, background_color, text):
    # 在指定的位置繪製圖片
    banner_image = Image.new('RGB', (500, 200), background_color)
    banner_image.paste(image, position)

    # 在圖片上繪製文字
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(banner_image)
    font = ImageFont.truetype("Pixels.ttf", 24)
    draw.text((50, 50), text, fill="white", font=font)

    return banner_image

# Streamlit App
def main():
    st.title("Banner Generator")

    uploaded_file = st.file_uploader("上傳圖片", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 將上傳的圖片讀取為PIL圖像
        image = Image.open(uploaded_file)

        # 移除圖片背景
        removed_background = remove_background(image)

        # 指定圖片位置
        position_x = st.slider("圖片位置 (X)", 0, 500, 100)
        position_y = st.slider("圖片位置 (Y)", 0, 200, 50)
        position = (position_x, position_y)

        # 指定背景顏色
        background_color = st.color_picker("選擇背景顏色", "#ffffff")

        # 指定Banner文字
        text = st.text_input("輸入Banner文字")

        # 生成Banner圖片
        banner_image = generate_banner(removed_background, position, background_color, text)

        # 顯示Banner圖片
        st.image(banner_image)

        # 下載完成的圖片
        buffered = BytesIO()
        banner_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/jpg;base64,{img_str}" download="banner.jpg">點擊下載</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
