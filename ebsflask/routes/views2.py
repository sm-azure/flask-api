from flask import Blueprint
from flask import abort, request, jsonify, g, url_for, Response, json
from flask_login import login_required
#import base64

from model.database import db
from model.mca import ManagedAccount

posts = Blueprint("post", __name__, url_prefix="/post")

@posts.route('/<int:post_id>')
@login_required
def post(post_id):
    return 'Post %d' % post_id
