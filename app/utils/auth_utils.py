from functools import wraps
from flask import request, abort, g
from ..models.api_user import APIUser

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            abort(401, description='API key required')
        user = APIUser.query.filter_by(api_key=api_key).first()
        if not user:
            abort(403, description='Invalid API key')
        g.current_user = user
        return f(*args, **kwargs)
    return decorated

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, 'current_user', None)
            if not user or user.role != role:
                abort(403, description='Insufficient permissions')
            return f(*args, **kwargs)
        return decorated
    return decorator