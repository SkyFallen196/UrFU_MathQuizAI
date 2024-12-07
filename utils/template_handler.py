import streamlit as st

from utils.RAG import get_response
from utils.button_utils import handle_back_to_main_menu_button, handle_save_to_db_button
from utils.wolfram_api import calculate_determinant_from_text


def handle_template_mode(template, title, calculate_determinant=False):
    st.subheader(title)

    if st.button("Составить задание"):
        st.session_state.is_loading = True
        st.session_state.is_button_clicked = False

        with st.spinner("Генерация задания..."):
            try:
                response = get_response(template)
                st.session_state.is_loading = False
                st.session_state.generated_answer = response
                st.session_state.user_input = template
                
                if calculate_determinant:
                    determinant = calculate_determinant_from_text(response)
                    if determinant:
                        st.session_state.determinant_result = f"\nОтвет: {determinant}"
                    
            except Exception as error:
                st.session_state.is_loading = False
                st.error(f"Ошибка при генерации задания: {error}")

    if st.session_state.get("generated_answer"):
        st.markdown("### **Задание:**")
        st.markdown(st.session_state.generated_answer)
        
        if calculate_determinant and st.session_state.get("determinant_result"):
            st.markdown("### **Результат:**")
            st.markdown(st.session_state.determinant_result)
            
        handle_save_to_db_button(st.session_state.user_input, st.session_state.generated_answer)

    handle_back_to_main_menu_button()
