from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "itsasecret#123456789"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def root_route():
    return redirect('/users')


@app.route('/users')
def list_users():
    """Shows list of all users in db."""
    users = User.query.all()
    return render_template('landing.html', users=users)


@app.route("/users/new")
def show_user_form():
    return render_template('new_user_form.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')


@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details of a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)
