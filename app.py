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
<<<<<<< HEAD
    )
=======
    )


@app.route("/view_entries", methods=["GET", "POST"])
def users_entries():
    """The following data is fake entries that'll be deleted later
    when our database is good to go.
    """
    entries = [
        {"title": "Great day", "post": "Today was a fantastic from sunrise to sunset"},
        {"title": "Horrible day", "post": "Today was the worst day of my life, smh"},
        {"title": "Spontaneous", "post": "Today, me and wife went on an amazing adventure in the wilderness."}
    ]   
    '''Here we will call a method that queries for the
        entries made by our user from the database. For the time
        being I'll just use the value from the entries
        list that I made above
    '''
    return render_template(
            "entries.html", user_entries=entries, length=len(entries)
        )


@app.route('/delete_entry', methods=['GET','POST'])
def delete_entry():
    if request.method=='POST':
        '''Here we will call a method that removes the
        entry we deleted from the database. For the time
        being I'll just print the value(index of entry deleted).
        Later I'll replace with a database algorith'''
        
        index = int(request.form['Delete'])
        print(index)
    return redirect('/view_entries')


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
>>>>>>> parent of 1193cbd (Revert "Added a tiny amount of bootstrap to the entry post and added the x/cancek button to them as well.")
