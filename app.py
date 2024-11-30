import streamlit as st
from dotenv import load_dotenv

from utils.file_handler import handle_file_upload
from utils.modes_manager import handle_mode
from utils.page_configurator import configure_page
from utils.session_manager import initialize_session_state


def show_main_menu():
    st.subheader("Пожалуйста, выберите действие ниже")
    col1, col2, col3 = st.columns(3)

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
    with col3:
        if st.button("Сохранённые ответы", key="saved_answers_button", use_container_width=True):
            st.session_state.mode = "saved_answers"
            st.rerun()


def main():
    load_dotenv(".env")
    configure_page()
    initialize_session_state()
    st.title("RAG-система для математических заданий")

    if st.session_state.mode is None:
        show_main_menu()
        handle_file_upload()
    else:
        handle_mode()


if __name__ == "__main__":
    main()
