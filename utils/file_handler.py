import os

import streamlit as st


def handle_file_upload():
    uploaded_files = st.file_uploader("Загрузите ваши документы (формат .md)", type=["md"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(os.path.join("data", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Файл «{uploaded_file.name}» успешно загружен!")
