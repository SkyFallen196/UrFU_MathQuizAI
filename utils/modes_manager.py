import streamlit as st

from modes.custom_request import handle_custom_request_mode
from modes.modes_with_template import handle_matrix_determinant_2x2_mode, handle_matrix_determinant_3x3_mode, \
    handle_matrix_multiplication_2x2_mode, handle_matrix_multiplication_3x3_mode
from modes.view_saved_answers import handle_saved_answers_mode

MODES_DICT = {
    "matrix_determinant_2x2": handle_matrix_determinant_2x2_mode,
    "matrix_determinant_3x3": handle_matrix_determinant_3x3_mode,
    "matrix_2_multip_2x2": handle_matrix_multiplication_2x2_mode,
    "matrix_2_multip_3x3": handle_matrix_multiplication_3x3_mode,
    "custom_request": handle_custom_request_mode,
    "saved_answers": handle_saved_answers_mode,
}


def handle_mode():
    mode_function = MODES_DICT.get(st.session_state.mode)

    if mode_function:
        mode_function()
    else:
        st.error(f"Неизвестный режим: {st.session_state.mode}")
