from flask import Blueprint
from flask import abort, request, jsonify, g, url_for, Response, json
#from flask_login import LoginManager, login_required, logout_user, login_user, current_user
#import base64

from model.database import db
from model.mca import ManagedAccount

posts = Blueprint("post", __name__, url_prefix="/post")

# @apis.route('/logout', methods= ['GET'] )
# #@login_required
# def logout():
#     user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return  Response(response=json.dumps({'message':'Successfull Logout!'}), status=200)
#
#
#
# @apis.route('/login', methods = ['POST', 'GET'] )
# #@login_required
# def login():
#     token = g.user.generate_auth_token()
#     resp =  Response(response=json.dumps({'message':'Hello, %s' % g.user.email}), status=200)
#     resp.headers['api-key']= token.decode('ascii')
#     return resp

@posts.route('/<int:post_id>')
#@login_required
def post(post_id):
    return 'Post %d' % post_id
