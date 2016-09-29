from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from model.billingmodel import db
from model.billingmodel import User, ManagedAccount, VPNTunnel
from flask_httpauth import HTTPBasicAuth


application = Flask(__name__)
auth = HTTPBasicAuth()

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
@auth.login_required
def hello_world():
    token = g.user.generate_auth_token()
    #return jsonify({'message':'Hello, %s' % g.user.email},{ 'token': token.decode('ascii') })
    resp =  Response(response=jsonify({'message':'Hello, %s' % g.user.email}), status=200)
    resp.headers['api-key']= token.decode('ascii')
    return resp

@application.route('/post/<int:post_id>')
def post(post_id):
    return 'Post %d' % post_id

@auth.verify_password
def verify_password(email_or_token, password):
    # try token verification
    print 'Trying token verification'
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try with email verification
        print 'Trying email verification'
        user = User.query.filter_by(email = email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    print 'Setting user'
    g.user = user
    return True

if __name__ == '__main__':
    #application.debug = True
    application.run(host='0.0.0.0', port=3000)
    #application.run()
