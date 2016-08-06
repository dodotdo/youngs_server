import json

def make_data(token, namespace, data=''):
    return json.dumps({
        'token': token,
        'namespace': namespace,
        'payload': data
    }).encode()