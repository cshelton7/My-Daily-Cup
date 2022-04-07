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
from .database_functions import get_entries, deleteEntry
from .models import db, Joes, Entry
from .fun_fact import fun_fact
from .nyt import nyt_results
from .twitter import get_trends

load_dotenv(find_dotenv())

main = Blueprint("main", __name__)

# route to user's home page
@main.route("/home")
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
    )


# route to mainly user settings
# this is still in progress. how to store preferences, etc
@main.route("/settings")
@login_required
def settings():
    """
    Home page of application
    """
    return render_template(
        "settings.html",
    )


@main.route("/view_entries", methods=["GET", "POST"])
@login_required
def users_entries():
    """When the user enters there entries page, we'll then use this function
    to display all of their previous entries."""
    # The following algorithm in the database functions file
    prev_entries = get_entries(current_user.id)
    print(prev_entries[0].timestamp)
    if prev_entries is None:
        flask.flash("Sorry, you have no entries at the moment, please add one.")
        return redirect(flask.url_for("main.home"))
    else:
        return render_template(
            "entries.html", user_entries=prev_entries, length=len(prev_entries)
        )


@main.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    if request.method == "POST":
        """Here we will call a method that removes the
        entry we deleted from the database. For the time
        being I'll just print the value(index of entry deleted).
        Later I'll replace with a database algorith"""

        index = int(flask.request.form["Delete"])
        # The following algorithm in the database functions file
        deleteEntry(index)
    return flask.redirect(flask.url_for("main.users_entries"))


@main.route("/add_entry", methods=["GET", "POST"])
def add():
    # new entry object information
    poster = current_user.id
    title = flask.request.form["title"]
    contents = flask.request.form["entry"]

    newEntry = Entry(
        user=poster, title=title, content=contents, timestamp=datetime.now()
    )
    db.session.add(newEntry)
    db.session.commit()
    return flask.redirect(flask.url_for("main.users_entries"))
