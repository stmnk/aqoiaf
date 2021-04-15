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
    blurred = blurred.replace(entity, '[:snowflake::fire::snowflake::fire:]')

st.write(blurred)

BOOKS_LABELS = ['agot', 'acok', 'asos', 'affc', 'adwd']
BOOKS_TITLES = ['A Game of Thrones', 'A Clash of Kings', 'A Strom of Swords', 'A Feast for Crows', 'A Dance with Dragons']
BOOKS_DICT = dict(list(zip(BOOKS_LABELS, BOOKS_TITLES)))

ANSWER_BOOK = st.selectbox('Pick the book this passage beongs to:', ['Pick a book'] + BOOKS_TITLES, key='box_select_book')

if ANSWER_BOOK != 'Pick a book': 
    st.write(ANSWER_BOOK)

POV_NAMES = ['T', 'J', 'C', 'D', 'B', ]
ANSWER_POV = st.selectbox('Pick the point-of-view character the passage beongs to:', ['Pick a POV character'] + POV_NAMES, key='box_select_book')

if ANSWER_POV != 'Pick a POV character': 
    st.write(ANSWER_POV)

LOCATIONS_NAMES = ['W', 'CR', 'KL', 'RR', 'E', 'HG', 'SS']
ANSWER_LOC = st.selectbox('Pick the location in which the passage happens:', ['Pick a location'] + LOCATIONS_NAMES, key='box_select_book')

if ANSWER_LOC != 'Pick a location': 
    st.write(ANSWER_LOC)

if st.checkbox(f'Spoiler: show me the book this passage is from! (-25 points)'):
    st.write(BOOKS_DICT[result['hits']['hits'][0]['_source']['book']])
if st.checkbox(f'Spoiler: show me the blurred entities! (-25 points)'):
    st.write(str(entities_from))
if st.checkbox(f'Spoiler: show me the POV character! (-25 points)'):
    st.write(result['hits']['hits'][0]['_source']['pov_character'])
if st.checkbox(f'Spoiler: show me the full text of the passage! (-25 points)'):
    st.write(passage_text)

