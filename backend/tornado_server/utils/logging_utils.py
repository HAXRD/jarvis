import logging
import uuid

def setup_request_logger():
    """Setup a logger for with unique request ID"""
    request_id = str(uuid.uuid4())
    logger = logging.getLogger(f"request.{request_id}")

    # Add the request ID as an extra field to all logs
    logger = logging.LoggerAdapter(logger, {"request_id": request_id})

    return logger

