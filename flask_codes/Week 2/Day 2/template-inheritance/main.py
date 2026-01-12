from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """
    Renders the home.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template('home.html')

@app.route('/about')
def about():
    """
    Renders the about.html template.

    Returns:
        str: The rendered template as a string.
    """
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)