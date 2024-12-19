import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WOLFRAM_ALPHA_APP_ID")
BASE_URL = "http://api.wolframalpha.com/v2/query"


def send_wolfram_query(query):
    params = {
        "input": query,
        "format": "plaintext",
        "output": "JSON",
        "appid": api_key
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def extract_result_from_response(response, title="Result"):
    try:
        pods = response.get("queryresult", {}).get("pods", [])

        for pod in pods:
            if pod.get("title") == title:
                return pod.get("subpods", [{}])[0].get("plaintext")
    except Exception as error:
        print(f"Ошибка в процессе обработки запроса: {error}")

    return None


def build_query(operation, *args):
    match operation:
        case "determinant":
            return f"determinant {args[0]}"
        case "multiplication":
            return f"{args[0]} * {args[1]}"
        case "trace":
            return f"trace {args[0]}"
        case "rank":
            return f"rank {args[0]}"
        case "vector_length":
            return f"magnitude of ({args[0]}, {args[1]}, {args[2]})"
        case "matrix_expression":
            n1, A, n2, B = args

            return f"{n1} * {A} + {n2} * {B}"
        case _:
            raise ValueError(f"Неизвестная операция: {operation}")


def get_single_matrix_query(text, operation):
    matrix_str = extract_matrix(text, "A")

    if not matrix_str:
        return None

    return build_query(operation, matrix_str)


def get_two_matrices_query(text, operation):
    A_matrix = extract_matrix(text, "A")
    B_matrix = extract_matrix(text, "B")

    if not (A_matrix and B_matrix):
        return None

    return build_query(operation, A_matrix, B_matrix)


def get_matrix_expression_query(text):
    A_matrix = extract_matrix(text, "A")
    B_matrix = extract_matrix(text, "B")

    if not (A_matrix and B_matrix):
        return None

    n1_match = re.search(r"(\d+)A", text)
    n2_match = re.search(r"(\d+)B", text)

    if not (n1_match and n2_match):
        return None

    n1, n2 = n1_match.group(1), n2_match.group(1)

    return build_query("matrix_expression", n1, A_matrix, n2, B_matrix)


def extract_matrix(text, label):
    pattern = rf"{label} = (\[\[.*?\]\])"
    match = re.search(pattern, text)

    return match.group(1) if match else None


def get_operation_result(text, operation):
    query = None

    match operation:
        case "determinant" | "trace" | "rank":
            query = get_single_matrix_query(text, operation)
        case "multiplication":
            query = get_two_matrices_query(text, operation)
        case "matrix_expression":
            query = get_matrix_expression_query(text)
        case "vector_length":
            vector_match = re.search(r"A = \((\d+), (\d+), (\d+)\)", text)

            if vector_match:
                x, y, z = map(int, vector_match.groups())
                query = build_query("vector_length", x, y, z)
        case "function_evaluation":
            function_match = re.search(r"f\(x\) = (.+)\. Найдите", text)
            point_match = re.search(r"x = ([\d\-\+\.]+)", text)

            if function_match and point_match:
                function = function_match.group(1)
                point = point_match.group(1)
                query = f"value of {function} at x={point}"

    if not query:
        return None

    print("Запрос к Wolfram Alpha:", query)
    response = send_wolfram_query(query)

    return extract_result_from_response(response)
