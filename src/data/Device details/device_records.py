"""
Device Records Dataset
-----------------------
Simulates telecom tower data for 5 victims:
  - BEFORE SIM swap: original device registered to the victim
  - AFTER  SIM swap: same phone number appears on a NEW IMEI in a different city
                     (criminal's device — location switched from victim's city to Jamtara)
"""

# ─────────────────────────────────────────────
# BEFORE SIM SWAP  (victim's legitimate device)
# ─────────────────────────────────────────────
DEVICE_RECORDS_BEFORE = [
    {
        "record_id": "BEF-001",
        "victim_name": "Ramesh Kumar",
        "phone_number": "9876543210",
        "imei": "354678901234567",
        "sim_provider": "Airtel",
        "city": "Patna",
        "state": "Bihar",
        "tower_id": "PTNA-TOWER-042",
        "last_active": "2023-04-10 08:45:00",
        "status": "ACTIVE",
    },
    {
        "record_id": "BEF-002",
        "victim_name": "Sunita Devi",
        "phone_number": "9123456780",
        "imei": "357891234567890",
        "sim_provider": "Jio",
        "city": "Ranchi",
        "state": "Jharkhand",
        "tower_id": "RNCH-TOWER-017",
        "last_active": "2023-04-10 09:10:00",
        "status": "ACTIVE",
    },
    {
        "record_id": "BEF-003",
        "victim_name": "Manoj Singh",
        "phone_number": "9988776655",
        "imei": "352345678901234",
        "sim_provider": "Vi",
        "city": "Dhanbad",
        "state": "Jharkhand",
        "tower_id": "DNBD-TOWER-009",
        "last_active": "2023-04-10 09:30:00",
        "status": "ACTIVE",
    },
    {
        "record_id": "BEF-004",
        "victim_name": "Priya Sharma",
        "phone_number": "9765432109",
        "imei": "356789012345678",
        "sim_provider": "Airtel",
        "city": "Bokaro",
        "state": "Jharkhand",
        "tower_id": "BKRO-TOWER-031",
        "last_active": "2023-04-10 09:55:00",
        "status": "ACTIVE",
    },
    {
        "record_id": "BEF-005",
        "victim_name": "Anil Yadav",
        "phone_number": "9654321098",
        "imei": "351234567890123",
        "sim_provider": "BSNL",
        "city": "Gaya",
        "state": "Bihar",
        "tower_id": "GAYA-TOWER-005",
        "last_active": "2023-04-10 10:15:00",
        "status": "ACTIVE",
    },
]

# ─────────────────────────────────────────────
# AFTER SIM SWAP  (criminal's device — different IMEI, different city, same phone number)
# SIM swap approved by telecom fraudulently using fake ID proof
# ─────────────────────────────────────────────
DEVICE_RECORDS_AFTER = [
    {
        "record_id": "AFT-001",
        "victim_name": "Ramesh Kumar",        # same victim phone number
        "phone_number": "9876543210",         # same number — now on criminal's device
        "imei": "990012345678901",            # NEW IMEI (criminal's handset)
        "sim_provider": "Airtel",
        "city": "Jamtara",                    # location SWITCHED → red flag
        "state": "Jharkhand",
        "tower_id": "JMTR-TOWER-003",
        "swap_timestamp": "2023-04-10 10:22:00",    # moment SIM swap completed
        "first_upi_access": "2023-04-10 10:23:14",  # 1 min 14 sec after swap
        "status": "SWAPPED",
        "previous_city": "Patna",
        "distance_km": 412,
    },
    {
        "record_id": "AFT-002",
        "victim_name": "Sunita Devi",
        "phone_number": "9123456780",
        "imei": "990023456789012",
        "sim_provider": "Jio",
        "city": "Jamtara",
        "state": "Jharkhand",
        "tower_id": "JMTR-TOWER-003",
        "swap_timestamp": "2023-04-10 10:25:00",
        "first_upi_access": "2023-04-10 10:26:08",
        "status": "SWAPPED",
        "previous_city": "Ranchi",
        "distance_km": 178,
    },
    {
        "record_id": "AFT-003",
        "victim_name": "Manoj Singh",
        "phone_number": "9988776655",
        "imei": "990034567890123",
        "sim_provider": "Vi",
        "city": "Jamtara",
        "state": "Jharkhand",
        "tower_id": "JMTR-TOWER-007",
        "swap_timestamp": "2023-04-10 10:28:00",
        "first_upi_access": "2023-04-10 10:29:02",
        "status": "SWAPPED",
        "previous_city": "Dhanbad",
        "distance_km": 95,
    },
    {
        "record_id": "AFT-004",
        "victim_name": "Priya Sharma",
        "phone_number": "9765432109",
        "imei": "990045678901234",
        "sim_provider": "Airtel",
        "city": "Jamtara",
        "state": "Jharkhand",
        "tower_id": "JMTR-TOWER-003",
        "swap_timestamp": "2023-04-10 10:31:00",
        "first_upi_access": "2023-04-10 10:32:17",
        "status": "SWAPPED",
        "previous_city": "Bokaro",
        "distance_km": 142,
    },
    {
        "record_id": "AFT-005",
        "victim_name": "Anil Yadav",
        "phone_number": "9654321098",
        "imei": "990056789012345",
        "sim_provider": "BSNL",
        "city": "Jamtara",
        "state": "Jharkhand",
        "tower_id": "JMTR-TOWER-007",
        "swap_timestamp": "2023-04-10 10:34:00",
        "first_upi_access": "2023-04-10 10:35:11",
        "status": "SWAPPED",
        "previous_city": "Gaya",
        "distance_km": 320,
    },
]
