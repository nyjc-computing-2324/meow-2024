from typing import Dict
from flask import Flask, redirect, request, session
import view, validate, dbfunctions
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

dbfunctions.make_tables()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["logged_in"] = False
    return view.index()


@app.route('/temp')
def temp():
    return view.temp()


@app.route('/home')
def home():
    if not session["logged_in"]:
        return redirect("/login")
    return view.home()


@app.route('/edit_activities')
def edit_activities():
    if not session["logged_in"]:
        return redirect("/login")
    return view.edit_activities()


@app.route('/about')
def about():
    return view.about()


@app.route('/pp')
def pp():
    return view.pp()


@app.route('/tac')
def tac():
    return view.tac()


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return view.login()
    else:
        username = request.form["username"]
        password = request.form["password"]
        if dbfunctions.login(username, password):
            session["logged_in"] = True
            session["user"] = username
            return redirect("/home")
        else:
            return view.login(error="Invalid username or password")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return view.register()
    else:
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        if validate.username_isvalid(username):
            if validate.password_isvalid(password):
                if dbfunctions.username_taken(username):
                    dbfunctions.create_account(username, password)
                    dbfunctions.create_profile(name, "0000", "meow@meow.com", "77777777", "Meow!", username)
                    session["logged_in"] = True
                    session["user"] = username
                    return redirect("/home")
                else:
                    return view.register(error="Username is already taken")
            else:
                return view.register(error="Password does not meet requirements.")
        else:
            return view.register(error="Username does not meet requirements.")


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if not session["logged_in"]:
        return redirect("/login")
    info = dbfunctions.retrieve_profile(session.get("user"))
    if request.method == "POST":
        if request.form["response"] == "Edit":
            return view.profile(edit=True, profile=info)
        elif request.form["response"] == "Cancel":
            return view.profile(edit=False, profile=info)
        elif request.form["response"] == "Save":
            output = request.form
            fields = output.keys()
            for key in fields:
                if key != "response":
                    dbfunctions.update_profile(session.get("user"), key, output[key])
            info = dbfunctions.retrieve_profile(session.get("user"))
            return view.profile(edit=False, profile=info)
    return view.profile(profile=info)


@app.route('/profile_edit', methods=["GET", "POST"])
def profile_edit():
    if not session["logged_in"]:
        return redirect("/login")
    return view.profile_edit()


@app.route('/view_cca')
def view_cca():
    if not session["logged_in"]:
        return redirect("/login")
    return view.view_cca()


@app.route('/edit_cca')
def edit_cca():
    if not session["logged_in"]:
        return redirect("/login")
    return view.edit_cca()


@app.route('/records_cca')
def records_cca():
    if not session["logged_in"]:
        return redirect("/login")
    return view.records_cca()


@app.route('/records_activities')
def records_activities():
    if not session["logged_in"]:
        return redirect("/login")
    return view.records_activities()


@app.route('/view_activities')
def view_activities():
    if not session["logged_in"]:
        return redirect("/login")
    return view.view_activities()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
