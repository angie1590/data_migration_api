# Data Migration API

This is a Proof of Concept (PoC) API built with FastAPI to support a large-scale data migration pipeline. It enables loading historical data from CSV files, managing data via REST endpoints, and backing up or restoring table contents in AVRO format. Also, It generate reports using this data and visualize them using Streamlite.

Note: This solution (first part: Load Historical data, backup and restore and data ingestion via API Rest) was implemented using pyspark and mongo too. It is in the folder data-migration-spark-mongo

---

## 🚀 Features

- Load historic data from CSV files into a SQL database
- Receive and validate new data via REST endpoints
- Single and batch transaction support (1 to 1000 rows)
- AVRO export of each table's data
- Table restoration from AVRO backups
- Docker-ready and deployable in isolated environments
- Generate reports via REST endpoint
- Create a dashboard to visualize the reports using Streamlite

---

## 📁 Project Structure

```
├── app/
│   ├── core/                          # Logging and configuration
│   │   └── logger.py                  # Logger configuration
│   ├── dashboard/                     # Streamlit dashboard for visual reports
│   │   └── hiring_dashboard.py        # Streamlit app to visualize hiring reports
│   ├── exporters/                     # Backup and restore logic (AVRO)
│   │   ├── avro_utils.py              # Utility functions for AVRO read/write
│   │   ├── backup_departments.py      # AVRO backup logic for departments
│   │   ├── backup_hired_employees.py  # AVRO backup logic for hired employees
│   │   └── backup_jobs.py             # AVRO backup logic for jobs
│   ├── loaders/                       # Loaders for historical data
│   │   ├── base_loader.py             # Common logic for all data loaders
│   │   ├── department_loader.py       # Loader for departments.csv
│   │   ├── hire_employee_loader.py    # Loader for hired_employees.csv
│   │   └── job_loader.py              # Loader for jobs.csv
│   ├── reports/                       # Report generation logic using PySpark
│   │   ├── hiring_above_average.py    # Generate report of departments above average hiring
│   │   └── hiring_quarterly_report.py # Generate quarterly hiring report by job and department
│   ├── routers/                       # FastAPI endpoints
|   ├── backup_data.py                 # Backup dispatcher for all tables
│   ├── database.py                    # DB engine/session creation
|   ├── load_data.py                   # Load all CSVs into the database
│   ├── models.py                      # ORM models
│   ├── restore_data.py                # Restore dispatcher for all tables
│   └── schemas.py                     # Pydantic schemas
├── data/                              # Historical CSV files
├── drivers/                           # JDBC drivers (SQLite)
├── backups/                           # Generated AVRO backup files
├── utils/                             # Utility scripts
│   └── clean_data.py                  # Script to delete all data from DB
├── .gitignore                         # Git ignore file
├── Dockerfile                         # Docker image definition
├── main.py                            # FastAPI entry point
├── Makefile                           # Automation of common tasks
├── README.md                          # Project documentation
└── requirements.txt                   # Python dependencies

```

---

## ⚙️ Setup Instructions

### 📦 1. Clone the Repository

```bash
git clone git@github.com:angie1590/data_migration_api.git
cd data_migration_api
```

### 🐍 2. Create Virtual Environment (Optional if not using Docker)
> You must have installed python 3.10+. Also the library lmaz (brew install xy) and JAVA 11+
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔧 Installing `make` on the Local Environment (Windows/Mac) (Must)
> Required to run `Makefile` commands
```bash
# Windows (con Chocolatey)
choco install make

# Mac
brew install make
```

---

## 🐳 Docker Deployment (Recommended)

>The system is fully dockerized and ready for deployment.

### 🔧 1. Build the Docker Image

```bash
make docker-build
```

### ▶️ 2. Run the API Container

```bash
make docker-run
```
Now the API is available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### ▶️ 3. Open a container shell

```bash
make docker-run-shell
```

---

## 📂 Load Historical Data

### ➕ From the Host:

```bash
make load-historical-data
```

### ➕ From Docker:

```bash
make docker-load-historical
```

---

## 💾 Backup & Restore (AVRO Format)
> You can backup and restore the three tables: departments, jobs, hired_employees. It is possible to do those process for all of them.

