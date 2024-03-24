from flask import Flask, redirect, request
import view, validate, database

logged_in = False

app = Flask(__name__)

@app.route('/')
def index():
    return view.index()

@app.route('/temp')
def temp():
    return view.temp()

@app.route('/home')
def home():
    return view.temp()

@app.route('/about')
def about():
    return view.temp()

@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/about')
def index():
    return render_template("home.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return view.login()
    else:
        username = request.form["username"]
        password = request.form["password"]
        if validate.user_isvalid(username, password):
            logged_in = True
            return redirect("/home")
        else:
            return view.login(error="invalid username or password")

@app.route('/register', methods = ["GET", "POST"])
def register():
    return view.register()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)