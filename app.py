import streamlit as st
from dotenv import load_dotenv

from utils.file_handler import handle_file_upload
from utils.modes_manager import handle_mode
from utils.page_configurator import configure_page
from utils.session_manager import initialize_session_state
from utils.button_utils import handle_back_to_main_menu_button


def create_menu_button(label, mode, col, parent_mode=None):
    if col.button(label, key=f"{mode}_button", use_container_width=True):
        if parent_mode:
            st.session_state.parent_mode = parent_mode

        st.session_state.mode = mode
        st.rerun()


def show_main_menu():
    st.subheader("Пожалуйста, выберите действие ниже")
    col1, col2 = st.columns(2)

    create_menu_button("Сохранённые ответы", "saved_answers", col1)
    create_menu_button("Режимы", "mode_selection", col2)


def show_modes_submenu():
    st.subheader("Выберите режим")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)

    create_menu_button("Свой запрос", "custom_request", col1)
    create_menu_button("Найти определитель матрицы 2x2", "matrix_determinant_2x2", col2)
    create_menu_button("Найти определитель матрицы 3x3", "matrix_determinant_3x3", col3)
    create_menu_button("Найти произведение двух матриц 2x2", "matrix_2_multip_2x2", col4)
    create_menu_button("Найти произведение двух матриц 3x3", "matrix_2_multip_3x3", col5)
    create_menu_button("Найти след матрицы 4x4", "matrix_trace", col6)
    create_menu_button("Найти ранг матрицы 3x3", "matrix_rank", col7)
    create_menu_button("Вычислить n1A + n2B", "matrix_expression", col8)
    handle_back_to_main_menu_button()


def main():
    load_dotenv(".env")
    configure_page()
    initialize_session_state()
    st.title("RAG-система для математических заданий")

    if st.session_state.mode is None:
        show_main_menu()
        handle_file_upload()
    elif st.session_state.mode == "mode_selection":
        show_modes_submenu()
    else:
        handle_mode()


if __name__ == "__main__":
    main()
