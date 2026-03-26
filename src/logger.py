"""
Logger Implementation
====================
Logging utilities for Google Cloud Logging integration
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dictionary, Optional
from google.cloud import logging as cloud_logging
from google.oauth2 import service_account

from .config import LoggerConfig


class Logger:
    """Base logger for local and cloud logging"""

    def __init__(self, name: str = "app", config: Optional[LoggerConfig] = None):
        """
        Initialize logger

        Args:
            name: Logger name
            config: LoggerConfig instance
        """
        self.name = name
        self.config = config or LoggerConfig()
        self.logger = logging.getLogger(name)
        self.setup_logging()

    def setup_logging(self) -> None:
        """Setup logging handlers"""
        # Set logger level
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        if self.config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, exception: Optional[Exception] = None, **kwargs) -> None:
        """Log error message"""
        if exception:
            self.logger.error(message, exc_info=True, extra=kwargs)
        else:
            self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)


class CloudLogger(Logger):
    """Logger with Google Cloud Logging integration"""

    def __init__(self, name: str = "cloud-app", config: Optional[LoggerConfig] = None):
        """
        Initialize Cloud Logger

        Args:
            name: Logger name
            config: LoggerConfig instance
        """
        self.config = config or LoggerConfig()
        self.config.validate()

        super().__init__(name, self.config)

        if self.config.enable_cloud:
            self.setup_cloud_logging()

    def setup_cloud_logging(self) -> None:
        """Setup Google Cloud Logging client"""
        try:
            # Initialize Cloud Logging client
            if self.config.service_account_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.config.service_account_path
                )
                self.cloud_client = cloud_logging.Client(
                    project=self.config.project_id, credentials=credentials
                )
            else:
                self.cloud_client = cloud_logging.Client(
                    project=self.config.project_id
                )

            # Get Cloud Logging handler
            cloud_handler = self.cloud_client.logging_handler_class(
                name=self.config.log_name
            )
            cloud_handler.setLevel(logging.DEBUG)

            # Add handler to logger
            self.logger.addHandler(cloud_handler)

            self.logger.info(
                f"Cloud Logging initialized for project: {self.config.project_id}"
            )
        except Exception as e:
            self.logger.error(f"Failed to setup Cloud Logging: {str(e)}")
            if not self.config.enable_console:
                raise

    def log_query(
        self,
        query: str,
        execution_time: float,
        rows_affected: int = 0,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """
        Log SQL query execution

        Args:
            query: SQL query string
            execution_time: Query execution time in seconds
            rows_affected: Number of rows affected
            success: Whether query executed successfully
            error: Error message if failed
        """
        log_data = {
            "type": "query_execution",
            "query": query,
            "execution_time_seconds": execution_time,
            "rows_affected": rows_affected,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "environment": self.config.environment,
        }

        if error:
            log_data["error"] = error
            self.logger.error(json.dumps(log_data))
        else:
            self.logger.info(json.dumps(log_data))

    def log_error_details(
        self, error_type: str, message: str, context: Optional[dict] = None
    ) -> None:
        """
        Log detailed error information

        Args:
            error_type: Type of error
            message: Error message
            context: Additional context information
        """
        log_data = {
            "type": "error",
            "error_type": error_type,
            "message": message,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
            "environment": self.config.environment,
        }
        self.logger.error(json.dumps(log_data))

    def log_performance_metric(
        self, metric_name: str, value: float, unit: str = "", tags: Optional[dict] = None
    ) -> None:
        """
        Log performance metric

        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            tags: Additional tags
        """
        log_data = {
            "type": "performance_metric",
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "tags": tags or {},
            "timestamp": datetime.utcnow().isoformat(),
            "environment": self.config.environment,
        }
        self.logger.info(json.dumps(log_data))
