from flask import Flask, render_template, redirect, request, session

# completed is a bool, by default False.
completed = False

def index():
    # display index.html which is the launch page
    return render_template("index.html")

def view_edit_cca():
    # display view_edit_cca.html
    if not completed:
        # redirects the user to temp
        return redirect("/temp")
    return render_template("view_edit_cca.html")

def records_cca():
    # display records_cca.html
    # if not completed:
    #     # redirects the user to temp
    #     return redirect("/temp")
    return render_template("records_cca.html")

def records_activities():
    # display records_activities.html
    # if not completed:
    #     # redirects the user to temp
    #     return redirect("/temp")
    return render_template("records_activities.html")

def temp():
    # displays the underdevelopment page temp.html
    return render_template("temp.html")
  
def home():
    #display home.html
    return render_template("home.html")

def profile():
    # displays profile.html
    # if not completed:
    #     # redirects the user to temp.html
    #     return redirect("/temp")
    return render_template("profile.html")

def about():
    #display about.html
    #also doesn't exist yet
    if not completed:
        return redirect("/temp")
    raise NotImplementedError

def login(error = ""):
    #display login.html
    return render_template("login.html", error_msg = error)

def register(error = ""):
    #display register.html
    return render_template("register.html", error_msg = error)

def pp():
    # display pravacy-policy.html
    return render_template("privacy-policy.html")

def toc():
    # display terms-and-conditions.html
    return render_template("terms-and-conditions.html")