from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid 
from forms import LoginForm, RegisterForm, NewPostForm, ApiKeyForm
from models import Author, Department, Post, ROLE_USER, ROLE_ADMIN
from datetime import datetime 

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user 				#see the "before request" function
	form = NewPostForm()
	return render_template("index.html",
		title = 'Home',
		user = user,
		form = form)


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
		user = Author(nickname = nickname, email = resp.email, role = ROLE_USER)
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


@app.route('/register')
def register():
	form = RegisterForm()
	return render_template('register.html', #from base.html
		form = form)


@app.route('/api_key_form')
def register_api():
	form = ApiKeyForm()
	return render_template('api_key_form.html',
		title = 'api_key_form', #from base.html
		form = form)


@app.route('/user/<nickname>')
@login_required
def user(nickname):
	date = datetime.utcnow()
	department_id = g.user.user_department
	user = Author.query.filter_by(nickname = nickname).first()
	department = Department.query.get(department_id)
	if user == None:
		flash('User' + nickname + " not found.")
		return redirect(url_for('index'))
	user_posts = Post.query.filter_by(user_id = user.id).all()
	dept_posts = db.session.query(
		Post).join(Post.Author).filter(
		Author.user_department == g.user.user_department)
	return render_template('profile.html', user_posts = user_posts,
						date = date, user = user, 
						dept_posts = dept_posts)
	#put in jinja
	for p in posts:
		print p.body

	# q = db.session.query(
	# 	Author).join(Author.posts).filter(
	# 	Author.user_department == g.user.user_department)
	#count = db.session.query(Author).count()
	# for num in range(count):
	# 	post_count = q[num].posts.count()
	# 	for num in range(post_count):
	# 		print q[num].posts[num]
	#return render_template("profile.html", posts = posts, 
	#						date = date, user = user)


@app.route('/registration_saved', methods = ["POST"])
def after_register():
	#update the user's profile
	u = Author.query.filter_by(id = g.user.id).first()
	if u is None:
		flash('Invalid registration. Please enter a valid department ID.')
		return redirect(url_for('register'))	
	u.username = request.form["username"]
	u.user_department = request.form["department_id"]
	u.subject = request.form["subject"]
	db.session.add(u)
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/post_saved', methods = ["POST"])
def add_post():
	p = request.form["post"]
	q = Post(body = p, timestamp = datetime.utcnow(), 
					user_id = g.user.id)
	db.session.add(q)
	db.session.commit()
	return redirect(url_for('index'))





