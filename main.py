from flask import Flask, redirect, request, session
import view, validate, database, dbfunctions
import os


app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        session["logged_in"] = False
    return view.index()

@app.route('/temp')
def temp():
    return view.temp()

@app.route('/home')
def home():
    return view.home()

@app.route('/about')
def about():
    return view.about()

@app.route('/pp')
def pp():
    return view.pp()

@app.route('/tac')
def tac():
    return view.tac()

@app.route('/login', methods = ["GET", "POST"])
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
            return view.login(error="invalid username or password")

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return view.register()
    else:
        username = request.form["username"]
        password = request.form["password"]
        if validate.username_isvalid(username):
            if validate.password_isvalid(password):
                dbfunctions.create_account(username, password)
                session["logged_in"] = True
                session["user"] = username
                return redirect("/home")
            else:
                return view.register(error="Password does not meet requirements.")
        else:
            return view.register(error="Username does not meet requirements.")

@app.route('/profile', methods = ["GET", "POST"])
def profile():
    if request.method == "POST":
        if request.form["response"] == "Edit":
            return view.profile(edit = True)
        elif request.form["response"] == "Save":
            return view.profile(edit = False)
        elif request.form["response"] == "Cancel":
            return view.profile(edit = False)
    return view.profile()

@app.route('/profile_edit', methods = ["GET", "POST"])
def profile_edit():
    return view.profile_edit()

@app.route('/view_edit_cca')
def view_edit_cca():
    return view.view_edit_cca()

@app.route('/records_cca')
def records_cca():
    return view.records_cca()

@app.route('/records_activities')
def records_activities():
    return view.records_activities()

@app.route('/view_edit_activities')
def view_edit_activities():
    return view.view_edit_activities()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)