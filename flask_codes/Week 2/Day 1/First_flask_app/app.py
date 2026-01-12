from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    """
    Renders the index.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
    
@app.route("/<name>")
def welcome(name):
    """
    Renders the welcome.html template with the given name.

    Parameters:
        name (str): The name to be passed to the template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("welcome.html", name=name)

@app.route("/home")
def home():
    """
    Renders the home.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("home.html")

