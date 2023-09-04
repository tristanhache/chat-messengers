from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
socketio = SocketIO(app)

# Dictionary to store connected users
connected_users = {}

# Create a room for private conversations
private_rooms = {}

# Create a dictionary to store messages for each user
user_messages = {}

# Dictionary to store user accounts
user_accounts = {}

# Check if a user is logged in before allowing access to chat routes
def require_login(route_function):
    def check_login(*args, **kwargs):
        if 'username' not in session:
            flash('You need to log in first.', 'error')
            return redirect(url_for('login'))
        return route_function(*args, **kwargs)
    return check_login

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in user_accounts:
            flash('Username already exists', 'error')
        else:
            password_hash = generate_password_hash(password, method='sha256')
            user_accounts[username] = {'password_hash': password_hash}
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in user_accounts and check_password_hash(user_accounts[username]['password_hash'], password):
        session['username'] = username
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Chat route (protected with require_login decorator)
@app.route('/')
@require_login
def index():
    return render_template('index.html', username=session['username'])

# ... (remaining code, including SocketIO functionality)

if __name__ == '__main__':
    socketio.run(app, debug=True)
