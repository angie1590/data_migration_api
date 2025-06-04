# Data Migration with PySpark and MongoDB

Este módulo es una solución de procesamiento ETL desarrollada con **PySpark** y **MongoDB** como alternativa al sistema basado en SQLite. Está optimizada para ser escalable, robusta y fácilmente mantenible, cumpliendo los requisitos de un desafío técnico.

## 📁 Estructura del Proyecto

```
data_migration_spark_mongo/
│
├── config/                  # Configuración general (SparkSession, Logger)
│   ├── logger_config.py     # Configuración del sistema de logging
│   └── spark_config.py      # Inicialización del SparkSession
│
│
├── etl/                     # Módulos ETL independientes
│   ├── load_departments.py
│   ├── load_jobs.py
│   ├── load_hired_employees.py
│   ├── run_etl.py           # Orquestador principal
│   ├── backup_avro.py       # Respaldo en formato Avro
│   └── restore_from_backup.py # Restauración desde el último backup
│
├── schemas/
│   └── validations.py       # Validaciones y limpieza de datos
│
├── backups/                 # Respaldos generados (nombre_fecha-hora.avro)
│
└── api/                     # FastAPI para inserción de datos
    └── main.py              # Servidor FastAPI corriendo en puerto 8005
```

## 🛠️ Requisitos

- Python 3.10+
- PySpark 3.5.1
- MongoDB local corriendo en `localhost:27017`
- Paquetes de Python: ver `requirements.txt`

## ▶️ Ejecución

### Activar entorno virtual

```bash
source venv-optimized/bin/activate
pip install -r requirements.txt
```

### Correr ETL completo

```bash
python3 -m etl.run_etl
```

### Crear respaldo (formato Avro)

```bash
python3 -m etl.backup_avro
```

### Restaurar desde último backup

```bash
python3 -m etl.restore_from_backup
```

## 🌐 API (FastAPI)

El servidor corre en `http://localhost:8005` y expone endpoints para insertar datos:

- `POST /departments/` — Inserta un solo departamento
- `POST /departments/batch/` — Inserta hasta 1000 en batch
- `POST /jobs/`
- `POST /jobs/batch/`
- `POST /hired_employees/`
- `POST /hired_employees/batch/`

## 📦 Ejemplo de inserción vía API

```bash
curl -X POST http://localhost:8005/departments/ \
     -H "Content-Type: application/json" \
     -d '{"id": 101, "department": "Data Engineering"}'
```

## 🧪 Validaciones

- Validación de esquema (tipos y columnas esperadas)
- Verificación de claves foráneas (en empleados)
- Validación de formato de fecha ISO en `hired_employees`
- Registro de logs para cada inserción con detalles

---

🗂️ Proyecto orientado a demostrar capacidades de ingestión robusta, validación y persistencia de datos con herramientas modernas.

