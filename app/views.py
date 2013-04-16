from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': "Mrs. M"} #fake user
	posts = [ #fake array of posts
		{
			'author': { 'nickname': 'Mrs. J'},
			'body': 'Sarah can wear her iPod during tests.'
		},
		{
			'author': {'nickname': 'Mrs. T'},
			'body': 'Tim will complete a daily self-evaluation.'
		}
	]
	return render_template("index.html",
		title = 'Home',
		user = user,
		posts = posts) #The extra parameters (ie "title", 
					   #"user" refer to variables 
					   #that are in the Index HTML template.

@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = LoginForm() #see forms.py
	if form.validate_on_submit():
		flash('Login requested for OpenID=' + form.openid.data + ', remember_me=' + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html',
		title = 'Sign In', #from base.html
		form = form,
		providers = app.config['OPENID_PROVIDERS']) 