### 🔐 Backup from Host:

```bash
make backup TABLE=departments
```

### 🔐 Backup from Docker:

```bash
make docker-backup departments
```

### 🔐 Backup all tables from Docker:

```bash
make docker-backup-all
```

### ♻️ Restore from Host:

```bash
make restore TABLE=departments
```

### ♻️ Restore from Docker:

```bash
make docker-restore TABLE=departments
```

### ♻️ Restore all tables from Docker:

```bash
make docker-restore-all
```

---
## 📊 Streamlit Dashboard

> Visual interface to analyze hiring reports using PySpark and SQLite.

### 🚀 Launch Dashboard from Host:
```bash
make dashboard-create
```

### 🚀 Launch Dashboard from Host:
```bash
make docker-dashboard
```
> The dashboard will be available at: http://localhost:8501
---

## 🧪 Clean the Database

### Clean Data from Docker:

```bash
make docker-clean
```

## 🛠 Inspecting the SQLite Database inside the Docker Container
To inspect the SQLite database that runs inside the container, a utility Make command is provided:
```bash
make docker-inspect-db
```
This will:

1. Launch an interactive bash shell inside the data-migration-api container.

2. Open the app.db SQLite file using the sqlite3 command-line interface.
### 📌 Requirements:
- The container must be running.

## 🧪 Generate Batch Data for Testing
> Use this utility to generate realistic test data in .json format for API batch insertions. It includes departments, jobs, and hired_employees.
### 🔧 From Host:
```bash
make create-bash-files
```

### 🐳 From Docker:
```bash
make docker-create-bash-files
```
> The files will be saved in the folder utils.
---

## ✅ API Endpoints Summary

Visit the Swagger UI for testing endpoints:
[http://localhost:8000/docs](http://localhost:8000/docs)

## API - Data Ingestion

The system also exposes endpoints to insert data either individually or in batch mode into the following tables:

### Insert Individual Records

- **POST /departments**
  - Insert a new department.
  - Body JSON:
    ```json
    {
      "id": 1,
      "department": "Marketing"
    }
    ```

- **POST /jobs**
  - Insert a new job.
  - Body JSON:
    ```json
    {
      "id": 1,
      "job": "Data Engineer"
    }
    ```

- **POST /hired_employees**
  - Insert a new hired employee.
  - Body JSON:
    ```json
    {
      "id": 1,
      "name": "Jane Doe",
      "datetime": "2021-07-01T00:00:00",
      "department_id": 1,
      "job_id": 1
    }
    ```

### Insert Data in batches

- **POST /departments/batch**
  - Insert multiple departments.
  - Body JSON:
    ```json
    [
      {"id": 1, "department": "Marketing"},
      {"id": 2, "department": "Engineering"}
    ]
    ```

- **POST /jobs/batch**
  - Insert multiple jobs.
  - Body JSON:
    ```json
    [
      {"id": 1, "job": "Data Engineer"},
      {"id": 2, "job": "Backend Developer"}
    ]
    ```

- **POST /hired_employees/batch**
  - Insert multiple hired employees.
  - Body JSON:
    ```json
    [
      {
        "id": 1,
        "name": "Jane Doe",
        "datetime": "2021-07-01T00:00:00",
        "department_id": 1,
        "job_id": 1
      },
      {
        "id": 2,
        "name": "John Smith",
        "datetime": "2021-08-01T00:00:00",
        "department_id": 2,
        "job_id": 2
      }
    ]
    ```
### 📈 Hiring Reports API

The system provides two main report endpoints backed by PySpark logic and available via FastAPI.

#### `GET /reports/hiring-quarterly`
Returns the number of employees hired per department and job per quarter (Q1–Q4) for the year 2021.

- Response Format: JSON
- Columns: department, job, Q1, Q2, Q3, Q4

#### `GET /reports/hiring-above-average`
Returns the departments that hired more employees than the average in 2021.

- Response Format: JSON
- Columns: department_id, department, hired_count

You can test both endpoints using the interactive Swagger interface:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Security Considerations

- Codebase scoped to internal POC use
- Run inside Docker to prevent local pollution
- No public endpoints without container isolation

---

## 📄 License

This project is provided for demonstration purposes only.
