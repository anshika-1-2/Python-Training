from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:anshi@localhost/db_flask_sample'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by user_id for Flask-Login.

    Returns:
        Users: The user object if found, otherwise None.
    """
    return Users.query.get(int(user_id))

# Home route
@app.route("/")
def home():
    """
    Renders the home.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("home.html")

# Register route
@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Handles both GET and POST requests to the '/register' path.

    If a GET request is received, renders the 'sign_up.html' template.

    If a POST request is received, extracts the username and password from the request form.
    Validates the input, checking if the username is already taken.
    If the input is invalid, flashes an error message and renders the 'sign_up.html' template.
    If the input is valid, hashes the password using Werkzeug's generate_password_hash and stores the
    user data in memory. Logs the registration and flashes a success message, then redirects the user back to the
    login form.

    Returns:
        str: The rendered template as a string.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Username already taken!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    
    return render_template("sign_up.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles both GET and POST requests to the "/login" path.

    If a GET request is received, renders the "login.html" template.

    If a POST request is received, extracts the username and password from the request form.
    Validates the input, checking for empty values, invalid username, and mismatched password.
    If the input is invalid, flashes an error message and renders the "login.html" template.
    If the input is valid, logs the user in using Flask-Login and redirects the user to the dashboard page.

    Returns:
        str: The rendered template as a string.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# Protected dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    """
    Renders the dashboard.html template, displaying the username of the currently
    logged in user.

    Returns:
        str: The rendered template as a string.
    """

    return render_template("dashboard.html", username=current_user.username)

# Logout route
@app.route("/logout")
@login_required
def logout():
    """
    Logs the user out of the system and redirects them to the home page.

    Returns:
        str: The redirected URL as a string.
    """
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
    