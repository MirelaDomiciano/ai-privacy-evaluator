"""
Logging utilities for structured JSON logging
"""

from pydantic import BaseModel
from datetime import datetime
import logging
from typing import Optional, Any, Dict
import os


class LogInfo(BaseModel):
    level: str
    timestamp: datetime
    message: str
    metadata: Optional[Dict[str, Any]] = None


class SetupLogger:
    @staticmethod
    def setup_logger() -> None:
        environment = os.environ.get("ENVIRONMENT", "development")
        if environment == "development":
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO

        logging.basicConfig(
            level=logging_level,
            format="%(message)s",
            force=True
        )
        JsonLogger.log(
            level="INFO",
            message="Logger initialized",
            metadata={"level": logging.getLevelName(logging_level), "environment": environment}
        )


class JsonLogger:
    @staticmethod
    def log(
        level: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        log_info = LogInfo(
            level=level,
            timestamp=datetime.now(),
            message=message,
            metadata=metadata,
        )
        
        log_json = log_info.model_dump_json()
        
        if level == "CRITICAL":
            logging.critical(log_json)
        elif level == "ERROR":
            logging.error(log_json)
        elif level == "WARNING":
            logging.warning(log_json)
        elif level == "INFO":
            logging.info(log_json)
        elif level == "DEBUG":
            logging.debug(log_json)

