from sqlmodel import SQLModel, Field
from typing import List, Optional

class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FinantialEntry(SQLModel):
    #id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    account: str
    entry_date: str
    report_date: str
    description: str
    value: str
    category: str
    tags: str