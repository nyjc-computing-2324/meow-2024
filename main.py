from typing import Dict
from flask import Flask, redirect, request, session
import view, validate, dbfunctions
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

dbfunctions.make_tables()

all_ccas = dbfunctions.get_all_cca()
cca_names, cca_types = [], []

for cca in all_ccas:
    cca_names.append(cca["name"])
    cca_types.append(cca["type"])

activity_names = dbfunctions.get_all_activity()


def log():
    if session.get("logged_in") == None:
        session["logged_in"] = False


@app.route('/', methods=["GET", "POST"])
def index():
    log()
    if request.method == "POST":
        session["logged_in"] = False
    return view.index()


@app.route('/temp')
def temp():
    log()
    return view.temp()


@app.route('/home')
def home():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.home()


@app.route('/edit_activities')
def edit_activities():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.edit_activities()


@app.route('/about')
def about():
    log()
    return view.about()

@app.route('/pp')
def pp():
    log()
    return view.pp()


@app.route('/tac')
def tac():
    log()
    return view.tac()


@app.route('/login', methods=["GET", "POST"])
def login():
    log()
    if request.method == "GET":
        return view.login()
    else:
        username = request.form["username"]
        password = request.form["password"]
        if validate.user_isvalid(username, password):
            session["logged_in"] = True
            return redirect("/home")
        else:
            return view.login(error="Invalid username or password")


@app.route('/register', methods=["GET", "POST"])
def register():
    log()
    if request.method == "GET":
        return view.register()
    else:
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        tos = request.form.get("TOS-checkbox")
        if validate.username_isvalid(username):
            if validate.password_isvalid(password):
                if not dbfunctions.username_taken(username):
                    if tos == "True":
                        dbfunctions.create_account(username, password)
                        dbfunctions.create_profile(name, "0000",
                                                   "meow@meow.com", "77777777",
                                                   "Meow!", username)
                        session["logged_in"] = True
                        session["user"] = username
                        return redirect("/home")
                    else:
                        return view.register(
                            error="Must agree to terms and conditions")
                else:
                    return view.register(error="Username is already taken")
            else:
                return view.register(
                    error="Password does not meet requirements.")
        else:
            return view.register(error="Username does not meet requirements.")


@app.route('/profile', methods=["GET", "POST"])
def profile():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    info = dbfunctions.retrieve_profile(session.get("user"))
    if request.method == "POST":
        if request.form["response"] == "Edit":
            return view.profile(edit=True, profile=info)
        elif request.form["response"] == "Cancel":
            return view.profile(edit=False, profile=info)
        elif request.form["response"] == "Delete":
            dbfunctions.delete_all_info(session.get("user"))
            return redirect("/login")
        elif request.form["response"] == "Save":
            output = request.form
            fields = output.keys()
            for key in fields:
                if key != "response":
                    dbfunctions.update_profile(session.get("user"), key,
                                               output[key])
            info = dbfunctions.retrieve_profile(session.get("user"))
            return view.profile(edit=False, profile=info)
    return view.profile(profile=info)


@app.route('/add_cca', methods=["GET", "POST"])
def add_cca():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    ccas = dbfunctions.retrieve_all_studentcca("username", session.get("user"))
    data = []
    names = []
    for info in ccas:
        data.append({
            "name": info[1][1],
            "year": info[3],
            "role": info[2],
            "type": info[1][2],
            "status": info[4]
        })
        names.append(info[1][1])
    default = {
        "name": "",
        "start year": "",
        "end year": "",
        "role": "",
        "status": ""
    }
    if request.method == "POST":
        if request.form["response"] == "Cancel":
            return view.records_cca(cca_data=data, edit=False)
        elif request.form["response"] == "Save":
            cca_info = request.form
            if cca_info["name"] in names:
                return view.add_cca(
                    edit=True,
                    data=default,
                    names=cca_names,
                    msg=["error", "You are already in this CCA"])
            elif cca_info["name"] == "":
                return view.add_cca(
                    edit=True,
                    data=default,
                    names=cca_names,
                    msg=["error", "CCA name cannot be left blank"])
            else:
                dbfunctions.create_studentcca(
                    session.get("user"), cca_info["name"], cca_info["role"],
                    f"{cca_info['start-year']} - {cca_info['end-year']}",
                    cca_info["status"])
                return view.add_cca(edit=False,
                                    data={
                                        "name": cca_info["name"],
                                        "start year": cca_info['start-year'],
                                        "end year": cca_info['end-year'],
                                        "role": cca_info["role"],
                                        "status": cca_info["status"]
                                    },
                                    msg=["pass", "CCA added!"])
        elif request.form["response"] == "Okay":
            return view.records_cca(cca_data=data, edit=False)
    return view.add_cca(edit=True, data=default, names=cca_names)


