"""
Level 1 Mule Account Data
--------------------------
Each victim's money lands in a Level 1 mule account (MULE-L1-001A to 005A).
Within 1 minute of receiving, each L1 mule splits the amount into 5 sub-accounts (L2 mules).
Split is unequal — to avoid pattern detection. All L2 mule accounts are in different cities.

Source transactions (from victims):
  MULE-L1-001A received ₹85,000  from Ramesh Kumar  at 10:23:51
  MULE-L1-002A received ₹1,20,000 from Sunita Devi   at 10:26:49
  MULE-L1-003A received ₹67,500  from Manoj Singh   at 10:29:38
  MULE-L1-004A received ₹95,000  from Priya Sharma  at 10:32:58
  MULE-L1-005A received ₹53,000  from Anil Yadav    at 10:35:50
"""

# ── LEVEL 1 MULE ACCOUNT PROFILES ────────────────────────────────────────────
L1_MULE_PROFILES = [
    {
        "mule_id": "MULE-L1-001A",
        "holder_name": "Deepak Mandal",
        "phone_number": "8812345678",
        "upi_id": "mule.acc1a@ybl",
        "bank_name": "Paytm Payments Bank",
        "bank_account": "2001123456789",
        "city": "Jamtara",
        "state": "Jharkhand",
        "role": "L1_MULE",
        "recruited_by": "KINGPIN-001",
        "amount_received": 85000,
        "received_from": "Ramesh Kumar",
        "received_at": "2023-04-10 10:23:51",
    },
    {
        "mule_id": "MULE-L1-002A",
        "holder_name": "Sonu Yadav",
        "phone_number": "8823456789",
        "upi_id": "mule.acc2a@ybl",
        "bank_name": "Airtel Payments Bank",
        "bank_account": "2002234567890",
        "city": "Jamtara",
        "state": "Jharkhand",
        "role": "L1_MULE",
        "recruited_by": "KINGPIN-001",
        "amount_received": 120000,
        "received_from": "Sunita Devi",
        "received_at": "2023-04-10 10:26:49",
    },
    {
        "mule_id": "MULE-L1-003A",
        "holder_name": "Raju Paswan",
        "phone_number": "8834567890",
        "upi_id": "mule.acc3a@ybl",
        "bank_name": "India Post Payments Bank",
        "bank_account": "2003345678901",
        "city": "Jamtara",
        "state": "Jharkhand",
        "role": "L1_MULE",
        "recruited_by": "KINGPIN-001",
        "amount_received": 67500,
        "received_from": "Manoj Singh",
        "received_at": "2023-04-10 10:29:38",
    },
    {
        "mule_id": "MULE-L1-004A",
        "holder_name": "Bikram Tudu",
        "phone_number": "8845678901",
        "upi_id": "mule.acc4a@ybl",
        "bank_name": "Paytm Payments Bank",
        "bank_account": "2004456789012",
        "city": "Jamtara",
        "state": "Jharkhand",
        "role": "L1_MULE",
        "recruited_by": "KINGPIN-001",
        "amount_received": 95000,
        "received_from": "Priya Sharma",
        "received_at": "2023-04-10 10:32:58",
    },
    {
        "mule_id": "MULE-L1-005A",
        "holder_name": "Chandan Mahto",
        "phone_number": "8856789012",
        "upi_id": "mule.acc5a@ybl",
        "bank_name": "Airtel Payments Bank",
        "bank_account": "2005567890123",
        "city": "Jamtara",
        "state": "Jharkhand",
        "role": "L1_MULE",
        "recruited_by": "KINGPIN-001",
        "amount_received": 53000,
        "received_from": "Anil Yadav",
        "received_at": "2023-04-10 10:35:50",
    },
]

# ── LEVEL 1 → LEVEL 2 SPLIT TRANSACTIONS ─────────────────────────────────────
# Each L1 mule splits received amount into 5 L2 accounts within ~60 seconds.
# Amounts are unequal to avoid round-number detection.
# L2 mules are in different cities (Giridih, Deoghar, Dumka, Bokaro, Dhanbad).

