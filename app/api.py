from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from app.database import get_session, init_db
from app.models import *

import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/categories/', response_model=List[CategoryRead])
def read_categories(
    offset: int = 0, 
    limit: int = Query(default=20, le=20), 
    session: Session = Depends(get_session)
):
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

@app.post('/category/', status_code=201, response_model=CategoryRead)
def add_new_category(
    category: CategoryCreate,
    session: Session = Depends(get_session)
):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@app.post('/account/', status_code=201, response_model=AccountRead)
def add_new_account(account: AccountCreate, session: Session = Depends(get_session)):
    db_account = Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account

@app.get('/account/{account_id}', response_model=AccountRead)
def read_account(account_id: int, session: Session = Depends(get_session)):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account doesn't exists")
    return account

@app.get('/accounts/', response_model=List[AccountRead])
def read_accounts(session: Session = Depends(get_session)):
    accounts = session.exec(select(Account)).all()
    return accounts

@app.post('/entries/', status_code=201, response_model=FinancialEntryRead)
def add_new_entry(entry: FinancialEntryCreate, session: Session = Depends(get_session)):
    db_entry = FinancialEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry