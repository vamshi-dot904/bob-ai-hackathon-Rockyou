"""
Generates two CSV files from mule_l1_data.py:
  - mule_l1_profiles.csv       (L1 mule account holder details)
  - mule_l1_to_l2_splits.csv   (split transactions from L1 to L2 mules)
Run: py generate_mule_l1_csv.py
"""

import csv
from mule_l1_data import L1_MULE_PROFILES, L1_TO_L2_SPLITS

# ── L1 MULE PROFILES ─────────────────────────────────────────────────────────
PROFILE_FIELDS = [
    "mule_id", "holder_name", "phone_number", "upi_id",
    "bank_name", "bank_account", "city", "state", "role",
    "recruited_by", "amount_received", "received_from", "received_at",
]

with open("mule_l1_profiles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=PROFILE_FIELDS)
    writer.writeheader()
    for row in L1_MULE_PROFILES:
        writer.writerow({k: row[k] for k in PROFILE_FIELDS})

print("OK mule_l1_profiles.csv created")

# ── L1 → L2 SPLIT TRANSACTIONS ───────────────────────────────────────────────
SPLIT_FIELDS = [
    "split_txn_id", "from_mule", "from_holder",
    "to_account", "to_holder", "to_city", "to_state",
    "amount", "split_time", "seconds_after_receipt",
]

with open("mule_l1_to_l2_splits.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=SPLIT_FIELDS)
    writer.writeheader()
    for row in L1_TO_L2_SPLITS:
        writer.writerow({k: row[k] for k in SPLIT_FIELDS})

print("OK mule_l1_to_l2_splits.csv created")