L1_TO_L2_SPLITS = [

    # ── MULE-L1-001A splits ₹85,000 at 10:24:48 (57 sec after receiving) ──
    {"split_txn_id": "SPL-001A-01", "from_mule": "MULE-L1-001A", "from_holder": "Deepak Mandal",
     "to_account": "MULE-L2-001B", "to_holder": "Nitu Kumari",   "to_city": "Giridih",  "to_state": "Jharkhand",
     "amount": 18000, "split_time": "2023-04-10 10:24:48", "seconds_after_receipt": 57},

    {"split_txn_id": "SPL-001A-02", "from_mule": "MULE-L1-001A", "from_holder": "Deepak Mandal",
     "to_account": "MULE-L2-001C", "to_holder": "Pintu Shah",    "to_city": "Deoghar",  "to_state": "Jharkhand",
     "amount": 15500, "split_time": "2023-04-10 10:24:49", "seconds_after_receipt": 58},

    {"split_txn_id": "SPL-001A-03", "from_mule": "MULE-L1-001A", "from_holder": "Deepak Mandal",
     "to_account": "MULE-L2-001D", "to_holder": "Govind Das",    "to_city": "Dumka",    "to_state": "Jharkhand",
     "amount": 20000, "split_time": "2023-04-10 10:24:50", "seconds_after_receipt": 59},

    {"split_txn_id": "SPL-001A-04", "from_mule": "MULE-L1-001A", "from_holder": "Deepak Mandal",
     "to_account": "MULE-L2-001E", "to_holder": "Laxmi Devi",    "to_city": "Bokaro",   "to_state": "Jharkhand",
     "amount": 16500, "split_time": "2023-04-10 10:24:51", "seconds_after_receipt": 60},

    {"split_txn_id": "SPL-001A-05", "from_mule": "MULE-L1-001A", "from_holder": "Deepak Mandal",
     "to_account": "MULE-L2-001F", "to_holder": "Mukesh Rajak",  "to_city": "Dhanbad",  "to_state": "Jharkhand",
     "amount": 15000, "split_time": "2023-04-10 10:24:52", "seconds_after_receipt": 61},

    # ── MULE-L1-002A splits ₹1,20,000 at 10:27:43 (54 sec after receiving) ──
    {"split_txn_id": "SPL-002A-01", "from_mule": "MULE-L1-002A", "from_holder": "Sonu Yadav",
     "to_account": "MULE-L2-002B", "to_holder": "Kavita Singh",  "to_city": "Giridih",  "to_state": "Jharkhand",
     "amount": 25000, "split_time": "2023-04-10 10:27:43", "seconds_after_receipt": 54},

    {"split_txn_id": "SPL-002A-02", "from_mule": "MULE-L1-002A", "from_holder": "Sonu Yadav",
     "to_account": "MULE-L2-002C", "to_holder": "Rahul Tanti",   "to_city": "Deoghar",  "to_state": "Jharkhand",
     "amount": 22000, "split_time": "2023-04-10 10:27:44", "seconds_after_receipt": 55},

    {"split_txn_id": "SPL-002A-03", "from_mule": "MULE-L1-002A", "from_holder": "Sonu Yadav",
     "to_account": "MULE-L2-002D", "to_holder": "Bablu Gupta",   "to_city": "Dumka",    "to_state": "Jharkhand",
     "amount": 28000, "split_time": "2023-04-10 10:27:45", "seconds_after_receipt": 56},

    {"split_txn_id": "SPL-002A-04", "from_mule": "MULE-L1-002A", "from_holder": "Sonu Yadav",
     "to_account": "MULE-L2-002E", "to_holder": "Sarita Devi",   "to_city": "Bokaro",   "to_state": "Jharkhand",
     "amount": 23000, "split_time": "2023-04-10 10:27:46", "seconds_after_receipt": 57},

    {"split_txn_id": "SPL-002A-05", "from_mule": "MULE-L1-002A", "from_holder": "Sonu Yadav",
     "to_account": "MULE-L2-002F", "to_holder": "Dilip Kumar",   "to_city": "Dhanbad",  "to_state": "Jharkhand",
     "amount": 22000, "split_time": "2023-04-10 10:27:47", "seconds_after_receipt": 58},

    # ── MULE-L1-003A splits ₹67,500 at 10:30:32 (54 sec after receiving) ──
    {"split_txn_id": "SPL-003A-01", "from_mule": "MULE-L1-003A", "from_holder": "Raju Paswan",
     "to_account": "MULE-L2-003B", "to_holder": "Meena Turi",    "to_city": "Giridih",  "to_state": "Jharkhand",
     "amount": 14000, "split_time": "2023-04-10 10:30:32", "seconds_after_receipt": 54},

    {"split_txn_id": "SPL-003A-02", "from_mule": "MULE-L1-003A", "from_holder": "Raju Paswan",
     "to_account": "MULE-L2-003C", "to_holder": "Suresh Mahto",  "to_city": "Deoghar",  "to_state": "Jharkhand",
     "amount": 12500, "split_time": "2023-04-10 10:30:33", "seconds_after_receipt": 55},

    {"split_txn_id": "SPL-003A-03", "from_mule": "MULE-L1-003A", "from_holder": "Raju Paswan",
     "to_account": "MULE-L2-003D", "to_holder": "Anita Oraon",   "to_city": "Dumka",    "to_state": "Jharkhand",
     "amount": 15000, "split_time": "2023-04-10 10:30:34", "seconds_after_receipt": 56},

    {"split_txn_id": "SPL-003A-04", "from_mule": "MULE-L1-003A", "from_holder": "Raju Paswan",
     "to_account": "MULE-L2-003E", "to_holder": "Ramdev Soren",  "to_city": "Bokaro",   "to_state": "Jharkhand",
     "amount": 13000, "split_time": "2023-04-10 10:30:35", "seconds_after_receipt": 57},

    {"split_txn_id": "SPL-003A-05", "from_mule": "MULE-L1-003A", "from_holder": "Raju Paswan",
     "to_account": "MULE-L2-003F", "to_holder": "Puja Mandal",   "to_city": "Dhanbad",  "to_state": "Jharkhand",
     "amount": 13000, "split_time": "2023-04-10 10:30:36", "seconds_after_receipt": 58},

    # ── MULE-L1-004A splits ₹95,000 at 10:33:51 (53 sec after receiving) ──
    {"split_txn_id": "SPL-004A-01", "from_mule": "MULE-L1-004A", "from_holder": "Bikram Tudu",
     "to_account": "MULE-L2-004B", "to_holder": "Shyam Babu",    "to_city": "Giridih",  "to_state": "Jharkhand",
     "amount": 20000, "split_time": "2023-04-10 10:33:51", "seconds_after_receipt": 53},

    {"split_txn_id": "SPL-004A-02", "from_mule": "MULE-L1-004A", "from_holder": "Bikram Tudu",
     "to_account": "MULE-L2-004C", "to_holder": "Jyoti Besra",   "to_city": "Deoghar",  "to_state": "Jharkhand",
     "amount": 18000, "split_time": "2023-04-10 10:33:52", "seconds_after_receipt": 54},

    {"split_txn_id": "SPL-004A-03", "from_mule": "MULE-L1-004A", "from_holder": "Bikram Tudu",
     "to_account": "MULE-L2-004D", "to_holder": "Nandu Hembram", "to_city": "Dumka",    "to_state": "Jharkhand",
     "amount": 22000, "split_time": "2023-04-10 10:33:53", "seconds_after_receipt": 55},

    {"split_txn_id": "SPL-004A-04", "from_mule": "MULE-L1-004A", "from_holder": "Bikram Tudu",
     "to_account": "MULE-L2-004E", "to_holder": "Seema Rajwar",  "to_city": "Bokaro",   "to_state": "Jharkhand",
     "amount": 17500, "split_time": "2023-04-10 10:33:54", "seconds_after_receipt": 56},

    {"split_txn_id": "SPL-004A-05", "from_mule": "MULE-L1-004A", "from_holder": "Bikram Tudu",
     "to_account": "MULE-L2-004F", "to_holder": "Kiran Devi",    "to_city": "Dhanbad",  "to_state": "Jharkhand",
     "amount": 17500, "split_time": "2023-04-10 10:33:55", "seconds_after_receipt": 57},

    # ── MULE-L1-005A splits ₹53,000 at 10:36:43 (53 sec after receiving) ──
    {"split_txn_id": "SPL-005A-01", "from_mule": "MULE-L1-005A", "from_holder": "Chandan Mahto",
     "to_account": "MULE-L2-005B", "to_holder": "Ravi Mochi",    "to_city": "Giridih",  "to_state": "Jharkhand",
     "amount": 11000, "split_time": "2023-04-10 10:36:43", "seconds_after_receipt": 53},

    {"split_txn_id": "SPL-005A-02", "from_mule": "MULE-L1-005A", "from_holder": "Chandan Mahto",
     "to_account": "MULE-L2-005C", "to_holder": "Sunita Lohra",  "to_city": "Deoghar",  "to_state": "Jharkhand",
     "amount": 10000, "split_time": "2023-04-10 10:36:44", "seconds_after_receipt": 54},

    {"split_txn_id": "SPL-005A-03", "from_mule": "MULE-L1-005A", "from_holder": "Chandan Mahto",
     "to_account": "MULE-L2-005D", "to_holder": "Mohan Ghosh",   "to_city": "Dumka",    "to_state": "Jharkhand",
     "amount": 12000, "split_time": "2023-04-10 10:36:45", "seconds_after_receipt": 55},

    {"split_txn_id": "SPL-005A-04", "from_mule": "MULE-L1-005A", "from_holder": "Chandan Mahto",
     "to_account": "MULE-L2-005E", "to_holder": "Kamla Devi",    "to_city": "Bokaro",   "to_state": "Jharkhand",
     "amount": 10000, "split_time": "2023-04-10 10:36:46", "seconds_after_receipt": 56},

    {"split_txn_id": "SPL-005A-05", "from_mule": "MULE-L1-005A", "from_holder": "Chandan Mahto",
     "to_account": "MULE-L2-005F", "to_holder": "Durgesh Nayak", "to_city": "Dhanbad",  "to_state": "Jharkhand",
     "amount": 10000, "split_time": "2023-04-10 10:36:47", "seconds_after_receipt": 57},
]
