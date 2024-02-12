from fastapi import Depends, FastAPI
from sqlmodel import Session

from app.db import get_session, init_db
from app.models import FinantialEntry

import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# Rodar: uvicorn app.main:app --reload

'''
    # Avaliar se vou manter isso. Ver como se comporta, se apaga o banco toda vez.
@app.on_event("startup")
def on_startup():
    init_db()
'''

@app.get('/ping')
async def pong():
    return {'ping': 'pong!'}

@app.post('/new_entry')
def add_new_entry(input: dict, session: Session = Depends(get_session)):
    logger.info(f'Entrada: {input}')
    entry = FinantialEntry(**input)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry