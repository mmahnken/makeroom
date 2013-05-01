import os
basedir = os.path.abspath(os.path.dirname(__file__))


#SQLALCHEMY_DATABASE_URI = 'postgresql://meggie:passwordish@localhost/mrdatabase'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/mrdatabase')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
	{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
	{ 'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
	{ 'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
	{ 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
	{ 'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
	]

#email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'specialeducationtool@gmail.com'
MAIL_PASSWORD = 'happenstancecake'

# administrator list
ADMINS = ['specialeducationtool@gmail.com']

