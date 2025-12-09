import os

SECRET_KEY = 'COuT9Mlb1oLA5Q'


SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")

db_url = os.environ.get("MYSQL_URL")

# Fix if someone accidentally uses the old mysql:// format
if db_url and db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

SQLALCHEMY_DATABASE_URI = db_url

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 5,
    "max_overflow": 10
}


UPLOAD_FOLDER = 'elec/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf','avif'}