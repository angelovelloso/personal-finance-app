from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime

class AccountBase(SQLModel):
    account: str = Field(index=True)
    description: str
    account_currency: str = Field(default='BRL')

    @field_validator('account_currency')
    @classmethod
    def check_currency(cls, value):
        if value not in ['BRL', 'USD', 'EUR']:
            raise ValueError("Currency must be 'BRL', 'USD' or 'EUR'")
        return value

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int

class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CategoryBase(SQLModel):
    category: str = Field(max_length=100)
    parent_category_id: Optional[int] = Field(
        default=None,
        foreign_key='category.id',
        nullable=True)
    category_polarity: int = Field(default=int(-1))
    
    @field_validator('category_polarity')
    @classmethod
    def check_polarity(cls, value):
        if value not in [1, -1]:
            raise ValueError("Polarity must be 1 or -1")
        return value

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FinancialEntryBase(SQLModel):
    source: str
    entry_date: date 
    report_date: date
    description: str = Field(max_length=100)
    value: Decimal = Field(decimal_places=2)
    tags: Optional[str] = None

    @field_validator('entry_date', 'report_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()

class FinancialEntryCreate(FinancialEntryBase):
    account: Optional[str] = None
    category: Optional[str] = None

class FinancialEntryRead(FinancialEntryBase):
    id: int
    account: Optional[AccountRead] = None
    category: Optional[CategoryRead] = None

class FinancialEntry(FinancialEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(default=-1, foreign_key='account.id')
    account: Optional[Account] = Relationship()
    category_id: Optional[int] = Field(default=-1, foreign_key='category.id')
    category: Optional[Category] = Relationship()