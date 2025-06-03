import json
import random
from datetime import datetime, timedelta

TOTAL = 1000

departments = [
    {
        "id": i,
        "department": f"Department {i}"
    }
    for i in range(1, TOTAL + 1)
]

jobs = [
    {
        "id": i,
        "job": f"Job {i}"
    }
    for i in range(1, TOTAL + 1)
]

records = []
base_date = datetime(2021, 1, 1)
for i in range(1, 1001):
    record = {
        "id": i,
        "name": f"Employee {i}",
        "datetime": (base_date + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%dT%H:%M:%S"),
        "department_id": random.randint(1, 10),
        "job_id": random.randint(1, 10)
    }
    records.append(record)

with open("departments_batch_1000.json", "w") as f:
    json.dump(departments, f, indent=2)

with open("jobs_batch_1000.json", "w") as f:
    json.dump(jobs, f, indent=2)

with open("hired_employees_batch_1000.json", "w") as f:
    json.dump(records, f, indent=2)

print("✅ Archivos generados:")
print("- departments_batch_1000.json")
print("- jobs_batch_1000.json")
print("- hired_employees_batch_1000.json")
