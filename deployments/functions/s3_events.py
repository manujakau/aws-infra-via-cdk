import boto3
import json
import logging
import os

__author__ = 'Manuja'
__email__ = 'manuja@github'
__version__ = '0.0.1'
__status__ = 'test'


class global_args:
    OWNER = "manuja"
    ENVIRONMENT = "test"
    MODULE_NAME = "s3_event_processor"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

aws_s3_client = boto3.client('s3')
aws_ddb = boto3.resource('dynamodb')


def aws_ddb_put_item(item):
    if os.environ.get('DDB_TABLE_NAME'):
        aws_ddb_table = aws_ddb.Table(os.environ.get('DDB_TABLE_NAME'))
        try:
            return(aws_ddb_table.put_item(Item=item))
        except Exception as e:
            raise


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())

    LOGGER.info(f"received_event:{event}")
    resp = {
        "statusCode": 400,
        "body": json.dumps({"message": {}})
    }
    try:
        if "Records" in event:
            item = {}
            item["event_id"] = event["Records"][0]["s3"]["object"]["key"]
            item["item_size"] = event["Records"][0]["s3"]["object"]["size"]
            item["s3_bucket"] = event["Records"][0]["s3"]["bucket"]["name"]
            item["s3_bucket_owner"] = event["Records"][0]["s3"]["bucket"]["ownerIdentity"]["principalId"]
            response = aws_ddb_put_item(item)
            resp["statusCode"] = 200
            resp["body"] = json.dumps({"message": response})
    except Exception as e:
        LOGGER.error(f"{str(e)}")
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp