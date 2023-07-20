import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from PIL import ImageDraw, ImageFont
import time


def fix_image(upload, position, background_color, text, banner_size, text_size, text_color, text_position, use_custom_settings, progress):
    image = Image.open(upload)

    if use_custom_settings:
        fixed = remove(
            image,
            alpha_matting=True,
            alpha_matting_foreground_threshold=9,
            alpha_matting_background_threshold=3,
            alpha_matting_erode_size=17
        )
    else:
        fixed = remove(image)

    # Rest of the code remains unchanged...


# Streamlit App
def main():
    st.set_page_config(layout='centered', initial_sidebar_state='expanded')

    # Rest of the code remains unchanged...

    if uploaded_file is not None:
        # Rest of the code remains unchanged...

        with st.expander("Image Setting"):
            # Rest of the code remains unchanged...

        with st.expander("Text Setting"):
            # Rest of the code remains unchanged...

        # 指定Banner尺寸
        banner_size = (banner_width, banner_height)

        # Add a selectbox for processing options
        processing_option = st.selectbox("Choose Processing Option", ("default", "customize"))

        if processing_option == "customize":
            # Add sliders for custom settings
            alpha_matting_foreground_threshold = st.slider("Alpha Matting Foreground Threshold", 0, 20, 9)
            alpha_matting_background_threshold = st.slider("Alpha Matting Background Threshold", 0, 20, 3)
            alpha_matting_erode_size = st.slider("Alpha Matting Erode Size", 0, 50, 17)
        else:
            alpha_matting_foreground_threshold = 9
            alpha_matting_background_threshold = 3
            alpha_matting_erode_size = 17

        progress_placeholder = st.empty()

        with st.spinner('Image processing, please wait...'):
            # Rest of the code remains unchanged...
            # Use the processing_option and custom settings in fix_image function
            banner_image = fix_image(
                uploaded_file, position, background_color, text, banner_size, text_size, text_color, text_position,
                processing_option == "customize", progress_placeholder
            )
        # Rest of the code remains unchanged...


if __name__ == "__main__":
    main()
