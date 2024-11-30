import streamlit as st

from utils.RAG import get_response
from utils.button_utils import handle_back_to_main_menu_button, handle_save_to_db_button
from utils.database import initialize_db

initialize_db()


def handle_custom_request_mode():
    st.write("Напишите вопрос на основе заданного контекста.")

    st.session_state.user_input = st.text_area(
        "Введите свой промпт ниже",
        value=st.session_state.user_input,
        height=300,
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
        st.session_state.is_button_clicked = False

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
        handle_save_to_db_button(st.session_state.user_input, st.session_state.generated_answer)

    handle_back_to_main_menu_button()
