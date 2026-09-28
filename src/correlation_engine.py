"""
correlation_engine.py
----------------------
Core logic for correlating a user's fraud complaint submission
against all available investigation data layers.

Input  : victim submission dict (phone, imei, bank_account, amount, time, city)
Output : CorrelationResult with evidence, mule chain, pattern, risk score
"""

import csv
import os
from datetime import datetime, timedelta

# ── PATH RESOLVER ─────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

def _csv(folder, filename):
    return os.path.join(BASE, folder, filename)

# ── CSV LOADERS ───────────────────────────────────────────────────────────────
def _load(folder, filename):
    path = _csv(folder, filename)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_all_data():
    return {
        "before_swap":       _load("Device details",      "device_records_before_swap.csv"),
        "after_swap":        _load("Device details",      "device_records_after_swap.csv"),
        "upi_access":        _load("UPI access details",  "upi_access_logs.csv"),
        "upi_txn":           _load("UPI access details",  "upi_transactions.csv"),
        "l1_profiles":       _load("1st mule account",    "mule_l1_profiles.csv"),
        "l1_splits":         _load("1st mule account",    "mule_l1_to_l2_splits.csv"),
        "l2_profiles":       _load("2nd mule account",    "mule_l2_profiles.csv"),
        "l2_splits":         _load("2nd mule account",    "mule_l2_to_kingpin_splits.csv"),
        "kingpin_profile":   _load("kingpin account",     "kingpin_profile.csv"),
        "kingpin_inflow":    _load("kingpin account",     "kingpin_inflow_transfers.csv"),
        "kingpin_summary":   _load("kingpin account",     "kingpin_account_summary.csv"),
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — VICTIM IDENTITY CHECK
# Match submitted phone against device_records_before_swap
# ─────────────────────────────────────────────────────────────────────────────
def check_victim_identity(submission, data):
    phone = submission["phone_number"].strip()
    match = next((r for r in data["before_swap"] if r["phone_number"] == phone), None)

    if not match:
        return {"status": "NOT_FOUND", "detail": f"Phone {phone} not in device records"}

    return {
        "status":       "MATCHED",
        "victim_name":  match["victim_name"],
        "phone":        phone,
        "original_imei":match["imei"],
        "sim_provider": match["sim_provider"],
        "home_city":    match["city"],
        "home_state":   match["state"],
        "tower_id":     match["tower_id"],
        "last_legit_active": match["last_active"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — SIM SWAP DETECTION
# Same phone → different IMEI in after_swap records
# ─────────────────────────────────────────────────────────────────────────────
def detect_sim_swap(submission, data, identity):
    phone = submission["phone_number"].strip()
    swap  = next((r for r in data["after_swap"] if r["phone_number"] == phone), None)

    if not swap:
        return {"status": "NO_SWAP_DETECTED"}

    original_imei   = identity.get("original_imei", "")
    criminal_imei   = swap["imei"]
    imei_changed    = original_imei != criminal_imei

    # Victim-submitted IMEI should match original, not criminal
    submitted_imei  = submission.get("imei", "").strip()
    victim_imei_ok  = (submitted_imei == original_imei) if submitted_imei else None

    return {
        "status":           "SIM_SWAP_CONFIRMED" if imei_changed else "NO_CHANGE",
        "original_imei":    original_imei,
        "criminal_imei":    criminal_imei,
        "imei_changed":     imei_changed,
        "swap_city":        swap["city"],             # Jamtara
        "swap_state":       swap["state"],
        "swap_tower":       swap["tower_id"],
        "swap_timestamp":   swap["swap_timestamp"],
        "first_upi_access": swap["first_upi_access"],
        "previous_city":    swap["previous_city"],
        "distance_km":      swap["distance_km"],
        "impossible_travel":True,                    # same second, different city
        "victim_imei_verified": victim_imei_ok,
        "seconds_swap_to_upi": _sec_diff(
            swap["swap_timestamp"], swap["first_upi_access"]
        ),
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — UPI ACCESS CORRELATION
# Confirm unauthorized UPI login from criminal's device
# ─────────────────────────────────────────────────────────────────────────────
def correlate_upi_access(submission, data):
    phone = submission["phone_number"].strip()
    log   = next((r for r in data["upi_access"] if r["phone_number"] == phone), None)

    if not log:
        return {"status": "NO_UPI_ACCESS_RECORD"}

    return {
        "status":               "UNAUTHORIZED_ACCESS_CONFIRMED",
        "upi_id":               log["upi_id"],
        "bank_name":            log["bank_name"],
        "bank_account":         log["bank_account"],
        "access_time":          log["access_time"],
        "access_city":          log["access_city"],        # Jamtara
        "access_ip":            log["access_ip"],
        "criminal_imei":        log["device_imei"],
        "access_type":          log["access_type"],        # OTP_LOGIN
        "otp_hijacked_to":      log["otp_delivered_to"],   # victim's number → criminal's SIM
        "seconds_after_swap":   int(log["seconds_after_swap"]),
        "automated_attack":     int(log["seconds_after_swap"]) < 120,
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — TRANSACTION VERIFICATION
# Confirm debit amount and identify receiving mule
# ─────────────────────────────────────────────────────────────────────────────
def verify_transaction(submission, data):
    phone  = submission["phone_number"].strip()
    txn    = next((r for r in data["upi_txn"] if r["phone_number"] == phone), None)

    if not txn:
        return {"status": "NO_TRANSACTION_RECORD"}

    submitted_amount = int(submission.get("amount_debited", 0))
    actual_amount    = int(txn["amount_debited"])
    amount_match     = (submitted_amount == actual_amount) if submitted_amount else None

    return {
        "status":           "TRANSACTION_CONFIRMED",
        "txn_id":           txn["txn_id"],
        "upi_id":           txn["upi_id"],
        "amount_debited":   actual_amount,
        "amount_match":     amount_match,
        "txn_time":         txn["txn_time"],
        "txn_city":         txn["txn_city"],
        "receiver_upi":     txn["receiver_upi"],
        "receiver_account": txn["receiver_account"],   # MULE-L1-XXXX
        "txn_status":       txn["txn_status"],
        "seconds_after_upi_access": int(txn.get("seconds_after_access", 0)),
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — L1 MULE CHAIN TRACE
# Identify L1 mule and all 5 L2 accounts it split money into
# ─────────────────────────────────────────────────────────────────────────────
def trace_l1_mule(txn_result, data):
    mule_id = txn_result.get("receiver_account", "")
    profile = next((r for r in data["l1_profiles"] if r["mule_id"] == mule_id), None)

    if not profile:
        return {"status": "L1_MULE_NOT_FOUND"}

    splits = [r for r in data["l1_splits"] if r["from_mule"] == mule_id]

    return {
        "status":           "L1_MULE_IDENTIFIED",
        "mule_id":          profile["mule_id"],
        "holder_name":      profile["holder_name"],
        "phone":            profile["phone_number"],
        "upi_id":           profile["upi_id"],
        "bank_name":        profile["bank_name"],
        "bank_account":     profile["bank_account"],
        "city":             profile["city"],
        "state":            profile["state"],
        "recruited_by":     profile.get("recruited_by", "KINGPIN-001"),
        "amount_received":  int(profile["amount_received"]),
        "l2_splits": [
            {
                "split_txn_id":   s["split_txn_id"],
                "to_account":     s["to_account"],
                "to_holder":      s["to_holder"],
                "to_city":        s["to_city"],
                "amount":         int(s["amount"]),
                "split_time":     s["split_time"],
                "seconds_after_receipt": int(s["seconds_after_receipt"]),
            }
            for s in splits
        ],
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — L2 MULE CHAIN TRACE
# For each L2 account from L1 splits, get profile + pre-KP splits
# ─────────────────────────────────────────────────────────────────────────────
def trace_l2_mules(l1_result, data):
    l2_mule_ids = [s["to_account"] for s in l1_result.get("l2_splits", [])]
    results = []

    for mule_id in l2_mule_ids:
        profile = next((r for r in data["l2_profiles"] if r["mule_id"] == mule_id), None)
        splits  = [r for r in data["l2_splits"] if r["from_mule"] == mule_id]

        if profile:
            results.append({
                "mule_id":        profile["mule_id"],
                "holder_name":    profile["holder_name"],
                "phone":          profile["phone"],
                "city":           profile["city"],
                "bank":           profile["bank"],
                "amount_received":int(profile["amount_received"]),
                "received_at":    profile["received_at"],
                "pre_kp_splits": [
                    {
                        "to_account":  s["to_account"],
                        "to_city":     s["to_city"],
                        "amount":      int(s["amount"]),
                        "split_time":  s["split_time"],
                        "destination": s["final_destination"],
                    }
                    for s in splits
                ],
            })

    return {
        "status":      "L2_MULES_TRACED",
        "total_l2":    len(results),
        "l2_mules":    results,
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — KINGPIN LINKAGE
# Confirm all money flows to KINGPIN-001
# ─────────────────────────────────────────────────────────────────────────────
def link_to_kingpin(l1_result, data):
    mule_id   = l1_result.get("mule_id", "")
    # find all kingpin inflows that originated from this L1's L2 mules
    inflows   = [r for r in data["kingpin_inflow"] if mule_id[:10] in r.get("originated_from_l2","")]
    kingpin   = data["kingpin_profile"][0] if data["kingpin_profile"] else {}
    summary   = data["kingpin_summary"][0]  if data["kingpin_summary"]  else {}

    return {
        "status":               "KINGPIN_LINKED",
        "kingpin_id":           kingpin.get("kingpin_id"),
        "name":                 kingpin.get("name"),
        "alias":                kingpin.get("alias"),
        "phone":                kingpin.get("phone"),
        "upi_id":               kingpin.get("upi_id"),
        "bank_name":            kingpin.get("bank_name"),
        "bank_account":         kingpin.get("bank_account"),
        "city":                 kingpin.get("city"),
        "total_victims_in_ring":int(kingpin.get("total_victims", 0)),
        "total_amount_in_ring": int(summary.get("total_amount_received", 0)),
        "ring_operation_mins":  summary.get("operation_duration_minutes"),
        "inflow_count_from_this_case": len(inflows),
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — FRAUD PATTERN CLASSIFIER
# ─────────────────────────────────────────────────────────────────────────────
def classify_fraud_pattern(swap, upi_access, txn, l1):
    flags = []
    score = 0

    if swap.get("status") == "SIM_SWAP_CONFIRMED":
        flags.append("SIM_SWAP_DETECTED")
        score += 30

    if swap.get("impossible_travel"):
        flags.append("IMPOSSIBLE_LOCATION_JUMP")
        score += 20

    if upi_access.get("automated_attack"):
        flags.append("AUTOMATED_UPI_ACCESS_UNDER_120S")
        score += 20

    if txn.get("status") == "TRANSACTION_CONFIRMED":
        flags.append("FRAUDULENT_DEBIT_CONFIRMED")
        score += 15

    if len(l1.get("l2_splits", [])) >= 5:
        flags.append("LAYERED_MULE_SPLITTING_DETECTED")
        score += 15

    pattern = "UNKNOWN"
    if score >= 80:
        pattern = "SIM_SWAP_UPI_LAYERED_MULE — ORGANISED_GANG"
    elif score >= 50:
        pattern = "SIM_SWAP_UPI_FRAUD — PARTIAL_EVIDENCE"
    elif score >= 30:
        pattern = "POSSIBLE_UPI_FRAUD — NEEDS_INVESTIGATION"

    return {
        "pattern":      pattern,
        "risk_score":   score,
        "max_score":    100,
        "flags":        flags,
        "gang_involved": score >= 80,
    }

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — EVIDENCE TIMELINE BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def build_timeline(swap, upi_access, txn, l1):
    events = []

    if swap.get("swap_timestamp"):
        events.append({"time": swap["swap_timestamp"],   "event": "SIM SWAP activated on criminal device",        "city": swap.get("swap_city","Jamtara")})
    if swap.get("first_upi_access"):
        events.append({"time": swap["first_upi_access"], "event": f"UPI login via OTP (intercepted) — {swap.get('seconds_swap_to_upi')}s after swap", "city": swap.get("swap_city","Jamtara")})
    if upi_access.get("access_time"):
        events.append({"time": upi_access["access_time"],"event": f"Unauthorized UPI access from IP {upi_access.get('access_ip')}", "city": upi_access.get("access_city","Jamtara")})
    if txn.get("txn_time"):
        events.append({"time": txn["txn_time"],          "event": f"₹{txn.get('amount_debited'):,} debited to {txn.get('receiver_account')}",       "city": txn.get("txn_city","Jamtara")})
    for split in l1.get("l2_splits", []):
        events.append({"time": split["split_time"],      "event": f"₹{split['amount']:,} split to {split['to_account']} ({split['to_holder']}) in {split['to_city']}", "city": split["to_city"]})

    events.sort(key=lambda x: x["time"])
    return events

# ─────────────────────────────────────────────────────────────────────────────
# MASTER CORRELATE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def correlate(submission: dict) -> dict:
    """
    Main entry point.
    submission = {
        "phone_number":  "9876543210",
        "imei":          "354678901234567",   # optional
        "bank_account":  "9140056789123",     # optional
        "amount_debited": 85000,              # optional
        "city":          "Patna",             # optional
    }
    Returns a full CorrelationResult dict.
    """
    data = load_all_data()

    # Run all steps
    identity    = check_victim_identity(submission, data)
    if identity["status"] == "NOT_FOUND":
        return {"status": "NO_MATCH", "detail": identity["detail"]}

    swap        = detect_sim_swap(submission, data, identity)
    upi_access  = correlate_upi_access(submission, data)
    txn         = verify_transaction(submission, data)
    l1          = trace_l1_mule(txn, data) if txn.get("receiver_account") else {}
    l2          = trace_l2_mules(l1, data) if l1.get("l2_splits") else {}
    kingpin     = link_to_kingpin(l1, data) if l1.get("mule_id") else {}
    pattern     = classify_fraud_pattern(swap, upi_access, txn, l1)
    timeline    = build_timeline(swap, upi_access, txn, l1)

    return {
        "status":           "CORRELATION_COMPLETE",
        "victim_identity":  identity,
        "sim_swap":         swap,
        "upi_access":       upi_access,
        "transaction":      txn,
        "l1_mule":          l1,
        "l2_mules":         l2,
        "kingpin":          kingpin,
        "fraud_pattern":    pattern,
        "evidence_timeline":timeline,
    }

# ── HELPER ────────────────────────────────────────────────────────────────────
def _sec_diff(t1_str, t2_str):
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        return int((datetime.strptime(t2_str, fmt) - datetime.strptime(t1_str, fmt)).total_seconds())
    except Exception:
        return None
