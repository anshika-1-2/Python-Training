
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    """
    Renders the index.html template with the title "Home".
    
    Returns:
        str: The rendered template as a string.
    """
    return render_template("index.html", title="Home")

@app.route("/about")
def about():
    """
    Renders the about.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("about.html", title="About")

@app.route("/contact")
def contact():
    """
    Renders the contact.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template("contact.html", title="Contact")

if __name__ == "__main__":
    app.run(debug=True)
