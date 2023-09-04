from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Sample user data (for demonstration purposes)
users = {
    'tristan': {'password': 'test'},
    'user2': {'password': 'password2'}
}

# Create a user class for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@socketio.on('message')
@login_required
def handle_message(data):
    message = data['message']
    user = current_user.id  # Get the current user's username
    send({'user': user, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
