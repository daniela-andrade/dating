from app.models import User
from app import db
import csv

with open("users.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        db_User = User(username=row["username"],
                       email=row["email"],
                       country=row["country"])
        db_User.set_password(row['password_hash'])
        db.session.add(db_User)

    db.session.commit()

db.session.close()