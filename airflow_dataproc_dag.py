"""
Airflow DAG Example: Submitting Dataproc Jobs with Audit Logging
==================================================================

This is an example Apache Airflow DAG that orchestrates Dataproc jobs
which use the bosp-audit-logger for comprehensive audit logging.

Note: The bosp-audit-logger module is INDEPENDENT OF THE SQL ASSIGNMENT.
It's a general-purpose logging library for any Dataproc job type.

Prerequisites:
- Apache Airflow 2.x installed
- google-cloud-dataproc provider installed
- Google Cloud credentials configured
- Dataproc cluster created in your GCP project

Install requirements:
    pip install apache-airflow google-cloud-dataproc
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitJobOperator,
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
)
from airflow.utils.dates import days_ago

# Configuration
PROJECT_ID = "your-gcp-project-id"
CLUSTER_NAME = "bosp-audit-cluster"
REGION = "us-central1"
ZONE = f"{REGION}-a"
GCS_BUCKET = "your-gcs-bucket"

# DAG Configuration
default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# DAG Definition
dag = DAG(
    "bosp_audit_logging_dataproc_job",
    default_args=default_args,
    description="Dataproc job with comprehensive audit logging",
    schedule_interval="0 2 * * *",  # Daily at 2 AM UTC
    tags=["dataproc", "audit-logging", "gcp"],
)

# Cluster Configuration
CLUSTER_CONFIG = {
    "project_id": PROJECT_ID,
    "cluster_name": CLUSTER_NAME,
    "config": {
        "gce_cluster_config": {
            "zone": ZONE,
            "service_account": "dataproc-sa@your-project.iam.gserviceaccount.com",
        },
        "master_config": {
            "num_instances": 1,
            "machine_type_uri": "n1-standard-4",
        },
        "worker_config": {
            "num_instances": 2,
            "machine_type_uri": "n1-standard-4",
        },
        "properties": {
            "dataproc:dataproc.protocol.version": "auto",
        },
    },
}

# PySpark Job Configuration (using bosp-audit-logger)
PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": f"gs://{GCS_BUCKET}/jobs/dataproc_job_example.py",
        "python_file_uris": [
            f"gs://{GCS_BUCKET}/libs/bosp-audit-logger.py",
            f"gs://{GCS_BUCKET}/libs/src/__init__.py",
            f"gs://{GCS_BUCKET}/libs/src/config.py",
            f"gs://{GCS_BUCKET}/libs/src/logger.py",
        ],
        "args": [
            f"--output-path=gs://{GCS_BUCKET}/output/",
            f"--job-id={CLUSTER_NAME}-pyspark-job",
        ],
    },
}

# Alternative: Spark SQL Job Configuration
SPARK_SQL_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "spark_sql_job": {
        "query_list": {
            "queries": [
                "SELECT * FROM employees LIMIT 100;",
                "SELECT dept_name, COUNT(*) FROM departments GROUP BY dept_name;",
            ]
        },
    },
}

# ============================================================================
# DAG Tasks
# ============================================================================

# Task 1: Create Dataproc Cluster
create_cluster = DataprocCreateClusterOperator(
    task_id="create_cluster",
    project_id=PROJECT_ID,
    cluster_config=CLUSTER_CONFIG,
    region=REGION,
    gcp_conn_id="google_cloud_default",
)

# Task 2: Submit PySpark Job with Audit Logging
submit_pyspark_job = DataprocSubmitJobOperator(
    task_id="submit_pyspark_audit_job",
    job_config=PYSPARK_JOB,
    region=REGION,
    project_id=PROJECT_ID,
    gcp_conn_id="google_cloud_default",
)

# Task 3: Alternative - Submit Spark SQL Job
submit_spark_sql_job = DataprocSubmitJobOperator(
    task_id="submit_spark_sql_job",
    job_config=SPARK_SQL_JOB,
    region=REGION,
    project_id=PROJECT_ID,
    gcp_conn_id="google_cloud_default",
)

# Task 4: Delete Cluster (cleanup)
delete_cluster = DataprocDeleteClusterOperator(
    task_id="delete_cluster",
    project_id=PROJECT_ID,
    cluster_name=CLUSTER_NAME,
    region=REGION,
    gcp_conn_id="google_cloud_default",
    trigger_rule="all_done",  # Run even if previous tasks failed
)

# ============================================================================
# Task Dependencies
# ============================================================================

create_cluster >> submit_pyspark_job >> delete_cluster
# Uncomment to run Spark SQL job instead:
# create_cluster >> submit_spark_sql_job >> delete_cluster


# ============================================================================
# Notes for Deployment
# ============================================================================
"""
1. Upload files to GCS:
   gsutil cp dataproc_job_example.py gs://your-gcs-bucket/jobs/
   gsutil cp bosp-audit-logger.py gs://your-gcs-bucket/libs/
   gsutil -m cp -r src/ gs://your-gcs-bucket/libs/

2. Set up GCP credentials:
   gcloud auth application-default login
   
3. Create service account for Dataproc:
   gcloud iam service-accounts create dataproc-sa
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member=serviceAccount:dataproc-sa@PROJECT_ID.iam.gserviceaccount.com \
       --role=roles/dataproc.worker
   
4. Create Airflow connection:
   In Airflow UI: Admin > Connections > google_cloud_default
   - Connection Type: Google Cloud
   - Project ID: your-gcp-project-id
   - Extra JSON: {} (or add service account key)

5. Run the DAG:
   airflow dags unpause bosp_audit_logging_dataproc_job
   airflow dags trigger bosp_audit_logging_dataproc_job

6. View logs in Google Cloud Console:
   - Dataproc > Clusters > bosp-audit-cluster > Logs
   - Cloud Logging > bosp-audit-logs (JSON logs from the audit logger)
"""
