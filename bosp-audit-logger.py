"""
BOSP Audit Logger - General-Purpose Audit Logging for Dataproc & Airflow
=========================================================================

A production-grade audit logging module designed to run within Google Cloud Dataproc jobs
orchestrated by Apache Airflow DAGs. Provides structured logging and audit trail management
across all job types (NOT limited to SQL).

This module is INDEPENDENT OF THE SQL ASSIGNMENT - it's a general-purpose logging library
for monitoring and auditing any Dataproc job running under Airflow orchestration.

This module integrates with Google Cloud Logging to track:
- Query executions (SQL, Spark SQL, or any query-like operations)
- Data processing metrics and events
- Error events and exceptions
- Audit trails and compliance logging
- Performance metrics and KPIs

Usage:
    from bosp_audit_logger import get_logger
    
    logger = get_logger()
    logger.log_query_execution(query, execution_time)
    logger.log_data_process_event(event_name, status, records_processed)
    logger.log_exception(exception, context)
    logger.log_job_event(event_name, status, message)
"""

import os
import sys
import traceback
from typing import Optional, Dict, Any
from datetime import datetime

# Import logger library
try:
    from src import CloudLogger, LoggerConfig
except ImportError:
    print("Warning: src module not found. Installing from requirements...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "src/requirements.txt"])
    from src import CloudLogger, LoggerConfig


class BospAuditLogger:
    """
    BOSP (Big Data Operations Service Platform) Audit Logger
    
    Centralized logging for data processing jobs, particularly for Dataproc
    """

    # Singleton instance
    _instance = None
    
    def __new__(cls, project_id: Optional[str] = None, job_id: Optional[str] = None):
        """Singleton pattern - ensure only one logger instance"""
        if cls._instance is None:
            cls._instance = super(BospAuditLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, project_id: Optional[str] = None, job_id: Optional[str] = None):
        """
        Initialize BOSP Audit Logger
        
        Args:
            project_id: GCP project ID (defaults to GOOGLE_CLOUD_PROJECT env var)
            job_id: Dataproc job ID (defaults to DATAPROC_JOB_ID env var)
        """
        if self._initialized:
            return

        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.job_id = job_id or os.getenv("DATAPROC_JOB_ID", "unknown")
        self.cluster_name = os.getenv("DATAPROC_CLUSTER_NAME", "unknown")
        self.environment = os.getenv("ENVIRONMENT", "production")
        self.start_time = datetime.utcnow()

        # Initialize configuration
        config = LoggerConfig(
            project_id=self.project_id,
            log_name="bosp-audit-logs",
            environment=self.environment,
            enable_console=True,
            enable_cloud=True,
        )

        # Initialize cloud logger
        self.cloud_logger = CloudLogger(name="bosp-audit-logger", config=config)
        
        # Log initialization
        self.cloud_logger.info(
            f"BOSP Audit Logger initialized - Job: {self.job_id}, Cluster: {self.cluster_name}"
        )
        
        self._initialized = True

    def log_query_execution(
        self,
        query: str,
        execution_time: float,
        rows_processed: int = 0,
        rows_output: int = 0,
        success: bool = True,
        error: Optional[str] = None,
        query_type: str = "SQL",
        database: str = "default",
    ) -> None:
        """
        Log SQL/Spark query execution
        
        Args:
            query: Query string
            execution_time: Execution time in seconds
            rows_processed: Number of rows processed
            rows_output: Number of rows in output
            success: Whether query succeeded
            error: Error message if failed
            query_type: Type of query (SQL, Spark, etc.)
            database: Database/table name
        """
        log_data = {
            "event_type": "query_execution",
            "query_type": query_type,
            "database": database,
            "query_preview": query[:500],  # First 500 chars for preview
            "execution_time_seconds": round(execution_time, 3),
            "rows_processed": rows_processed,
            "rows_output": rows_output,
            "success": success,
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if error:
            log_data["error"] = error
            self.cloud_logger.log_error_details(
                error_type="QueryExecutionError",
                message=f"Query failed after {execution_time:.2f}s",
                context=log_data,
            )
        else:
            self.cloud_logger.log_query(
                query=query,
                execution_time=execution_time,
                rows_affected=rows_output,
                success=success,
            )

    def log_data_process_event(
        self,
        event_name: str,
        status: str,
        records_processed: int = 0,
        records_valid: int = 0,
        records_invalid: int = 0,
        duration: float = 0.0,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log data processing event
        
        Args:
            event_name: Name of the processing event
            status: Event status (started, in_progress, completed, failed)
            records_processed: Total records processed
            records_valid: Valid records
            records_invalid: Invalid records
            duration: Duration in seconds
            details: Additional event details
        """
        log_data = {
            "event_type": "data_processing",
            "event_name": event_name,
            "status": status,
            "records_processed": records_processed,
            "records_valid": records_valid,
            "records_invalid": records_invalid,
            "duration_seconds": round(duration, 3),
            "success_rate": (
                round((records_valid / records_processed * 100), 2)
                if records_processed > 0
                else 0
            ),
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        if status in ["failed", "error"]:
            self.cloud_logger.log_error_details(
                error_type="DataProcessingError",
                message=f"Data processing event '{event_name}' failed",
                context=log_data,
            )
        else:
            self.cloud_logger.info(str(log_data))

    def log_job_event(
        self,
        event_name: str,
        status: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log job-level event
        
        Args:
            event_name: Event name (job_started, job_completed, etc.)
            status: Event status (success, failure, warning)
            message: Status message
            details: Additional details
        """
        log_data = {
            "event_type": "job_event",
            "event_name": event_name,
            "status": status,
            "message": message,
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        if status == "failure":
            self.cloud_logger.log_error_details(
                error_type="JobEventError",
                message=message,
                context=log_data,
            )
        elif status == "warning":
            self.cloud_logger.warning(str(log_data))
        else:
            self.cloud_logger.info(str(log_data))

    def log_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Log performance or business metric
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            tags: Additional metric tags
        """
        metric_tags = tags or {}
        metric_tags.update({
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
        })

        self.cloud_logger.log_performance_metric(
            metric_name=metric_name,
            value=value,
            unit=unit,
            tags=metric_tags,
        )

    def log_exception(
        self,
        exception: Exception,
        context: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log exception with full traceback
        
        Args:
            exception: Exception object
            context: Context description
            additional_info: Additional information
        """
        log_data = {
            "event_type": "exception",
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "traceback": traceback.format_exc(),
            "context": context,
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
            "additional_info": additional_info or {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.cloud_logger.log_error_details(
            error_type=type(exception).__name__,
            message=str(exception),
            context=log_data,
        )

    def log_audit_trail(
        self,
        action: str,
        resource: str,
        user: str = "system",
        changes: Optional[Dict[str, Any]] = None,
        result: str = "success",
    ) -> None:
        """
        Log audit trail for compliance
        
        Args:
            action: Action performed (create, update, delete, etc.)
            resource: Resource affected
            user: User performing action
            changes: Changes made
            result: Result of action
        """
        log_data = {
            "event_type": "audit_trail",
            "action": action,
            "resource": resource,
            "user": user,
            "changes": changes or {},
            "result": result,
            "job_id": self.job_id,
            "cluster_name": self.cluster_name,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.cloud_logger.info(str(log_data))

    def get_job_summary(self) -> Dict[str, Any]:
        """Get job execution summary"""
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        return {
            "job_id": self.job_id,
            "project_id": self.project_id,
            "cluster_name": self.cluster_name,
            "start_time": self.start_time.isoformat(),
            "current_duration_seconds": round(duration, 2),
            "environment": self.environment,
        }


# Module-level convenience functions for easy access from anywhere
def get_logger() -> BospAuditLogger:
    """Get global BOSP Audit Logger instance"""
    return BospAuditLogger()


def log_query(query: str, execution_time: float, **kwargs) -> None:
    """Log query execution using global logger"""
    get_logger().log_query_execution(query, execution_time, **kwargs)


def log_event(event_name: str, status: str, **kwargs) -> None:
    """Log job event using global logger"""
    get_logger().log_job_event(event_name, status, "", **kwargs)


def log_metric(metric_name: str, value: float, **kwargs) -> None:
    """Log metric using global logger"""
    get_logger().log_metric(metric_name, value, **kwargs)


if __name__ == "__main__":
    """Example usage"""
    
    print("BOSP Audit Logger - Example Usage")
    print("=" * 50)
    
    # Initialize logger
    logger = BospAuditLogger()
    
    # Log job start
    logger.log_job_event(
        event_name="job_started",
        status="success",
        message="Dataproc job started",
        details={"version": "1.0"},
    )
    
    # Log data processing
    logger.log_data_process_event(
        event_name="employee_data_validation",
        status="completed",
        records_processed=1000,
        records_valid=950,
        records_invalid=50,
        duration=2.5,
    )
    
    # Log query execution
    logger.log_query_execution(
        query="SELECT * FROM employees WHERE emp_no = 10001",
        execution_time=0.245,
        rows_processed=100,
        rows_output=1,
        success=True,
        query_type="SQL",
        database="employee_db",
    )
    
    # Log metric
    logger.log_metric(
        metric_name="data_processing_throughput",
        value=400,
        unit="records/second",
        tags={"table": "employees"},
    )
    
    # Log audit trail
    logger.log_audit_trail(
        action="export_data",
        resource="employee_export_2026_03_26.csv",
        user="dataproc_job",
        result="success",
    )
    
    # Get job summary
    summary = logger.get_job_summary()
    print("\nJob Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Example logging completed!")
