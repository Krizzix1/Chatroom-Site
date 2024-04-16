'''
app.py contains all of the server application
this is where you'll find all of the get/post request handlers
the socket event handlers are inside of socket_routes.py
'''

from flask import Flask, render_template, request, abort, url_for
from flask_socketio import SocketIO
import db
import secrets

# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
socketio = SocketIO(app)

# don't remove this!!
import socket_routes
from flask import jsonify

# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)
    if user is None:
        return "Error: User does not exist!"

    if user.password != password:
        return "Error: Password does not match!"

    return url_for('home', username=request.json.get("username"))

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = request.json.get("password")

    if db.get_user(username) is None:
        if "?" in username:
            return "Error: Username cannot contain question marks!"
        db.insert_user(username, password)
        return url_for('home', username=username)
    return "Error: User already exists!"

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    if request.args.get("username") is None:
        abort(404)
    username=request.args.get("username")
    friends = db.get_friend_list(username)
    return render_template("home.jinja", username=username, friends=friends)

@app.route('/get_friends/<username>', methods=['GET'])
def get_friends(username):
    friends = db.get_friend_list(username)
    print(f"Friends of {username}: {friends}")
    return jsonify(friends), 200
@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = request.get_json()
    print(f"Adding friend: {data['friend_username']} to user: {data['username']}")  # Debug print
    db.add_friend(data['username'], data['friend_username'])
    return "Friend added"

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    data = request.get_json()
    db.send_friend_request(data['username'], data['friend_username'])
    return "Friend request sent"

@app.route('/approve_friend_request', methods=['POST'])
def approve_friend_request():
    data = request.get_json()
    db.approve_friend_request(data['username'], data['friend_username'])
    socketio.emit('friendAdded', {'username': data['username']}, room=data['friend_username'])
    socketio.emit('friendAdded', {'username': data['friend_username']}, room=data['username'])
    return "Friend request approved"
@app.route('/remove_friend_request', methods=['POST'])
def remove_friend_request():
    data = request.json
    username = data['username']
    friend_username = data['friend_username']
    db.remove_friend_request(username, friend_username)
    return jsonify({'message': 'Friend request removed'})

@app.route('/get_incoming_requests/<username>')
def get_incoming_requests(username):
    incoming_requests = db.get_incoming_requests(username)
    return jsonify(incoming_requests)

@app.route('/get_outgoing_requests/<username>')
def get_outgoing_requests(username):
    outgoing_requests = db.get_outgoing_requests(username)
    return jsonify(outgoing_requests)

if __name__ == '__main__':
    socketio.run(app)
