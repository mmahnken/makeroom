from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid 
from forms import LoginForm, RegisterForm
from models import Author, Department, Post, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user 				#see the "before request" function
	posts = [
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
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
			return redirect(url_for('index'))
	form = LoginForm() #see forms.py
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = 
							['nickname', 'email'])
	return render_template('login.html',
		title = 'Sign In', #from base.html
		form = form,
		providers = app.config['OPENID_PROVIDERS']) 

@lm.user_loader
def load_user(id):
	return Author.query.get(int(id))

@oid.after_login
def after_login(resp):
	#The "resp" is information returned by the Open ID provider.
	#This if statement is to ascertain a valid email.
	print resp.email
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please enter an email.')
		redirect(url_for('login'))
	user = Author.query.filter_by(email = resp.email).first()
	#The next if statement searches the database for the email provided.
	#The nested if statement handles the case of a missing nickname.
	#If the email is not in the database, this if statement adds it.
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = Author(nickname = nickname, email = resp.email, subject = subject, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	#The value for remember_me is loaded from the Flask session here.
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	#The last line navigates the user to the next page, or 
	# to the index page is the next page was not provided.
	#if user.subject != None and user.user_department != None:
	if user.email == resp.email:
		return redirect(request.args.get('next') or url_for('index'))
	else:
		return redirect(url_for('register'))

@app.before_request
def before_request():
	#The current user is set by Flask-Login. Now there is a copy in
	# the g object in order to have better access to the current user.
	g.user = current_user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = Author.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	posts = [
		{ 'author': user, 'body': 'Test post #1'},
		{ 'author':user, 'body': 'Test post #2' }
	]
	return render_template('user.html',
		user = user,
		posts = posts)


@app.route('/register')
def register():
	form = RegisterForm()
	return render_template('register.html',
		title = 'register', #from base.html
		form = form)

@app.route('/registration_saved', methods = ["POST"])
def after_register():
	#check for department_id in database
	a = request.form["department_id"]
	d = Department.query.filter_by(department_id = a).first()
	if d is None:
		flash('Invalid registration. Please enter a valid department ID.')
		redirect(url_for('register'))
	#query for user info
	b = g.user.id
	u = Author.query.filter_by(id = b).first()
	#accepts, adds, and commits nickname, email, subject
	u.user_department = d
	u.username = request.form["username"]
	u.subject = request.form["subject"]
	db.session.commit()
	return redirect(url_for('index'))





