import sys, os
from datetime import date

sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd
from sqlmodel import select
from sqlalchemy.orm import aliased

from app.models import FinancialEntry, Account, Category
from app.database import get_session

session = next(get_session())

entries = map(
    lambda x: x.model_dump(),
    session.exec(select(FinancialEntry)).all())

accounts = map(
    lambda x: x.model_dump(),
    session.exec(select(Account)).all())

parent_categories = aliased(Category)

categories = map(
    lambda x: x.model_dump(),
    session.exec(select(Category) \
        .where(~(select(parent_categories.id) \
        .where(parent_categories.parent_category_id == Category.id)) \
        .exists())) \
        .all())

df_entries = pd.DataFrame(entries)

df_accounts = pd.DataFrame(accounts)

df_categories = pd.DataFrame(categories)

df_ui = df_entries[['entry_date', 'account_id', 'description', 'value', 'category_id']] \
        .merge(df_accounts[['id', 'account']], left_on='account_id', right_on='id', how='left') \
        .merge(df_categories[['id', 'category']], left_on='category_id', right_on='id', how='left') \
        [['entry_date', 'account', 'description', 'value', 'category']]

st.title('Lançamentos Financeiros')

edited_table_df = st.data_editor(
    df_ui, 
    hide_index=True,
    column_config={
        'category': st.column_config.SelectboxColumn(
            'Categoria',
            help='Escolha uma categoria para o lançamento',
            width='medium',
            options=df_categories['category'].to_list()
        ),
        'entry_date': st.column_config.DateColumn(
                    'Data do Lançamento',
                    min_value=date(2000, 1, 1),
                    max_value=date(2005, 1, 1),
                    format="DD/MM/YYYY",
                    step=1,
        ),
    }
)