from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

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
    tags = Tag.query.all()
    return render_template('posts/new_post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Show a form to create a new post."""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form["title"],
                    content=request.form["content"], user=user, tags=tags)
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
    tags = Tag.query.all()
    return render_template('posts/edit_post_form.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Form submission to update an existing post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' updated.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Form submission to delete an existing post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/{post.user_id}")

# Tag routes


@app.route('/tags')
def show_tags():
    """Show list of tags."""

    tags = Tag.query.all()
    return render_template('tags/tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show details and post for a single tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_detail.html', tag=tag)


@app.route('/tags/new')
def show_new_tag_form():
    """Show for for adding a new tag."""

    posts = Post.query.all()
    print(posts)
    return render_template('tags/new_tag_form.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def new_tag():
    """Handle adding a new tag."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["tag_name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")
    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show form to edit an existing tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/edit_tag_form.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Handle update of existing tag."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle deleting a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect(f"/users")
