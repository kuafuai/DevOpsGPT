from functools import wraps
import traceback
from flask import jsonify

def json_response(func):
    @wraps(func)  # Preserve the original function's name and docstring
    def decorated_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            response = {
                'success': True,
                'data': result
            }
        except Exception as e:
            response = {
                'success': False,
                'error': str(e)
            }
            traceback.print_exc()
        return jsonify(response)

    return decorated_function