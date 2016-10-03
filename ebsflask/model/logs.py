# import logging
# from logging.handlers import RotatingFileHandler
#
#
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# logger.setLevel(logging.DEBUG)
# handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
# #handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
# #handler = RotatingFileHandler('/var/log/application.log', maxBytes=1024,backupCount=5)
# handler.setFormatter(formatter)
# application.logger.addHandler(handler)
#
# login_manager = LoginManager()
# login_manager.init_app(application)
#
#
# @login_manager.request_loader
# def load_user_from_request(request):
#     # try token verification from headers
#     token = request.headers.get('api_key')
#     if token:
#         logger.debug('Got api-key token')
#         logger.debug(token)
#         user = User.verify_auth_token(token)
#         # token is valid and user is already logged in - continue
#         if user and user.is_authenticated():
#             g.user = user
#             return user
#         # token is invalid (experied/incorrect) and user is logged in - logout
#         if not user and user.is_authenticated():
#             user.authenticated = False
#             db.session.add(user)
#             db.session.commit()
#             return None
#
#     # try Basic authentication [for initial login]
#     token = request.headers.get('Authorization')
#     if token:
#         logger.debug('Got Authorization token')
#         logger.debug(token)
#         token = token.replace('Basic ', '', 1)
#         try:
#             token = base64.b64decode(token)
#         except TypeError:
#             return None
#         email, password = token.split(":")
#         logger.debug(email)
#         logger.debug(password)
#         user = User.query.filter_by(email = email).first()
#         if not user or not user.verify_password(password):
#             return None
#         # User exists and is logging in - save state
#         user.authenticated = True
#         db.session.add(user)
#         db.session.commit()
#         logger.debug('Setting user')
#         g.user = user
#         return user
#
#     return None
