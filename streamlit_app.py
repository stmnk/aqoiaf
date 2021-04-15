import os
import time
import json
import streamlit as st
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from expertai.nlapi.cloud.client import ExpertAiClient

load_dotenv()

LOCAL_URL = 'localhost:9200'
BONSAI_URL = os.getenv('BONSAI_URL')
SEARCHLY_URL = os.getenv('SEARCHLY_URL')
AWS_ES_URL = os.getenv('AWS_ES_URL')
CLOUD_ES_URL = os.getenv('CLOUD_ES_URL')
os.environ["EAI_USERNAME"] = os.getenv('EAI_USERNAME')
os.environ["EAI_PASSWORD"] = os.getenv('EAI_PASSWORD')

ES_URL_LABELS = ['Local Elasticsearch URL', 'Bonsai Elasticsearch URL', 'Searchly Elasticsearch URL',
                 'AWS Elasticsearch URL', 'Cloud Elasticsearch URL']
ES_URL_STRINGS = [LOCAL_URL, BONSAI_URL,
                  SEARCHLY_URL, AWS_ES_URL, CLOUD_ES_URL]

ACTIVE_URL_LABEL = 'Searchly Elasticsearch URL'

ES_URLS_DICT = dict(list(zip(ES_URL_LABELS, ES_URL_STRINGS)))
ES_INDEX_KEYS = ['document', 'document', 'asoiaf', '', '']
ES_INDEXES_DICT = dict(list(zip(ES_URL_LABELS, ES_INDEX_KEYS)))
ES_INDEX_FIELD = ['text', 'text', 'paragraph_text', '', '']
ES_FIELDS_DICT = dict(list(zip(ES_URL_LABELS, ES_INDEX_FIELD)))
ACTIVE_URL = ES_URLS_DICT[ACTIVE_URL_LABEL]
ACTIVE_INDEX = ES_INDEXES_DICT[ACTIVE_URL_LABEL]
ACTIVE_FIELD = ES_FIELDS_DICT[ACTIVE_URL_LABEL]

client = Elasticsearch(SEARCHLY_URL)
query_body = {"size": 1, "query": {
    "function_score": {"functions": [{"random_score": {
        "seed": int(time.time())}}]}}}
result = client.search(index=ACTIVE_INDEX, body=query_body)

expert_ai_client = ExpertAiClient()

passage_text = result['hits']['hits'][0]['_source'][ACTIVE_FIELD]
language= 'en'

output = expert_ai_client.specific_resource_analysis(body={"document": {"text": passage_text}}, 
    params={'language': language, 'resource': 'entities'})

entities_from = []
for entity in output.entities:
    entities_from.append(str(entity.lemma))

blurred = passage_text
for entity in entities_from:
    blurred = blurred.replace(entity, '[XXXX]')

st.write(blurred)


