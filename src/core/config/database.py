from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

print("DATABASE_URL",os.getenv("DATABASE_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocale = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()