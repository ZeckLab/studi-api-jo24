from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from . import config

engine = create_engine(config.DATABASE_URI)
SessionLocale = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()