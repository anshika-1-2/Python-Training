import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "change-this-in-production"

USERS = {}  

@app.route("/")
def home():
    """
    Renders the index.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("index.html")

@app.route("/register", methods=["GET"])
def register_get():
    """
    Renders the register.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    """
    Handles POST requests to the "/register" path.

    Extracts the name, email, password, and confirm password from the request form.
    Validates the input, checking for empty values, invalid email, short password, and
    mismatched password and confirm password.

    If there are errors, flashes them and redirects the user back to the registration form.

    If the email is already registered, flashes an error message and redirects the user back to the
    registration form.

    Otherwise, hashes the password using Werkzeug's generate_password_hash and stores the
    user data in memory. Logs the registration and flashes a success message, then redirects the
    user back to the home page.

    Returns:
        str: The redirected URL as a string.
    """
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errors = []
    if not name:
        errors.append("Name is required.")
    if not email or "@" not in email:
        errors.append("A valid email is required.")
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if password != confirm:
        errors.append("Password and confirm password do not match.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("register_get"))

    if email in USERS:
        flash("Email is already registered.", "error")
        return redirect(url_for("register_get"))

    password_hash = generate_password_hash(password)
    USERS[email] = {"name": name, "password_hash": password_hash}

    logger.debug("Registered user: %s", email)
    flash("Registration successful! (Stored in memory)", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
