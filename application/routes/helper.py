import datetime
from functools import wraps
from flask import current_app as app
from flask import request, jsonify
import jwt
from application.models.user import User
from werkzeug.security import check_password_hash


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    user = User.query.filter(User.username == auth.username).one()
    if not user:
        return jsonify({'message': 'user not found', 'data': []}), 401

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        print(token)
        return jsonify({'message': 'Validated successfully', 'token': jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])})

    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401


def token_require(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        print(token)

        if not token:
            return jsonify({'message': 'token is missing', 'data': {}}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter(User.id == data['id']).first()
        except:
            return jsonify({'message': 'failed to decode token', 'data': {}}), 401

        return f(current_user, *args, **kwargs)
    return decorated
