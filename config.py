import os
from app import app
basedir = os.path.abspath(os.path.dirname(__file__))


#SQLALCHEMY_DATABASE_URI = 'postgresql://meggie:passwordish@localhost/mrdatabase'
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/mrdatabase'
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

