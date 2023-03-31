import streamlit as st
from PIL import Image

uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
file_name = "SMDG-2022"
if uploaded_file is not None:
    # 直接转换为PIL的格式（需要转为array，不然无法识别）
    st.write(uploaded_file)
    st.write(uploaded_file.type)
    image = Image.open(uploaded_file)
    image.save("C:/Users/fuqin/Desktop/SMDG-2022.png")
