
import json

def wrap_data(namespace, payload):

    return json.dumps({
        "namespace": namespace,
        "payload": payload.decode('utf-8')
    })

def make_response(status_code, message, namespace=''):
    response = (json.dumps({
        'status_code': status_code,
        'namespace': namespace,
        'message': message
    }) + "\n").encode()
    print(response)
    return response

def make_voice_packet(payload):
    # json_payload = b'{"namespace":"receive_voice","payload":'+payload+b'"}\n'
    # print(json_payload)
    return payload
