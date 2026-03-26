"""
Google Cloud Logging Library
=============================
A Python library for logging to Google Cloud Logging (Stackdriver)

Features:
- Simple configuration
- Automatic JSON formatting
- Structured logging support
- Error tracking
- Performance metrics logging
"""

from .logger import Logger, CloudLogger
from .config import LoggerConfig

__version__ = "1.0.0"
__all__ = ["Logger", "CloudLogger", "LoggerConfig"]
