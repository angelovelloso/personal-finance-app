from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime

# alembic revision --autogenerate -m "<msg>"

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
    annotation: Optional[str] = Field(default=None, max_length=100)
    value: Decimal = Field(decimal_places=2)
    tags: Optional[str] = None

    @field_validator('entry_date', 'report_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(
                value,
                "%d/%m/%Y"
            ).date()
        
        else:
            return value

class NewFinancialEntryCreate(FinancialEntryBase):
    account: Optional[str] = None

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
    transfer_id: Optional[int] = Field(default=None, foreign_key='financialentry.id')

class LoadClassifyDataQuery(SQLModel):
    start_date: date = Field(default=None)
    end_date: date = Field(default=None)
    account_filters: List[str] = Field(default=None)
    category_filters: List[str] = Field(default=None)
    only_leaf: bool = Field(default=False)

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

class LoadClassifyDataResponse(SQLModel):
    accounts_list: List[str] = Field(default=None)
    categories_list: List[str] = Field(default=None)
    entries: List[list] = Field(default=None)

class ClassifyEntryRequest(SQLModel):
    entry_id: str
    new_category: str
    new_annotation: Optional[str] = Field(default=None)