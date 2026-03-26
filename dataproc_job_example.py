"""
Example: Using BOSP Audit Logger in Dataproc Jobs (Orchestrated by Airflow)
=============================================================================

This is an example of how to integrate bosp-audit-logger into a Dataproc job
for logging queries and tracking data processing metrics.

Note: This module runs WITHIN a Dataproc job submitted by an Airflow DAG.
The Airflow DAG handles the job orchestration and submission.

Example Airflow DAG pattern:
    from airflow import DAG
    from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
    
    with DAG('dataproc_audit_job') as dag:
        submit_job = DataprocSubmitJobOperator(
            task_id='submit_dataproc_job',
            job={
                'pyspark_job': {
                    'main_python_file_uri': 'gs://my-bucket/dataproc_job_example.py',
                }
            },
            cluster_name='my-cluster',
            region='us-central1',
            project_id='my-gcp-project',
        )

Direct Dataproc submission (non-Airflow):
    gcloud dataproc jobs submit pyspark \\
        --cluster=my-cluster \\
        --region=us-central1 \\
        dataproc_job_example.py
"""

import sys
import os
from datetime import datetime
import time

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bosp_audit_logger import BospAuditLogger, get_logger


def process_employee_data():
    """Example Dataproc job that processes employee data"""
    
    # Initialize BOSP Audit Logger
    logger = BospAuditLogger()
    
    try:
        # Log job start
        logger.log_job_event(
            event_name="job_started",
            status="success",
            message="Employee data processing job started",
            details={
                "script": "dataproc_job_example.py",
                "version": "1.0",
            },
        )
        
        # Simulate database connection and query execution
        print("Step 1: Connecting to database...")
        logger.log_job_event(
            event_name="database_connection",
            status="success",
            message="Connected to MySQL database",
        )
        
        # Simulate query 1: Fetch employees
        print("Step 2: Fetching employee data...")
        start = time.time()
        time.sleep(0.5)  # Simulate query execution
        query_time_1 = time.time() - start
        
        logger.log_query_execution(
            query="SELECT emp_no, first_name, last_name FROM employees LIMIT 1000",
            execution_time=query_time_1,
            rows_processed=1000,
            rows_output=1000,
            success=True,
            query_type="SQL",
            database="employee_db",
        )
        
        # Log data processing event
        print("Step 3: Processing employee records...")
        start = time.time()
        time.sleep(1.0)  # Simulate processing
        processing_time = time.time() - start
        
        logger.log_data_process_event(
            event_name="employee_record_processing",
            status="in_progress",
            records_processed=1000,
            records_valid=950,
            records_invalid=50,
            duration=processing_time,
            details={
                "validation_rules": ["email_format", "age_range", "salary_range"],
                "error_types": {
                    "invalid_email": 30,
                    "age_out_of_range": 15,
                    "salary_negative": 5,
                },
            },
        )
        
        # Simulate query 2: Get department information
        print("Step 4: Enriching with department data...")
        start = time.time()
        time.sleep(0.3)  # Simulate query
        query_time_2 = time.time() - start
        
        logger.log_query_execution(
            query="SELECT d.dept_no, d.dept_name FROM departments d",
            execution_time=query_time_2,
            rows_processed=12,
            rows_output=12,
            success=True,
            query_type="SQL",
            database="employee_db",
        )
        
        # Log metrics
        print("Step 5: Recording metrics...")
        logger.log_metric(
            metric_name="records_processed_per_second",
            value=850,
            unit="records/sec",
            tags={
                "table": "employees",
                "operation": "scan_and_validate",
            },
        )
        
        logger.log_metric(
            metric_name="data_quality_score",
            value=95.0,
            unit="percent",
            tags={
                "validation_checks": "4",
                "dataset": "employee_records",
            },
        )
        
        # Log audit trail
        print("Step 6: Creating audit trail...")
        logger.log_audit_trail(
            action="process_data",
            resource="employees_table",
            user="dataproc_job",
            changes={
                "records_processed": 1000,
                "records_validated": 950,
                "output_format": "parquet",
            },
            result="success",
        )
        
        # Simulate writing results
        print("Step 7: Writing results to storage...")
        logger.log_job_event(
            event_name="data_export",
            status="success",
            message="Processed data exported to GCS",
            details={
                "destination": "gs://my-bucket/employee_data_output/",
                "format": "parquet",
                "rows_written": 950,
                "size_gb": 0.042,
            },
        )
        
        # Job completion
        print("Step 8: Finalizing...")
        summary = logger.get_job_summary()
        
        logger.log_job_event(
            event_name="job_completed",
            status="success",
            message="Employee data processing job completed successfully",
            details=summary,
        )
        
        print("\n✅ Job completed successfully!")
        print(f"\nJob Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        return 0
        
    except Exception as e:
        # Log exception
        logger.log_exception(
            exception=e,
            context="Employee data processing job",
            additional_info={
                "step": "processing",
                "recoverable": False,
            },
        )
        
        # Log job failure
        logger.log_job_event(
            event_name="job_failed",
            status="failure",
            message=f"Job failed with error: {str(e)}",
        )
        
        print(f"\n❌ Job failed: {str(e)}")
        return 1


def example_with_spark_sql():
    """Example using Spark SQL in Dataproc"""
    
    logger = get_logger()
    
    logger.log_job_event(
        event_name="spark_job_started",
        status="success",
        message="Spark SQL job started",
    )
    
    try:
        # Simulate Spark SQL query
        print("Running Spark SQL query...")
        start = time.time()
        time.sleep(0.7)  # Simulate computation
        execution_time = time.time() - start
        
        spark_query = """
            SELECT 
                e.emp_no,
                CONCAT(e.first_name, ' ', e.last_name) as full_name,
                s.salary,
                d.dept_name
            FROM employees e
            JOIN salaries s ON e.emp_no = s.emp_no
            JOIN dept_emp de ON e.emp_no = de.emp_no
            JOIN departments d ON de.dept_no = d.dept_no
            WHERE s.to_date = '9999-01-01'
            AND de.to_date = '9999-01-01'
        """
        
        logger.log_query_execution(
            query=spark_query,
            execution_time=execution_time,
            rows_processed=240124,
            rows_output=240124,
            success=True,
            query_type="Spark SQL",
            database="employee_db",
        )
        
        logger.log_metric(
            metric_name="spark_query_execution_time",
            value=execution_time,
            unit="seconds",
            tags={"engine": "spark", "distributed": "true"},
        )
        
        print("✅ Spark SQL query completed successfully")
        
    except Exception as e:
        logger.log_exception(e, context="Spark SQL execution")
        print(f"❌ Spark SQL query failed: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("BOSP Audit Logger - Dataproc Job Example")
    print("=" * 60)
    print()
    
    # Example 1: Basic data processing
    print("Example 1: Employee Data Processing")
    print("-" * 60)
    exit_code = process_employee_data()
    
    print()
    print("Example 2: Spark SQL Execution")
    print("-" * 60)
    example_with_spark_sql()
    
    print()
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    
    sys.exit(exit_code)
