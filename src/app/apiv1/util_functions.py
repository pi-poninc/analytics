# coding: utf-8
import sys, os, glob
import pandas as pd
import boto3
from   boto3.session import Session
import tempfile
from pptx import Presentation
import pickle
from sklearn.feature_extraction.text import CountVectorizer
# profile = 'gateway_jcb'
# session = Session(profile_name=profile)
# s3 = session.resource('s3')
s3 = boto3.resource('s3')


def get(file_path, download_path, **kwargs):
    bucket_name, key_path = extract_bucket_and_key_path(file_path)
    download_data(key_path, download_path, bucket_name, **kwargs)
    return

def upload_data(key_path, file_path, bucket_name="pptx-copy"):
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(file_path, key_path)

def download_data(key_path, download_path, bucket_name="pptx-copy"):
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(key_path, download_path)

def output_upload_data(df, save_path, key_path):

    df.to_csv(save_path, index=False)
    upload_data(key_path, save_path)
    os.remove(save_path)

def output_upload_pptx(save_path, key_path):

    upload_data(key_path, save_path)
    os.remove(save_path)

def download_read_data(download_path, key_path):

    download_data(key_path, download_path)
    df = pd.read_csv(download_path)
    os.remove(download_path)

    return df

def download_and_save_pptx(download_path, key_path):

    download_data(key_path, download_path)

def download_pickle(download_path, key_path):

    download_data(key_path, download_path)
    tfidftransformer = pickle.load(open(download_path, "rb"))
    os.remove(download_path)

    return tfidftransformer

def download_count_vectorizer(download_path, key_path):

    download_data(key_path, download_path)
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(download_path, "rb")))
    os.remove(download_path)

    return loaded_vec


def get_key_path_list(path, bucket_name="pptx-copy"):
    bucket = s3.Bucket(bucket_name)

    key_path_list = []
    for obj in bucket.objects.filter(Prefix=path):
        key_path_list.append(obj.key)
    return key_path_list

def read_csv_in_s3(file_path, **kwargs):
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_path = os.path.join(tmp_dir, file_path.split('/')[-1])
        get(file_path, download_path)
        df = pd.read_csv(download_path, encoding="cp932", **kwargs)
    return df

def extract_bucket_and_key_path(file_path):
    bucket_name = file_path.split('//')[-1].split('/')[0]
    key_path = '/'.join(file_path.split('//')[-1].split('/')[1:])
    return bucket_name, key_path
