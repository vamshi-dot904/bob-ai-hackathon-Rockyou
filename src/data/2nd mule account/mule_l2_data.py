"""
Level 2 Mule Account Data
--------------------------
25 L2 mule accounts (5 per L1 mule) each split their received amount into 5
sub-accounts (L3 / pre-kingpin accounts) within ~60 seconds of receipt.
All L3 accounts are controlled by the kingpin network (KINGPIN-001).

L2 accounts are spread across Giridih, Deoghar, Dumka, Bokaro, Dhanbad.
L3 accounts are in mixed cities — Hazaribagh, Koderma, Lohardaga,
Chatra, Pakur — further scattering the trail before convergence.

L2 accounts and amounts received (from L1 splits):
  001B  Nitu Kumari    Giridih   ₹18,000   at 10:24:48
  001C  Pintu Shah     Deoghar   ₹15,500   at 10:24:49
  001D  Govind Das     Dumka     ₹20,000   at 10:24:50
  001E  Laxmi Devi     Bokaro    ₹16,500   at 10:24:51
  001F  Mukesh Rajak   Dhanbad   ₹15,000   at 10:24:52
  002B  Kavita Singh   Giridih   ₹25,000   at 10:27:43
  002C  Rahul Tanti    Deoghar   ₹22,000   at 10:27:44
  002D  Bablu Gupta    Dumka     ₹28,000   at 10:27:45
  002E  Sarita Devi    Bokaro    ₹23,000   at 10:27:46
  002F  Dilip Kumar    Dhanbad   ₹22,000   at 10:27:47
  003B  Meena Turi     Giridih   ₹14,000   at 10:30:32
  003C  Suresh Mahto   Deoghar   ₹12,500   at 10:30:33
  003D  Anita Oraon    Dumka     ₹15,000   at 10:30:34
  003E  Ramdev Soren   Bokaro    ₹13,000   at 10:30:35
  003F  Puja Mandal    Dhanbad   ₹13,000   at 10:30:36
  004B  Shyam Babu     Giridih   ₹20,000   at 10:33:51
  004C  Jyoti Besra    Deoghar   ₹18,000   at 10:33:52
  004D  Nandu Hembram  Dumka     ₹22,000   at 10:33:53
  004E  Seema Rajwar   Bokaro    ₹17,500   at 10:33:54
  004F  Kiran Devi     Dhanbad   ₹17,500   at 10:33:55
  005B  Ravi Mochi     Giridih   ₹11,000   at 10:36:43
  005C  Sunita Lohra   Deoghar   ₹10,000   at 10:36:44
  005D  Mohan Ghosh    Dumka     ₹12,000   at 10:36:45
  005E  Kamla Devi     Bokaro    ₹10,000   at 10:36:46
  005F  Durgesh Nayak  Dhanbad   ₹10,000   at 10:36:47
"""

