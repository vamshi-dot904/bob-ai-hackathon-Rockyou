"""
Generates two CSV files from mule_l2_data.py:
  - mule_l2_profiles.csv          (25 L2 mule account holder details)
  - mule_l2_to_kingpin_splits.csv (125 split transactions → pre-kingpin accounts)
Run: py generate_mule_l2_csv.py
"""

import csv
from mule_l2_data import L2_MULE_PROFILES, L2_TO_KINGPIN_SPLITS

# ── L2 MULE PROFILES ─────────────────────────────────────────────────────────
PROFILE_FIELDS = [
    "mule_id", "holder_name", "phone", "upi_id",
    "bank", "bank_account", "city", "state",
    "received_from_mule", "amount_received", "received_at",
]

with open("mule_l2_profiles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=PROFILE_FIELDS)
    writer.writeheader()
    for row in L2_MULE_PROFILES:
        writer.writerow({k: row[k] for k in PROFILE_FIELDS})

print("OK mule_l2_profiles.csv created  (25 rows)")

# ── L2 → KINGPIN SPLIT TRANSACTIONS ──────────────────────────────────────────
SPLIT_FIELDS = [
    "split_txn_id", "from_mule", "from_holder",
    "to_account", "to_holder", "to_city", "to_state",
    "amount", "split_time", "seconds_after_receipt", "final_destination",
]

with open("mule_l2_to_kingpin_splits.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=SPLIT_FIELDS)
    writer.writeheader()
    for row in L2_TO_KINGPIN_SPLITS:
        writer.writerow({k: row[k] for k in SPLIT_FIELDS})

print(f"OK mule_l2_to_kingpin_splits.csv created  ({len(L2_TO_KINGPIN_SPLITS)} rows)")
