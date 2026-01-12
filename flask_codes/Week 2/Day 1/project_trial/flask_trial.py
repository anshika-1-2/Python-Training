import flask 

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    """Redirects to the login page."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles both GET and POST requests to the '/login' path.

    If a GET request is received, renders the 'name.html' template.

    If a POST request is received, extracts the 'username' from the request form
    and returns a string greeting the user by name, indicating that a POST request
    was received.
    """
    if request.method == 'POST':
        name = request.form['username']
        return f"Hello {name}, POST request received"
    return render_template('name.html')

if __name__ == '__main__':
    app.run(debug=True)