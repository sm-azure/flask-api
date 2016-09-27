from flask import Flask
application = Flask(__name__)

@application.route('/')
def index():
    return 'Index Page'

@application.route('/hello')
def hello_world():
    return 'Hello, World!'

@application.route('/user/<username>')
def user(username):
    return 'User %s' % username

@application.route('/post/<int:post_id>')
def post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
    application.debug = True
    #application.run(host='0.0.0.0', port=3000)
    applciation.run()
