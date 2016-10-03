from flask import Flask, abort, request, jsonify, g, url_for, Response, json
from flask_sqlalchemy import SQLAlchemy
from model.billingmodel import db
from model.billingmodel import User, ManagedAccount, VPNTunnel
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
import logging
from logging.handlers import RotatingFileHandler
import base64

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
#handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
#handler = RotatingFileHandler('/var/log/application.log', maxBytes=1024,backupCount=5)
handler.setFormatter(formatter)


application = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(application)
application.logger.addHandler(handler)

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


@login_manager.request_loader
def load_user_from_request(request):
    # try token verification from headers
    token = request.headers.get('api_key')
    if token:
        logger.debug('Got api-key token')
        logger.debug(token)
        user = User.verify_auth_token(token)
        # token is valid and user is already logged in - continue
        if user and user.is_authenticated():
            g.user = user
            return user
        # token is invalid (experied/incorrect) and user is logged in - logout
        if not user and user.is_authenticated():
            user.authenticated = False
            db.session.add(user)
            db.session.commit()
            return None

    # try Basic authentication [for initial login]
    token = request.headers.get('Authorization')
    if token:
        logger.debug('Got Authorization token')
        logger.debug(token)
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
        except TypeError:
            return None
        email, password = token.split(":")
        logger.debug(email)
        logger.debug(password)
        user = User.query.filter_by(email = email).first()
        if not user or not user.verify_password(password):
            return None
        # User exists and is logging in - save state
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        logger.debug('Setting user')
        g.user = user
        return user

    return None


@application.route('/logout', methods= ['GET'] )
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return  Response(response=json.dumps({'message':'Successfull Logout!'}), status=200)



@application.route('/login', methods = ['POST', 'GET'] )
@login_required
def login():
    token = g.user.generate_auth_token()
    resp =  Response(response=json.dumps({'message':'Hello, %s' % g.user.email}), status=200)
    resp.headers['api-key']= token.decode('ascii')
    return resp

@application.route('/post/<int:post_id>')
@login_required
def post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
    application.debug = True
    #application.run(host='0.0.0.0', port=3000)
    application.run()
