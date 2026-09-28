"""
Generates two CSV files from device_records.py:
  - device_records_before_swap.csv
  - device_records_after_swap.csv
Run: py generate_device_csv.py
"""

import csv
from device_records import DEVICE_RECORDS_BEFORE, DEVICE_RECORDS_AFTER

# ── BEFORE SWAP ──────────────────────────────────────────────────────────────
BEFORE_FIELDS = [
    "record_id",
    "victim_name",
    "phone_number",
    "imei",
    "sim_provider",
    "city",
    "state",
    "tower_id",
    "last_active",
    "status",
]

with open("device_records_before_swap.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=BEFORE_FIELDS)
    writer.writeheader()
    for row in DEVICE_RECORDS_BEFORE:
        writer.writerow({k: row[k] for k in BEFORE_FIELDS})

print("OK device_records_before_swap.csv created")

# ── AFTER SWAP ───────────────────────────────────────────────────────────────
AFTER_FIELDS = [
    "record_id",
    "victim_name",
    "phone_number",
    "imei",
    "sim_provider",
    "city",
    "state",
    "tower_id",
    "swap_timestamp",
    "first_upi_access",
    "status",
    "previous_city",
    "distance_km",
]

with open("device_records_after_swap.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=AFTER_FIELDS)
    writer.writeheader()
    for row in DEVICE_RECORDS_AFTER:
        writer.writerow({k: row[k] for k in AFTER_FIELDS})

print("OK device_records_after_swap.csv created")
