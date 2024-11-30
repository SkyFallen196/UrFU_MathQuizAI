import streamlit as st
from time import sleep

from utils.database import save_response_to_db


def handle_back_to_main_menu_button():
    if st.button("Вернуться в главное меню", key="back_to_menu_button"):
        st.session_state.mode = None
        st.session_state.user_input = ""
        st.session_state.show_answer = False
        st.session_state.generated_answer = ""
        st.session_state.is_loading = False
        st.session_state.is_button_clicked = False
        st.rerun()


def handle_save_to_db_button(query, response):
    st.markdown("Сохранить ответ в базу данных?")
    col1, col2 = st.columns(2)

    with col1:
        save_to_db = st.button(
            "Да",
            key="save_yes_button",
            use_container_width=True,
            disabled=st.session_state.is_button_clicked
        )
    with col2:
        do_not_save = st.button(
            "Нет",
            key="save_no_button",
            use_container_width=True,
            disabled=st.session_state.is_button_clicked
        )

    if save_to_db:
        try:
            save_response_to_db(query, response)
            st.success("Ответ был успешно сохранён в базу данных.")
            st.session_state.user_input = query
            st.session_state.generated_answer = response
            sleep(3)
        except Exception as error:
            st.error(f"Ошибка сохранения ответа в базу данных: {error}")
        finally:
            st.session_state.is_button_clicked = True
            st.rerun()
    elif do_not_save:
        st.info("Ответ не был сохранён в базу данных.")
        st.session_state.user_input = query
        st.session_state.generated_answer = response
        st.session_state.is_button_clicked = True
        sleep(3)
        st.rerun()
