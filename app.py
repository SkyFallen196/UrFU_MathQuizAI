import streamlit as st
from dotenv import load_dotenv

from utils.file_handler import handle_file_upload
from utils.modes_manager import handle_mode
from utils.page_configurator import configure_page
from utils.session_manager import initialize_session_state


def create_menu_button(label: str, mode: str, col) -> None:
    if col.button(label, key=f"{mode}_button", use_container_width=True):
        st.session_state.mode = mode
        st.rerun()


def show_main_menu():
    st.subheader("Пожалуйста, выберите действие ниже")
    col1, col2, col3, col4 = st.columns(4)

    create_menu_button("Найти определитель матрицы 2x2", "matrix_determinant_2x2", col1)
    create_menu_button("Найти определитель матрицы 3x3", "matrix_determinant_3x3", col2)
    create_menu_button("Свой запрос", "custom_request", col3)
    create_menu_button("Сохранённые ответы", "saved_answers", col4)


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
