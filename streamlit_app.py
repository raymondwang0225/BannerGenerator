import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np


def remove_background(image, mask):
    # Convert image to RGBA mode to support transparency
    image = image.convert("RGBA")

    # Get pixel data of the image
    data = np.array(image)

    # Set the background region from the segmentation mask as transparent
    data[..., 3] = np.where(mask == 0, 0, 255)

    # Create a new image and return
    new_image = Image.fromarray(data)
    return new_image


# Streamlit App
def main():
    st.title("Background Removal")

    # Upload image
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Read the uploaded image
        image = Image.open(uploaded_file)

        # Display the original image
        st.image(image, caption="Original Image")

        # Display the image selection tool
        st.subheader("Select Background Region")
        selected_area = st.image(image, caption="Selected Background Region", use_column_width=True, clamp=True)

        # Create an empty mask image
        mask = np.zeros(image.size, dtype=np.uint8)

        # Set the mouse event callback function
        def mouse_callback(event):
            if event["type"] == "mousedown":
                # Draw a white point on the mask image
                x, y = event["x"], event["y"]
                mask[y, x] = 255
                selected_area.image(mask, caption="Selected Background Region", use_column_width=True, clamp=True)

        # Add the mouse event callback to the image selection tool
        selected_area = st.image(image, caption="Selected Background Region", use_column_width=True, clamp=True)
        selected_area._add_mouse_callbacks(mouse_callback)

        # Perform image segmentation using an algorithm such as watershed or GrabCut
        # Obtain the segmentation mask result

        # Call the remove background function and apply the segmentation result to the image
        removed_background = remove_background(image, mask)

        # Display the image with the background removed
        st.subheader("Image with Background Removed")
        st.image(removed_background)


if __name__ == "__main__":
    main()
