from fastapi import Depends, FastAPI, HTTPException, Query
from typing import List
from database import get_session
from datetime import datetime
from models import (
    Account, Category, CategoryRead, 
    NewFinancialEntryCreate, FinancialEntry, FinancialEntryRead,
    LoadClassifyDataQuery, LoadClassifyDataResponse, ClassifyEntryRequest
)
from sqlalchemy.orm import aliased
from sqlmodel import Session, select


import logging

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post(
    '/new_entry',
    status_code=201)
def add_new_entry(
    new_entry_data: List[NewFinancialEntryCreate],
    session: Session = Depends(get_session)
):
    
    for new_entry in new_entry_data:

        account_stmt = select(Account) \
            .where(Account.account == new_entry.account)
        
        account = session.exec(account_stmt).first()

        if account is not None:
            new_entry = FinancialEntry(
                source=new_entry.source,
                entry_date=new_entry.entry_date,
                report_date=new_entry.report_date,
                description=new_entry.description,
                value=new_entry.value,
                account_id=account.id
            )

            session.add(new_entry)
            
    session.commit()

    return {
        'entries_created': len(new_entry_data)
    }


@app.post(
    '/load_classify_data',
    status_code=201,
    response_model=LoadClassifyDataResponse)
def load_classify_data_api(
    load_query: LoadClassifyDataQuery,
    session: Session = Depends(get_session)
):
    
    parent_categories = aliased(Category)
    category_stmt = select(Category.category)

    if load_query.only_leaf:
        category_stmt = category_stmt.where(
            ~(
                select(parent_categories.id).where(
                    parent_categories.parent_category_id == Category.id
                )
            ).exists()
        )

    entry_stmt = select(
        FinancialEntry.id,
        FinancialEntry.report_date,
        Account.account,
        FinancialEntry.description,
        FinancialEntry.value,
        Category.category,
        FinancialEntry.annotation
    ) \
        .join(Account) \
        .join(Category)
    
    if load_query.start_date:
        entry_stmt = entry_stmt.where(
            FinancialEntry.report_date >= load_query.start_date
        )

    if load_query.end_date:
        entry_stmt = entry_stmt.where(
            FinancialEntry.report_date <= load_query.end_date
        )

    if load_query.account_filters:
        entry_stmt = entry_stmt.where(
            Account.account.in_(load_query.account_filters)
        )

    if load_query.category_filters:
        entry_stmt = entry_stmt.where(
            Category.category.in_(load_query.category_filters)
        )

    response = LoadClassifyDataResponse(
        accounts_list = session.exec(select(Account.account)).all(),
        categories_list = session.exec(category_stmt).all(),
        entries = session.exec(entry_stmt).all()
    )

    return response

@app.patch(
    '/classify',
    status_code=200)
def classify_entries_api(
    new_entry_data: List[ClassifyEntryRequest],
    session: Session = Depends(get_session)
):

    for entry_updated in new_entry_data:

        updated_entry = session.get(FinancialEntry, entry_updated.entry_id)
        category_stmt = select(Category) \
            .where(Category.category == entry_updated.new_category)
        
        updated_category = session.exec(category_stmt).first()

        if updated_category is not None:
            updated_entry.category_id = updated_category.id

        if entry_updated.new_annotation is not None:
            updated_entry.annotation = entry_updated.new_annotation

            session.add(updated_entry)

    session.commit()

    return {
        'entries_updated': len(new_entry_data)
    }