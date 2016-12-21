import ast
from flask import current_app
from youngs_server.youngs_app import youngs_redis, log
from ..customlib.flask_restful import abort

def userid_to_id(userid):
    if userid is None:
        return None
    try:
        redis_result = youngs_redis.get('userid-'+userid)
        if redis_result is None:
            abort(404, message='wrong userid')
        p = ast.literal_eval(redis_result.decode('utf-8'))
    except ValueError as e:
        abort(404, message='wrong userid')
    if p is None or 'id' not in p:
        abort(404, message='wrong userid')
    return p['id']
