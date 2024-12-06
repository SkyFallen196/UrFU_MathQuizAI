import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()

api_key = os.getenv('WOLFRAM_ALPHA_APP_ID')

def query_wolfram_alpha(query):
    base_url = 'http://api.wolframalpha.com/v2/query'
    params = {
        'input': query,
        'format': 'plaintext',
        'output': 'JSON',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error: {response.status_code} - {response.text}')

def extract_matrix(text):
    match = re.search(r'A = (\[\[.*?\]\])', text)
    if match:
        matrix_str = match.group(1)
        return f'determinant {matrix_str}'
    return None

def calculate_determinant_from_text(text):
    query = extract_matrix(text)
    if query:
        print('Запрос к Wolfram Alpha:', query)
        result = query_wolfram_alpha(query)
        try:
            pods = result.get('queryresult', {}).get('pods', [])
            for pod in pods:
                if pod.get('title') == 'Result':
                    return pod.get('subpods', [{}])[0].get('plaintext')
        except Exception as e:
            print(f"Ошибка при обработке результата: {e}")
        
    return None
