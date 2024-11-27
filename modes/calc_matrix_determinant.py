import streamlit as st


def handle_matrix_determinant_2x2_mode():
    st.subheader("Вычисление определителя матрицы 2x2")
    st.write("Функция находится в разработке...")

    if st.button("Вернуться к выбору режима", key="back_button_matrix"):
        st.session_state.mode = None
        st.rerun()
