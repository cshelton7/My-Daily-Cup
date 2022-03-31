from flask import Flask, render_template, redirect, flash, request
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

@app.route("/")
def login():
    """
    Login page of application
    """
    return render_template(
        "login.html",
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