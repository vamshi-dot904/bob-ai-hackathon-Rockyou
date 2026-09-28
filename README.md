# Cyber Fraud Investigation Tool — Jamtara SIM-Swap Ring

> **Hackathon Submission | Team RockYou | Track: Cyber Forensics**
> From victim complaint to FIR-ready case brief in 30 seconds. Powered by IBM Bob.

---

## Team

| Field | Details |
|---|---|
| **Team Name** | RockYou |
| **Track** | Cyber Forensics |
| **Lead** | Kumar Ganesh |
| **Email** | ganeshrajgaria00@gmail.com |
| **Members** | Kumar Ganesh, Kanike Vamshi Chandra |

---

## Problem Statement

In FY2023, Jharkhand's Jamtara district produced **95,000+ UPI fraud cases**. Investigators manually traced connections between bank accounts, SIM cards, and devices — taking weeks per case. Most went unsolved due to lack of network visualisation tools.

**The attack chain:** Tower data → Bank data → Trap data → Complaint data.  
SIM-swap executes in under 74 seconds. Money then splits through 2 layers of mule accounts before consolidating at the kingpin — entire operation takes ~13 minutes.

---

## Solution

A Bob-powered investigation platform that ingests a victim's complaint, runs it through a **9-step automated correlation engine**, and produces an FIR-ready case brief with full network visualisation.

### What It Does

- ✅ SIM swap confirmation via IMEI mismatch in telecom device records
- ✅ Interactive network graph — Victim → L1 Mule → L2 Mules → Kingpin
- ✅ Full organisational hierarchy of the criminal ring
- ✅ Colour-coded evidence tables with badge classification
- ✅ Chronological event timeline (SIM swap → UPI login → drain → split → consolidate)
- ✅ Downloadable FIR-ready case brief with IPC section recommendations (Sec. 66C, 66D IT Act; Sec. 420 IPC)
- ✅ Risk score 0–100 with fraud pattern classification

---

## IBM Technologies Used

| Technology | Usage |
|---|---|
| **IBM Bob** | AI assistant — generated all code (1,400+ lines), designed mock data schemas, mapped IPC sections, debugged all edge cases, built entire correlation engine through natural language conversation |

---

## Tech Stack

| Component | Technology |
|---|---|
| App Framework | Python 3.11 + Streamlit 1.64 |
| Network Graph | pyvis + NetworkX |
| Data Layer | pandas + CSV |
| AI Assistant | IBM Bob |

---

## How to Run

```bash
cd jamtara-fraud-investigation/src
pip install streamlit pandas pyvis networkx
streamlit run app.py
```

Click any of the **5 demo victim buttons** on the landing page to auto-fill the form and run a complete investigation instantly.

---

## Repository Structure

```
jamtara-fraud-investigation/
├── README.md                    ← This file
├── submission.yaml              ← Structured submission metadata
├── requirements.txt             ← Python dependencies
├── src/
│   ├── app.py                   ← Main Streamlit application
│   ├── correlation_engine.py    ← 9-step automated correlation engine
│   ├── test_correlation.py      ← CLI test runner
│   └── data/
│       ├── Device details/      ← Before/after SIM-swap device records
│       ├── UPI access details/  ← UPI login + transaction logs
│       ├── 1st mule account/    ← L1 mule profiles + split records
│       ├── 2nd mule account/    ← L2 mule profiles + split records
│       ├── kingpin account/     ← Kingpin profile + inflow records
│       └── cases/               ← Saved investigation outputs
├── docs/
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/
│   ├── screenshots/
│   └── demo-video-link.txt
└── presentation/
    └── Cyber_Fraud_Investigation.pptx
```

---

## Mock Data: 5 Victims, 1 Ring

| Victim | City | Amount Stolen | L1 Mule | Kingpin |
|---|---|---|---|---|
| Ramesh Kumar | Patna, Bihar | Rs. 85,000 | Deepak Mandal | Santosh Mandal |
| Sunita Devi | Ranchi, Jharkhand | Rs. 1,20,000 | Sonu Yadav | Santosh Mandal |
| Manoj Singh | Dhanbad, Jharkhand | Rs. 67,500 | Raju Paswan | Santosh Mandal |
| Priya Sharma | Bokaro, Jharkhand | Rs. 95,000 | Bikram Tudu | Santosh Mandal |
| Anil Yadav | Gaya, Bihar | Rs. 53,000 | Chandan Mahto | Santosh Mandal |

**Total: Rs. 4,20,500 stolen across 3 mule layers in 12 minutes 12 seconds.**

Data scope: 5 L1 mules · 25 L2 mules · 125 pre-kingpin accounts · 160+ tracked transactions.

---

## Documentation

| Document | Description |
|---|---|
| [Problem Statement](docs/problem-statement.md) | Real-world Jamtara case context and the investigation gap |
| [Solution Overview](docs/solution-overview.md) | Tool capabilities, mock data scope, output types |
| [Architecture](docs/architecture.md) | System design, data flow, component breakdown |
| [Setup Guide](docs/setup-guide.md) | Installation, running the app, regenerating data |

---

## Built With IBM Bob

Every line of code in this repository was generated through IBM Bob. The correlation engine, Streamlit UI, pyvis graph builder, FIR template, IPC section mapping, and all 6 mock data CSV schemas were built by describing the Jamtara fraud pattern in plain English to Bob.
