# Backend Files
There is a total of 3 files used by backend.

## auth.py
auth.py file provides functions for hashing passwords and validating passwords against their hashes. It utilizes secure hashing algorithms to generate and verify hashes, enhancing password security.

## database.py
database.py file provides a framework for creating and managing tables in a database. It creates a parent class Table and includes child classes such as Student, Account, CCA, Activity, JunctionTable, StudentCCA, and StudentActivity, each representing a specific type of table with its own set of attributes and methods.

## dbfunction.py
dbfunction.py file instantiates Account, Student, CCA, Activity objects, defines functions(create, update, retrieve, delete) for these tables and junctiontables(Student-Activity, Student-CCA).

# Frontend files
There is a total of 16 files used by frontend

## edit_activities.html
edit_activities.html is the page for editing the user's activites.

## edit_cca.html
edit_cca.html is the page for editing the user's cca.

## home.html
home.html is the home page after the user has logged in.

## index.html
index.html is the home page for the website when user is not logged in.

## login.html
login.html is the page for the user to log into their account.

## navigation.html
navigation.html is the block that is included in every html file. It specifies the links and topbar for each html file depending on if user is logged in.

## privacy-policy.html
privacy-policy.html is the page displaying the privacy policy.

## profile_edit.html
profile_edit.html is the page for the user to edit their profile.

## profile.html
profile.html is the page for the user to view their profile.

## records_activites.html
records_activites.html views all your current activities in general.

## records_cca.html
records_cca.html views all your current ccas in general.

## register.html
register.html is the page for the user to create an account.

## temp.html
temp.html is the landing page for the website.

## terms-and-conditions.html
terms-and-conditions.html is the page displaying the terms of conditions.

## view_activities.html
view_activities.html is the page for viewing a specific activity.

## view_cca.html
view_cca.html is the page for viewing a specific cca.

# Quality Assurance(QA) files
There are a total of 3 files used by QA, which are all stored in the tests folder. These files are all for the purpose of unit-testing via Python's 'unittest' module, where each instantiated class is known, and from herein will be referred to as a 'test case'.

## __init__.py
__init__.py serves as a marker to help Python to detect the test cases in the files below and execute them via the shell.

## test_backend.py
test_backend.py provides test cases to test various isolated groups of functions in dbfunctions.py, namely for account, student profile, co-curricular activity(cca), and activity.

## test_integration.py
test_integration.py provides the test case to test for the correct loading of webapp pages for flask as in main.py/view.py. All other forms of frontend and integration testing such as UI/UX functionality were done via exploratory means for better coverage and integrity.

## test_validate.py
test_validate.py provides the test case to test the validation logic of username and password inputs in validate.py.