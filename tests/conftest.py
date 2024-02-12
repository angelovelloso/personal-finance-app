import pytest
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
from app.models import FinancialEntry, Account

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    SQLModel.metadata.create_all(engine)
    yield Session()
    SQLModel.metadata.drop_all(engine)