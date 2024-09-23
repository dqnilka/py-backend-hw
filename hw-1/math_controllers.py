import json
from urllib.parse import parse_qs

def calculate_factorial(params):
    try:
        n = int(params.get('n', [None])[0])
        if n is None or n < 0:
            return create_error_response(400, 'Value must be a non-negative integer')
    except (ValueError, TypeError):
        return create_error_response(422, 'Invalid input for factorial calculation')

    result = 1
    for i in range(2, n + 1):
        result *= i

    return create_success_response({'number': n, 'result': result})


def calculate_fibonacci(path):
    try:
        n_str = path.rsplit('/', 1)[-1]
        n = int(n_str)
        if n < 0:
            return create_error_response(400, 'Value must be a non-negative integer')
    except (ValueError, TypeError):
        return create_error_response(422, 'Invalid input for fibonacci calculation')

    fibonacci_sequence = [0, 1]
    for _ in range(2, n):
        fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])

    return create_success_response({'n': n, 'result': fibonacci_sequence[:n]})


def calculate_mean(body):
    try:
        numbers_list = json.loads(body)
        if not isinstance(numbers_list, list) or not numbers_list:
            return create_error_response(400, 'The numbers list cannot be empty')

        numbers_list = list(map(float, numbers_list))
    except (ValueError, TypeError, json.JSONDecodeError):
        return create_error_response(422, 'Invalid input for mean calculation')

    mean_value = sum(numbers_list) / len(numbers_list)
    return create_success_response({'numbers': numbers_list, 'result': mean_value})


def create_success_response(data):
    return {
        'status': 200,
        'body': json.dumps(data)
    }


def create_error_response(status, message):
    return {
        'status': status,
        'body': json.dumps({'detail': message})
    }
