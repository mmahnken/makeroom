from app import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class Author(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	subject = db.Column(db.String(120), index = True, unique = False)
	user_department = db.Column(db.Integer, 
					db.ForeignKey('department.id'))
	posts = db.relationship('Post', backref = 'Author', lazy = 'dynamic')
	api_key = db.Column(db.String(64), index = True, unique = False)
	org_id = db.Column(db.String(64), index = True, unique = False)
	students = db.relationship('Student', backref = 'Author', lazy = 'dynamic')

	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def get_id(self):
		return unicode(self.id)
	
	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def __repr__(self):
		return '<User %r>' % (self.nickname)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('author.id'))
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	goals = db.relationship('Goal', backref = 'Post', lazy = 'dynamic')
	mods = db.relationship('Mod', backref = 'Mod', lazy = 'dynamic')
	comments = db.relationship('Comment', backref = 'Comment', lazy = 'dynamic')


	def __repr__(self):
		return '<Post %r>' % (self.body)

class Department(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	state = db.Column(db.String(120))
	school_id = db.Column(db.String(120), index = True, unique = False)
	authors = db.relationship('Author', backref = 'Department', lazy = 'dynamic')

	def __repr__(self):
		return '<Department %r>' % (self.id)

class Student(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String(120), index = True, unique = False)
	last_name = db.Column(db.String(120), index = True, unique = False)
	birthday = db.Column(db.String(120), index = False, unique = False)
	lsid = db.Column(db.String(120), index = False, unique = True)
	grade = db.Column(db.Integer(12), index = False, unique = False)
	school_id = db.Column(db.String(120), index = True, unique = False)
	posts = db.relationship('Post', backref = 'Student', lazy = 'dynamic')
	teacher_id = db.Column(db.Integer, db.ForeignKey('author.id'))
	
	def __repr__(self):
		return '<Student %r>' % (self.id)

class Goal(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(200))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('author.id'))

class Mod(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(200))	
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('author.id'))

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(300))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('author.id'))



