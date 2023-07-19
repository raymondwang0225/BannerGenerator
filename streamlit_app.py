import streamlit as st
import cv2
import numpy as np
from PIL import Image


def remove_background(image, mask):
    # 将图像转换为RGBA模式，以支持透明度
    image = image.convert("RGBA")

    # 获取图像的像素数据
    data = np.array(image)

    # 将分割的背景区域设置为透明
    data[..., 3] = np.where(mask == 0, 0, 255)

    # 创建新的图像并返回
    new_image = Image.fromarray(data)
    return new_image


# Streamlit App
def main():
    st.title("背景去除")

    # 上传图像
    uploaded_file = st.file_uploader("上传图像", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # 读取上传的图像
        image = Image.open(uploaded_file)

        # 显示图像
        st.image(image, caption="原始图像")

        # 显示图像选择工具
        st.subheader("选择背景区域")
        selected_area = st.image(image, caption="选择背景区域", use_column_width=True, clamp=True)

        # 创建空的掩码图像
        mask = np.zeros(image.size, dtype=np.uint8)

        # 设置鼠标事件处理函数
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # 在掩码图像上绘制白色点
                cv2.circle(mask, (x, y), 3, (255, 255, 255), -1)
                selected_area.image(mask, caption="选择背景区域", use_column_width=True, clamp=True)

        # 将图像转换为OpenCV格式
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 创建窗口并设置鼠标事件回调
        cv2.namedWindow("Select Background")
        cv2.setMouseCallback("Select Background", mouse_callback)

        # 显示OpenCV窗口
        cv2.imshow("Select Background", cv_image)

        # 等待用户选择背景区域
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 运行图像分割算法，如分水岭算法或GrabCut算法，对选择的背景区域进行分割并获得分割结果的掩码

        # 调用去除背景函数，将分割结果应用于图像
        removed_background = remove_background(image, mask)

        # 显示去除背景后的图像
        st.subheader("去除背景后的图像")
        st.image(removed_background)


if __name__ == "__main__":
    main()
