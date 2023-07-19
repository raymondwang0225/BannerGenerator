import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload, position, background_color, text):
    # 去除图片背景
    with st.spinner('正在去除背景...'):
        image_data = convert_image(upload)
        result = remove(image_data)

    # 创建 Banner 图片
    banner_image = Image.new('RGBA', (500, 200), background_color)
    banner_image.paste(Image.open(BytesIO(result)), position)
    
    # 在 Banner 图片上添加文字
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(banner_image)
    font = ImageFont.truetype("arial.ttf", 24)
    draw.text((50, 50), text, fill="white", font=font)

    return banner_image

# Streamlit App
def main():
    st.title("Banner Generator")

    uploaded_file = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 指定图片位置
        position_x = st.slider("图片位置 (X)", 0, 500, 100)
        position_y = st.slider("图片位置 (Y)", 0, 200, 50)
        position = (position_x, position_y)

        # 指定背景颜色
        background_color = st.color_picker("选择背景颜色", "#ffffff")

        # 指定Banner文字
        text = st.text_input("输入Banner文字")

        # 生成Banner图片
        banner_image = fix_image(uploaded_file, position, background_color, text)

        # 显示Banner图片
        st.image(banner_image)

        # 下载完成的图片
        buffered = BytesIO()
        banner_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="banner.png">点击下载</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
