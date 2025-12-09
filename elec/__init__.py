from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from elec.admin_routes import admin_bp
    from elec.user_routes import user
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user)

    # Inject settings into templates
    from elec.model import Settings
    @app.context_processor
    def inject_settings():
        settings = Settings.query.first()
        return dict(settings=settings)

    return app

@login_manager.user_loader
def load_user(user_id):
    from elec.model import User
    return User.query.get(int(user_id))
