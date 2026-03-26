"""
Example usage of the Google Cloud Logger library
"""

from src import CloudLogger, LoggerConfig


def main():
    """Example usage"""

    # Initialize logger with configuration
    config = LoggerConfig(
        project_id="your-gcp-project-id",
        log_name="employee-assignment-logs",
        environment="development",
        enable_console=True,
        enable_cloud=False,  # Set to True when GCP credentials are configured
    )

    # Create cloud logger instance
    logger = CloudLogger(name="sql-assignment", config=config)

    # Example: Log query execution
    logger.log_query(
        query="SELECT * FROM employees LIMIT 10",
        execution_time=0.245,
        rows_affected=10,
        success=True,
    )

    # Example: Log error details
    logger.log_error_details(
        error_type="DatabaseConnectionError",
        message="Failed to connect to MySQL server",
        context={
            "host": "localhost",
            "port": 3306,
            "database": "employee_db",
        },
    )

    # Example: Log performance metric
    logger.log_performance_metric(
        metric_name="query_execution_time",
        value=0.245,
        unit="seconds",
        tags={"query_type": "SELECT", "table": "employees"},
    )

    # Example: Regular logging
    logger.info("Application started successfully")
    logger.debug("Debug information", user_id=12345)
    logger.warning("This is a warning message")


if __name__ == "__main__":
    main()
