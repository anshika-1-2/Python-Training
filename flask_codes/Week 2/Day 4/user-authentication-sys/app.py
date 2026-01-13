from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:anshi@localhost:5432/flask_auth_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user object given an ID

    :param user_id: The ID of the user to load
    :type user_id: int
    :return: The user object, or None if no user is found
    :rtype: User
    """
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles registration of new users.

    GET requests will render the registration form.

    POST requests will validate the input, check if the email is already registered, and if
    so, flash an error message and redirect the user back to the registration form.

    If the email is not already registered, the user data will be stored in the database, and a
    success message will be flashed, then the user will be redirected to the login page.

    :return: The rendered template, or the redirected URL as a string
    :rtype: str
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles GET and POST requests to the "/login" path.

    GET requests will render the login form.

    POST requests will validate the input, check if the email and password are correct, and if
    so, log the user in, then redirect the user to the dashboard page.

    If the email or password are incorrect, flash an error message, and redirect the user back to the
    login form.

    :return: The rendered template, or the redirected URL as a string
    :rtype: str
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the dashboard page, displaying the current user's information.

    :return: The rendered template as a string
    :rtype: str
    """
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    """
    Logs the user out, and redirects them back to the login page.

    :return: The redirected URL as a string
    :rtype: str
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    """Redirects to the login page."""
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
