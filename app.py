from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

# List to store chat messages
chat_history = []

# Sample user data (for demonstration purposes)
users = {
    'tristanhache2009@gmail.com': {'password': 'trust'},
    'user2@example.com': {'password': 'password2'}
}

# Create a user class for Flask-Login
class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(data):
    message = data['message']
    user = data['user']
    chat_history.append({'user': user, 'message': message})
    send({'user': user, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
