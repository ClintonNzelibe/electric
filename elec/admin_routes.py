# admin/routes.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from elec.model import db, User, QuoteRequest, Service, Project, Message,Settings
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from elec import bcrypt  # we initialized bcrypt in app.py
from elec.utils import save_image
from flask import current_app

admin_bp = Blueprint("admin", __name__, template_folder="templates", static_folder="../static")




@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("admin.login"))
    return render_template("admin/admin_login.html")

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    # show counts and quick items
    total_services = Service.query.count()
    total_projects = Project.query.count()
    total_quotes = QuoteRequest.query.count()
    total_messages = Message.query.count()
    recent_quotes = QuoteRequest.query.order_by(QuoteRequest.date_created.desc()).limit(6).all()
    return render_template("admin/admin_dashboard.html",
                           total_services=total_services,
                           total_projects=total_projects,
                           total_quotes=total_quotes,
                           total_messages=total_messages,
                           recent_quotes=recent_quotes)



# You can add CRUD routes for services and projects similarly later
# -------- SERVICES CRUD -------- #

@admin_bp.route("/services")
@login_required
def admin_services():
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template("admin/services.html", services=services)

@admin_bp.route("/services/add", methods=["GET", "POST"])
@login_required
def add_service():
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")

        # File handling
        file = request.files.get("image")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        new_service = Service(
            title=title,
            category=category,
            description=description,
            image=filename,
            image_path=filename
        )

        db.session.add(new_service)
        db.session.commit()

        flash("Service added successfully.", "success")
        return redirect(url_for("admin.admin_services"))

    return render_template("admin/add_service.html")

@admin_bp.route("/services/edit/<int:service_id>", methods=["GET", "POST"])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        service.title = request.form.get("title")
        service.category = request.form.get("category")
        service.description = request.form.get("description")

        file = request.files.get("image")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            service.image_path = filename  # update

        db.session.commit()   # <<< YOU FORGOT THIS

        flash("Service updated successfully!", "success")
        return redirect(url_for("admin.admin_services"))

    return render_template("admin/edit_service.html", service=service)



@admin_bp.route("/services/delete/<int:service_id>")
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)

    db.session.delete(service)
    db.session.commit()

    flash("Service deleted successfully.", "info")
    return redirect(url_for("admin.admin_services"))


@admin_bp.route('/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)


@admin_bp.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        description = request.form['description']
        category = request.form['category']

        before_image = save_image(request.files['before_image'])
        after_image = save_image(request.files['after_image'])

        new_project = Project(
            title=title,
            location=location,
            description=description,
            category=category,
            before_image=before_image,
            after_image=after_image
        )

        db.session.add(new_project)
        db.session.commit()

        flash('Project created successfully')
        return redirect(url_for('admin.admin_projects'))

    return render_template('admin/add_project.html')

@admin_bp.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form['title']
        project.location = request.form['location']
        project.description = request.form['description']
        project.category = request.form['category']

        if 'before_image' in request.files and request.files['before_image'].filename:
            project.before_image = save_image(request.files['before_image'])

        if 'after_image' in request.files and request.files['after_image'].filename:
            project.after_image = save_image(request.files['after_image'])

        db.session.commit()
        flash('Project updated successfully')
        return redirect(url_for('admin.admin_projects'))

    return render_template('admin/edit_project.html', project=project)



@admin_bp.route('/projects/delete/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('admin.admin_projects'))


@admin_bp.route('/admin/quotes')
@login_required
def admin_quotes():
    quotes = QuoteRequest.query.order_by(QuoteRequest.date_created.desc()).all()
    return render_template('admin/quotes.html', quotes=quotes)

@admin_bp.route('/admin/quotes/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_quote(id):
    quote = QuoteRequest.query.get_or_404(id)
    db.session.delete(quote)
    db.session.commit()
    flash("Quote request deleted.")
    return redirect(url_for('admin.admin_quotes'))

@admin_bp.route('/admin/quotes/<int:id>')
@login_required
def admin_view_quote(id):
    quote = QuoteRequest.query.get_or_404(id)
    return render_template('admin/view_quote.html', quote=quote)

@admin_bp.route('/admin/messages')
@login_required
def admin_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)


@admin_bp.route('/admin/messages/<int:id>')
@login_required
def admin_view_message(id):
    message = Message.query.get_or_404(id)
    return render_template('admin/view_message.html', message=message)


@admin_bp.route('/admin/messages/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def admin_delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully.", "success")
    return redirect(url_for('admin.admin_messages'))


@admin_bp.route("/settings")
@login_required
def admin_settings():
    settings = Settings.query.first()

    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    return render_template("admin/settings.html", settings=settings)


@admin_bp.route("/settings/update", methods=["POST"])
@login_required
def update_settings():
    settings = Settings.query.first()

    # Company identity
    settings.company_name = request.form.get("company_name")
    settings.slogan = request.form.get("slogan")
    settings.about_text = request.form.get("about_text")

    # Contact info
    settings.phone = request.form.get("phone")
    settings.phone_alt = request.form.get("phone_alt")
    settings.email = request.form.get("email")
    settings.address = request.form.get("address")
    settings.whatsapp_number = request.form.get("whatsapp_number")

    # Social media
    settings.facebook = request.form.get("facebook")
    settings.instagram = request.form.get("instagram")
    settings.twitter = request.form.get("twitter")
    settings.youtube = request.form.get("youtube")

    # File uploads
    logo = request.files.get("logo")
    hero = request.files.get("hero_image")
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    if logo:
        filename = secure_filename(logo.filename)
        logo.save(os.path.join(upload_folder, filename))
        settings.logo_filename = filename

    if hero:
        filename = secure_filename(hero.filename)
        hero.save(os.path.join(upload_folder, filename))
        settings.hero_image_filename = filename

    db.session.commit()
    flash("Settings updated successfully", "success")
    return redirect(url_for("admin.admin_settings"))


