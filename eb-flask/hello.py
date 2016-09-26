from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>')
def user(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
