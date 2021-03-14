import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

LOCAL_URL = 'localhost:9200'; 
BONSAI_URL = os.getenv('BONSAI_URL'); SEARCHLY_URL = os.getenv('SEARCHLY_URL'); 
AWS_ES_URL = os.getenv('AWS_ES_URL'); CLOUD_ES_URL = os.getenv('CLOUD_ES_URL')
ES_URL_LABELS = ['Local Elasticsearch URL', 'Bonsai Elasticsearch URL', 'Searchly Elasticsearch URL',
    'AWS Elasticsearch URL', 'Cloud Elasticsearch URL' ]
ES_URL_STRINGS = [LOCAL_URL, BONSAI_URL, SEARCHLY_URL, AWS_ES_URL, CLOUD_ES_URL]

if st.checkbox(f'Configure Elasticsearch URLs (default value: {LOCAL_URL})'):
    LOCAL_URL = st.text_input('Local Elasticsearch URL', LOCAL_URL, max_chars=500, key='es_local_url')
    BONSAI_URL = st.text_input('Bonsai Elasticsearch URL', max_chars=500, key='es_bonsai_url')
    SEARCHLY_URL = st.text_input('Searchly Elasticsearch URL', max_chars=500, key='es_searchly_url')
    AWS_ES_URL = st.text_input('AWS Elasticsearch URL', max_chars=500, key='es_aws_url')
    CLOUD_ES_URL = st.text_input('Cloud Elasticsearch URL', max_chars=500, key='es_cloud_url')
    ES_URL_STRINGS = [LOCAL_URL, BONSAI_URL, SEARCHLY_URL, AWS_ES_URL, CLOUD_ES_URL]

ACTIVE_URL_LABEL = st.selectbox('Select the active Elasticsearch URL: ', ES_URL_LABELS, key='box_select_url')

ES_URLS_DICT = dict(list(zip(ES_URL_LABELS, ES_URL_STRINGS)))
ACTIVE_URL = ES_URLS_DICT[ACTIVE_URL_LABEL]

st.write(f'Your acive elastcsearch URL is: {ACTIVE_URL_LABEL}')

if not ACTIVE_URL:
    st.write(f'Your acive elastcsearch URL is empty, please configure it above')
else:
    if ACTIVE_URL_LABEL == ES_URL_LABELS[0]: # localhost URL can be fully shown in the open 
        st.write(f'Your acive elastcsearch URL is: {ACTIVE_URL}')
    else:                                    # obfuscate sensitive entries in the URL string
        st.write(f'Your acive elastcsearch URL is: https://<YOUR_USER>:********@{ACTIVE_URL.split("@")[1]}')


