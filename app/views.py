from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': "Mrs. M"} #fake user
	return render_template("index.html",
		title = 'Home',
		user = user) #The extra parameters "title" and
					 #"user" refer to variables 
					 #that are in the Index HTML template.

