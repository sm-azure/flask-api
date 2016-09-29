from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from model.billingmodel import db
from model.billingmodel import User, ManagedAccount, VPNTunnel

application = Flask(__name__)

@application.route('/api/users', methods = ['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400)  # missing args
    if User.query.filter_by(email=email).first() is not None:
        abort(400)  # existing user
    user = User(email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': email}, 201, {'Location':url_for('get_user', id = user.id, _external = True)})


@application.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.email})


@application.route('/')
def index():
    return 'Index Page'

@application.route('/hello')
def hello_world():
    return 'Hello, World!'

@application.route('/post/<int:post_id>')
def post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=3000)
    #application.run()
