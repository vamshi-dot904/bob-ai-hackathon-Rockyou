# Problem Statement

## Real-World Case: Jamtara SIM-Swap Ring — Jharkhand, India

### Background

In FY2023, investigators in Jharkhand recorded **95,000+ UPI fraud cases** linked to a single district — **Jamtara**. This small district became the operational centre of an organised cyber fraud ring specialising in **SIM-swap attacks**.

### How the Fraud Works

The attackers follow a precise, scripted sequence:

```
Tower Data → Bank Data → Trap Data → Complaint Data
```

| Step | Time | Event |
|------|------|-------|
| 1 | T+0 | Criminal visits telecom retailer with fake ID — SIM swap approved |
| 2 | T+74s | UPI app accessed using OTP intercepted on swapped SIM |
| 3 | T+111s | Full account balance debited via UPI to Level 1 mule account |
| 4 | T+170s | L1 mule instantly splits funds across 5 different accounts in 5 cities |
| 5 | T+230s | Each L2 mule sends money to 5 pre-kingpin accounts across 5 more cities |
| 6 | T+290s | All 125 streams converge into the kingpin's single HDFC account |

### The Investigation Problem

Investigators had to **manually trace** connections between:
- Bank accounts
- SIM cards and IMEI numbers
- Telecom tower logs
- Device binding records
- Mule account hierarchies

This manual process took **weeks per case** and most cases went **unsolved** due to the lack of:
1. Network visualisation tools
2. Automated entity correlation
3. Cross-database linkage between telecom, bank, and device data
4. A structured way to map the criminal hierarchy

### Why It Matters

- **95,000+ victims** in a single financial year
- Average fraud amount: **₹4,20,500 per operation run** (5 victims in 13 minutes)
- **3-layer mule architecture** designed to defeat manual tracing
- Operations complete in **under 13 minutes** — faster than any human investigator can respond

### The Gap

> There was no tool that could take raw complaint data and automatically trace the full money trail from victim to kingpin, visualise the criminal network, and produce an FIR-ready case brief.

This is the problem this project solves.
