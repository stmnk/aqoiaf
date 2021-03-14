import streamlit as st

LOCAL_URL = 'localhost:9200'

if st.checkbox(f'Configure Elasticsearch URLs (default value: {LOCAL_URL})'):
    LOCAL_URL = st.text_input('Local Elasticsearch URL', LOCAL_URL, max_chars=500, key='es_local_url')
    BONSAI_URL = st.text_input('Bonsai Elasticsearch URL', max_chars=500, key='es_bonsai_url')
    SEARCHLY_URL = st.text_input('Searchly Elasticsearch URL', max_chars=500, key='es_searchly_url')
    AWS_ES_URL = st.text_input('AWS Elasticsearch URL', max_chars=500, key='es_aws_url')
    CLOUD_ES_URL = st.text_input('Cloud Elasticsearch URL', max_chars=500, key='es_cloud_url')

ACTIVE_URL = LOCAL_URL

st.write(f'Your acive elastcsearch URL is: {ACTIVE_URL}')
