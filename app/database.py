import os
import pandas as pd
from sqlmodel import create_engine, SQLModel, Session
from app import models
from app.settings import Settings

# alembic revision --autogenerate -m "<msg>"

database_url = Settings().DATABASE_URL

engine = create_engine(
    database_url, 
    connect_args={ "check_same_thread": False },
    echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
