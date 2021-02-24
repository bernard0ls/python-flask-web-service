from flask import request, jsonify
from datetime import datetime as dt
from flask import current_app as app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from application.routes import helper

from application.models.user import User, db


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    return helper.auth()


@app.route('/user/create/', methods=['GET'])
def create_user():
    password = request.args.get('password')
    email = request.args.get('email')
    username = request.args.get('username')
    if email:
        existing_user = User.query.filter(
            User.email == email
        ).first()
        if existing_user:
            return jsonify(success=False, user=None), 201
        pass_hash = generate_password_hash(password)
        new_user = User(email=email, username=username, password=pass_hash, created=dt.now())

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True, user=new_user.serialize), 200
        except Exception as e:
            print(e)
            return jsonify(success=False, user=None), 500


@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users=[user.serialize for user in users])


@app.route('/user/id=<int:userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get(userId)
    if user is not None:
        return jsonify(user=user.serialize)
    else:
        return jsonify(user=None)


@app.route('/user/update/password', methods=['POST'])
@helper.token_require
def change_password(current_user):
    data = request.get_json()
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    email = data.get("email")

    user = User.query.get(current_user.id)
    if user.email == email and check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        if user is not None:
            db.session.commit()
            return jsonify(success=True, message='Changed password successfully!', user=user.serialize), 200
        else:
            return jsonify(success=False, message='User does not exist', user=None), 201
    else:
        return jsonify(success=False, message='Credentials does not match', user=None), 202


@app.route('/user/update/email', methods=['POST'])
@helper.token_require
def change_email(current_user):
    data = request.get_json()
    password = data.get("password")
    old_email = data.get("oldEmail")
    new_email = data.get("newEmail")

    user = User.query.get(current_user.id)
    if user.email == old_email and check_password_hash(user.password, password):
        if new_email:
            existing_user = User.query.filter(
                User.email == new_email
            ).first()
            if existing_user:
                return jsonify(success=False, message='Email in use', user=None), 201

        user.email = new_email
        if user is not None:
            db.session.commit()
            return jsonify(success=True, message='Changed email successfully!', user=user.serialize), 200
        else:
            return jsonify(success=False, message='User does not exist', user=None), 202
    else:
        return jsonify(success=False, message='Credentials does not match', user=None), 203
