"""
Connecting db with our flask app.
"""
from webapp import create_app, db

db.create_all(app=create_app())
