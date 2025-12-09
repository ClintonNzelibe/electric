import os

SECRET_KEY = 'COuT9Mlb1oLA5Q'

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")

# Use Railway full DB URL if available
SQLALCHEMY_DATABASE_URI = os.environ.get("MYSQL_URL")  # Railway full URL

# Local fallback for testing
if not SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:powerhouse123@localhost/powerhouse"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 5,
    "max_overflow": 10
}



UPLOAD_FOLDER = 'elec/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf','avif'}