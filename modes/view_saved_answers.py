from time import sleep

import pandas as pd
import streamlit as st

from utils.button_utils import handle_back_to_main_menu_button
from utils.database import get_all_responses, delete_response_by_id


def handle_saved_answers_mode():
    st.subheader("Сохранённые ответы")
    data = get_all_responses()

    if not data:
        st.info("Сохранённые ответы не найдены.")
        handle_back_to_main_menu_button()

        return

    df = pd.DataFrame(data, columns=["ID", "Дата и время", "Запрос", "Ответ"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("### Удаление ответа")
    response_id = st.number_input("Введите ID ответа для удаления", min_value=1, step=1, key="delete_id_input")

    if st.button("Удалить ответ", key="delete_button"):
        is_deleted = delete_response_by_id(response_id)

        if is_deleted:
            st.success(f"Ответ с ID {response_id} успешно удалён!")
            sleep(3)
            st.rerun()
        else:
            st.error(f"Ответ с ID {response_id} не найден!")

    handle_back_to_main_menu_button()
