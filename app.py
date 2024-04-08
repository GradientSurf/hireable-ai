import streamlit as st
import os

uploaded_file = st.file_uploader("Choose a file",type="pdf")
file_name = "resume.pdf"
folder_name = "./temp"
if uploaded_file:
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    path = os.path.join(folder_name,file_name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())