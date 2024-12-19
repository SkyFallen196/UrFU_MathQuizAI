import streamlit as st

from utils.RAG import get_response
from utils.button_utils import handle_back_to_main_menu_button, handle_save_to_db_button
from utils.wolfram_api import get_operation_result


def generate_task_and_result(template, operation=None):
    try:
        response = get_response(template)
        st.session_state.generated_answer = response
        st.session_state.user_input = template

        if operation:
            result = get_operation_result(response, operation)

            if result:
                st.session_state.operation_result = f"\nОтвет: {result}"
    except Exception as error:
        st.error(f"Ошибка при генерации задания: {error}")


def display_generated_task():
    if st.session_state.get("generated_answer"):
        st.markdown("### **Задание:**")
        st.markdown(st.session_state.generated_answer)

        if st.session_state.get("operation_result"):
            st.markdown("### **Результат:**")
            st.markdown(st.session_state.operation_result)

        handle_save_to_db_button(
            st.session_state.user_input, st.session_state.generated_answer
        )


def handle_template_mode(template, title, operation=None):
    st.subheader(title)

    if st.button("Составить задание"):
        st.session_state.is_loading = True

        with st.spinner("Генерация задания..."):
            try:
                generate_task_and_result(template, operation)
            finally:
                st.session_state.is_loading = False

    display_generated_task()
    handle_back_to_main_menu_button()
