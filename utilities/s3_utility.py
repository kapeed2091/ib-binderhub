"""
Set Environment Variables
"""

import backoff
import logging
import os
import requests
from botocore.exceptions import ClientError

S3_BOTO_MAX_TRIES = os.environ.get('S3_BOTO_MAX_TRIES', 5)
S3_BOTO_MAX_TIMEOUT = os.environ.get('S3_BOTO_MAX_TIMEOUT', 20)

logger = logging.getLogger()


def on_tpm_give_up(details):
    raise Exception


class S3Utility:
    def __init__(self,
                 aws_access_key_id=os.environ['S3_AWS_ACCESS_KEY_ID'],
                 aws_secret_access_key=os.environ['S3_AWS_SECRET_ACCESS_KEY'],
                 region_name=os.environ['S3_AWS_REGION'],
                 bucket_name=os.environ['S3_AWS_BUCKET_NAME']
                 ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket_name = bucket_name

        self.client = self._get_s3_client()

    @backoff.on_exception(backoff.expo, Exception, max_tries=S3_BOTO_MAX_TRIES,
                          max_time=S3_BOTO_MAX_TIMEOUT,
                          jitter=backoff.full_jitter,
                          on_giveup=on_tpm_give_up, logger=logger)
    def _get_s3_client(self):
        import boto3

        aws_access_key_id = self.aws_access_key_id
        aws_secret_access_key = self.aws_secret_access_key
        region_name = self.region_name

        from botocore.client import Config
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name,
                          config=Config(
                              s3={'addressing_style': 'path'}
                              , signature_version='s3v4')
                          )
        return s3

    @backoff.on_exception(backoff.expo, Exception, max_tries=S3_BOTO_MAX_TRIES,
                          max_time=S3_BOTO_MAX_TIMEOUT,
                          jitter=backoff.full_jitter,
                          on_giveup=on_tpm_give_up, logger=logger)
    def put_object(self, key_name, content):
        bucket_name = self.bucket_name
        self.client.put_object(Body=content, Bucket=bucket_name, Key=key_name)
        return

    @backoff.on_exception(backoff.expo, Exception, max_tries=S3_BOTO_MAX_TRIES,
                          max_time=S3_BOTO_MAX_TIMEOUT,
                          jitter=backoff.full_jitter,
                          on_giveup=on_tpm_give_up, logger=logger)
    def read_object(self, key_name):
        bucket_name = self.bucket_name
        obj = self.client.get_object(Bucket=bucket_name, Key=key_name)
        data = obj['Body'].read()
        return data

    @backoff.on_exception(backoff.expo, Exception, max_tries=S3_BOTO_MAX_TRIES,
                          max_time=S3_BOTO_MAX_TIMEOUT,
                          jitter=backoff.full_jitter,
                          on_giveup=on_tpm_give_up, logger=logger)
    def get_presigned_url(self, key_name, expires_in_seconds=3600):
        bucket_name = self.bucket_name

        url = self.client.generate_presigned_url(
            ClientMethod='get_object', Params={
                'Bucket': bucket_name, 'Key': key_name
            }, ExpiresIn=expires_in_seconds)
        return url

    def create_presigned_post(self, key_name, fields=None, conditions=None,
                              expires_in_seconds=3600):
        bucket_name = self.bucket_name
        try:
            response = self.client.generate_presigned_post(
                bucket_name, key_name, Fields=fields, Conditions=conditions,
                ExpiresIn=expires_in_seconds)
        except ClientError as e:
            return None
        return response

    def post_with_presigned_url(self, file_to_write, key_name,
                                 expires_in_seconds=3600):
        response = self.create_presigned_post(
            key_name=key_name, expires_in_seconds=expires_in_seconds)
        self.write_with_presigned_url(response, file_to_write)
        return

    @staticmethod
    def write_with_presigned_url(presigned_post_response, file_to_write):
        with open(file_to_write, 'rb') as f:
            files = {'file': (file_to_write, f)}
            requests.post(
                presigned_post_response['url'],
                data=presigned_post_response['fields'],
                files=files
            )
        return
