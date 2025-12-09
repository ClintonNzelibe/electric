import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_image(image_file):
    if image_file:
        filename = secure_filename(image_file.filename)
        # Use current_app to access config
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        filepath = os.path.join(upload_folder, filename)

        # Make sure the folder exists
        os.makedirs(upload_folder, exist_ok=True)

        image_file.save(filepath)
        return filename
    return None
