from flask import Flask, render_template, request, redirect, session
import functions

app = Flask(__name__)

app.secret_key = b'cfryegvuhbdwij4879'


def logged_in() -> bool:
    return ("username" in session)

def authenticate(username: str, password: str) -> bool:
    return validate_login(username, password)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        print("Usermame: ", request.form["username"])
        print("Password: ", request.form["password"])

    username, password = request.form["username"], request.form["password"]
    authorised = validate_register(username, password)
    if authorised:
        session['username'] = username
        return redirect("/login")
    else:
        return render template("register.html", errror_mdg="wrong username or password format, try again!")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        print("Usermame: ", request.form["username"])
        print("Password: ", request.form["password"])

    username, password = request.form["username"], request.form["password"]

    authorised = authenticate(username, password)
    if authorised:
        session['username'] = username  # do not store password!
        return redirect("/profile")
    else:
        return render_template("login.html", error_msg="wrong username or password! try again!")


@app.route("/profile")
def profile():
    if not logged_in():
        return redirect("/login")
    return render_template("profile.html", username=session["username"])

app.run("0.0.0.0")