# Data Migration API

This is a Proof of Concept (PoC) API built with FastAPI to support a large-scale data migration pipeline. It enables loading historical data from CSV files, managing data via REST endpoints, and backing up or restoring table contents in AVRO format.

---

## 🚀 Features

- Load historic data from CSV files into a SQL database
- Receive and validate new data via REST endpoints
- Single and batch transaction support (1 to 1000 rows)
- AVRO export of each table's data
- Table restoration from AVRO backups
- Docker-ready and deployable in isolated environments

---

## 📁 Project Structure

```
├── app/
│   ├── core/                          # Logging and configuration
│   │   └── logger.py                  # Logger configuration
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
│   ├── routers/                       # FastAPI endpoints
|   ├── backup_data.py                 # Backup dispatcher for all tables
│   ├── database.py                    # DB engine/session creation
|   ├── load_data.py                   # Load all CSVs into the database
│   ├── models.py                      # ORM models
│   ├── restore_data.py                # Restore dispatcher for all tables
│   └── schemas.py                     # Pydantic schemas
├── data/                              # Historical CSV files
├── backups/                           # Generated AVRO backup files
├── utils/                             # Utility scripts
│   └── clean_data.py                  # Script to delete all data from DB
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
> En estos casos es necesario tener instalado python 3.10 o superior. Además instalar la librería lmaz (brew install xy)
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

### ▶️ 3. Open a container shell

```bash
make docker-run-shell
```

Now the API is available at: [http://localhost:8000/docs](http://localhost:8000/docs)

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
---

## ✅ API Endpoints Summary

Visit the Swagger UI for testing endpoints:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Security Considerations

- Codebase scoped to internal POC use
- Run inside Docker to prevent local pollution
- No public endpoints without container isolation

---

## 📄 License

This project is provided for demonstration purposes only.
