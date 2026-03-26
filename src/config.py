"""
Google Cloud Logging Configuration
===================================
Configure logging for Google Cloud Platform
"""

import os
from typing import Optional, Dict, Any


class LoggerConfig:
    """Configuration for Google Cloud Logger"""

    def __init__(
        self,
        project_id: Optional[str] = None,
        log_name: str = "employee-assignment-logs",
        service_account_path: Optional[str] = None,
        environment: str = "development",
        enable_console: bool = True,
        enable_cloud: bool = True,
    ):
        """
        Initialize logger configuration

        Args:
            project_id: GCP project ID (uses GOOGLE_CLOUD_PROJECT env var if not provided)
            log_name: Name of the log in Cloud Logging
            service_account_path: Path to service account JSON key file
            environment: Environment name (development, staging, production)
            enable_console: Enable console logging
            enable_cloud: Enable Google Cloud Logging
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.log_name = log_name
        self.service_account_path = service_account_path or os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.environment = environment
        self.enable_console = enable_console
        self.enable_cloud = enable_cloud

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "project_id": self.project_id,
            "log_name": self.log_name,
            "service_account_path": self.service_account_path,
            "environment": self.environment,
            "enable_console": self.enable_console,
            "enable_cloud": self.enable_cloud,
        }

    def validate(self) -> bool:
        """Validate configuration"""
        if not self.project_id:
            raise ValueError("project_id not set. Set GOOGLE_CLOUD_PROJECT env var")
        if self.enable_cloud and not self.service_account_path:
            raise ValueError(
                "service_account_path required for Cloud Logging. Set GOOGLE_APPLICATION_CREDENTIALS env var"
            )
        return True
