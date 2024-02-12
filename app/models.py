from sqlmodel import SQLModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import date

class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account: str = Field(index=True)
    description: str

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str

class FinancialEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    account_id: int = Field(foreign_key='account.id')
    entry_date: date = None
    report_date: date = None
    description: str = Field(max_length=100)
    value: Decimal = Field(decimal_places=2)
    category_id: Optional[int] = Field(foreign_key='category.id')
    tags: Optional[str]