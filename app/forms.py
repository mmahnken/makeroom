from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required

class LoginForm(Form):
	openid = TextField('openid')
	remember_me = BooleanField('remember_me', default = False)
	dev_login = TextField('dev_login')
	dev_email = TextField('dev_email')
	
class RegisterForm(Form):
	username = TextField('username', validators = [Required()])
	subject = TextField('subject', validators = [Required()])
	department_id = TextField('department_id', validators = [Required()])





