from flask import Flask, redirect, request, session
import view, validate, database, dbfunctions

app = Flask(__name__)

@app.route('/')
def index():
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

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return view.login()
    else:
        username = request.form["username"]
        password = request.form["password"]
        if dbfunctions.login(username, password):
            session["logged_in"] = True
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
                return redirect("/home")
            else:
                return view.register(error="Password does not meet requirements.")
        else:
            return view.register(error="Username does not meet requirements.")

@app.route('/profile')
def profile():
    return view.profile()

@app.route('/view_edit_cca')
def view_edit_cca():
    return view.view_edit_cca()

@app.route('/records_cca')
def records_cca():
    return view.records_cca()

@app.route('/records_activities')
def records_activities():
    return view.records_activities()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)