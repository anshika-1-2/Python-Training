from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:anshi@localhost:5432/flask_blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=10240,
    backupCount=5
)

file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.ERROR)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.exception("Database initialization failed")

@app.route('/')
def index():
    """
    Index page of the blog.

    Displays all posts in the database.

    If there is an error while loading the posts, returns an
    "Internal Server Error" response with a 500 status code.

    :return: A rendered template
    :rtype: tuple
    :raises: Exception
    """
    try:
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    except Exception:
        app.logger.exception("Failed to load posts")
        return "Internal Server Error", 500


@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Creates a new post.

    On GET, renders a form to create a post.

    On POST, creates a new post with the given title and content,
    and redirects to the index page.

    If there is an error while creating the post, returns an
    "Internal Server Error" response with a 500 status code.
    :return: A rendered template on GET, a redirect on POST
    :rtype: tuple
    :raises: Exception
    """
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']

            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('index'))

        except Exception:
            db.session.rollback()
            app.logger.exception("Failed to create post")
            return "Internal Server Error", 500

    return render_template('create.html')


@app.route('/post/<int:id>')
def view(id):
    """
    Views a post with the given id.

    On GET, renders a view template for the post.

    If the post does not exist, or if there is an error while
    viewing the post, returns an "Internal Server Error" response
    with a 500 status code.

    :param id: The id of the post to be viewed
    :return: A rendered template on GET
    :rtype: tuple
    :raises: Exception
    """
    try:
        post = Post.query.get_or_404(id)
        return render_template('view.html', post=post)
    except Exception:
        app.logger.exception(f"Failed to view post with id={id}")
        return "Internal Server Error", 500


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    Edits a post with the given id.

    On GET, renders an edit form for the post.

    On POST, updates the post with the given title and content,
    and redirects to the index page.

    If the post does not exist, or if there is an error while
    editing the post, returns an "Internal Server Error" response
    with a 500 status code.

    :param id: The id of the post to be edited
    :return: A rendered template on GET, a redirect on POST
    :rtype: tuple
    :raises: Exception
    """
    try:
        post = Post.query.get_or_404(id)

        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('edit.html', post=post)

    except Exception:
        db.session.rollback()
        app.logger.exception(f"Failed to edit post with id={id}")
        return "Internal Server Error", 500


@app.route('/delete/<int:id>')
def delete(id):
    """
    Deletes a post with the given id.

    :param id: The id of the post to be deleted
    :return: A redirect to the home page
    :rtype: tuple
    :raises: Exception
    """
    try:
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))

    except Exception:
        db.session.rollback()
        app.logger.exception(f"Failed to delete post with id={id}")
        return "Internal Server Error", 500


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global error handler for unhandled exceptions.

    Logs the exception using the application logger and returns a 500 Internal Server Error response.

    :param e: The exception to be handled
    :return: A tuple containing the response text and status code
    :rtype: tuple
    """
    app.logger.exception("Unhandled exception occurred")
    return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(debug=True)