import streamlit as st

def initialize_session_state():
    session_defaults = {
        "mode": None,
        "user_input": "",
        "show_answer": False,
        "generated_answer": "",
        "is_loading": False,
        "is_button_clicked": False,
    }
    
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
