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
from .openweather import get_weather

# from database_functions import get_entries, deleteEntry
from .models import db, Joes, Entry

load_dotenv(find_dotenv())

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
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
                return flask.redirect(flask.url_for("main.home"))
                # if the user isn't logged in, the password is incorrect
                flask.flash("Password is not correct. Please try again.")
        # if the user does not exist, redirect to signup
        except:
            flask.flash("No user with that email found. Register below!")
            return flask.redirect(flask.url_for("auth.signup"))
    return render_template(
        "login.html",
    )


# route to allow a user to register
# add auth back later
@auth.route("/signup", methods=["GET", "POST"])
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
            return flask.redirect(flask.url_for("auth.login"))
        # if it throws an error, some input has conflicted with the rules
        except:
            flask.flash(
                "Something went wrong. Either that username is taken or you have left an entry blank. Please try again."
            )
            return flask.redirect(flask.url_for("auth.signup"))
    return render_template("signup.html")


# route to allow user to sign out
@auth.route("/signout")
@login_required
def signout():
    logout_user()
    flask.flash("You  have successfully logged out.")
    return flask.redirect(flask.url_for("auth.login"))
