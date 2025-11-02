# local_elt_pipeline

Simple local ELT pipeline with

* dependencies management: uv
* ingestion: dlt
* transformation: dbt
* OLAP db: duckdb
* Orchestration: Prefect
* BI tool: Evidence (BI as code)

## Quick Start

### Setup

```bash
# Install dependencies
uv sync

# Install dev dependencies (for testing)
uv sync --extra dev
```

### Configuration

Edit `src/cfg/config.py` to configure companies and start date:

```python
START_DATE = "2024-01-01"
COMPANIES = ["jpmorgan", "bank of america"]
```

### Run the Pipeline

```bash
# Run incremental pipeline (first run loads from START_DATE to today)
uv run python run_prefect_flow.py

# Reset state to reload from START_DATE
uv run python run_prefect_flow.py --reset-state
```

### Access Prefect UI (Optional)

```bash
# Start Prefect server
./start_prefect_server.sh

# Access UI at http://127.0.0.1:4200
```

### Access DuckDB UI and adding the database

```bash
duckdb -ui 
```

This will spin up the DuckDB's UI, where you can access the `database/cfpb_complaints.duckdb`. Wh

## Project Structure

```text
src/
  ├── __init__.py
  ├── apis/
  │   ├── __init__.py
  │   └── cfpb_api_client.py
  ├── cfg/
  │   ├── __init__.py
  │   └── config.py
  ├── pipelines/
  │   ├── __init__.py
  │   └── cfpb_complaints_pipeline.py
  ├── utils/
  │   ├── __init__.py
  │   └── state.py
  └── orchestration/
      ├── __init__.py
      └── cfpb_flows.py
```

## Key Components

* **apis/**: API client for CFPB Consumer Complaint Database
* **cfg/**: Configuration settings (start date, companies list)
* **pipelines/**: dlt pipeline definitions for data extraction and loading
* **utils/**: Utility functions for state management
* **orchestration/**: Prefect flows that orchestrate the pipeline

## How It Works

### Incremental Loading

1. **First run**: Loads data from `START_DATE` to today
2. **Subsequent runs**: Only loads new days (incremental)
3. **State tracking**: Saves last loaded date to `pipeline_state.json`
4. **Automatic**: Determines date range automatically

### Data Flow

```text
CFPB API → dlt Pipeline → DuckDB (raw schema)
                ↓
         Prefect Orchestration
                ↓
         State Management
```

## Documentation

* [README_INGESTION.md](README_INGESTION.md) - Complete ingestion pipeline documentation

## Testing

```bash
# Run tests
uv run pytest tests/
```

## License

See [LICENSE](LICENSE) file for details.
