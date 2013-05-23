makeroom
========

storing and sharing student data for public educators
implemented using the LearnSprout API 
compatibility with most Student Information Systems currently in use

visit Make Room at www.specialeducationapp.com

app
======
Contains all views, templates, and static files. 

init.py instantiates the app in Flask.

models.py contains the sqlalchemy classes that generate tables in a heroku PostgreSQL database. Any time
these models change, the database should be migrated using db_migrate.py.

pysprout.py
=======
A critical component to the Make Room's functionality. Pysprout connects to the LearnSprout API using
Python's requests module, grabs the JSON relevant to the request, and pumps it into the Make Room database
on Heroku. Views.py then displays this information directly from the database in various forms.

Currently, the anyone can visit Make Room and grab Learn Sprout's sample data set. The sample API key
and organization IDs can be found on the relevant registration pages.

Database Scripts 
==============
(db_migrate.py, db_create.py, db_downgrade.py, db_upgrade.py, db_repository)

These are database engine scripts from Miguel Grinberg's Flask tutorial. They are handling new model 
creation in the case that data models change (db_migrate.py), database version control (upgrade, downgrade),
and the initial creation of a database with connection to a some form of a sql database (I used PostgreSQL).
These files require connection to a running sql server, in my case on localhost or heroku's postgresql server.

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



