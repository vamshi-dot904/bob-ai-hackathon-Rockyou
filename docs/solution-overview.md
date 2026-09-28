# Solution Overview

## Cyber Fraud Investigation Tool — Powered by IBM Bob

### What It Does

This tool transforms a raw victim complaint into a **complete, traceable fraud investigation** in seconds — replacing weeks of manual detective work.

A victim (or police officer) submits a complaint form. The system automatically:

1. **Identifies the victim** by matching their phone number against telecom device records
2. **Confirms SIM swap** by detecting IMEI mismatch between before/after device records
3. **Corroborates the UPI access** — unauthorised login from Jamtara within 74 seconds of swap
4. **Verifies the transaction** — amount, time, receiver mule account
5. **Traces the L1 mule** — name, phone, bank, city, who recruited them
6. **Traces all 5 L2 mules** — the split layer across Giridih, Deoghar, Dumka, Bokaro, Dhanbad
7. **Links to the Kingpin** — Santosh Mandal, HDFC Bank, Jamtara
8. **Classifies the fraud pattern** — risk score 100/100, ORGANISED GANG
9. **Generates FIR-ready case brief** — with accused list, evidence, and recommended actions

### Key Capabilities

| Capability | Description |
|---|---|
| Entity Extraction | Extracts victim, mule, device, bank, and location entities from submitted data |
| Relationship Mapping | Maps who called whom, which account received which transfer |
| Pattern Detection | Detects SIM-swap + UPI fraud + layered mule splitting as a combined attack pattern |
| Hierarchy Mapping | Reconstructs Kingpin → L2 Mule → L1 Mule → Victim chain automatically |
| Network Graph | Interactive pyvis graph showing full money flow with amounts on every edge |
| Evidence Tables | Colour-coded field-value evidence cards per layer (SIM swap / UPI / Transaction) |
| Event Timeline | Chronological event log from SIM swap to kingpin consolidation |
| FIR Brief | Structured, downloadable case brief with IPC section recommendations |

### Mock Data Scope

The tool ships with full mock data for **5 simultaneous victims** from a single Jamtara ring operation:

| Victim | City | Amount | L1 Mule | Kingpin |
|---|---|---|---|---|
| Ramesh Kumar | Patna, Bihar | ₹85,000 | Deepak Mandal | Santosh Mandal |
| Sunita Devi | Ranchi, Jharkhand | ₹1,20,000 | Sonu Yadav | Santosh Mandal |
| Manoj Singh | Dhanbad, Jharkhand | ₹67,500 | Raju Paswan | Santosh Mandal |
| Priya Sharma | Bokaro, Jharkhand | ₹95,000 | Bikram Tudu | Santosh Mandal |
| Anil Yadav | Gaya, Bihar | ₹53,000 | Chandan Mahto | Santosh Mandal |

**Total ring fraud: ₹4,20,500 in 12 minutes 12 seconds.**

### Data Layers

```
Telecom Tower Data     →  Device records (before + after SIM swap)
UPI Access Logs        →  Login events from criminal device
UPI Transaction Data   →  Money debit events
L1 Mule Profiles       →  First-layer mule account holders (Jamtara)
L1→L2 Splits           →  25 split transactions across 5 cities
L2 Mule Profiles       →  Second-layer mule account holders
L2→Kingpin Splits      →  125 micro-transfers to pre-kingpin accounts
Kingpin Profile        →  Final beneficiary identity + summary
```

### Correlation Engine

The `correlation_engine.py` runs 9 sequential steps on each submission:

```
Step 1 → Victim identity check
Step 2 → SIM swap detection (IMEI mismatch + impossible travel)
Step 3 → UPI access correlation
Step 4 → Transaction verification
Step 5 → L1 mule trace
Step 6 → L2 mule chain trace
Step 7 → Kingpin linkage
Step 8 → Fraud pattern classification (risk score 0–100)
Step 9 → Evidence timeline builder
```
