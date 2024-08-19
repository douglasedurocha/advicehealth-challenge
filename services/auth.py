from functools import wraps
from flask import request, abort
from flask_basicauth import BasicAuth

basic_auth = BasicAuth()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not basic_auth.check_credentials(auth.username, auth.password):
            abort(401, description="Unauthorized access. Please provide valid credentials.")
        return f(*args, **kwargs)
    return decorated_function
