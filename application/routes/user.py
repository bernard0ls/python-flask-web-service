from flask import request, make_response, url_for, jsonify
from datetime import datetime as dt
from flask import current_app as app
from werkzeug.utils import redirect

from application.models.user import User, db


@app.route('/user/create/', methods=['GET'])
def create_user():
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return make_response(f"{new_user} successfully created!")


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
        return "Couldn´t find this user"


@app.route('/user/update/', methods=['POST'])
def update_user():
    data = request.get_json()

    user_id = data.get("userId")
    user_name = data.get("username")
    bio = data.get("bio")

    user = User.query.get(user_id)
    if user is not None:
        user.username = user_name
        user.bio = bio
        db.session.commit()
        return jsonify(user=user.serialize)
    else:
        return "Couldn´t find this user"
