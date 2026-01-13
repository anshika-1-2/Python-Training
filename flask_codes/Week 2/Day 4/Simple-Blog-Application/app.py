from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:anshi@localhost:5432/flask_blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """
    Index page of the blog application.

    Retrieves all posts from the database and renders the index.html template
    with the posts.

    Returns:
        str: The rendered index.html template as a string.
    """
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new blog post.

    If the request method is POST, create a new blog post based on the
    title and content provided in the request form. Add the new post to
    the database and commit the changes. Redirect the user back to the
    index page.

    If the request method is GET, render the create.html template.
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/post/<int:id>')
def view(id):
    """
    Views a post with the given id.

    :param id: The id of the post to view
    :return: A rendered template of the post
    """
    post = Post.query.get_or_404(id)
    return render_template('view.html', post=post)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    Edits a post with the given id.

    :param id: The id of the post to edit
    :return: A redirect to the index page if the request method is POST, 
             otherwise renders the edit.html template with the post to edit
    """
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:id>')
def delete(id):
    """
    Deletes a post with the given id.

    :param id: The id of the post to delete
    :return: A redirect to the index page
    """
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
