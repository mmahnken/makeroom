from flask.ext.wtf import Form, TextField, TextAreaField, BooleanField, Required


class LoginForm(Form):
	openid = TextField('openid')
	remember_me = BooleanField('remember_me', default = False)
	dev_login = TextField('dev_login')
	dev_email = TextField('dev_email')
	
class RegisterForm(Form):
	username = TextField('username', validators = [Required()])
	subject = TextField('subject', validators = [Required()])
	department_id = TextField('department_id', validators = [Required()])

class NewPostForm(Form):
	post = TextAreaField('post', validators = [Required()])
	student_id = TextField('student_id', validators = [Required()])
	is_goal = BooleanField('is_goal', default = False)
	is_mod = BooleanField('is_mod', default = False)

class ApiKeyForm(Form):
	api_key = TextField('api_key', validators = [Required()])
	org_id = TextField('org_id', validators = [Required()])

class CreateDepartmentForm(Form):
	ls_school_id = TextField('ls_school_id', validators = [Required()])
	state = TextField('state', validators = [Required()])





