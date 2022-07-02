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

# main config
SECRET_KEY = 'lsdjgnwognowig04929rj2'
SECURITY_PASSWORD_SALT = '1do1nu30189310jk1d19381'
DEBUG = False
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = 'vinyushev@gmail.com'
MAIL_PASSWORD = 'Fyfcnfcbz1305'

# mail accounts
MAIL_DEFAULT_SENDER = 'vinyushev@mail.ru'
# APP_MAIL_USERNAME = 'foo'
# APP_MAIL_PASSWORD = 'bar'
