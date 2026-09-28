"""
Kingpin Final Consolidation Data
----------------------------------
125 pre-kingpin accounts (PRE-KP-*) each transfer their balance to
the kingpin's main account (KINGPIN-001 — Santosh Mandal) within 60 seconds
of receiving from L2 mules.

Kingpin's main account aggregates all ₹4,20,500 from 5 victims
through 3 layers of mules across ~15 minutes.

KINGPIN-001 profile:
  Name         : Santosh Mandal
  Phone        : 9700000001
  UPI          : santosh.main@ybl
  Bank         : HDFC Bank (private — opened with fake KYC)
  Account      : 9999000000001
  City         : Jamtara (operates remotely via hawala after aggregation)
"""

import csv
from datetime import datetime, timedelta

# ── READ PRE-KINGPIN SPLITS FROM CSV ─────────────────────────────────────────
PRE_KP_ROWS = []
with open("mule_l2_to_kingpin_splits.csv", newline="", encoding="utf-8") as f:
    PRE_KP_ROWS = list(csv.DictReader(f))

# ── KINGPIN PROFILE ───────────────────────────────────────────────────────────
KINGPIN_PROFILE = {
    "kingpin_id":    "KINGPIN-001",
    "name":          "Santosh Mandal",
    "alias":         "Sanu Bhai",
    "phone":         "9700000001",
    "upi_id":        "santosh.main@ybl",
    "bank_name":     "HDFC Bank",
    "bank_account":  "9999000000001",
    "ifsc":          "HDFC0003421",
    "city":          "Jamtara",
    "state":         "Jharkhand",
    "role":          "KINGPIN",
    "total_accounts_controlled": 125,   # all PRE-KP accounts
    "total_l1_mules":            5,
    "total_l2_mules":            25,
    "total_victims":             5,
}

# ── PRE-KP → KINGPIN TRANSFER RECORDS (125 rows) ─────────────────────────────
# Each PRE-KP account fires its transfer ~60 seconds after receiving from L2.
# Transfer arrives at KINGPIN-001's HDFC account.

KINGPIN_INFLOW_TRANSFERS = []
total_received = 0

for i, row in enumerate(PRE_KP_ROWS):
    pre_kp_recv_time = datetime.strptime(row["split_time"], "%Y-%m-%d %H:%M:%S")
    # pre-kp account transfers to kingpin ~60 sec after receiving
    transfer_time = pre_kp_recv_time + timedelta(seconds=58 + (i % 5))
    amount = int(row["amount"])
    total_received += amount

    KINGPIN_INFLOW_TRANSFERS.append({
        "transfer_id":        f"KP-IN-{str(i+1).zfill(3)}",
        "from_account":       row["to_account"],           # PRE-KP-XXXX
        "from_holder":        row["to_holder"],            # Santosh Net Acc-X
        "from_city":          row["to_city"],
        "from_state":         row["to_state"],
        "originated_from_l2": row["from_mule"],            # trace back to L2
        "to_kingpin_id":      "KINGPIN-001",
        "to_name":            "Santosh Mandal",
        "to_upi":             "santosh.main@ybl",
        "to_bank_account":    "9999000000001",
        "to_bank":            "HDFC Bank",
        "amount":             amount,
        "currency":           "INR",
        "transfer_time":      transfer_time.strftime("%Y-%m-%d %H:%M:%S"),
        "seconds_after_l2_receipt": 58 + (i % 5),
        "transfer_status":    "SUCCESS",
        "transfer_method":    "UPI",
    })

# ── KINGPIN ACCOUNT SUMMARY ───────────────────────────────────────────────────
first_credit = min(r["transfer_time"] for r in KINGPIN_INFLOW_TRANSFERS)
last_credit  = max(r["transfer_time"] for r in KINGPIN_INFLOW_TRANSFERS)

KINGPIN_ACCOUNT_SUMMARY = {
    "kingpin_id":         "KINGPIN-001",
    "name":               "Santosh Mandal",
    "bank_account":       "9999000000001",
    "bank_name":          "HDFC Bank",
    "total_inflow_txns":  len(KINGPIN_INFLOW_TRANSFERS),
    "total_amount_received": total_received,
    "first_credit_at":    first_credit,
    "last_credit_at":     last_credit,
    "total_victims":      5,
    "total_l1_mules":     5,
    "total_l2_mules":     25,
    "total_pre_kp_accounts": 125,
    "fraud_pattern":      "SIM_SWAP_UPI_LAYERED_MULE",
    "operation_duration_minutes": round(
        (datetime.strptime(last_credit, "%Y-%m-%d %H:%M:%S") -
         datetime.strptime(first_credit, "%Y-%m-%d %H:%M:%S")).seconds / 60, 2
    ),
}
