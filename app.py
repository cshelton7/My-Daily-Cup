import os
import flask
from flask import Flask, render_template, redirect, flash, request, Blueprint
from datetime import datetime
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
from database_functions import get_entries, deleteEntry
from models import db, Joes, Entry

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
            userInfo = Joes.query.filter_by(email=email).first()
            if check_password_hash(userInfo.password, password):
                login_user(userInfo)
                return flask.redirect(flask.url_for("home"))
                # if the user isn't logged in, the password is incorrect
                flask.flash("Password is not correct. Please try again.")
        # if the user does not exist, redirect to signup
        except:
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
            registerUser = Joes(
                email=email,
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(registerUser)
            db.session.commit()
            flask.flash("You have successfully registered.")
            return flask.redirect(flask.url_for("login"))
        # if it throws an error, some input has conflicted with the rules
        except:
            flask.flash(
                "Something went wrong. Either that username is taken or you have left an entry blank. Please try again."
            )
            return flask.redirect(flask.url_for("signup"))
    return render_template("signup.html")


# route to allow user to sign out
@app.route("/signout")
@login_required
def signout():
    logout_user()
    flask.flash("You  have successfully logged out.")
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
    )


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


@app.route("/view_entries", methods=["GET", "POST"])
@login_required
def users_entries():
    """The following data is fake entries that'll be deleted later
    when our database is good to go.

    entries = [
        {"title": "Great day", "post": "Today was a fantastic from sunrise to sunset"},
        {"title": "Horrible day", "post": "Today was the worst day of my life, smh"},
        {
            "title": "Spontaneous",
            "post": "Today, me and wife went on an amazing adventure in the wilderness.",
        },
    ]
    Here we will call a method that queries for the
        entries made by our user from the database. For the time
        being I'll just use the value from the entries
        list that I made above
    """
    # The following algorithm in database functions file
    prev_entries = get_entries(current_user.id)
    if prev_entries is None:
        flask.flash("Sorry, you have no entries at the moment, please add one.")
        return redirect(flask.url_for("home"))
    else:
        return render_template(
            "entries.html", user_entries=prev_entries, length=len(prev_entries)
        )


@app.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    if request.method == "POST":
        """Here we will call a method that removes the
        entry we deleted from the database. For the time
        being I'll just print the value(index of entry deleted).
        Later I'll replace with a database algorith"""

        index = int(flask.request.form["Delete"])
        # The following algorithm in database functions file
        deleteEntry(index)
    return flask.redirect(flask.url_for("users_entries"))


@app.route("/add_entry", methods=["GET", "POST"])
def add():
    # new entry object information
    poster = current_user.id
    title = flask.request.form("title")
    contents = flask.request.form("entry")

    newEntry = Entry(
        user=poster, title=title, content=contents, timestamp=datetime.now()
    )
    db.session.add(newEntry)
    db.session.commit()
    return flask.redirect(flask.url_for("users_entries"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
