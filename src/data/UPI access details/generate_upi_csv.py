"""
Generates two CSV files from upi_access_data.py:
  - upi_access_logs.csv       (who accessed UPI, when, from where)
  - upi_transactions.csv      (money debit from victim to mule)
Run: py generate_upi_csv.py
"""

import csv
from upi_access_data import UPI_ACCESS_LOGS, UPI_TRANSACTIONS

# ── UPI ACCESS LOGS ───────────────────────────────────────────────────────────
ACCESS_FIELDS = [
    "access_id",
    "victim_name",
    "phone_number",
    "upi_id",
    "bank_name",
    "bank_account",
    "access_time",
    "access_city",
    "access_state",
    "access_ip",
    "device_imei",
    "access_type",
    "otp_delivered_to",
    "login_success",
    "seconds_after_swap",
]

with open("upi_access_logs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=ACCESS_FIELDS)
    writer.writeheader()
    for row in UPI_ACCESS_LOGS:
        writer.writerow({k: row[k] for k in ACCESS_FIELDS})

print("OK upi_access_logs.csv created")

# ── UPI TRANSACTIONS ──────────────────────────────────────────────────────────
TXN_FIELDS = [
    "txn_id",
    "victim_name",
    "phone_number",
    "upi_id",
    "bank_account",
    "amount_debited",
    "currency",
    "txn_time",
    "txn_city",
    "txn_state",
    "receiver_upi",
    "receiver_account",
    "txn_status",
    "seconds_after_access",
]

with open("upi_transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=TXN_FIELDS)
    writer.writeheader()
    for row in UPI_TRANSACTIONS:
        writer.writerow({k: row[k] for k in TXN_FIELDS})

print("OK upi_transactions.csv created")
