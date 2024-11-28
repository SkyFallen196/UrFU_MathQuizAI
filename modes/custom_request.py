import streamlit as st

from utils.RAG import get_response
from utils.database import initialize_db, save_response_to_db

initialize_db()


def handle_custom_request_mode():
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
        st.markdown("Сохранить ответ в базу данных?")
        col1, col2 = st.columns(2)

        with col1:
            save_to_db = st.button("Да", key="save_yes_button", use_container_width=True)
        with col2:
            do_not_save = st.button("Нет", key="save_no_button", use_container_width=True)

        if save_to_db:
            try:
                save_response_to_db(st.session_state.user_input, st.session_state.generated_answer)
                st.success("Ответ был успешно сохранён в базу данных.")
            except Exception as error:
                st.error(f"Ошибка сохранения ответа в базу данных: {error}")
        elif do_not_save:
            st.info("Ответ не был сохранён в базу данных – выбран ответ «Нет».")

    if st.button("Вернуться к выбору режима", key="back_button_request"):
        st.session_state.mode = None
        st.session_state.show_answer = False
        st.session_state.user_input = ""
        st.session_state.generated_answer = ""
        st.rerun()
