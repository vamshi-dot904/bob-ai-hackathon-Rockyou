# Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   STREAMLIT FRONTEND (app.py)                    │
│                                                                   │
│  Landing Page   →   Complaint Form   →   Investigation Workspace │
│  (5 demo victims)   (3 sections)         (5 tabs)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │ active_case dict
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              CORRELATION ENGINE (correlation_engine.py)          │
│                                                                   │
│  Step 1: Victim Identity Check                                   │
│  Step 2: SIM Swap Detection  ──────────────────────────────┐    │
│  Step 3: UPI Access Correlation                            │    │
│  Step 4: Transaction Verification                          │    │
│  Step 5: L1 Mule Trace                                     │    │
│  Step 6: L2 Mule Chain Trace                               │    │
│  Step 7: Kingpin Linkage                                   │    │
│  Step 8: Fraud Pattern Classifier (risk score 0–100)       │    │
│  Step 9: Evidence Timeline Builder                         │    │
└───────────────────────────┬────────────────────────────────┘    │
                            │                                       │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER (CSV Files)                       │
│                                                                   │
│  Device details/                                                  │
│  ├── device_records_before_swap.csv   ← telecom before swap      │
│  └── device_records_after_swap.csv    ← criminal device record   │
│                                                                   │
│  UPI access details/                                              │
│  ├── upi_access_logs.csv              ← login events             │
│  └── upi_transactions.csv             ← debit events             │
│                                                                   │
│  1st mule account/                                                │
│  ├── mule_l1_profiles.csv             ← L1 mule identities       │
│  └── mule_l1_to_l2_splits.csv         ← 25 split transactions    │
│                                                                   │
│  2nd mule account/                                                │
│  ├── mule_l2_profiles.csv             ← L2 mule identities       │
│  └── mule_l2_to_kingpin_splits.csv    ← 125 micro-transfers      │
│                                                                   │
│  kingpin account/                                                 │
│  ├── kingpin_profile.csv              ← kingpin identity          │
│  ├── kingpin_inflow_transfers.csv     ← 125 inflow records        │
│  └── kingpin_account_summary.csv      ← aggregated totals         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### `app.py` — Streamlit Frontend
- **Landing page**: stats banner, 5 demo victim buttons, new case button
- **Complaint form**: 3 sections (Victim / Device / Financial) + indicators
- **Investigation workspace**: 5 tabs driven entirely by correlation results

### `correlation_engine.py` — Backend Intelligence
- Pure Python, no ML required
- CSV-driven lookup with 9 sequential correlation steps
- Returns a single `CorrelationResult` dict consumed by all 5 tabs
- `@st.cache_data` cached — runs once per unique phone/IMEI combination

### Data Layer
- All data stored as UTF-8 CSV files
- Regenerated from Python source files (`device_records.py`, `upi_access_data.py`, etc.)
- No database required — fully portable

## Data Flow

```
User submits phone + IMEI + bank account + amount
              │
              ▼
    correlate(submission)
              │
    ┌─────────┴──────────┐
    │ load_all_data()     │  ← reads all 11 CSV files once
    └─────────┬──────────┘
              │
    9 sequential steps
              │
    CorrelationResult dict
              │
    ┌─────────┴──────────────────────────────────┐
    │  Tab 1: Network Graph (pyvis)               │
    │  Tab 2: Org Hierarchy (styled cards)         │
    │  Tab 3: Evidence Detail (field-value tables) │
    │  Tab 4: Event Timeline (chronological HTML)  │
    │  Tab 5: FIR Brief (downloadable .txt)        │
    └─────────────────────────────────────────────┘
```

## Money Flow Architecture

```
5 VICTIMS (different cities)
    │
    │  UPI debit (within 74–77 sec of SIM swap)
    ▼
5 L1 MULES (all in Jamtara, Jharkhand)
    │
    │  Split into 5 accounts each (~57 sec after receipt)
    ▼
25 L2 MULES (Giridih / Deoghar / Dumka / Bokaro / Dhanbad)
    │
    │  Split into 5 accounts each (~57 sec after receipt)
    ▼
125 PRE-KINGPIN ACCOUNTS (Hazaribagh / Koderma / Lohardaga / Chatra / Pakur)
    │
    │  Transfer (~60 sec after receipt)
    ▼
KINGPIN — Santosh Mandal — HDFC Bank — Jamtara
Total: Rs. 4,20,500 in 12 minutes 12 seconds
```

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.64+ |
| Network Graph | pyvis |
| Data Processing | pandas, Python csv |
| Graph Layout | NetworkX (via pyvis) |
| Data Storage | CSV files |
| Case Persistence | JSON + CSV (data/cases/) |
| Language | Python 3.11 |
