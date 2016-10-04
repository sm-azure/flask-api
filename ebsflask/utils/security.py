from flask import current_app
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from model.database import db
from model.user import User

import base64, json

login_manager = LoginManager()

@login_manager.request_loader
def load_user_from_request(request):
    # try token verification from headers
    req = request.headers
    #raise Exception (req)
    current_app.logger.error(req)
    token = request.headers.get('api_key')
    if token:
        current_app.logger.error("Got api-key token")
        current_app.logger.error(token)
        user = User.verify_auth_token(token)
        # token is valid and user is already logged in - continue
        if user and user.is_authenticated():
            #login_user(user)
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
        current_app.logger.error("Got Authorization")
        current_app.logger.error(token)
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
        except TypeError:
            return None
        email, password = token.split(":")
        current_app.logger.error(email)
        current_app.logger.error(password)
        user = User.query.filter_by(email = email).first()
        if not user or not user.verify_password(password):
            return None
        # User exists and is logging in - save state
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        current_app.logger.debug('Setting user')
        #login_user(user)
        return user
    current_app.logger.error("Found nothing!!")
    return None
