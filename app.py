import streamlit as st
from dotenv import load_dotenv
import os

from RAG import get_response

load_dotenv(".env")

st.set_page_config(
    page_title="MathQuizGenerator",
    page_icon="🏛",
    layout="centered"
)

if "mode" not in st.session_state:
    st.session_state.mode = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "generated_answer" not in st.session_state:
    st.session_state.generated_answer = ""
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

st.title("RAG-система для математических заданий")

if st.session_state.mode is None:
    st.subheader("Пожалуйста, выберите действие ниже")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Найти определитель матрицы 2x2",
                     key="matrix_determinant_2x2_button",
                     use_container_width=True):
            st.session_state.mode = "matrix_determinant_2x2"
            st.rerun()
    with col2:
        if st.button("Свой запрос", key="custom_request_button", use_container_width=True):
            st.session_state.mode = "custom_request"
            st.rerun()

    uploaded_files = st.file_uploader("Загрузите ваши документы (формат .md)", type=["md"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(os.path.join("data", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Файл {uploaded_file.name} успешно загружен!")

elif st.session_state.mode == "matrix_determinant_2x2":
    st.subheader("Вычисление определителя матрицы 2x2")
    st.write("Функция находится в разработке...")

    if st.button("Вернуться к выбору режима", key="back_button_matrix"):
        st.session_state.mode = None
        st.rerun()

elif st.session_state.mode == "custom_request":
    st.write("Напишите вопрос на основе заданного контекста.")

    st.session_state.user_input = st.text_area(
        "Введите свой промпт ниже",
        value=st.session_state.user_input,
        height=300
    )

    if st.session_state.is_loading:
        st.spinner("Генерация ответа...")

    is_disabled = st.session_state.is_loading

    if st.button("Получить ответ", type="primary", key="generate_answer_button", disabled=is_disabled):
        if st.session_state.user_input:
            st.session_state.show_answer = False
            st.session_state.is_loading = True
            st.rerun()

    if st.session_state.is_loading and not st.session_state.show_answer:
        with st.spinner("Генерация ответа..."):
            try:
                answer = get_response(st.session_state.user_input)
                st.session_state.show_answer = True
                st.session_state.generated_answer = answer
            except Exception as error:
                st.error(f"Ошибка при генерации ответа: {error}")
            finally:
                st.session_state.is_loading = False
                st.rerun()

    if st.session_state.show_answer:
        st.markdown("### **Ответ:**")
        st.markdown(f"{st.session_state.generated_answer}")

    if st.button("Вернуться к выбору режима", key="back_button_request"):
        st.session_state.mode = None
        st.session_state.show_answer = False
        st.session_state.user_input = ""
        st.session_state.generated_answer = ""
        st.rerun()