from flask import Blueprint, current_app
from flask import abort, request, jsonify, g, url_for, Response, json

from model.database import db
from model.user import User
from utils.security import login_manager, login_required, login_required, logout_user, login_user, current_user

apis = Blueprint("api", __name__, url_prefix="/api")

@apis.route('/users', methods = ['POST'])
def new_user():
    print request
    current_app.logger.error("Error---1")
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        print 'missing email'
        abort(400)  # missing args
    if User.query.filter_by(email=email).first() is not None:
        print 'existing email'
        abort(400)  # existing user
    user = User(email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': email}, 201, {'Location':url_for('api.get_user', id = user.id, _external = True)})


@apis.route('/users/<int:id>')
def get_user(id):
    current_app.logger.error("Error---2")
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.email})


@apis.route('/')
def index():
    current_app.logger.error("Error---3")
    return 'Index Page'


@apis.route('/logout', methods= ['GET'] )
#@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return  Response(response=json.dumps({'message':'Successfull Logout!'}), status=200)



@apis.route('/login', methods = ['POST', 'GET'] )
@login_required
def login():
    token = current_user.generate_auth_token()
    resp =  Response(response=json.dumps({'message':'Hello, %s' % current_user.email}), status=200)
    resp.headers['api-key']= token.decode('ascii')
    return resp
