from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
socketio = SocketIO(app)

# Dictionary to store connected users
connected_users = {}

# Create a room for private conversations
private_rooms = {}

# Create a dictionary to store messages for each user
user_messages = {}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        user_id = request.sid
        username = session['username']
        connected_users[user_id] = username
        emit_user_list()
        emit_existing_messages(username)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_users:
        username = connected_users[request.sid]
        del connected_users[request.sid]
        emit_user_list()
        leave_all_private_rooms(username)

@socketio.on('message')
def handle_message(data):
    if 'username' in session:
        username = session['username']
        message = data['message']
        emit('message', {'user': username, 'message': message}, broadcast=True)

        # Store the message for the user
        if username in user_messages:
            user_messages[username].append({'user': username, 'message': message})
        else:
            user_messages[username] = [{'user': username, 'message': message}]

@app.route('/private/<recipient>')
def private_chat(recipient):
    if 'username' in session:
        if recipient == session['username']:
            return redirect(url_for('index'))

        room_name = get_private_room_name(session['username'], recipient)
        return render_template('private_chat.html', room_name=room_name)
    return redirect(url_for('index'))

@socketio.on('join_private')
def handle_join_private(data):
    room = data['room']
    join_room(room)

@socketio.on('leave_private')
def handle_leave_private(data):
    room = data['room']
    leave_room(room)

@socketio.on('private_message')
def handle_private_message(data):
    recipient = data['recipient']
    message = data['message']
    sender = session['username']
    room_name = get_private_room_name(sender, recipient)

    emit('message', {'user': sender, 'message': message}, room=room_name)
    emit('message', {'user': sender, 'message': message}, room=request.sid)

    # Store the private message for both sender and recipient
    store_private_message(sender, recipient, message)

def emit_user_list():
    user_list = list(connected_users.values())
    emit('update_user_list', {'users': user_list}, broadcast=True)

def emit_existing_messages(username):
    if username in user_messages:
        messages = user_messages[username]
        for message in messages:
            emit('message', message)

def get_private_room_name(user1, user2):
    return f'private_{user1}_{user2}' if user1 < user2 else f'private_{user2}_{user1}'

def leave_all_private_rooms(username):
    rooms_to_leave = [room for room in private_rooms if username in private_rooms[room]]
    for room in rooms_to_leave:
        leave_room(room)

def store_private_message(sender, recipient, message):
    room_name = get_private_room_name(sender, recipient)
    if room_name in private_rooms:
        private_rooms[room_name].append(sender)
    else:
        private_rooms[room_name] = [sender]
    emit('private_message', {'sender': sender, 'message': message}, room=room_name)
    emit('private_message', {'sender': sender, 'message': message}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
