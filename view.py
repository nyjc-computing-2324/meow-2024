from flask import Flask, render_template, redirect, request, session

# completed is a bool, by default False.
completed = False

def index():
    # display index.html which is the launch page
    return render_template("index.html")

def view_activities():
    # display view_activities.html
    # if not completed:
    #     # redirects the user to temp
    #     return redirect("/temp")
    return render_template("view_activities.html")

def edit_activities():
    # display edit_activiies.html
    return render_template("edit_activities.html")

def view_cca():
    # display view_cca.html
    if not completed:
        #redirects the user to temp
        return redirect("/temp")
    return render_template("view_cca.html")

def edit_cca():
    # display view_cca.html
    if not completed:
        #redirects the user to temp
        return redirect("/temp")
    return render_template("edit_cca.html")

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

def profile(edit = False, profile = None):
    # displays profile.html
    # if not completed:
    #     # redirects the user to temp.html
    #     return redirect("/temp")
    return render_template("profile.html", edit = edit, profile = profile)

def profile_edit():
    #displays profile_edit.html
    return render_template("profile_edit.html")

def about():
    #display about.html
    if not completed:
        return redirect("/temp")
    raise NotImplementedError

def manage():
    #display about.html
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

def tac():
    # display terms-and-conditions.html
    return render_template("terms-and-conditions.html")
