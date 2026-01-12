from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    """
    Render the index.html template with a message.

    Returns:
        str: The rendered template as a string.
    """
    message = "Hello, World"
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)