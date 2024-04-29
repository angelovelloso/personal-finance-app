import datetime
import json

import requests
import streamlit as st
from pandas import DataFrame
from settings import Settings
from importers import importers, importers_list

st.set_page_config(
    page_title='Personal Finance - Import statements and balances', layout='wide'
)

api_url = Settings().API_BASE_URL

st.title('Import statements and balances')

uploaded_file = st.file_uploader(
    'Upload your file',
    type=['pdf', 'csv']
)

selected_importer_name = st.selectbox(
    'Choose which importer to use',
    options=importers_list
)

import_log_table = DataFrame()

if 'preview' not in st.session_state:
    st.session_state.preview = False

def show_preview():
    st.session_state.preview = not st.session_state.preview

st.button('Parse and Review', type='primary', on_click=show_preview)

if st.session_state.preview:

    selected_importer = importers[importers_list.index(selected_importer_name)]['class']
    account_importer = importers[importers_list.index(selected_importer_name)]['account']
    importer_id = importers[importers_list.index(selected_importer_name)]['id']

    file_details = {
        "filename":uploaded_file.name, 
        "filetype":uploaded_file.type,
        "filesize":uploaded_file.size
    }

    parsed_file = selected_importer(
        uploaded_file.read(), 
        file_details,
        account_importer)
    
    import_log_table = DataFrame.from_dict(
        [entry.__dict__ for entry in parsed_file.parsed_data], 
        orient='columns'
    )

    import_log_table['import_check'] = True

if not import_log_table.empty:

    columns_to_show = ['import_check', 'account', 'entry_date', 'report_date', 'description', 'value']

    file_detail_col1, file_detail_col2, file_detail_col3 = st.columns(
        [0.40, 0.25, 0.25]
    )

    file_detail_col1.text_input(
        label='Filename',
        value=uploaded_file.name,
        disabled=True
    )

    file_detail_col2.text_input(
        label='Filetype',
        value=uploaded_file.type,
        disabled=True
    )

    file_detail_col3.text_input(
        label='Filesize',
        value=uploaded_file.size,
        disabled=True
    )

    with st.form(key='import-form', clear_on_submit=True, border=True):

        parsed_entries_table = st.data_editor(
            import_log_table[columns_to_show], 
            use_container_width=True, 
            hide_index=True,
            disabled=columns_to_show[1:],
            column_config={          
                'account': st.column_config.TextColumn('Account'),
                'description': st.column_config.TextColumn('Entry description'),
                'import_check': st.column_config.CheckboxColumn(
                    'Import?',
                    default=True
                ),
                'entry_date': st.column_config.DateColumn(
                    'Entry date',
                    min_value=datetime.datetime(2000, 1, 1),
                    max_value=datetime.datetime(2999, 12, 31),
                    format='DD/MM/YYYY',
                    step=1,
                ),
                'report_date': st.column_config.DateColumn(
                    'Report date',
                    min_value=datetime.datetime(2000, 1, 1),
                    max_value=datetime.datetime(2999, 12, 31),
                    format='DD/MM/YYYY',
                    step=1,
                ),
                'value': st.column_config.NumberColumn('Value', format='%.2f'),
            }
        )

        submitted = st.form_submit_button("Import", type='primary')

    if submitted:

        filter = parsed_entries_table['import_check']

        request_body = list()

        for index, row in parsed_entries_table[filter].iterrows():

            request_item = dict(
                source=importer_id + ' - ' + uploaded_file.name,
                entry_date=row['entry_date'].strftime("%d/%m/%Y"),
                report_date=row['report_date'].strftime("%d/%m/%Y"),
                description=row['description'],
                value=str(round(row['value'],2)),
                account=row['account']
            )

            request_body.append(request_item)

        response = requests.post(
            url=api_url + '/new_entry/',
            data=json.dumps(request_body),
            headers={'accept': 'application/json'},
        )