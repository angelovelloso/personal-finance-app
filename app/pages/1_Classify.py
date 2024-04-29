import datetime
import json

import requests
import streamlit as st
from pandas import DataFrame
from settings import Settings

st.set_page_config(
    page_title='Personal Finance - Classify financial entries', layout='wide'
)

api_url = Settings().API_BASE_URL


def load_classify_data():

    request_body = dict(only_leaf=True)

    if 'start_date_filter' not in st.session_state:
        st.session_state.start_date_filter = datetime.datetime.now().replace(
            day=1
        )

    request_body['start_date'] = st.session_state.start_date_filter.strftime(
        '%Y-%m-%d'
    )

    if 'end_date_filter' not in st.session_state:
        st.session_state.end_date_filter = datetime.datetime.now()

    request_body['end_date'] = st.session_state.end_date_filter.strftime(
        '%Y-%m-%d'
    )

    if 'account_filters' in st.session_state:
        request_body['account_filters'] = st.session_state.account_filters

    if 'category_filters' in st.session_state:
        request_body['category_filters'] = st.session_state.category_filters

    response = requests.post(
        url=api_url + '/load_classify_data/',
        data=json.dumps(request_body),
        headers={'accept': 'application/json'},
    )

    return json.loads(response.content)


data = load_classify_data()

st.title('Classify financial entries')

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
    [0.15, 0.15, 0.30, 0.30]
)

st.session_state.start_date_filter = filter_col1.date_input(
    'Start date', st.session_state.start_date_filter, format='DD/MM/YYYY'
)

st.session_state.end_date_filter = filter_col2.date_input(
    'End date', st.session_state.end_date_filter, format='DD/MM/YYYY'
)

st.session_state.account_filters = filter_col3.multiselect(
    'Accounts filter',
    data['accounts_list'],
    placeholder='Choose accounts to filter',
)

st.session_state.category_filters = filter_col4.multiselect(
    'Categories filter',
    data['categories_list'],
    placeholder='Choose categories to filter',
)

loaded_table = DataFrame(
    data['entries'],
    columns=[
        'pk',
        'report_date',
        'account',
        'description',
        'value',
        'category',
        'annotation'
    ],
)

classified_table = st.data_editor(
    loaded_table.sort_values(by='report_date'),
    key='category_input',
    hide_index=True,
    use_container_width=True,
    disabled=list(loaded_table.columns[:-2]),
    column_config={
        'pk': None,
        'category': st.column_config.SelectboxColumn(
            'Category',
            help='Escolha uma categoria para o lançamento',
            width='medium',
            options=data['categories_list'],
        ),
        'annotation': st.column_config.TextColumn(
            'Annotations',
            help='Some helpful info about this entry',
            width='medium'
        ),
        'report_date': st.column_config.DateColumn(
            'Date',
            min_value=datetime.datetime(2000, 1, 1),
            max_value=datetime.datetime(2999, 12, 31),
            format='DD/MM/YYYY',
            step=1,
        ),
        'value': st.column_config.NumberColumn('Value', format='%.2f'),
    },
)

change_log_table = classified_table.sort_index()[['pk', 'category', 'annotation']][
    loaded_table.category.sort_index()
    != classified_table.category.sort_index()
]

if st.button('Save', type='primary'):

    request_body = list()

    for index, row in change_log_table.iterrows():

        request_item = dict(
            entry_id=str(row['pk']),
            new_category=row['category']
        )

        if row['annotation'] is not None:
            request_item['new_annotation']=row['annotation']

        request_body.append(request_item)

    response = requests.patch(
        url=api_url + '/classify',
        data=json.dumps(request_body),
        headers={'accept': 'application/json'},
    )

    st.rerun()

with st.expander('Show log of changes'):

    st.dataframe(change_log_table, use_container_width=True, hide_index=True)
