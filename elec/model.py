from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from elec import db,bcrypt



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(300))
    image = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # electrical, interior, cctv, solar, etc
    before_image = db.Column(db.String(300))
    after_image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Company Identity
    company_name = db.Column(db.String(200), default="Powerhouse Tech & Decor")
    slogan = db.Column(db.String(300))
    about_text = db.Column(db.Text)

    # Contact Info
    phone = db.Column(db.String(50))
    phone_alt = db.Column(db.String(50))
    email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    whatsapp_number = db.Column(db.String(50))

    # Branding
    logo_filename = db.Column(db.String(200))
    hero_image_filename = db.Column(db.String(200))

    # Social Media
    facebook = db.Column(db.String(300))
    instagram = db.Column(db.String(300))
    twitter = db.Column(db.String(300))
    youtube = db.Column(db.String(300))

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
