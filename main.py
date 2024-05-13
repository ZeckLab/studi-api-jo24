from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api
from src.core.config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router, prefix="/api")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)