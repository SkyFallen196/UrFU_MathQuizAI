import streamlit as st

from modes.custom_request import handle_custom_request_mode
from modes.modes_with_template import handle_matrix_determinant_2x2_mode, handle_matrix_determinant_3x3_mode, \
    handle_matrix_multiplication_2x2_mode, handle_matrix_multiplication_3x3_mode, handle_matrix_trace_mode, \
    handle_matrix_rank_mode, handle_matrix_expression_mode, handle_vector_length_mode, \
    handle_function_evaluation_mode, handle_module_of_complex_number, handle_derivative_evaluation
from modes.view_saved_answers import handle_saved_answers_mode

MODES_DICT = {
    "matrix_determinant_2x2": handle_matrix_determinant_2x2_mode,
    "matrix_determinant_3x3": handle_matrix_determinant_3x3_mode,
    "matrix_2_multip_2x2": handle_matrix_multiplication_2x2_mode,
    "matrix_2_multip_3x3": handle_matrix_multiplication_3x3_mode,
    "matrix_trace": handle_matrix_trace_mode,
    "matrix_rank": handle_matrix_rank_mode,
    "matrix_expression": handle_matrix_expression_mode,
    "vector_length": handle_vector_length_mode,
    "function_evaluation": handle_function_evaluation_mode,
    "complex_module": handle_module_of_complex_number,
    "derivative_evaluation": handle_derivative_evaluation,
    "custom_request": handle_custom_request_mode,
    "saved_answers": handle_saved_answers_mode,
}


def handle_mode():
    mode_function = MODES_DICT.get(st.session_state.mode)

    if mode_function:
        mode_function()
    else:
        st.error(f"Неизвестный режим: {st.session_state.mode}")
