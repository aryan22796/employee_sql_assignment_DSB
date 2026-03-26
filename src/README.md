# Google Cloud Logger Library

## 📚 Overview

A Python logging library that integrates with Google Cloud Logging (Stackdriver) for centralized log management and monitoring.

## 📦 Installation

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup

Set up Google Cloud credentials:

```bash
# Option 1: Using service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Option 2: Using application default credentials
gcloud auth application-default login
```

Set GCP project ID:
```bash
export GOOGLE_CLOUD_PROJECT=your-gcp-project-id
```

## 🚀 Quick Start

### Basic Usage

```python
from src import CloudLogger, LoggerConfig

# Create configuration
config = LoggerConfig(
    project_id="my-gcp-project",
    log_name="my-app-logs",
    environment="production"
)

# Create logger
logger = CloudLogger(name="my-app", config=config)

# Log messages
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred", exception=None)
```

## 📖 API Reference

### CloudLogger

#### Methods

**`log_query(query, execution_time, rows_affected, success, error)`**
- Log SQL query execution
- Tracks execution time and affected rows

**`log_error_details(error_type, message, context)`**
- Log detailed error information
- Includes error type and context

**`log_performance_metric(metric_name, value, unit, tags)`**
- Log performance metrics
- Useful for monitoring

**`info(message, **kwargs)`**
- Log info level message
- Additional context via kwargs

**`debug(message, **kwargs)`**
- Log debug level message

**`warning(message, **kwargs)`**
- Log warning level message

**`error(message, exception, **kwargs)`**
- Log error level message
- Optionally include exception traceback

**`critical(message, **kwargs)`**
- Log critical level message

## 🔧 Configuration

### LoggerConfig Options

```python
config = LoggerConfig(
    project_id="your-gcp-project",        # GCP project ID
    log_name="app-logs",                   # Log name in Cloud
    service_account_path="/path/to/key",   # Service account JSON
    environment="production",               # Environment name
    enable_console=True,                   # Console output
    enable_cloud=True                      # Cloud Logging
)
```

## 📊 Log Format

### Query Execution Log
```json
{
  "type": "query_execution",
  "query": "SELECT * FROM employees",
  "execution_time_seconds": 0.245,
  "rows_affected": 100,
  "success": true,
  "timestamp": "2026-03-26T10:30:00",
  "environment": "production"
}
```

### Error Log
```json
{
  "type": "error",
  "error_type": "DatabaseConnectionError",
  "message": "Failed to connect",
  "context": {"host": "localhost"},
  "timestamp": "2026-03-26T10:30:00",
  "environment": "production"
}
```

### Performance Metric Log
```json
{
  "type": "performance_metric",
  "metric_name": "query_execution_time",
  "value": 0.245,
  "unit": "seconds",
  "tags": {"query_type": "SELECT"},
  "timestamp": "2026-03-26T10:30:00",
  "environment": "production"
}
```

## 🔍 Example Usage

```python
from src import CloudLogger, LoggerConfig

# Initialize logger
config = LoggerConfig(
    project_id="my-project",
    environment="development"
)
logger = CloudLogger(config=config)

# Log query execution
logger.log_query(
    query="SELECT * FROM employees WHERE emp_no = 10001",
    execution_time=0.125,
    rows_affected=1,
    success=True
)

# Log performance metric
logger.log_performance_metric(
    metric_name="query_execution_time",
    value=0.125,
    unit="seconds",
    tags={"table": "employees"}
)

# Log error
logger.log_error_details(
    error_type="QueryError",
    message="Invalid column reference",
    context={"column": "invalid_col"}
)
```

## ⚙️ Google Cloud Setup

### 1. Create GCP Project
```bash
gcloud projects create my-project
gcloud config set project my-project
```

### 2. Enable Cloud Logging API
```bash
gcloud services enable logging.googleapis.com
```

### 3. Create Service Account
```bash
gcloud iam service-accounts create logger-sa
```

### 4. Grant Permissions
```bash
gcloud projects add-iam-policy-binding my-project \
  --member=serviceAccount:logger-sa@my-project.iam.gserviceaccount.com \
  --role=roles/logging.logWriter
```

### 5. Create Key
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=logger-sa@my-project.iam.gserviceaccount.com
```

### 6. Set Environment Variable
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

## 📝 Notes

- All timestamps are in UTC ISO format
- Logs are automatically JSON formatted for easy parsing
- Structured logging enables better searching and filtering in Cloud Logging console
- Performance metrics can be monitored using Cloud Monitoring

## 🆘 Troubleshooting

### "project_id not set"
- Set `GOOGLE_CLOUD_PROJECT` environment variable

### "service_account_path required"
- Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Connection issues
- Verify service account has logging.logWriter role
- Check internet connectivity to Google Cloud APIs

## 📚 References

- [Google Cloud Logging Documentation](https://cloud.google.com/logging/docs)
- [Python Client Library](https://googleapis.dev/python/logging/latest/)
- [Service Account Setup](https://cloud.google.com/docs/authentication/getting-started)
