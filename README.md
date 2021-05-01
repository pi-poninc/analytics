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
  
  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEYの値を `docker.env` に指定しておく
  `docker.env` は、gitignore対象なので、 `docker.env.sample` を参考に手元で `docker.env` を作成し、クレデンシャル情報を設定してください。
  (docker-compose.yml内で参照します)。
  
  ```
  docker-compose up -d
  ```
  
  ## テスト方法
  
  ```
  python3 src/test.py #必要に応じてpostのdataの値を変更
  ```

## ECRへのPush方法について

リポジトリのルート直下で、以下のコマンドを実行

例：ステージング用のECRをpushしたい場合

```bash
$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 172570774766.dkr.ecr.ap-northeast-1.amazonaws.com

$ docker build -f docker/Dockerfile -t staging_search_pptx_page_api .

$ docker tag staging_search_pptx_page_api:latest 172570774766.dkr.ecr.ap-northeast-1.amazonaws.com/staging_search_pptx_page_api:latest

$ docker push 172570774766.dkr.ecr.ap-northeast-1.amazonaws.com/staging_search_pptx_page_api:latest
```
