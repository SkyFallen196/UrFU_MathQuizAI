FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 11434

EXPOSE 8000

EXPOSE 8501

CMD ["sh", "-c", "chroma run --host localhost --port 8000 & sleep 2 && streamlit run app.py"]