import os
from datetime import timedelta

UPLOAD_FOLDER = 'images/collage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    basedir, '..', 'webapp.db'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SECRET_KEY = os.urandom(32)
