from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid 
from forms import LoginForm, RegisterForm, NewPostForm, ApiKeyForm
from models import Author, Department, Post, Student, Comment, Goal, Mod, ROLE_USER, ROLE_ADMIN
from datetime import datetime 

from pysprout import LearnSproutClient

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user 		#from @app.route.before_request
	today = datetime.utcnow()
	posts = Post.query.all()
	return render_template("index.html",
			title = 'Home',
			today = today,
			user = user,
			posts = posts)

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
		title = 'LearnSprout Registration',
		form = form)

@app.route('/api_key_registered', methods = ["POST"])
def api_registered():
	#Update the teacher's api_key and org_id.
	u = Author.query.filter_by(id = g.user.id).first()
	u.api_key = request.form['api_key']
	u.org_id = request.form['org_id']
	db.session.add(u)
	db.session.commit()
	#Register the client using form info and access the Learn Sprout JSON.
	client = LearnSproutClient(g.user.api_key)
	list_of_students = client.get_students(g.user.org_id, 'student')
	print list_of_students
	for i in list_of_students['data']:
		#Add each student to the database.
		id_check = i['id']
		s = Student.query.filter_by(lsid = id_check).first()
		if s != None:
			continue
		else:	
			s = Student(first_name = i['first_name'], last_name = i['last_name'], 
			birthday = i['birthday'], lsid = i['id'], 
			grade = i['grade'], school_id = i['school']['id'], teacher_id = g.user.id)
			db.session.add(s)
	#Commit all new information to database.
	db.session.commit()
	flash('LearnSprout connection successful.')
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	date = datetime.utcnow()
	department_id = g.user.user_department
	user = Author.query.filter_by(nickname = nickname).first()
	if user.user_department:
		#department = Department.query.get(department_id)
		dept_posts = db.session.query(
			Post).join(Post.Author).filter(
			Author.user_department == g.user.user_department
			)
	else:
		dept_posts =  None
	user_posts = Post.query.filter_by(user_id = user.id).all()
	if user == None:
		flash('User' + nickname + " not found.")
		return redirect(url_for('index'))
	return render_template('profile.html', user_posts = user_posts,
						date = date, user = user, 
						dept_posts = dept_posts)


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


@app.route('/goal_saved', methods = ["POST", "GET"])
def add_goal():
	p = request.form["post"]
	s = request.form["student_id"]
	timestamp = datetime.utcnow()
	q = Post(body = p, timestamp = timestamp, 
					user_id = g.user.id, student_id = s)
	m = Goal(body = p, user_id = g.user.id)
	db.session.add(q)
	db.session.add(m)
	db.session.commit()
	flash('Post successful.')
	return redirect(url_for('user', nickname = g.user.nickname))

@app.route('/mod_saved', methods = ["POST", "GET"])
def add_mod():
	p = request.form["post"]
	s = request.form["student_id"]
	timestamp = datetime.utcnow() 
	q = Post(body = p, timestamp = timestamp, 
					user_id = g.user.id, student_id = s)
	m = Mod(body = p, user_id = g.user.id)
	db.session.add(q)
	db.session.add(m)
	db.session.commit()
	flash('Post successful.')
	return redirect(url_for('user', nickname = g.user.nickname))

@app.route('/student_profile/<student>')
def view_student(student):
	s = Student.query.filter_by(last_name = student).first()
	student_id = s.id
	student_firstname = s.first_name
	student_lastname = s.last_name
	student_grade = s.grade
	student_birthday = s.birthday 
	student_posts = s.posts
	teachers = Author.query.filter_by(user_department = g.user.user_department).all() 
	goals = Goal.query.filter_by(user_id=g.user.id)
	mods = Mod.query.filter_by(user_id = g.user.id)
	form = NewPostForm()
	return render_template('student_profile.html',
		student_id = student_id,
		student_firstname = student_firstname,
		student_lastname = student_lastname,
		student_grade = student_grade,
		student_birthday = student_birthday,
		student_posts = student_posts,
		teachers = teachers,
		mods = mods,
		goals = goals,
		form = form)

@app.route('/students')
def show_students():
	students = Student.query.filter_by(teacher_id = g.user.id).all()
	return render_template('students.html', students = students)

@app.route('/add_comment/<post>')
def add_comment(post):
	p = Post.query.filter_by(id = post).first()
	post_id = p.id 
	form = NewPostForm()
	comments = Comment.query.filter_by(post_id = post).all()
	return render_template('add_comment.html', form = form,
		post = p,
		post_id = post_id,
		comments = comments)

@app.route('/comment_saved/<post>', methods = ["POST", "GET"])
def comment_saved(post):
	p = Post.query.filter_by(id = post).first()
	c = request.form["post"]
	c = Comment(body = c, user_id = g.user.id, post_id = p.id)
	db.session.add(c)
	db.session.commit()
	flash('Comment successful.')
	return redirect("/index")







