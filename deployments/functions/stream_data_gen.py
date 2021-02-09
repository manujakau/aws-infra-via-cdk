import json
import logging
import os
import random
import string
import time
import uuid

import boto3

__author__ = "Manuja"
__email__ = "manuja@github"
__version__ = "0.0.1"
__status__ = "test"


class global_args:
    OWNER = "Manuja"
    ENVIRONMENT = "test"
    MODULE_NAME = "sample_kinesis_producer"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    STREAM_NAME = os.getenv("STREAM_NAME", "data_pipe")
    AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")


def set_logging(lv=global_args.LOG_LEVEL):
    logging.basicConfig(level=lv)
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(lv)
    return LOGGER


def sys_gen_uuid():
    return str(uuid.uuid4())


def random_str_generator(size=40, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def send_data(client, data, key, stream_name):
    resp = client.put_records(
        Records=[
            {
                "Data": json.dumps(data),
                "PartitionKey": key},
        ],
        StreamName=stream_name

    )
    LOGGER.info(f"Response:{resp}")


client = boto3.client(
    "kinesis", region_name=global_args.AWS_REGION)


def lambda_handler(event, context):
    global LOGGER
    LOGGER = set_logging(logging.INFO)
    resp = {"status": False, "resp": ""}
    LOGGER.info(f"Event: {json.dumps(event)}")

    random_username = ["Johnson", "Horst", "Reed", "Garcia", "Fortin", "Samuels", "Linda", "Shelly"]

    try:
        record_count = 0
        for i in range(random.randint(1, 3)):
            send_data(client, {"name": random.choice(random_username),
                               "age": random.randint(1, 500),
                               "location": f"Euorpe"
                               },
                      sys_gen_uuid(), global_args.STREAM_NAME)
            record_count += 1
        resp["resp"] = record_count
        resp["status"] = True

    except Exception as e:
        LOGGER.error(f"ERROR:{str(e)}")
        resp["error_message"] = str(e)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": resp
        })
    }


if __name__ == "__main__":
    lambda_handler({}, {})