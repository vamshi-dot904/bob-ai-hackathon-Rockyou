"""
Generates three CSV files from kingpin_data.py:
  - kingpin_profile.csv             (1 row — kingpin identity)
  - kingpin_inflow_transfers.csv    (125 rows — all money arriving at kingpin)
  - kingpin_account_summary.csv     (1 row — total aggregation stats)
Run: py generate_kingpin_csv.py
"""

import csv
from kingpin_data import KINGPIN_PROFILE, KINGPIN_INFLOW_TRANSFERS, KINGPIN_ACCOUNT_SUMMARY

# ── KINGPIN PROFILE ───────────────────────────────────────────────────────────
PROFILE_FIELDS = [
    "kingpin_id", "name", "alias", "phone", "upi_id",
    "bank_name", "bank_account", "ifsc", "city", "state", "role",
    "total_accounts_controlled", "total_l1_mules", "total_l2_mules", "total_victims",
]

with open("kingpin_profile.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=PROFILE_FIELDS)
    writer.writeheader()
    writer.writerow({k: KINGPIN_PROFILE[k] for k in PROFILE_FIELDS})

print("OK kingpin_profile.csv created  (1 row)")

# ── KINGPIN INFLOW TRANSFERS ──────────────────────────────────────────────────
INFLOW_FIELDS = [
    "transfer_id", "from_account", "from_holder", "from_city", "from_state",
    "originated_from_l2", "to_kingpin_id", "to_name", "to_upi",
    "to_bank_account", "to_bank", "amount", "currency",
    "transfer_time", "seconds_after_l2_receipt", "transfer_status", "transfer_method",
]

with open("kingpin_inflow_transfers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=INFLOW_FIELDS)
    writer.writeheader()
    for row in KINGPIN_INFLOW_TRANSFERS:
        writer.writerow({k: row[k] for k in INFLOW_FIELDS})

print(f"OK kingpin_inflow_transfers.csv created  ({len(KINGPIN_INFLOW_TRANSFERS)} rows)")

# ── KINGPIN ACCOUNT SUMMARY ───────────────────────────────────────────────────
SUMMARY_FIELDS = [
    "kingpin_id", "name", "bank_account", "bank_name",
    "total_inflow_txns", "total_amount_received",
    "first_credit_at", "last_credit_at",
    "total_victims", "total_l1_mules", "total_l2_mules", "total_pre_kp_accounts",
    "fraud_pattern", "operation_duration_minutes",
]

with open("kingpin_account_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
    writer.writeheader()
    writer.writerow({k: KINGPIN_ACCOUNT_SUMMARY[k] for k in SUMMARY_FIELDS})

print("OK kingpin_account_summary.csv created  (1 row)")
print()
print("--- KINGPIN ACCOUNT SUMMARY ---")
for k, v in KINGPIN_ACCOUNT_SUMMARY.items():
    print(f"  {k:<35}: {v}")
