# coding: utf-8
import requests

url = 'http://127.0.0.1:5000/v1/search_pptx_page'
#url = 'http://3.112.61.72:5000/v1/search_pptx_page'
r = requests.post(url, data="データサイエンス".encode('utf-8'))
print(r.text)