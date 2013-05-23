makeroom
========

storing and sharing student data for public educators


Database Scripts (db_migrate.py, db_create.py, db_downgrade.py, db_upgrade.py, db_repository)
==============
These are database engine scripts from Miguel Grinberg's Flask tutorial. They are handling new model 
creation in the case that data models change (db_migrate.py), database version control (upgrade, downgrade),
and the initial creation of a database with connection to a some form of a sql database (I used PostgreSQL).
These files require connection to a running sql server, in my case on localhost or heroku's postgresql server.

app
======
Contains all views, templates, and static files. 

init.py instantiates the app in Flask.

models.py contains the sqlalchemy classes that generate tables in a heroku PostgreSQL database. Any time
these models change, the database should be migrated using db_migrate.py.

Virtual Environment (env)
==========
Uses the latest version of virtualenv.py. Contains Python, Flask, WTForms, Flask's openid module, Flask's sqlalchemy.

Procfile
======
declares the process type for heroku.

config.py
======
Holds a variety of environmental constants, including database URIs, open id providers and their URLs,
declarations for the (future) email server, and cross site request forgery protection constants. 

run.py
======
The python file that gets the app as a Flask instance, and runs it using app.run under a set of parameters 
including port (from config.py) and the host ip address (0.0.0.0 for heroku and localhost).



