import streamlit as st
from PIL import Image
from PIL import ImageOps
from io import BytesIO
import base64

def remove_background(image):
    # 在這裡添加你的去背景程式碼
    # 這個函數應該接受一個圖片作為輸入，並返回一個去除背景的圖片
    # 這裡只是一個示例，你需要使用你自己的去背景方法
    inverted_image = ImageOps.invert(image)
    return inverted_image

def generate_banner(image, position, background_color, text):
    # 在指定的位置繪製圖片
    banner_image = Image.new('RGB', (500, 200), background_color)
    banner_image.paste(image, position)

    # 在圖片上繪製文字
    # 這裡只是一個示例，你可以根據需要自定義文字的字體、大小等
    # 你也可以更改文字的位置和顏色
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(banner_image)

    # 讀取字體文件
    with open("Pixels.ttf", "rb") as f:
        font_data = f.read()
    
    font = ImageFont.truetype(BytesIO(font_data), 24)
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
        position = (100, 50)

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
