# coding: utf-8
import os
import boto3

s3 = boto3.resource('s3')

APP_ENV = os.environ.get("APP_ENV")
origin_pptx_bucket_name = f"{APP_ENV}-origin-pptx"
preprocess_bucket_name = f"{APP_ENV}-preprocessed-resources"

def download_data(key_path, download_path, bucket_name=preprocess_bucket_name):
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(key_path, download_path)

def extract_bucket_and_key_path(file_path):
    bucket_name = file_path.split('//')[-1].split('/')[0]
    key_path = '/'.join(file_path.split('//')[-1].split('/')[1:])
    return bucket_name, key_path
