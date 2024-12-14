import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WOLFRAM_ALPHA_APP_ID")


def query_wolfram_alpha(query):
    base_url = "http://api.wolframalpha.com/v2/query"

    params = {
        "input": query,
        "format": "plaintext",
        "output": "JSON",
        "appid": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def extract_matrix(text, label):
    pattern = rf"{label} = (\[\[.*?\]\])"
    match = re.search(pattern, text)

    if match:
        return match.group(1)

    return None


def extract_two_matrices(text):
    A_matrix = extract_matrix(text, "A")
    B_matrix = extract_matrix(text, "B")

    return A_matrix, B_matrix


def build_wolfram_query(operation, matrix_str):
    return f"{operation} {matrix_str}"


def build_wolfram_query_for_operation(operation, *matrices):
    match operation:
        case "determinant":
            return f"determinant {matrices[0]}"
        case "multiplication":
            return f"{matrices[0]} * {matrices[1]}"
        case "trace":
            return f"trace {matrices[0]}"
        case "rank":
            return f"rank {matrices[0]}"
        case _:
            raise ValueError(f"Неизвестная операция: {operation}")


def get_matrix_operation_result(text, operation):
    if operation in ("determinant", "trace", "rank"):
        matrix_str = extract_matrix(text, "A")

        if not matrix_str:
            return None

        query = build_wolfram_query_for_operation(operation, matrix_str)
    elif operation == "multiplication":
        A_matrix, B_matrix = extract_two_matrices(text)

        if not (A_matrix and B_matrix):
            return None

        query = build_wolfram_query_for_operation(operation, A_matrix, B_matrix)
    else:
        return None

    print("Запрос к Wolfram Alpha:", query)
    result = query_wolfram_alpha(query)

    try:
        pods = result.get("queryresult", {}).get("pods", [])

        for pod in pods:
            if pod.get("title") == "Result":
                return pod.get("subpods", [{}])[0].get("plaintext")
    except Exception as e:
        print(f"Ошибка при обработке результата: {e}")

    return None
