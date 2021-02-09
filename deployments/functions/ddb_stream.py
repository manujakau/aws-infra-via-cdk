import json
import logging
import os

import boto3

__author__ = "manuja"
__email__ = "manuja@github"
__version__ = "0.0.2"
__status__ = "test"


class global_args:
    OWNER = "manuja"
    ENVIRONMENT = "test"
    MODULE_NAME = "Dynamodb-Stream-Processor"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def set_logging(lv=global_args.LOG_LEVEL):
    logging.basicConfig(level=lv)
    logger = logging.getLogger()
    logger.setLevel(lv)
    return logger


# Initialize Logger
logger = set_logging()


def lambda_handler(event, context):

    response = {"status": False, "response": ""}
    logger.info(f"Event: {json.dumps(event)}")

    response = {"status": False, "TotalItems": {}, "Items": []}

    if not "Records" in event:
        response = {"status": False, "error_message": "No Records found in Event"}
        return response

    logger.debug(f"Event:{event}")
    for r in event.get("Records"):
        if r.get("eventName") == "INSERT":
            response["Items"].append(r)

    if response.get("Items"):
        response["status"] = True
        response["TotalItems"] = {"Received": len(
            event.get("Records")), "Processed": len(response.get("Items"))}

    logger.info(f"response: {json.dumps(response)}")

    return response


if __name__ == "__main__":
    lambda_handler({}, {})