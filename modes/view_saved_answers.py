import pandas as pd
import streamlit as st

from utils.database import get_all_responses, delete_response_by_id


def handle_saved_answers_mode():
    st.subheader("Сохранённые ответы")
    data = get_all_responses()

    if not data:
        st.info("Сохранённые ответы не найдены.")

        if st.button("Вернуться в главное меню"):
            st.session_state.mode = None
            st.rerun()

        return

    df = pd.DataFrame(data, columns=["ID", "Дата и время", "Запрос", "Ответ"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("### Удаление ответа")
    response_id = st.number_input("Введите ID ответа для удаления", min_value=1, step=1, key="delete_id_input")

    if st.button("Удалить ответ", key="delete_button"):
        try:
            delete_response_by_id(response_id)
            st.success(f"Ответ с ID {response_id} успешно удалён!")
            st.rerun()
        except Exception as error:
            st.error(f"Ошибка при удалении ответа с ID {response_id}: {error}")

    if st.button("Вернуться в главное меню", key="back_to_menu_button"):
        st.session_state.mode = None
        st.rerun()
