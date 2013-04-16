from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)
	school_name = TextField('school_name', validators = [Required()])
	school_state = TextField('school_state', validators = [Required()])
	subject = TextField('subject', validators = [Required()])
