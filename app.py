# pylint: disable=no-member
"""App routing and logic of application, application runs based off this file"""
import os
from datetime import datetime
import flask
from flask import Flask, render_template, redirect, request
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv
from openweather import get_weather
from database_functions import get_entries, delete_Entry
from models import db, Joes, Entry

from fun_fact import fun_fact
from nyt import nyt_results

from twitter import get_trends
from nasa import nasa_picture
from formatDate import formation
from sentiment import get_emotion
from nasa import nasa_picture


load_dotenv(find_dotenv())

# Create app, configure db
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = os.getenv("SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")

db.init_app(app)
with app.app_context():
    db.create_all()

# initializing login feature
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Loads user ID of user"""
    return Joes.query.get(int(user_id))


# route to log a user in
# add auth back later
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Login page of application
    """
    # when the user submits credentials
    if flask.request.method == "POST":
        # check form information
        email = request.form.get("email")
        password = request.form.get("pass")
        # if the user exists, log in & redirect to home page
        try:
            user_info = Joes.query.filter_by(email=email).first()
            if check_password_hash(user_info.password, password):
                login_user(user_info)
                return flask.redirect(flask.url_for("home"))
                # if the user isn't logged in, the password is incorrect
                flask.flash("Password is not correct. Please try again.")
        # if the user does not exist, redirect to signup
        except LookupError:
            flask.flash("No user with that email found. Register below!")
            return flask.redirect(flask.url_for("signup"))
    return render_template(
        "login.html",
    )


# route to allow a user to register
# add auth back later
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Signup page of application
    """
    # when the user submits credentials
    if flask.request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("pass")
        # hash the password to store in the db
        try:
            # includes password hashing with the 256 bit-long encrypting method
            register_user = Joes(
                email=email,
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(register_user)
            db.session.commit()
            flask.flash("You have successfully registered.")
            return flask.redirect(flask.url_for("login"))
        # if it throws an error, some input has conflicted with the rules
        except LookupError:
            flask.flash(
                "Something went wrong. Either that username is taken or \
                you have left an entry blank. Please try again."
            )
            return flask.redirect(flask.url_for("signup"))
    return render_template("signup.html")


# route to allow user to sign out
@app.route("/signout")
@login_required
def signout():
    """Simple signout function using logout_user"""
    logout_user()
    flask.flash("You have successfully logged out.")
    return flask.redirect(flask.url_for("login"))


# route to user's home page
@app.route("/home")
@login_required
def home():
    """
    Home page of application
    """
    return render_template(
        "home.html",
        user=current_user.username,
        weather_info=get_weather(),
        fun_fact=fun_fact(),
        nyt=nyt_results(),
        twitter_trends=get_trends(),
        nasa=nasa_picture(),
    )


<<<<<<< Updated upstream
# route to apply user settings
# this is still in progress. how to store preferences, etc
@app.route("/settings")
@login_required
def settings():
    """
    Home page of application
    """
    return render_template(
        "settings.html",
    )

=======
@app.route("/add_task_list", methods=["GET", "POST"])
def add_task_list():
    """Function to add items to task list"""
    if flask.request.method == "POST":
        user = current_user.id
        title = request.form.get("task_list_title")
        content = request.form.get("task_entry")
        print(title)
        print(content)
        task_list_information = Task(title=title, content=content, user=user)

        db.session.add(task_list_information)
        db.session.commit()

    return flask.redirect(flask.url_for("home"))


@app.route("/display_task_lists", methods=["GET", "POST"])
def display_task_list():
    """Function to display items in task list."""

    task_lists = get_task_lists(current_user.id)

    return render_template(
        "home.html", task_lists=task_lists, all_task_lists=len(task_lists)
    )


@app.route("/delete_task_list", methods=["GET", "POST"])
def delete_task_list():
    """Function to delete item from task list"""
    if flask.request.method == "POST":
        index = request.form.get("delete_task_list")
        delete_task_list(index)
    return flask.redirect(flask.url_for("home"))


>>>>>>> Stashed changes

@app.route("/view_entries", methods=["GET", "POST"])
@login_required
def users_entries():
    """When the user enters there entries page, we'll then use this function
    to display all of their previous entries."""
    # The following algorithm in the database functions file
    prev_entries = get_entries(current_user.id)
    # adding tone aspect for each entry
    tones = []
    if len(prev_entries) == 0:
        print("here")
        flask.flash(
            "Sorry, you have no entries at the moment, please add one at the bottom."
        )
        return redirect(flask.url_for("home"))
    else:
        for entry in prev_entries:
            pass
            # tones.append(get_emotion(entry))
        return render_template(
            "entries.html",
            user_entries=prev_entries,
            length=len(prev_entries),
            tones=tones,
            num_tones=len(tones),
        )


@app.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    """Route to delete an entry in the users journal.
    Here we will call a method that removes the
    entry we deleted from the database. For the time
    being I'll just print the value(index of entry deleted).
    Later I'll replace with a database algorith"""
    if request.method == "POST":
        index = int(flask.request.form["Delete"])
        # The following algorithm in the database functions file
        delete_Entry(index)
    return flask.redirect(flask.url_for("users_entries"))


@app.route("/add_entry", methods=["GET", "POST"])
def add():
    """Function to add entry to user journals"""
    # new entry object information
    poster = current_user.id
    title = flask.request.form["title"]
    contents = flask.request.form["entry"]

    newEntry = Entry(
        user=poster, title=title, content=contents, timestamp=formation(datetime.now())
    )
    db.session.add(new_entry)
    db.session.commit()
    return flask.redirect(flask.url_for("users_entries"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
