import os

SECRET_KEY = 'COuT9Mlb1oLA5Q'
SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root@localhost/powerhouse'
SQLALCHEMY_TRACK_MODIFICATIONS=False



UPLOAD_FOLDER = 'elec/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf','avif'}