import os

import qiniu

from swiper import platform_config as plt
from worker import call_by_worker

authorization = qiniu.Auth(plt.QN_ACCESS_KEY, plt.QN_SECRET_KEY)


def qiniu_upload(bucket_name, filepath, filename=None):
    '''
    向七牛云上传文件

    Args:
        bucket_name: 空间名
        filepath: 本地文件路径
        filename: 上传后的文件名
    '''
    if filename is None:
        filename = os.path.basename(filepath)
    token = authorization.upload_token(bucket_name, filename, 3600)  # 生成上传 Token
    ret, info = qiniu.put_file(token, filename, filepath)
    return ret, info


def qiniu_upload_data(bucket_name, filedata, filename):
    '''
    向七牛云上传二进制数据流

    Args:
        bucket_name: 空间名
        filedata: 二进制数据流
        filename: 上传后的文件名
    '''
    token = authorization.upload_token(bucket_name, filename, 3600)  # 生成上传 Token
    ret, info = qiniu.put_data(token, filename, filedata)
    return ret, info


def qiniu_fetch(bucket_name, resource_url, filename=None):
    '''
    由七牛抓取网络资源到空间

    Args:
        bucket_name: 空间名
        resource_url: 网络资源地址
        filename: 上传后的文件名
    '''
    bucket = qiniu.BucketManager(authorization)
    ret, info = bucket.fetch(resource_url, bucket_name, filename)
    return ret, info


async_qiniu_upload = call_by_worker(qiniu_upload)
async_qiniu_upload_data = call_by_worker(qiniu_upload_data)
async_qiniu_fetch = call_by_worker(qiniu_fetch)