@app.route('/view_cca')
def view_cca():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.view_cca()


@app.route('/edit_cca')
def edit_cca():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.edit_cca()


@app.route('/records_cca', methods=["GET", "POST"])
def records_cca():
    log()
    ccas = dbfunctions.retrieve_all_studentcca("username", session.get("user"))
    data = []
    names = []
    for info in ccas:
        data.append({
            "name": info[1][1],
            "year": info[3],
            "role": info[2],
            "type": info[1][2],
            "status": info[4]
        })
        names.append(info[1][1])
    default = {
        "name": "",
        "start year": "",
        "end year": "",
        "role": "",
        "status": ""
    }
    if not session["logged_in"]:
        return redirect("/login")
    if request.method == "POST":
        if request.form["response"] == "+":
            return view.add_cca(edit=True, data=default, names=cca_names)
        elif request.form["response"] == "-":
            return view.records_cca(cca_data=data, edit=False, delete=True)
        elif request.form["response"] == "Edit":
            return view.records_cca(cca_data=data, edit=True)
        elif request.form["response"] == "Save":
            edits = dict(request.form.lists())
            for i in range(len(data)):
                dbfunctions.update_studentcca(session.get("user"),
                                              data[i]["name"], "role",
                                              edits["role"][i])
                dbfunctions.update_studentcca(session.get("user"),
                                              data[i]["name"], "status",
                                              edits["status"][i])
                dbfunctions.update_studentcca(session.get("user"),
                                              data[i]["name"], "year",
                                              edits["year"][i])
        elif request.form["response"] == "Cancel" or request.form[
                "response"] == "Done":
            pass
        elif request.form["response"] in names:
            dbfunctions.delete_studentcca(session.get("user"),
                                          request.form["response"])
            ccas = dbfunctions.retrieve_all_studentcca("username",
                                                       session.get("user"))
            data = []
            for info in ccas:
                data.append({
                    "name": info[1][1],
                    "year": info[3],
                    "role": info[2],
                    "type": info[1][2],
                    "status": info[4]
                })
            return view.records_cca(cca_data=data, edit=False, delete=True)
    ccas = dbfunctions.retrieve_all_studentcca("username", session.get("user"))
    data = []
    for info in ccas:
        data.append({
            "name": info[1][1],
            "year": info[3],
            "role": info[2],
            "type": info[1][2],
            "status": info[4]
        })
    return view.records_cca(cca_data=data, edit=False)


def get_activity_data():
    activities = dbfunctions.retrieve_studentactivity("username",
                                                      session.get("user"))
    data = []
    names = []
    for info in activities:
        data.append({
            "name": info[1][1],
            "organiser": info[1][2],
            "date": info[1][3],
            "location": info[1][4],
            "status": info[2]
        })
        names.append(info[1][1])
    return data, names


