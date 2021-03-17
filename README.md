# elastic_search

## 概要

- input 

  preprocess_pptxリポジトリで前処理した結果

- output
  
  Amazon Elasticsearch Serviceを使ってキーワードを元に、それと類似した単語をもつスライドに関する情報をjson形式で返す。
  
  jsonの形式は以下の通り。
  
  ```
  {"pathes":そのpptxのS3上でのpath,
  "slide_num":そのスライドページ,
  "extracted_text":そのスライドが含むテキスト,
  "image":そのスライドの画像のS3上でのpath,
  "similarity score": elastic searchで計算された検索ワードとの類似スコア,
  "pptx_page_num": そのスライドだけをpptxにしたpptxのS3上でのpath
  }
  ```
  
  ## 実行方法
  
  GITHUB_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEYの環境変数を指定しておく(docker-compose.yml内で参照します)。
  
  ```
  docker-compose up -d
  ```
  
  ## テスト方法
  
  ```
  python src/test.py #必要に応じてpostのdataの値を変更
  ```
  
