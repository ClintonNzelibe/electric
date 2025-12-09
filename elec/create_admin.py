# create_admin.py

from elec import create_app, db
from elec.model import User
import getpass

app = create_app()

with app.app_context():
    username = input("Admin username: ")
    while True:
        password1 = getpass.getpass("Admin password: ")
        password2 = getpass.getpass("Confirm password: ")
        if password1 == password2:
            break
        else:
            print("Passwords do not match. Try again.")

    admin = User(username=username)
    admin.set_password(password1)
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
