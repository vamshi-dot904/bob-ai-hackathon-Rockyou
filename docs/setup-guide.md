# Setup Guide

## Prerequisites

- Python 3.11+
- pip

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Install Dependencies

```bash
pip install streamlit pandas pyvis networkx
```

Or if a `requirements.txt` is provided:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
cd src
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Project Structure

```
src/
├── app.py                          # Main Streamlit application
├── correlation_engine.py           # Core investigation logic
├── test_correlation.py             # CLI test for all 5 victims
└── data/
    ├── Device details/
    │   ├── device_records.py                  # Source data generator
    │   ├── device_records_before_swap.csv     # Victim device records
    │   └── device_records_after_swap.csv      # Criminal device records
    ├── UPI access details/
    │   ├── upi_access_data.py                 # Source data generator
    │   ├── upi_access_logs.csv                # UPI login events
    │   └── upi_transactions.csv               # Money debit events
    ├── 1st mule account/
    │   ├── mule_l1_data.py                    # Source data generator
    │   ├── mule_l1_profiles.csv               # L1 mule identities
    │   └── mule_l1_to_l2_splits.csv           # Split transactions
    ├── 2nd mule account/
    │   ├── mule_l2_data.py                    # Source data generator
    │   ├── mule_l2_profiles.csv               # L2 mule identities
    │   └── mule_l2_to_kingpin_splits.csv      # Pre-kingpin transfers
    ├── kingpin account/
    │   ├── kingpin_data.py                    # Source data generator
    │   ├── kingpin_profile.csv                # Kingpin identity
    │   ├── kingpin_inflow_transfers.csv        # All inflow records
    │   └── kingpin_account_summary.csv        # Aggregated totals
    └── cases/                                 # Saved complaint submissions (auto-created)
```

---

## Using the Demo

1. Open the app — you will see the **landing page** with 5 demo victim buttons
2. Click any victim name (e.g. **Ramesh Kumar**) — the form auto-fills
3. Click **🚀 Submit & Investigate**
4. Explore the 5 investigation tabs:
   - **Network Graph** — interactive money flow visualisation
   - **Org Hierarchy** — Kingpin → L1 → L2 → Victim tree
   - **Evidence Detail** — SIM swap, UPI access, transaction evidence
   - **Event Timeline** — chronological event log
   - **FIR Brief** — downloadable case document
5. Click **🔄 New Case / Switch Victim** in the sidebar to switch victims

---

## Regenerating Mock Data

If CSV files are missing or corrupted, regenerate them from the Python source:

```bash
cd "src/data/Device details"
py generate_device_csv.py

cd "../UPI access details"
py generate_upi_csv.py

cd "../1st mule account"
py generate_mule_l1_csv.py

cd "../2nd mule account"
py generate_mule_l2_csv.py

cd "../kingpin account"
py generate_kingpin_csv.py
```

---

## Running the Correlation Test

To verify all 5 victims correlate correctly without the UI:

```bash
cd src
py test_correlation.py
```

Expected output — each victim should show `score=100/100` and `L1=<mule name>`.

---

## Requirements

```
streamlit>=1.64.0
pandas
pyvis
networkx
```
