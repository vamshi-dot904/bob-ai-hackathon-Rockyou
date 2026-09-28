"""
test_correlation.py
--------------------
Run correlation for all 5 victims and print a clean summary.
Run: py test_correlation.py
"""

import json
from correlation_engine import correlate

SUBMISSIONS = [
    {"phone_number": "9876543210", "imei": "354678901234567", "amount_debited": 85000,  "city": "Patna"},
    {"phone_number": "9123456780", "imei": "357891234567890", "amount_debited": 120000, "city": "Ranchi"},
    {"phone_number": "9988776655", "imei": "352345678901234", "amount_debited": 67500,  "city": "Dhanbad"},
    {"phone_number": "9765432109", "imei": "356789012345678", "amount_debited": 95000,  "city": "Bokaro"},
    {"phone_number": "9654321098", "imei": "351234567890123", "amount_debited": 53000,  "city": "Gaya"},
]

for sub in SUBMISSIONS:
    result = correlate(sub)

    v  = result["victim_identity"]
    sw = result["sim_swap"]
    tx = result["transaction"]
    l1 = result["l1_mule"]
    kp = result["kingpin"]
    pt = result["fraud_pattern"]

    print("=" * 70)
    print(f"  VICTIM   : {v['victim_name']}  |  Phone: {v['phone']}")
    print(f"  CITY     : {v['home_city']}, {v['home_state']}")
    print(f"  SIM SWAP : {sw['status']}  |  Criminal IMEI: {sw.get('criminal_imei')}")
    print(f"             Swap city: {sw.get('swap_city')}  |  Distance: {sw.get('distance_km')} km")
    print(f"             Swap → UPI: {sw.get('seconds_swap_to_upi')} seconds")
    print(f"  UPI      : {result['upi_access']['status']}")
    print(f"             Access city: {result['upi_access'].get('access_city')}  |  IP: {result['upi_access'].get('access_ip')}")
    print(f"  TXN      : {tx['status']}  |  Amount: Rs.{tx.get('amount_debited'):,}  |  Match: {tx.get('amount_match')}")
    print(f"             Receiver: {tx.get('receiver_account')}")
    print(f"  L1 MULE  : {l1.get('holder_name')}  ({l1.get('city')})  |  Recruited by: {l1.get('recruited_by')}")
    print(f"             L2 splits: {len(l1.get('l2_splits', []))} accounts in {len(set(s['to_city'] for s in l1.get('l2_splits',[])))  } cities")
    print(f"  KINGPIN  : {kp.get('name')} ({kp.get('alias')})  |  A/C: {kp.get('bank_account')}")
    print(f"             Total ring amount: Rs.{kp.get('total_amount_in_ring'):,}  |  Op time: {kp.get('ring_operation_mins')} min")
    print(f"  PATTERN  : {pt['pattern']}")
    print(f"  RISK     : {pt['risk_score']}/100  |  Flags: {', '.join(pt['flags'])}")
    print(f"  TIMELINE : {len(result['evidence_timeline'])} events recorded")
    print()
