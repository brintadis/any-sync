"""
Creating a superuser with:
    username,
    email,
    password
for our flask-app then add it into db.
"""
import sys
from datetime import datetime
from getpass import getpass

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()
app.app_context().push()
with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    email = input('Введите email пользователя: ')

    if User.query.filter(User.email == email).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit(0)
new_user = User(
    username=username,
    role='admin',
    email=email,
    registration_date=datetime.today().strftime('%Y-%d-%m %H:%M:%S')
)
new_user.set_password(password)

db.session.add(new_user)
db.session.commit()
print(f'User with id {new_user.id} added')
