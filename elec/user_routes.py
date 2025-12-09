import os
from datetime import datetime,timedelta
from flask import Flask,Blueprint, render_template, request, redirect, url_for, flash,session,Request,jsonify
from werkzeug.utils import secure_filename
from elec.model import QuoteRequest,Project,Service,Message
from werkzeug.security import check_password_hash,generate_password_hash
from flask_wtf.csrf import CSRFError
from elec import db,mail


UPLOAD_FOLDER = "elec/static/uploads/quotes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


user = Blueprint("user", __name__)


@user.route("/")
def home():
    return render_template("home.html")

@user.route("/services/")
def services():
    all_services = Service.query.order_by(Service.id.asc()).all()
    return render_template('services.html', services=all_services)


@user.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)


@user.route("/about")
def about():
    return render_template("about.html")

@user.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message_text = request.form['message']

        new_message = Message(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )
        db.session.add(new_message)
        db.session.commit()
        flash("Your message has been sent successfully.", "success")
        return redirect(url_for('user.contact'))

    return render_template('contact.html')





@user.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service_type = request.form.get("service_type")
        location = request.form.get("location")
        description = request.form.get("description")
        image = request.files.get("image")

        image_filename = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            image_filename = filename

        new_request = QuoteRequest(
            name=name,
            email=email,
            phone=phone,
            service_type=service_type,
            location=location,
            description=description,
            image_filename=image_filename
        )

        db.session.add(new_request)
        db.session.commit()

        flash("Quote request submitted successfully.", "success")
        return redirect(url_for("user.quote"))

    return render_template("quote.html")

@user.route("/index/")
def index():
    return render_template("index.html")

