import os
from flask import Flask, render_template, redirect, flash, request
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# Code from project milestones

# point to heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# remove a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# a way to replace postgres with postgresql & it works for some reason
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")

# 

@app.route("/")
def login():
    """
    Login page of application
    """
    return render_template(
        "login.html",
        client_id = os.getenv("GSCLIENTID")
    )

@app.route("/home")
def home():
    """
    Home page of application
    """
    return render_template(
        "home.html",
    )

if __name__ == "__main__":
    app.run(
       # host=os.getenv("IP", "0.0.0.0"), 
       # port=int(os.getenv("PORT", 8080)), 
        debug=True
    )