import os
from datetime import timedelta

UPLOAD_FOLDER = 'images/collage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/playlist"

SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=30)

SECRET_KEY = os.urandom(32)