# ── LEVEL 2 MULE ACCOUNT PROFILES ────────────────────────────────────────────
L2_MULE_PROFILES = [
    # ── From MULE-L1-001A (Deepak Mandal) ────────────────────────────────────
    {"mule_id":"MULE-L2-001B","holder_name":"Nitu Kumari",   "phone":"8901234561","upi_id":"nitu.k001@paytm",  "bank":"Paytm Payments Bank",        "bank_account":"3001001234561","city":"Giridih", "state":"Jharkhand","received_from_mule":"MULE-L1-001A","amount_received":18000,"received_at":"2023-04-10 10:24:48"},
    {"mule_id":"MULE-L2-001C","holder_name":"Pintu Shah",    "phone":"8901234562","upi_id":"pintu.s001@ybl",   "bank":"PhonePe Payments Bank",       "bank_account":"3001001234562","city":"Deoghar","state":"Jharkhand","received_from_mule":"MULE-L1-001A","amount_received":15500,"received_at":"2023-04-10 10:24:49"},
    {"mule_id":"MULE-L2-001D","holder_name":"Govind Das",    "phone":"8901234563","upi_id":"govind.d001@oksbi", "bank":"Airtel Payments Bank",        "bank_account":"3001001234563","city":"Dumka",  "state":"Jharkhand","received_from_mule":"MULE-L1-001A","amount_received":20000,"received_at":"2023-04-10 10:24:50"},
    {"mule_id":"MULE-L2-001E","holder_name":"Laxmi Devi",    "phone":"8901234564","upi_id":"laxmi.d001@ybl",   "bank":"India Post Payments Bank",     "bank_account":"3001001234564","city":"Bokaro", "state":"Jharkhand","received_from_mule":"MULE-L1-001A","amount_received":16500,"received_at":"2023-04-10 10:24:51"},
    {"mule_id":"MULE-L2-001F","holder_name":"Mukesh Rajak",  "phone":"8901234565","upi_id":"mukesh.r001@okaxis","bank":"Paytm Payments Bank",        "bank_account":"3001001234565","city":"Dhanbad","state":"Jharkhand","received_from_mule":"MULE-L1-001A","amount_received":15000,"received_at":"2023-04-10 10:24:52"},
    # ── From MULE-L1-002A (Sonu Yadav) ───────────────────────────────────────
    {"mule_id":"MULE-L2-002B","holder_name":"Kavita Singh",  "phone":"8902345671","upi_id":"kavita.s002@paytm","bank":"Paytm Payments Bank",         "bank_account":"3002002345671","city":"Giridih", "state":"Jharkhand","received_from_mule":"MULE-L1-002A","amount_received":25000,"received_at":"2023-04-10 10:27:43"},
    {"mule_id":"MULE-L2-002C","holder_name":"Rahul Tanti",   "phone":"8902345672","upi_id":"rahul.t002@ybl",   "bank":"Airtel Payments Bank",        "bank_account":"3002002345672","city":"Deoghar","state":"Jharkhand","received_from_mule":"MULE-L1-002A","amount_received":22000,"received_at":"2023-04-10 10:27:44"},
    {"mule_id":"MULE-L2-002D","holder_name":"Bablu Gupta",   "phone":"8902345673","upi_id":"bablu.g002@oksbi", "bank":"PhonePe Payments Bank",        "bank_account":"3002002345673","city":"Dumka",  "state":"Jharkhand","received_from_mule":"MULE-L1-002A","amount_received":28000,"received_at":"2023-04-10 10:27:45"},
    {"mule_id":"MULE-L2-002E","holder_name":"Sarita Devi",   "phone":"8902345674","upi_id":"sarita.d002@ybl",  "bank":"India Post Payments Bank",     "bank_account":"3002002345674","city":"Bokaro", "state":"Jharkhand","received_from_mule":"MULE-L1-002A","amount_received":23000,"received_at":"2023-04-10 10:27:46"},
    {"mule_id":"MULE-L2-002F","holder_name":"Dilip Kumar",   "phone":"8902345675","upi_id":"dilip.k002@okaxis","bank":"Paytm Payments Bank",         "bank_account":"3002002345675","city":"Dhanbad","state":"Jharkhand","received_from_mule":"MULE-L1-002A","amount_received":22000,"received_at":"2023-04-10 10:27:47"},
    # ── From MULE-L1-003A (Raju Paswan) ──────────────────────────────────────
    {"mule_id":"MULE-L2-003B","holder_name":"Meena Turi",    "phone":"8903456781","upi_id":"meena.t003@paytm", "bank":"Paytm Payments Bank",         "bank_account":"3003003456781","city":"Giridih", "state":"Jharkhand","received_from_mule":"MULE-L1-003A","amount_received":14000,"received_at":"2023-04-10 10:30:32"},
    {"mule_id":"MULE-L2-003C","holder_name":"Suresh Mahto",  "phone":"8903456782","upi_id":"suresh.m003@ybl",  "bank":"Airtel Payments Bank",        "bank_account":"3003003456782","city":"Deoghar","state":"Jharkhand","received_from_mule":"MULE-L1-003A","amount_received":12500,"received_at":"2023-04-10 10:30:33"},
    {"mule_id":"MULE-L2-003D","holder_name":"Anita Oraon",   "phone":"8903456783","upi_id":"anita.o003@oksbi", "bank":"PhonePe Payments Bank",        "bank_account":"3003003456783","city":"Dumka",  "state":"Jharkhand","received_from_mule":"MULE-L1-003A","amount_received":15000,"received_at":"2023-04-10 10:30:34"},
    {"mule_id":"MULE-L2-003E","holder_name":"Ramdev Soren",  "phone":"8903456784","upi_id":"ramdev.s003@ybl",  "bank":"India Post Payments Bank",     "bank_account":"3003003456784","city":"Bokaro", "state":"Jharkhand","received_from_mule":"MULE-L1-003A","amount_received":13000,"received_at":"2023-04-10 10:30:35"},
    {"mule_id":"MULE-L2-003F","holder_name":"Puja Mandal",   "phone":"8903456785","upi_id":"puja.m003@okaxis", "bank":"Paytm Payments Bank",         "bank_account":"3003003456785","city":"Dhanbad","state":"Jharkhand","received_from_mule":"MULE-L1-003A","amount_received":13000,"received_at":"2023-04-10 10:30:36"},
    # ── From MULE-L1-004A (Bikram Tudu) ──────────────────────────────────────
    {"mule_id":"MULE-L2-004B","holder_name":"Shyam Babu",    "phone":"8904567891","upi_id":"shyam.b004@paytm", "bank":"Paytm Payments Bank",         "bank_account":"3004004567891","city":"Giridih", "state":"Jharkhand","received_from_mule":"MULE-L1-004A","amount_received":20000,"received_at":"2023-04-10 10:33:51"},
    {"mule_id":"MULE-L2-004C","holder_name":"Jyoti Besra",   "phone":"8904567892","upi_id":"jyoti.b004@ybl",   "bank":"Airtel Payments Bank",        "bank_account":"3004004567892","city":"Deoghar","state":"Jharkhand","received_from_mule":"MULE-L1-004A","amount_received":18000,"received_at":"2023-04-10 10:33:52"},
    {"mule_id":"MULE-L2-004D","holder_name":"Nandu Hembram", "phone":"8904567893","upi_id":"nandu.h004@oksbi", "bank":"PhonePe Payments Bank",        "bank_account":"3004004567893","city":"Dumka",  "state":"Jharkhand","received_from_mule":"MULE-L1-004A","amount_received":22000,"received_at":"2023-04-10 10:33:53"},
    {"mule_id":"MULE-L2-004E","holder_name":"Seema Rajwar",  "phone":"8904567894","upi_id":"seema.r004@ybl",   "bank":"India Post Payments Bank",     "bank_account":"3004004567894","city":"Bokaro", "state":"Jharkhand","received_from_mule":"MULE-L1-004A","amount_received":17500,"received_at":"2023-04-10 10:33:54"},
    {"mule_id":"MULE-L2-004F","holder_name":"Kiran Devi",    "phone":"8904567895","upi_id":"kiran.d004@okaxis","bank":"Paytm Payments Bank",         "bank_account":"3004004567895","city":"Dhanbad","state":"Jharkhand","received_from_mule":"MULE-L1-004A","amount_received":17500,"received_at":"2023-04-10 10:33:55"},
    # ── From MULE-L1-005A (Chandan Mahto) ────────────────────────────────────
    {"mule_id":"MULE-L2-005B","holder_name":"Ravi Mochi",    "phone":"8905678901","upi_id":"ravi.m005@paytm",  "bank":"Paytm Payments Bank",         "bank_account":"3005005678901","city":"Giridih", "state":"Jharkhand","received_from_mule":"MULE-L1-005A","amount_received":11000,"received_at":"2023-04-10 10:36:43"},
    {"mule_id":"MULE-L2-005C","holder_name":"Sunita Lohra",  "phone":"8905678902","upi_id":"sunita.l005@ybl",  "bank":"Airtel Payments Bank",        "bank_account":"3005005678902","city":"Deoghar","state":"Jharkhand","received_from_mule":"MULE-L1-005A","amount_received":10000,"received_at":"2023-04-10 10:36:44"},
    {"mule_id":"MULE-L2-005D","holder_name":"Mohan Ghosh",   "phone":"8905678903","upi_id":"mohan.g005@oksbi", "bank":"PhonePe Payments Bank",        "bank_account":"3005005678903","city":"Dumka",  "state":"Jharkhand","received_from_mule":"MULE-L1-005A","amount_received":12000,"received_at":"2023-04-10 10:36:45"},
    {"mule_id":"MULE-L2-005E","holder_name":"Kamla Devi",    "phone":"8905678904","upi_id":"kamla.d005@ybl",   "bank":"India Post Payments Bank",     "bank_account":"3005005678904","city":"Bokaro", "state":"Jharkhand","received_from_mule":"MULE-L1-005A","amount_received":10000,"received_at":"2023-04-10 10:36:46"},
    {"mule_id":"MULE-L2-005F","holder_name":"Durgesh Nayak", "phone":"8905678905","upi_id":"durgesh.n005@okaxis","bank":"Paytm Payments Bank",       "bank_account":"3005005678905","city":"Dhanbad","state":"Jharkhand","received_from_mule":"MULE-L1-005A","amount_received":10000,"received_at":"2023-04-10 10:36:47"},
]

