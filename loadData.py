from sqlalchemy.orm.scoping import scoped_session
from app.models import User
from app.db.setup import Base, SessionLocal, engine
import csv

session = scoped_session(SessionLocal)

Base.metadata.create_all(engine)
Base.query = session.query_property()


def loadUsers():
    with open("users.csv", "r") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:
            db_User = User(username=row["username"],
                           email=row["email"],
                           country=row["country"])
            db_User.set_password(row['password'])
            session.add(db_User)
        session.commit()


def loadLikes():
    with open("likes.csv", "r") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:

            liker = User.query.filter(row["liker_id"] == User.id).first()
            liked = User.query.filter(row["liked_id"] == User.id).first()

            if row["is_platonic"] == 'True':
                liker.like(liked)

            if row["is_romantic"] == 'True':
                liker.love(liked)

            session.commit()


def main():
    loadUsers()
    loadLikes()
    session.close()


if __name__ == '__main__':
    main()
