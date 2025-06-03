import json

type = "job"

records = [
    {
        "id": i,
        type: f"{type.capitalize()} {i}"
    }
    for i in range(1, 1001)
]

filename = f"{type}_batch_1000.json"

with open(filename, "w") as f:
    json.dump(records, f, indent=2)

print(f"Archivo generado: {filename}")