import json
import logging
import os
from typing import Any

from app.main import main


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(os.environ.get("LAMBDA_LOG_LEVEL", "INFO"))
    return logger


def handler(event: dict[str, Any], context):
    """
    Main entry point for the lambda function.
    """
    lambda_logger = get_logger()
    lambda_logger.info(
        f"Got event for invocation request with id: '{context.aws_request_id}'"
    )
    print(json.dumps(event))
    try:
        response = main()
    except Exception as e:
        lambda_logger.error(f"Received exception '{e}' while running the application.")
        raise
    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
