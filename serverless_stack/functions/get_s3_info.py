import boto3
import json
import logging
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def dynamodb_put_items(item):
    if os.environ.get('DDB_TABLE_NAME'):
        dynamodb_table = dynamodb.Table(
            os.environ.get('DDB_TABLE_NAME')
        )
        try:
            dynamodb_table.put_item(Item=item)
        except Exception as e:
            raise

def s3_bucket_inventory():
    try:
        response = s3_client.list_buckets()
        bucket_inventory = {
            "buckets": []
        }
        for bucket in response["Buckets"]:
            bucket_inventory["buckets"].append(bucket["Name"])
            dynamodb_put_items(
                {
                    "s3_id": bucket["Name"]
                }
            )
        return bucket_inventory
    except Exception as e:
        raise

def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())
    LOGGER.info(f"received_event:{event}")

    response = {
        "statusCode": 400,
        "body": json.dumps(
            {
                "message": event
            }
        )
    }

    try:
        bucket_inventory = s3_bucket_inventory()
        response["body"] = json.dumps(
            {
                "message": bucket_inventory
            }
        )
        response['statusCode'] = 200
    except Exception as e:
        response["body"] = json.dumps(
            {
                "message": f"ERROR:{str(e)}"
            }
        )
        
    return response