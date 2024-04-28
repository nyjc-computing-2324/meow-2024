# Backend Files
There is a total of 3 files used by backend.

## auth.py
auth.py file provides functions for hashing passwords and validating passwords against their hashes. It utilizes secure hashing algorithms to generate and verify hashes, enhancing password security.


## database.py
database.py file provides a framework for creating and managing tables in a database. It creates a parent class Table and includes child classes such as Student, Account, CCA, Activity, JunctionTable, StudentCCA, and StudentActivity, each representing a specific type of table with its own set of attributes and methods.

## dbfunction.py
dbfunction.py file instantiates Account, Student, CCA, Activity objects, defines functions(create, update, retrieve, delete) for these tables and junctiontables(Student-Activity, Student-CCA).