from elec import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # <-- this ensures tables are created when the app starts

if __name__ == "__main__":
    app.run(debug=True, port=5050)
