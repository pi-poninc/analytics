from . import api
from flask import render_template, request, current_app, jsonify
from app.exceptions import ValidationError
from pdf2image import convert_from_path
from .util_functions import *
import pandas as pd
from collections import OrderedDict
from ast import literal_eval
import csv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers, RequestError
import yaml
from ast import literal_eval
import csv
from requests_aws4auth import AWS4Auth
import boto3

host = 'search-yakuji-es-staging-6ms26qnhmlqm4f2oz44ptuvczy.ap-northeast-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'ap-northeast-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

#es = Elasticsearch(['localhost'], port=9200, use_ssl=False, verify_certs=False)

def create_index(data_file, index='index3'):
    index_file = './index.json'

    with open(index_file) as f:
      source = f.read().strip()
      source = literal_eval(source)
      properties = source['mappings']['properties']
      try:
        es.indices.create(index=index, body=source)
      except RequestError as es1:
        es.indices.delete(index=index, ignore=[400, 404])
        es.indices.create(index=index, body=source)
      es.indices.flush()

      def generate_data():
          with open(data_file, 'r') as f:
            reader = csv.reader(f)
            attrs = next(reader)
            for lid, row in enumerate(reader):
                data = {
                    '_op_type': 'index',
                    '_index': index,
                    '_id': lid,
                }
                for j, value in enumerate(row):
                    if attrs[j] in properties:
                      data[attrs[j]] = value
                yield data
    print(helpers.bulk(es, generate_data()))

def search_with_sudachi(query, es, index):

    response = es.search(
        index=index,
        body={
            "query": {
                "match": {
                    "extracted_texts": query
                }
            }
        }
    )
    return pd.DataFrame([
        OrderedDict({
            'extracted_texts': row['_source']['extracted_texts'], 
            'pathes': row['_source']['pathes'], 
            'slide_num': row['_source']['slide_num'], 
            'slide_show': row['_source']['slide_show'],
            'score': row['_score']
        }) for _, row in pd.DataFrame(response['hits']['hits']).iterrows()])

filename = "extract.csv"
download_data("tmp/"+filename,filename)
create_index("extract.csv")
os.remove(filename)


@api.route('/search_pptx_page', methods=['POST'])
def search_pptx_page():
    key_word = request.data.decode()
    data = {key_word:[]}
    results = search_with_sudachi(key_word,es,"index3")

    for row in range(0,len(results)):
        slide_bool = results.loc[row,"slide_show"]
        if slide_bool == 0:
          continue
        extracted_text = results.loc[row,"extracted_texts"]
        path = results.loc[row,"pathes"]
        file_suffix = path.split(".")[:-1]
        file_suffix = ",".join(file_suffix)
        slide_num = int(results.loc[row,"slide_num"])
        distance = results.loc[row,"score"]
        pptx_page_name = file_suffix.split("/")[-1:][0]+"_"+str(slide_num-1)+".pptx"
        filename = path.split("/")[-1]
        file_suffix = filename.split(".")[:-1][0]
        img_name = file_suffix+"_"+str(slide_num-1)+".png"
        img_path = "source/img/" + file_suffix + "/" + img_name
        r = {"path":path, "slide num": str(slide_num), "extracted text": str(extracted_text), "image": img_path, "similarity score":distance, "pptx_page_num":pptx_page_name}
        data[key_word].append(r)
    return jsonify(data)

