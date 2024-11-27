import streamlit as st
from dotenv import load_dotenv
from RAG import get_response

load_dotenv(".env")


st.set_page_config(page_title="MathQuizGenerator", page_icon="🏛", layout="centered")

st.title("RAG-система для математических заданий")

st.write("Напишите вопрос на основе заданного контекста:")

user_input = st.text_area("Введите свой промпт...", height=100)

if st.button("Получить ответ"):
    if user_input:
        answer = get_response(user_input)
        st.markdown(f"### Ответ: {answer}")
    else:
        st.warning("Пожалуйста, введите вопрос.")