# ── LEVEL 2 → KINGPIN SPLIT TRANSACTIONS (125 rows) ──────────────────────────
# Each L2 mule fires 5 small transfers within ~60 sec to 5 pre-kingpin accounts.
# All pre-kingpin accounts ultimately funnel into KINGPIN-001 (Santosh Mandal).
# Cities used: Hazaribagh, Koderma, Lohardaga, Chatra, Pakur.

def _make_splits(mule_id, holder, amount, recv_time_str, base_sec):
    """Generate 5 split entries for a given L2 mule."""
    from datetime import datetime, timedelta
    recv_dt = datetime.strptime(recv_time_str, "%Y-%m-%d %H:%M:%S")
    cities   = ["Hazaribagh", "Koderma", "Lohardaga", "Chatra", "Pakur"]
    pk_ids   = ["PKA", "PKB", "PKC", "PKD", "PKE"]
    pk_names = ["Santosh Net Acc-A", "Santosh Net Acc-B", "Santosh Net Acc-C",
                "Santosh Net Acc-D", "Santosh Net Acc-E"]
    suffix   = mule_id.replace("MULE-L2-", "")   # e.g. "001B"
    # unequal split: divide with slight variation
    base = amount // 5
    parts = [base - 500, base + 200, base + 300, base - 100, amount - (base-500) - (base+200) - (base+300) - (base-100)]
    rows = []
    for i, (city, pk, pkn, part) in enumerate(zip(cities, pk_ids, pk_names, parts)):
        split_dt = recv_dt + timedelta(seconds=base_sec + i)
        rows.append({
            "split_txn_id":        f"SPL2-{suffix}-0{i+1}",
            "from_mule":           mule_id,
            "from_holder":         holder,
            "to_account":          f"PRE-KP-{suffix}-{pk}",
            "to_holder":           pkn,
            "to_city":             city,
            "to_state":            "Jharkhand",
            "amount":              part,
            "split_time":          split_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "seconds_after_receipt": base_sec + i,
            "final_destination":   "KINGPIN-001",
        })
    return rows

L2_TO_KINGPIN_SPLITS = []
for p in L2_MULE_PROFILES:
    L2_TO_KINGPIN_SPLITS.extend(
        _make_splits(p["mule_id"], p["holder_name"],
                     p["amount_received"], p["received_at"], 55)
    )
