from flask import Flask, render_template, redirect, request, session

def index():
    #display index.html
    return render_template("index.html")

def temp():
    #display temp.html
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
    if request.method == "GET":
        return render_template("login.html")
    else:
        return redirect("/home")

def register():
    #display register.html
    if request.method == "GET":
        return render_template("register.html")
    else:
        return redirect("/home")
    