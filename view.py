from flask import Flask, render_template, redirect, request, session

# completed is a bool, by default False.
completed = True

def index():
    #display index.html which is the launch page
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("index.html")

def temp():
    return render_template("temp.html")
  
def home():
    #display home.html
    #yeah it doesn't exist yet just ignore this first
    raise NotImplementedError

def about():
    #display about.html
    #also doesn't exist yet
    raise NotImplementedError

def login():
    #display login.html
    if completed:
        if request.method == "GET":
            return render_template("login.html")
        # for here, the validation needs to be implemented
        else:
            return redirect("/home")
    else:
        return redirect("/temp")

def register():
    #display register.html
    if completed:
        if request.method == "GET":
            return render_template("register.html")
        # for here the validation needs to be implemented
        else:
            return redirect("/home")
    else:
        return redirect("/temp")
