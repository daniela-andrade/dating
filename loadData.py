from app.models import User, Like
from app import db
import csv


def loadUsers():
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


def loadLikes():
    with open("likes.csv", "r") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:

            if row["is_platonic"] == 'True':
                is_platonic = True
            else:
                is_platonic = False

            if row["is_romantic"] == 'True':
                is_romantic = True
            else:
                is_romantic = False

            db_Like = Like(liker_id=row["liker_id"],
                           liked_id=row["liked_id"],
                           is_platonic=is_platonic,
                           is_romantic=is_romantic)
            db.session.add(db_Like)
        db.session.commit()

    db.session.close()


def main():
    # loadUsers()
    loadLikes()


if __name__ == '__main__':
    main()
