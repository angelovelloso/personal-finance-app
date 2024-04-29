import os
import pandas as pd
from sqlmodel import create_engine, SQLModel, Session
import models
from settings import Settings

# alembic revision --autogenerate -m "<msg>"

database_url = Settings().DB_URL_COMPLETE

engine = create_engine(
    database_url, 
    connect_args={ "check_same_thread": False },
    echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
