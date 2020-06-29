from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SECRET_KEY'] = "itsasecret#123456789"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# User routes


@app.route("/")
def root_route():
    return redirect('/users')


@app.route('/users')
def list_users():
    """Shows list of all users in db."""
    users = User.query.all()
    return render_template('users/users.html', users=users)


@app.route("/users/new")
def new_user_form():
    """Show form for adding a new user."""

    return render_template('users/new_user_form.html')


@app.route('/users/new', methods=['POST'])
def new_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details for a single user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    print(posts)
    return render_template('users/user_detail.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show the edit form for an existing user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Form submission to update an existing user."""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Form submission to delete an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# Post routes


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show form for new post."""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new_post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Show a form to create a new post."""

    title = request.form["title"]
    content = request.form["content"]
    user = User.query.get_or_404(user_id)

    new_post = Post(title=title,
                    content=content, user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details for a single post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Show the edit form for an existing post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post_form.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Form submission to update an existing post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Form submission to delete an existing post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
