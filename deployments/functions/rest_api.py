import boto3
import json
import logging
import random
import os

__author__ = 'Manuja'
__email__ = 'manuja@github'
__version__ = '0.0.1'
__status__ = 'test'


class global_args:
    OWNER = "manuja"
    ENVIRONMENT = "test"
    MODULE_NAME = "rest_api_backend"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


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
    random_username = ["Johnson", "Horst", "Reed", "Garcia", "Fortin", "Samuels", "Linda", "Shelly"]

    try:
        if event.get("pathParameters"):
            item = {}
            item["api_id"] = event.get("pathParameters").get(
                "user_name", random.choice(random_username))
            item["likes"] = event.get('pathParameters').get(
                'likes', random.randint(1, 100))
            _put_resp = aws_ddb_put_item(item)
            resp["statusCode"] = 200
            resp["body"] = json.dumps(
                {"message": f"Successfully updated '{item['api_id']}' with '{item['likes']}' likes"})
    except Exception as e:
        LOGGER.error(f"{str(e)}")
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp