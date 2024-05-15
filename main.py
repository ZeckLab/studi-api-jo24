from fastapi import FastAPI

from src.api import api
from src.core.config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router, prefix="/api")