from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html")
    else:
        #get username and password
        #compare to database
        #log user in
        return redirect("/")

@app.route('/register', methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("register.html")
    else:
        #validate username and password
        #add to database
        #log user in
        return redirect("/")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
