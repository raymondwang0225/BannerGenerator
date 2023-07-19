import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="图片背景移除")

st.write("## 从图片移除背景")
st.write(
    ":dog: 请上传一张图片，去除背景后图片可在侧边栏下载. :grin:"
)
st.sidebar.write("## 上传和下载 :gear:")


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(upload):
    image = Image.open(upload)
    col1.write("原图片 :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("处理后 :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("下载图片", convert_image(fixed), "fixed.png", "image/png")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("上传图片", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    fix_image(upload=my_upload)
else:
    fix_image("./zebra.jpg")
