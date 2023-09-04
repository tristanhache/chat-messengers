from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
login_manager = LoginManager()
login_manager.init_app(app)


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

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", username=current_user.id)
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            print(f"Logged in as {email}")  # Add this line for debugging
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
