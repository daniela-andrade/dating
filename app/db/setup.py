from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask import _app_ctx_stack

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

Base = declarative_base()
Base.metadata.create_all(engine)
Base.query = session.query_property()
