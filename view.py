from flask import Flask, render_template, redirect, request, session

# completed is a bool, by default False.
completed = True

def index():
    # display index.html which is the launch page
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("index.html")

def view_edit_cca():
    # display view_edit_cca.html
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("view_edit_cca.html")

def records_cca():
    # display records_cca.html
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("records_cca.html")

def records_activities():
    # display records_activities.html
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("records_activities.html")

def temp():
    # displays the underdevelopment page temp.html
    return render_template("temp.html")

def home():
    #display home.html
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("home.html")

def profile():
    # displays profile.html
    if not completed:
        # redirects the user to temp.html
        return redirect("/temp")
    return render_template("profile.html")

def about():
    #display about.html
    #also doesn't exist yet
    raise NotImplementedError

def login(error = ""):
    #display login.html
    if completed:
        return render_template("login.html", error_msg = error)
    else:
        return redirect("/temp")

def register(error = ""):
    #display register.html
    if completed:
        return render_template("register.html", error_msg = error)
    else:
        return redirect("/temp")
