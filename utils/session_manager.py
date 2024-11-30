import streamlit as st


def initialize_session_state():
    if "mode" not in st.session_state:
        st.session_state.mode = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "generated_answer" not in st.session_state:
        st.session_state.generated_answer = ""
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    if "is_button_clicked" not in st.session_state:
        st.session_state.is_button_clicked = False
