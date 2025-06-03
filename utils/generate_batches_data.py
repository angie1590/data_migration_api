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

def random_date_2021():
    start = datetime(2021, 1, 1)
    end = datetime(2021, 12, 31)
    return (start + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")

hired_employees = [
    {
        "id": i,
        "name": f"Employee {i}",
        "datetime": random_date_2021(),
        "department_id": random.randint(1, TOTAL),
        "job_id": random.randint(1, TOTAL)
    }
    for i in range(1, TOTAL + 1)
]

with open("departments_batch_1000.json", "w") as f:
    json.dump(departments, f, indent=2)

with open("jobs_batch_1000.json", "w") as f:
    json.dump(jobs, f, indent=2)

with open("hired_employees_batch_1000.json", "w") as f:
    json.dump(hired_employees, f, indent=2)

print("✅ Archivos generados:")
print("- departments_batch_1000.json")
print("- jobs_batch_1000.json")
print("- hired_employees_batch_1000.json")
