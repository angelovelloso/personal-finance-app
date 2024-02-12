from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import FinancialEntry, Account

import logging

logger = logging.getLogger(__name__)

app = FastAPI()

'''
    # Avaliar se vou manter isso. Ver como se comporta, se apaga o banco toda vez.
@app.on_event("startup")
def on_startup():
    init_db()
'''

@app.get('/ping')
async def pong():
    return {'ping': 'pong!'}

@app.post('/new_account/', status_code=201, response_model=Account)
def add_new_account(account: Account, session: Session = Depends(get_session)):
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

@app.get('/account/')
def read_account(session: Session = Depends(get_session)):
    accounts = session.exec(select(Account)).all()
    return accounts

@app.post('/new_entry/', status_code=201, response_model=FinancialEntry)
def add_new_entry(entry: FinancialEntry, session: Session = Depends(get_session)):
    return entry

'''
    logger.info(f'Entrada: {entry}')
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
'''