import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.router import main_router
from app.db.engine import engine


SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = json.loads(os.getenv('CORS_ORIGINS'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