@app.route('/records_activities', methods=["GET", "POST"])
def records_activities():
    log()
    #dbfunctions.create_studentactivity(session.get("user"), "Meow Run", "Completed")

    data, names = get_activity_data()

    if not session["logged_in"]:
        return redirect("/login")

    if request.method == "POST":
        if request.form["response"] == "+":
            return view.add_activity(edit=True)

        elif request.form["response"] == "-":
            return view.records_activities(activity_data=data,
                                           edit=False,
                                           delete=True)

        elif request.form["response"] == "Edit":
            return view.records_activities(activity_data=data, edit=True)

        elif request.form["response"] == "Save":
            edits = dict(request.form.lists())
            for i in range(len(data)):
                dbfunctions.update_studentactivity(session.get("user"),
                                                   data[i]["name"], "status",
                                                   edits["status"][i])

        elif request.form["response"] in names:
            dbfunctions.delete_studentactivity(session.get("user"),
                                               request.form["response"])
            data, names = get_activity_data()
            return view.records_activities(activity_data=data,
                                           edit=False,
                                           delete=True)

        elif request.form["response"] == "Cancel" or request.form[
                "response"] == "Done":
            pass

        elif request.form["response"] == "Join":
            return view.join_activity(edit=True,
                                      name=dbfunctions.get_all_activity())

    data, names = get_activity_data()
    return view.records_activities(activity_data=data,
                                   edit=False,
                                   delete=False)


@app.route('/add_activity', methods=["GET", "POST"])
def add_activity():
    log()

    data, names = get_activity_data()

    if request.method == "POST":
        if request.form["response"] == "Cancel" or request.form[
                "response"] == "Okay":
            return view.records_activities(edit=False, activity_data=data)
        elif request.form["response"] == "Save":
            activity_info = request.form
            if activity_info["name"] in dbfunctions.get_all_activity():
                return view.add_activity(
                    edit=True,
                    msg=[
                        "error",
                        "Activity already exists, try joining the activity instead"
                    ])
            elif activity_info["name"] == "":
                return view.add_activity(
                    edit=True,
                    msg=["error", "Activity name cannot be left blank"])
            else:
                dbfunctions.create_activity(activity_info["name"],
                                            activity_info["organiser"],
                                            activity_info["date"],
                                            activity_info["location"],
                                            session.get("user"))
                dbfunctions.create_studentactivity(session.get("user"),
                                                   activity_info["name"],
                                                   activity_info["status"])
                return view.add_activity(edit=False,
                                         data={
                                             "name":
                                             activity_info["name"],
                                             "organiser":
                                             activity_info["organiser"],
                                             "date":
                                             activity_info["date"],
                                             "location":
                                             activity_info["location"],
                                             "status":
                                             activity_info["status"]
                                         },
                                         msg=["pass", "Activity Created!"])
    return view.add_activity(edit=True)


@app.route('/join_activity', methods=["GET", "POST"])
def join_activity():
    log()

    data, names = get_activity_data()

    if request.method == "POST":
        if request.form["response"] == "Cancel" or request.form[
                "response"] == "Okay":
            return view.records_activities(edit=False, activity_data=data)
        elif request.form["response"] == "Save":
            activity_info = request.form
            if activity_info["name"] in names:
                return view.join_activity(
                    edit=True,
                    msg=["error", "You already joined this activity"],
                    name=dbfunctions.get_all_activity())
            elif activity_info["name"] == "":
                return view.join_activity(
                    edit=True,
                    msg=["error", "Activity name cannot be left blank"],
                    name=dbfunctions.get_all_activity())
            else:
                dbfunctions.create_studentactivity(session.get("user"),
                                                   activity_info["name"],
                                                   activity_info["status"])
                return view.join_activity(edit=False,
                                          data={
                                              "name": activity_info["name"],
                                              "status": activity_info["status"]
                                          },
                                          msg=["pass", "Activity joined!"])
    return view.add_activity(edit=True, name=dbfunctions.get_all_activity())


@app.route('/view_activities')
def view_activities():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.view_activities()


@app.route('/manage')
def manage():
    log()
    if not session["logged_in"]:
        return redirect("/login")
    return view.manage()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
