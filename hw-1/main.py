import json
from typing import Any, Callable, Dict
from urllib.parse import parse_qs
from .math_controllers import calculate_factorial, calculate_fibonacci, calculate_mean, create_error_response

async def application(scope: Dict[str, Any], receive: Callable, send: Callable):
    assert scope.get('type') == 'http'

    path = get_path(scope)
    query_params = get_query_params(scope)

    response = route_request(path, query_params, await get_request_body(receive))
    await handle_response(send, response)

async def handle_response(send, reply):
    await send_headers(send, reply['status'])
    await send_body(send, reply['body'])

def get_path(scope):
    return scope.get('path', '')

def get_query_params(scope):
    query_string = scope.get('query_string', b'').decode()
    return parse_qs(query_string)

async def get_request_body(receive):
    body_content = b""
    while True:
        message = await receive()
        body_content += message.get('body', b'')
        if not message.get('more_body', False):
            break
    return body_content

def route_request(path, query_params, body):
    if path.startswith('/factorial'):
        return calculate_factorial(query_params)
    elif path.startswith('/fibonacci'):
        return calculate_fibonacci(path)
    elif path.startswith('/mean'):
        return calculate_mean(body)
    else:
        return create_error_response(404, 'Resource not found')

async def send_headers(send, status):
    headers = [(b'content-type', b'application/json')]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers
    })

async def send_body(send, body):
    await send({
        'type': 'http.response.body',
        'body': body.encode('utf-8')
    })
