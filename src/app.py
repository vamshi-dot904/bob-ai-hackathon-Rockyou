"""
Cyber Fraud Investigation Dashboard
-------------------------------------
Jamtara SIM-Swap Ring — Investigation Platform
Submit a victim complaint → correlation engine traces the full
SIM-swap → UPI access → L1 mule → L2 mules → Kingpin chain.
"""

import csv
import json
import os
import re
import tempfile
from datetime import date, time as dtime

import pandas as pd
import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

from correlation_engine import correlate

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cyber Fraud Investigation Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #1e2530;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] { font-size: 0.75rem; color: #8a9bb5; text-transform: uppercase; letter-spacing: .05em; }
[data-testid="stMetricValue"] { font-size: 1.35rem; font-weight: 700; }

/* ── Section cards ── */
.card {
    background: #1a2235;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.card-red    { border-left: 5px solid #e74c3c; }
.card-orange { border-left: 5px solid #e67e22; }
.card-yellow { border-left: 5px solid #f1c40f; }
.card-blue   { border-left: 5px solid #3498db; }
.card-green  { border-left: 5px solid #2ecc71; }

/* ── Badge pills ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
}
.badge-red    { background:#4d1a1a; color:#e74c3c; border:1px solid #e74c3c; }
.badge-orange { background:#4d3010; color:#e67e22; border:1px solid #e67e22; }
.badge-green  { background:#0d3320; color:#2ecc71; border:1px solid #2ecc71; }
.badge-blue   { background:#0d2040; color:#3498db; border:1px solid #3498db; }
.badge-yellow { background:#3d3000; color:#f1c40f; border:1px solid #f1c40f; }
.badge-grey   { background:#2a2a2a; color:#aaa;    border:1px solid #555; }

/* ── Timeline ── */
.tl-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid #2d3748;
}
.tl-row:last-child { border-bottom: none; }
.tl-time {
    min-width: 155px;
    font-family: monospace;
    font-size: 0.82rem;
    color: #8a9bb5;
    padding-top: 2px;
}
.tl-icon { font-size: 1.2rem; min-width: 26px; }
.tl-event { font-size: 0.9rem; color: #e0e6f0; flex: 1; }
.tl-city { font-size: 0.78rem; color: #8a9bb5; margin-top: 3px; }

/* ── Field-value table ── */
.fv-table { width:100%; border-collapse:collapse; font-size:0.88rem; }
.fv-table tr:nth-child(even) td { background:#1a2235; }
.fv-table tr:nth-child(odd)  td { background:#151d2b; }
.fv-table td { padding: 7px 12px; color: #ccd6e8; border-bottom: 1px solid #2d3748; }
.fv-table td:first-child { color:#8a9bb5; font-weight:600; width:42%; }

/* ── Tree node labels ── */
.tree-kp  { color:#e74c3c; font-size:1.05rem; font-weight:700; }
.tree-l1  { color:#e67e22; font-size:0.98rem; font-weight:600; }
.tree-l2  { color:#f1c40f; font-size:0.9rem; }
.tree-vic { color:#3498db; font-size:0.9rem; }

/* ── Alert banners ── */
.alert-red  { background:#2d1010; border:1px solid #e74c3c; border-radius:8px; padding:12px 16px; color:#f5a5a5; margin:8px 0; }
.alert-green{ background:#0d2515; border:1px solid #2ecc71; border-radius:8px; padding:12px 16px; color:#90f0b8; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
DATA_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CASES_DIR = os.path.join(DATA_DIR, "cases")

DEMO_VICTIMS = [
    {"label": "Ramesh Kumar",  "name": "Ramesh Kumar",  "city": "Patna",   "state": "Bihar",
     "phone": "9876543210", "imei": "354678901234567", "bank_name": "Axis Bank",
     "bank_account": "9140056789123",  "amount": 85000.0,
     "incident_date": "2023-04-10", "incident_time": "10:23:00"},
    {"label": "Sunita Devi",   "name": "Sunita Devi",   "city": "Ranchi",  "state": "Jharkhand",
     "phone": "9123456780", "imei": "357891234567890", "bank_name": "State Bank of India",
     "bank_account": "3567891234560",  "amount": 120000.0,
     "incident_date": "2023-04-10", "incident_time": "10:26:00"},
    {"label": "Manoj Singh",   "name": "Manoj Singh",   "city": "Dhanbad", "state": "Jharkhand",
     "phone": "9988776655", "imei": "352345678901234", "bank_name": "HDFC Bank",
     "bank_account": "5023456789012",  "amount": 67500.0,
     "incident_date": "2023-04-10", "incident_time": "10:29:00"},
    {"label": "Priya Sharma",  "name": "Priya Sharma",  "city": "Bokaro",  "state": "Jharkhand",
     "phone": "9765432109", "imei": "356789012345678", "bank_name": "ICICI Bank",
     "bank_account": "6234567890123",  "amount": 95000.0,
     "incident_date": "2023-04-10", "incident_time": "10:32:00"},
    {"label": "Anil Yadav",    "name": "Anil Yadav",    "city": "Gaya",    "state": "Bihar",
     "phone": "9654321098", "imei": "351234567890123", "bank_name": "Punjab National Bank",
     "bank_account": "7345678901234",  "amount": 53000.0,
     "incident_date": "2023-04-10", "incident_time": "10:35:00"},
]

# ── RENDER HELPERS ────────────────────────────────────────────────────────────
def _fv_table(rows: list[tuple]) -> str:
    """Render a field-value HTML table from list of (field, value) tuples."""
    inner = "".join(f"<tr><td>{f}</td><td>{v}</td></tr>" for f, v in rows)
    return f"<table class='fv-table'>{inner}</table>"

def _badge(text: str, colour: str = "grey") -> str:
    return f"<span class='badge badge-{colour}'>{text}</span>"

def _card(content: str, colour: str = "blue") -> str:
    return f"<div class='card card-{colour}'>{content}</div>"

def _alert(text: str, kind: str = "red") -> str:
    return f"<div class='alert-{kind}'>{text}</div>"

# ── HELPERS ───────────────────────────────────────────────────────────────────
def _save_case_files(case_id: str, case: dict) -> None:
    os.makedirs(CASES_DIR, exist_ok=True)
    safe_id = re.sub(r"[^\w\-]", "_", case_id)
    with open(os.path.join(CASES_DIR, f"{safe_id}.json"), "w", encoding="utf-8") as f:
        json.dump(case, f, indent=2, default=str)
    with open(os.path.join(CASES_DIR, f"{safe_id}.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(case.keys()))
        writer.writeheader()
        writer.writerow(case)


def _validate_case_form(fields: dict) -> dict:
    errors = {}
    if not fields["name"].strip():
        errors["name"] = "Full Name is required."
    if not fields["state"].strip():
        errors["state"] = "State is required."
    if not fields["city"].strip():
        errors["city"] = "City is required."
    if not fields["phone"].strip():
        errors["phone"] = "Phone Number is required."
    elif not re.fullmatch(r"[6-9]\d{9}", fields["phone"].strip()):
        errors["phone"] = "Enter a valid 10-digit Indian mobile number (starts with 6–9)."
    imei1 = fields["imei1"].strip()
    if not imei1:
        errors["imei1"] = "IMEI Number 1 is required."
    elif not re.fullmatch(r"\d{15}", imei1):
        errors["imei1"] = "IMEI must be exactly 15 digits."
    if not fields["bank_name"].strip():
        errors["bank_name"] = "Bank Name is required."
    if not fields["bank_account"].strip():
        errors["bank_account"] = "Bank Account Number is required."
    if fields["amount"] is None or fields["amount"] <= 0:
        errors["amount"] = "Amount Debited must be greater than zero."
    if fields["incident_date"] is None:
        errors["incident_date"] = "Date of Incident is required."
    if fields["incident_time"] is None:
        errors["incident_time"] = "Exact Time of Incident is required."
    return errors


# =============================================================================
# CASE ENTRY FORM
# =============================================================================
def _show_case_entry():
    """Landing page + multi-section complaint form."""

    # ── Landing ──────────────────────────────────────────────────────────────
    if not st.session_state.get("show_case_form", False):
        st.markdown("""
        <div style='text-align:center; padding: 3rem 0 1rem 0;'>
            <div style='font-size:3rem;'>🔍</div>
            <h1 style='font-size:2.2rem; font-weight:800; margin:0.4rem 0;'>
                Cyber Fraud Investigation System
            </h1>
            <p style='color:#8a9bb5; font-size:1.05rem; margin:0;'>
                Jamtara SIM-Swap Ring &nbsp;|&nbsp; Powered by Correlation Intelligence
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Stats banner
        st.markdown("""
        <div style='display:flex; gap:16px; justify-content:center; margin:1.5rem 0;'>
            <div class='card card-red' style='text-align:center; min-width:140px; padding:14px;'>
                <div style='font-size:1.6rem; font-weight:800; color:#e74c3c;'>95,000+</div>
                <div style='font-size:0.75rem; color:#8a9bb5;'>UPI FRAUD CASES FY2023</div>
            </div>
            <div class='card card-orange' style='text-align:center; min-width:140px; padding:14px;'>
                <div style='font-size:1.6rem; font-weight:800; color:#e67e22;'>3 LAYERS</div>
                <div style='font-size:0.75rem; color:#8a9bb5;'>MULE HIERARCHY</div>
            </div>
            <div class='card card-blue' style='text-align:center; min-width:140px; padding:14px;'>
                <div style='font-size:1.6rem; font-weight:800; color:#3498db;'>&lt; 13 MIN</div>
                <div style='font-size:0.75rem; color:#8a9bb5;'>FULL OPERATION TIME</div>
            </div>
            <div class='card card-green' style='text-align:center; min-width:140px; padding:14px;'>
                <div style='font-size:1.6rem; font-weight:800; color:#2ecc71;'>100/100</div>
                <div style='font-size:0.75rem; color:#8a9bb5;'>CORRELATION SCORE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='text-align:center; color:#8a9bb5; font-size:0.9rem;'>Select a demo victim to auto-fill the complaint form, or create a new case manually.</p>", unsafe_allow_html=True)

        cols = st.columns(5)
        icons = ["👨", "👩", "👨", "👩", "👨"]
        for i, v in enumerate(DEMO_VICTIMS):
            with cols[i]:
                st.markdown(f"<div style='text-align:center; color:#8a9bb5; font-size:0.75rem; margin-bottom:4px;'>{icons[i]} VICTIM {i+1}</div>", unsafe_allow_html=True)
                if st.button(v["label"], use_container_width=True, key=f"demo_{i}"):
                    st.session_state["_demo_prefill"] = v
                    st.session_state["show_case_form"] = True
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_c, col_r = st.columns([2, 1, 2])
        with col_c:
            if st.button("➕  File a New Complaint", use_container_width=True, type="primary"):
                st.session_state.pop("_demo_prefill", None)
                st.session_state["show_case_form"] = True
                st.rerun()
        return False

    # ── Form ─────────────────────────────────────────────────────────────────
    pre    = st.session_state.get("_demo_prefill", {})
    errors = st.session_state.get("_case_errors", {})

    if "cf_suspicious_message" not in st.session_state:
        st.session_state["cf_suspicious_message"] = "No"

    st.markdown("## 📋 New Investigation Case")
    st.caption("All fields marked * are required. Your submission is matched against the investigation database in real time.")

    # ── Section 1: Victim ────────────────────────────────────────────────────
    st.markdown("""<div class='card card-blue'><b style='color:#3498db;'>👤 SECTION 1 — VICTIM INFORMATION</b></div>""", unsafe_allow_html=True)
    with st.form("case_form_a"):
        case_id_val = st.text_input(
            "Case ID *", placeholder="e.g. JMT-2023-0001",
            value=f"JMT-2023-{pre.get('phone','0000')[-4:]}",
            key="cf_case_id",
        )
        c1, c2 = st.columns(2)
        with c1:
            name  = st.text_input("Full Name *",    value=pre.get("name",""),  placeholder="e.g. Ramesh Kumar", key="cf_name")
            state = st.text_input("State *",        value=pre.get("state",""), placeholder="e.g. Bihar",        key="cf_state")
        with c2:
            city  = st.text_input("City *",         value=pre.get("city",""),  placeholder="e.g. Patna",        key="cf_city")
            phone = st.text_input("Phone Number *", value=pre.get("phone",""), placeholder="10-digit mobile",   key="cf_phone")
        for fld in ["name","state","city","phone"]:
            if errors.get(fld): st.error(errors[fld])

        # ── Section 2: Device ────────────────────────────────────────────────
        st.markdown("""<div class='card card-orange' style='margin-top:12px;'><b style='color:#e67e22;'>📱 SECTION 2 — DEVICE DETAILS</b></div>""", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            imei1 = st.text_input("IMEI Number 1 *", value=pre.get("imei",""), placeholder="15-digit IMEI (dial *#06#)", key="cf_imei1")
        with c4:
            imei2 = st.text_input("IMEI Number 2 (dual-SIM, optional)", placeholder="15-digit IMEI", key="cf_imei2")
        for fld in ["imei1","imei2"]:
            if errors.get(fld): st.error(errors[fld])

        st.form_submit_button(" ", disabled=True)

    # ── Suspicious message widget (outside form — reactive) ──────────────────
    st.markdown("""<div class='card card-yellow' style='margin-top:4px;'><b style='color:#f1c40f;'>💬 SUSPICIOUS MESSAGE?</b></div>""", unsafe_allow_html=True)
    suspicious_message = st.radio(
        "Suspicious Message?", options=["No", "Yes"], horizontal=True,
        index=0, key="cf_suspicious_message", label_visibility="collapsed",
    )
    message_type = None
    if suspicious_message == "Yes":
        st.caption("Select the type of suspicious message received:")
        cur_type = st.session_state.get("cf_message_type")
        ckyc, cotp, _r = st.columns([1, 1, 4])
        with ckyc:
            if st.button("KYC Update", type="primary" if cur_type == "KYC" else "secondary", key="cf_msg_kyc"):
                st.session_state["cf_message_type"] = "KYC"
                st.rerun()
        with cotp:
            if st.button("OTP Request", type="primary" if cur_type == "OTP" else "secondary", key="cf_msg_otp"):
                st.session_state["cf_message_type"] = "OTP"
                st.rerun()
        message_type = st.session_state.get("cf_message_type")
        if message_type:
            st.success(f"Message type selected: **{message_type}**")

    # ── Section 3: Financial ─────────────────────────────────────────────────
    st.markdown("""<div class='card card-green' style='margin-top:4px;'><b style='color:#2ecc71;'>🏦 SECTION 3 — FINANCIAL DETAILS</b></div>""", unsafe_allow_html=True)
    with st.form("case_form_b"):
        c5, c6 = st.columns(2)
        with c5:
            bank_name    = st.text_input("Bank Name *",           value=pre.get("bank_name",""),    key="cf_bank_name")
            bank_account = st.text_input("Bank Account Number *", value=pre.get("bank_account",""), key="cf_bank_account")
            amount = st.number_input(
                "Amount Debited (Rs.) *", min_value=0.01, step=1.0,
                value=pre.get("amount", None), placeholder="e.g. 85000", format="%.2f",
                key="cf_amount",
            )
            transaction_ref = st.text_input("Transaction ID / UTR (optional)", key="cf_txn_ref")
        with c6:
            _idate = None
            try:
                _idate = date.fromisoformat(pre["incident_date"]) if pre.get("incident_date") else None
            except Exception:
                pass
            incident_date = st.date_input("Date of Incident *", value=_idate, key="cf_incident_date")

            _itime = None
            try:
                if pre.get("incident_time"):
                    h, m, *_ = pre["incident_time"].split(":")
                    _itime = dtime(int(h), int(m))
            except Exception:
                pass
            incident_time = st.time_input("Exact Time of Incident *", value=_itime, key="cf_incident_time", step=60)

            payment_channel = st.selectbox(
                "Payment Channel *",
                options=["", "UPI", "Net Banking", "Debit Card", "Credit Card", "Other"],
                index=1, key="cf_payment_channel",
            )
            num_transactions = st.number_input("No. of Suspicious Transactions *", min_value=1, step=1, value=1, key="cf_num_transactions")

        for fld in ["bank_name","bank_account","amount","incident_date","incident_time"]:
            if errors.get(fld): st.error(errors[fld])

        c7, c8 = st.columns(2)
        with c7:
            new_beneficiary = st.selectbox(
                "Transaction sent to new/unknown beneficiary? *",
                options=["", "Yes", "No", "Don't Know"], index=1, key="cf_new_beneficiary",
            )
        with c8:
            recipient_ref = st.text_input("Recipient UPI ID / Account (optional)", key="cf_recipient_ref")

        # ── Additional ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**🚨 Additional Indicators**")
        c9, _ = st.columns(2)
        with c9:
            suspicious_call = st.radio(
                "Suspicious call received before fraud?", options=["No", "Yes"],
                horizontal=True, index=0, key="cf_suspicious_call",
            )

        st.markdown("---")
        submitted = st.form_submit_button("🚀  Submit & Investigate", type="primary", use_container_width=True)

    if errors:
        st.error("Please correct the highlighted errors above before submitting.")

    # ── Handle submission ─────────────────────────────────────────────────────
    if submitted:
        amount_val  = float(amount) if amount is not None else None
        num_txn_val = int(num_transactions) if num_transactions is not None else 1
        case_id     = (st.session_state.get("cf_case_id") or "").strip() or "case"

        fields = {
            "case_id":          case_id,
            "name":             st.session_state.get("cf_name",""),
            "state":            st.session_state.get("cf_state",""),
            "city":             st.session_state.get("cf_city",""),
            "phone":            st.session_state.get("cf_phone",""),
            "imei1":            st.session_state.get("cf_imei1",""),
            "imei2":            st.session_state.get("cf_imei2",""),
            "bank_name":        bank_name,
            "bank_account":     bank_account,
            "amount":           amount_val,
            "incident_date":    incident_date,
            "incident_time":    incident_time,
            "transaction_ref":  transaction_ref,
            "payment_channel":  payment_channel,
            "num_transactions": num_txn_val,
            "new_beneficiary":  new_beneficiary,
            "recipient_ref":    recipient_ref,
        }

        val_errors = _validate_case_form(fields)
        if val_errors:
            st.session_state["_case_errors"] = val_errors
            st.rerun()
        else:
            active_case = {
                "case_id":            case_id,
                "name":               fields["name"].strip(),
                "state":              fields["state"].strip(),
                "city":               fields["city"].strip(),
                "phone":              fields["phone"].strip(),
                "imei":               fields["imei1"].strip(),
                "imei1":              fields["imei1"].strip(),
                "imei2":              fields["imei2"].strip(),
                "bank_name":          fields["bank_name"].strip(),
                "account":            fields["bank_account"].strip(),
                "bank_account":       fields["bank_account"].strip(),
                "amount":             fields["amount"],
                "incident_dt":        str(fields["incident_date"]),
                "incident_date":      str(fields["incident_date"]),
                "incident_time":      str(fields["incident_time"]),
                "transaction_ref":    fields["transaction_ref"].strip(),
                "payment_channel":    fields["payment_channel"],
                "num_transactions":   fields["num_transactions"],
                "new_beneficiary":    fields["new_beneficiary"],
                "recipient_ref":      fields["recipient_ref"].strip(),
                "suspicious_message": suspicious_message == "Yes",
                "message_type":       message_type,
                "suspicious_call":    suspicious_call == "Yes",
            }
            _save_case_files(case_id, active_case)
            st.session_state["active_case"]   = active_case
            st.session_state["case_submitted"] = True
            st.session_state.pop("_case_errors", None)
            st.session_state.pop("show_case_form", None)
            st.session_state.pop("_demo_prefill", None)
            st.rerun()

    return False


# ── GATE ──────────────────────────────────────────────────────────────────────
if not st.session_state.get("case_submitted", False):
    _show_case_entry()
    st.stop()


# =============================================================================
# INVESTIGATION WORKSPACE
# =============================================================================
_ac = st.session_state.get("active_case", {})

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🔍 Investigation Panel")
st.sidebar.markdown(f"""
<div class='card card-blue' style='font-size:0.85rem;'>
<b>Case ID</b><br><code>{_ac.get('case_id','—')}</code><br><br>
<b>Victim</b><br>{_ac.get('name','—')}<br><br>
<b>Location</b><br>{_ac.get('city','—')}, {_ac.get('state','—')}<br><br>
<b>Phone</b><br>{_ac.get('phone','—')}<br><br>
<b>Bank Account</b><br>{_ac.get('account','—')}<br><br>
<b>Amount Reported</b><br><span style='color:#e74c3c;font-weight:700;'>Rs. {_ac.get('amount',0):,.2f}</span><br><br>
<b>Incident Date</b><br>{_ac.get('incident_dt','—')}
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
if st.sidebar.button("🔄  New Case / Switch Victim", use_container_width=True):
    for k in ["case_submitted","active_case","show_case_form","_demo_prefill"]:
        st.session_state.pop(k, None)
    st.rerun()

investigator_name = st.sidebar.text_input("Investigating Officer Name", value="", placeholder="Enter officer name")

# ── Correlation ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Correlating complaint against investigation database...")
def _run_correlation(phone, imei, bank_account, amount):
    return correlate({
        "phone_number":   phone,
        "imei":           imei,
        "bank_account":   bank_account,
        "amount_debited": int(amount) if amount else 0,
    })


cr  = _run_correlation(_ac["phone"], _ac.get("imei",""), _ac.get("bank_account",""), _ac.get("amount",0))
vi  = cr.get("victim_identity", {})
sw  = cr.get("sim_swap", {})
ua  = cr.get("upi_access", {})
txn = cr.get("transaction", {})
l1  = cr.get("l1_mule", {})
l2  = cr.get("l2_mules", {})
kp  = cr.get("kingpin", {})
pt  = cr.get("fraud_pattern", {})
tl  = cr.get("evidence_timeline", [])

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:12px; padding:8px 0 4px 0;'>
    <span style='font-size:2rem;'>🔍</span>
    <div>
        <h1 style='margin:0; font-size:1.6rem; font-weight:800;'>Cyber Fraud Investigation Tool</h1>
        <p style='margin:0; color:#8a9bb5; font-size:0.85rem;'>SIM-Swap Ring Investigation &nbsp;·&nbsp; Jamtara, Jharkhand &nbsp;·&nbsp; FY 2023</p>
    </div>
</div>
""", unsafe_allow_html=True)

if cr.get("status") == "NO_MATCH":
    st.markdown(_alert(f"No match found in investigation database: {cr.get('detail')} — please verify the phone number and IMEI."), unsafe_allow_html=True)
    st.stop()

# ── TOP METRICS ───────────────────────────────────────────────────────────────
score = pt.get("risk_score", 0)
score_color = "#e74c3c" if score >= 80 else ("#e67e22" if score >= 50 else "#f1c40f")
score_label = "CRITICAL" if score >= 80 else ("HIGH" if score >= 50 else "MEDIUM")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Victim",         vi.get("victim_name","—"))
m2.metric("Fraud Pattern",  "SIM-Swap Mule Ring" if pt.get("gang_involved") else "UPI Fraud")
m3.metric("Risk Score",     f"{score}/100 — {score_label}")
m4.metric("Amount Stolen",  f"Rs. {txn.get('amount_debited',0):,}")
m5.metric("Op Duration",    f"{kp.get('ring_operation_mins','—')} min")

m6, m7, m8 = st.columns(3)
m6.metric("L1 Mule (Direct Receiver)", f"{l1.get('holder_name','—')} · {l1.get('city','—')}")
m7.metric("L2 Mule Accounts",          l2.get("total_l2", 0))
m8.metric("Kingpin",                   f"{kp.get('name','—')} ({kp.get('alias','—')})")

# ── FLAG PILLS ────────────────────────────────────────────────────────────────
flag_colours = {
    "SIM_SWAP_DETECTED":                "red",
    "IMPOSSIBLE_LOCATION_JUMP":         "red",
    "AUTOMATED_UPI_ACCESS_UNDER_120S":  "orange",
    "FRAUDULENT_DEBIT_CONFIRMED":       "orange",
    "LAYERED_MULE_SPLITTING_DETECTED":  "yellow",
}
pills = " ".join(_badge(f, flag_colours.get(f, "grey")) for f in pt.get("flags", []))
st.markdown(f"<div style='margin:8px 0 4px 0;'><b style='color:#8a9bb5;font-size:0.8rem;'>DETECTION FLAGS &nbsp;</b>{pills}</div>", unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# TABS
# =============================================================================
tab_network, tab_hierarchy, tab_evidence, tab_timeline, tab_brief = st.tabs([
    "🕸️  Network Graph",
    "🏛️  Org Hierarchy",
    "🔍  Evidence Detail",
    "📅  Event Timeline",
    "📄  FIR Brief",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — NETWORK GRAPH
# ─────────────────────────────────────────────────────────────────────────────
with tab_network:
    st.markdown("### Money Flow Network")
    st.markdown("""
    <div style='display:flex; gap:16px; margin-bottom:12px; font-size:0.82rem;'>
        <span>🔵 <b>Victim</b> — money source</span>
        <span>🟠 <b>L1 Mule</b> — first receiver in Jamtara</span>
        <span>🟡 <b>L2 Mules</b> — split across 5 cities</span>
        <span>⭐ <b>Kingpin</b> — final beneficiary</span>
    </div>
    """, unsafe_allow_html=True)

    net = Network(height="640px", width="100%", directed=True, bgcolor="#0e1117", font_color="white")
    net.set_options('{"physics":{"stabilization":{"iterations":150},"barnesHut":{"gravitationalConstant":-10000,"springLength":180}}}')

    victim_node = vi.get("victim_name", "Victim")
    l1_node     = l1.get("mule_id", "L1-MULE")
    kp_node     = kp.get("kingpin_id", "KINGPIN")

    # Victim node
    net.add_node(victim_node,
                 label=f"VICTIM\n{victim_node}\n{vi.get('home_city','')}",
                 color="#3498db", size=30, shape="dot",
                 title=(f"<b>VICTIM</b><br>Name: {vi.get('victim_name')}<br>"
                        f"Phone: {vi.get('phone')}<br>IMEI: {vi.get('original_imei')}<br>"
                        f"City: {vi.get('home_city')}, {vi.get('home_state')}<br>"
                        f"Bank: {ua.get('bank_name')}<br>UPI: {ua.get('upi_id')}"))

    # Kingpin node — added first so L2→KP edges work
    net.add_node(kp_node,
                 label=f"KINGPIN\n{kp.get('name','')}\n({kp.get('alias','')})",
                 color="#e74c3c", size=40, shape="star",
                 title=(f"<b>KINGPIN</b><br>Name: {kp.get('name')} ({kp.get('alias')})<br>"
                        f"Phone: {kp.get('phone')}<br>Bank: {kp.get('bank_name')}<br>"
                        f"A/C: {kp.get('bank_account')}<br>City: {kp.get('city')}<br>"
                        f"Total Ring Fraud: Rs.{kp.get('total_amount_in_ring',0):,}"))

    # L1 mule node
    net.add_node(l1_node,
                 label=f"L1 MULE\n{l1.get('holder_name','')}\n{l1.get('city','')}",
                 color="#e67e22", size=26, shape="dot",
                 title=(f"<b>L1 MULE</b><br>Name: {l1.get('holder_name')}<br>"
                        f"Phone: {l1.get('phone')}<br>Bank: {l1.get('bank_name')}<br>"
                        f"City: {l1.get('city')}<br>Recruited by: {l1.get('recruited_by')}<br>"
                        f"Received: Rs.{l1.get('amount_received',0):,}"))
    net.add_edge(victim_node, l1_node,
                 title=f"Rs.{l1.get('amount_received',0):,} via UPI (fraud)",
                 label=f"Rs.{l1.get('amount_received',0):,}",
                 color="#e67e22", width=4)

    # L2 mule nodes
    for sp in l1.get("l2_splits", []):
        l2_node = sp["to_account"]
        l2_prof = next((m for m in l2.get("l2_mules", []) if m["mule_id"] == l2_node), {})
        net.add_node(l2_node,
                     label=f"L2 MULE\n{sp['to_holder']}\n{sp['to_city']}",
                     color="#f1c40f", size=20, shape="dot",
                     title=(f"<b>L2 MULE</b><br>Name: {sp['to_holder']}<br>"
                            f"City: {sp['to_city']}<br>Bank: {l2_prof.get('bank','—')}<br>"
                            f"Received: Rs.{sp['amount']:,}<br>Split time: {sp['split_time']}<br>"
                            f"Pre-KP transfers: {len(l2_prof.get('pre_kp_splits',[]))}"))
        net.add_edge(l1_node, l2_node,
                     title=f"Rs.{sp['amount']:,} — split at {sp['split_time']}",
                     label=f"Rs.{sp['amount']:,}",
                     color="#f1c40f", width=2)
        # L2 → Kingpin (aggregated via pre-KP accounts)
        total_to_kp = sum(pk["amount"] for pk in l2_prof.get("pre_kp_splits", []))
        if total_to_kp:
            net.add_edge(l2_node, kp_node,
                         title=f"Rs.{total_to_kp:,} aggregated to kingpin via {len(l2_prof.get('pre_kp_splits',[]))} transfers",
                         color="#e74c3c", width=1)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        html_content = open(tmp.name, "r", encoding="utf-8").read()
    components.html(html_content, height=660, scrolling=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — ORG HIERARCHY
# ─────────────────────────────────────────────────────────────────────────────
with tab_hierarchy:
    st.markdown("### Fraud Ring Organisational Hierarchy")
    st.caption("Money flows from victim upward through 3 layers before reaching the kingpin.")

    # Kingpin card
    st.markdown(_card(f"""
    <div class='tree-kp'>⭐ KINGPIN — {kp.get('kingpin_id')} — {kp.get('name')} &nbsp;
        {_badge('ORGANISED GANG', 'red')} {_badge('PRIMARY ACCUSED', 'red')}
    </div>
    <div style='margin-top:10px;'>{_fv_table([
        ("Alias",           kp.get("alias","—")),
        ("Phone",           kp.get("phone","—")),
        ("UPI ID",          kp.get("upi_id","—")),
        ("Bank",            kp.get("bank_name","—")),
        ("Account",         kp.get("bank_account","—")),
        ("City",            kp.get("city","—")),
        ("Total Victims",   kp.get("total_victims_in_ring","—")),
        ("Total Ring Fraud",f"Rs. {kp.get('total_amount_in_ring',0):,}"),
        ("Op Duration",     f"{kp.get('ring_operation_mins','—')} minutes"),
    ])}</div>
    """, "red"), unsafe_allow_html=True)

    # L1 mule card
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;⬇️ *sent money to*")
    st.markdown(_card(f"""
    <div class='tree-l1'>🟠 L1 MULE — {l1.get('mule_id')} — {l1.get('holder_name')} &nbsp;
        {_badge('DIRECT RECEIVER', 'orange')} {_badge('JAMTARA', 'orange')}
    </div>
    <div style='margin-top:10px;'>{_fv_table([
        ("Phone",            l1.get("phone","—")),
        ("UPI ID",           l1.get("upi_id","—")),
        ("Bank",             l1.get("bank_name","—")),
        ("Account",          l1.get("bank_account","—")),
        ("City",             l1.get("city","—")),
        ("Recruited By",     l1.get("recruited_by","—")),
        ("Amount Received",  f"Rs. {l1.get('amount_received',0):,}"),
        ("Split Into",       f"{len(l1.get('l2_splits',[]))} L2 accounts within ~60 seconds"),
    ])}</div>
    """, "orange"), unsafe_allow_html=True)

    # L2 mules table
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️ *split into 5 L2 mule accounts*")
    l2_rows = []
    for m in l2.get("l2_mules", []):
        l2_rows.append({
            "Mule ID":            m["mule_id"],
            "Holder Name":        m["holder_name"],
            "Phone":              m["phone"],
            "City":               m["city"],
            "Bank":               m["bank"],
            "Received (Rs.)":     m["amount_received"],
            "Received At":        m["received_at"],
            "Pre-KP Transfers":   len(m.get("pre_kp_splits",[])),
        })
    if l2_rows:
        st.dataframe(
            pd.DataFrame(l2_rows).style
              .set_properties(**{"background-color": "#1a2235", "color": "#ccd6e8", "border-color": "#2d3748"}),
            use_container_width=True,
            hide_index=True,
        )

    # Victim card
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️ *originally stolen from*")
    st.markdown(_card(f"""
    <div class='tree-vic'>🔵 VICTIM — {vi.get('victim_name')} &nbsp;
        {_badge('COMPLAINANT', 'blue')} {_badge(vi.get('home_city','—'), 'blue')}
    </div>
    <div style='margin-top:10px;'>{_fv_table([
        ("Phone",          vi.get("phone","—")),
        ("City / State",   f"{vi.get('home_city','—')}, {vi.get('home_state','—')}"),
        ("Original IMEI",  vi.get("original_imei","—")),
        ("UPI ID",         ua.get("upi_id","—")),
        ("Bank",           ua.get("bank_name","—")),
        ("Account",        ua.get("bank_account","—")),
        ("Amount Stolen",  f"Rs. {txn.get('amount_debited',0):,}"),
    ])}</div>
    """, "blue"), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — EVIDENCE DETAIL
# ─────────────────────────────────────────────────────────────────────────────
with tab_evidence:
    # ── SIM Swap
    st.markdown("### 1. SIM Swap Evidence")
    swap_confirmed = sw.get("status") == "SIM_SWAP_CONFIRMED"
    if swap_confirmed:
        st.markdown(_alert(
            f"SIM SWAP CONFIRMED — Criminal IMEI <b>{sw.get('criminal_imei')}</b> registered at "
            f"<b>{sw.get('swap_city')}</b> ({sw.get('distance_km')} km from victim's city) "
            f"on <b>{sw.get('swap_timestamp')}</b>"
        ), unsafe_allow_html=True)
    else:
        st.markdown(_alert("SIM swap status could not be confirmed.", "green"), unsafe_allow_html=True)

    _swap_table = _fv_table([
        ("Status",               _badge(sw.get("status", "—"), "red" if swap_confirmed else "grey")),
        ("Victim Original IMEI", sw.get("original_imei", "—")),
        ("Criminal IMEI (New)",  _badge(sw.get("criminal_imei", "—"), "red")),
        ("IMEI Changed?",        _badge("YES — Confirmed", "red") if sw.get("imei_changed") else _badge("NO", "green")),
        ("Victim City (Before)", sw.get("previous_city", "—")),
        ("Criminal Location",    f"{sw.get('swap_city','—')}, {sw.get('swap_state','—')}"),
        ("Tower ID",             sw.get("swap_tower", "—")),
        ("Impossible Travel",    f"{sw.get('distance_km','—')} km in 0 seconds — physical impossibility"),
        ("SIM Swap Timestamp",   sw.get("swap_timestamp", "—")),
        ("First UPI Access",     sw.get("first_upi_access", "—")),
        ("Swap to UPI Gap",      f"{sw.get('seconds_swap_to_upi','—')} seconds — automated attack"),
        ("Victim IMEI Verified", _badge("YES", "green") if sw.get("victim_imei_verified") else _badge("NO", "grey")),
    ])
    st.markdown(_card(_swap_table, "red"), unsafe_allow_html=True)

    # ── UPI Access
    st.markdown("### 2. UPI Access Evidence")
    st.markdown(_alert(
        f"UNAUTHORIZED UPI LOGIN — Access from <b>{ua.get('access_city')}</b> (IP: {ua.get('access_ip')}) "
        f"using criminal IMEI <b>{ua.get('criminal_imei')}</b>. OTP intercepted via swapped SIM."
    ), unsafe_allow_html=True)
    _upi_table = _fv_table([
        ("Status",               _badge(ua.get("status", "—"), "red")),
        ("UPI ID",               ua.get("upi_id", "—")),
        ("Bank",                 ua.get("bank_name", "—")),
        ("Bank Account",         ua.get("bank_account", "—")),
        ("Access Time",          ua.get("access_time", "—")),
        ("Access City",          _badge(ua.get("access_city", "—"), "red")),
        ("Access IP",            ua.get("access_ip", "—")),
        ("Criminal Device IMEI", _badge(ua.get("criminal_imei", "—"), "red")),
        ("Access Method",        ua.get("access_type", "—")),
        ("OTP Delivered To",     str(ua.get("otp_hijacked_to", "—")) + " (hijacked — criminal's SIM)"),
        ("Seconds After Swap",   f"{ua.get('seconds_after_swap','—')} seconds"),
        ("Automated Attack?",    _badge("YES", "red") if ua.get("automated_attack") else _badge("NO", "green")),
    ])
    st.markdown(_card(_upi_table, "orange"), unsafe_allow_html=True)

    # ── Transaction
    st.markdown("### 3. Transaction Evidence")
    _txn_st = "red" if txn.get("status") == "TRANSACTION_CONFIRMED" else "grey"
    _txn_table = _fv_table([
        ("Status",                _badge(txn.get("status", "—"), _txn_st)),
        ("Transaction ID",        txn.get("txn_id", "—")),
        ("UPI ID",                txn.get("upi_id", "—")),
        ("Amount Debited",        _badge(f"Rs. {txn.get('amount_debited',0):,}", "red")),
        ("Amount Matches Report", _badge("YES — Verified", "red") if txn.get("amount_match") else _badge("MISMATCH", "orange")),
        ("Transaction Time",      txn.get("txn_time", "—")),
        ("Transaction City",      _badge(txn.get("txn_city", "—"), "red")),
        ("Receiver UPI",          txn.get("receiver_upi", "—")),
        ("Receiver Account",      _badge(txn.get("receiver_account", "—"), "orange")),
        ("Transaction Status",    txn.get("txn_status", "—")),
        ("Seconds After Login",   f"{txn.get('seconds_after_upi_access','—')} seconds"),
    ])
    st.markdown(_card(_txn_table, "yellow"), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — EVENT TIMELINE
# ─────────────────────────────────────────────────────────────────────────────
with tab_timeline:
    st.markdown("### Chronological Evidence Timeline")
    st.caption("Every correlated event from SIM swap to final kingpin consolidation, in exact time order.")

    ICON_MAP = {
        "SIM SWAP":  ("🔴", "red"),
        "UPI login": ("🔵", "blue"),
        "access":    ("🔵", "blue"),
        "debited":   ("🟠", "orange"),
        "split":     ("🟡", "yellow"),
        "kingpin":   ("⭐", "red"),
    }

    if tl:
        tl_html = "<div class='card'>"
        for ev in tl:
            ev_lower = ev["event"].lower()
            icon, col = "⚪", "grey"
            for kw, (ic, cl) in ICON_MAP.items():
                if kw.lower() in ev_lower:
                    icon, col = ic, cl
                    break
            badge_html = _badge(ev["city"], col)
            tl_html += f"""
            <div class='tl-row'>
                <div class='tl-time'>{ev['time']}</div>
                <div class='tl-icon'>{icon}</div>
                <div class='tl-event'>
                    {ev['event']}<br>
                    <span class='tl-city'>📍 {badge_html}</span>
                </div>
            </div>"""
        tl_html += "</div>"
        st.markdown(tl_html, unsafe_allow_html=True)
    else:
        st.info("No timeline events found for this case.")

    # L2 pre-KP splits table
    if l2.get("l2_mules"):
        st.markdown("### L2 → Pre-Kingpin Transfer Summary")
        st.caption("All 125 micro-transfers from L2 mules to pre-kingpin accounts, funnelling into Santosh Mandal's account.")
        pre_kp_rows = []
        for m in l2.get("l2_mules", []):
            for pk in m.get("pre_kp_splits", []):
                pre_kp_rows.append({
                    "From L2 Mule":    m["mule_id"],
                    "L2 Holder":       m["holder_name"],
                    "To Pre-KP Acct":  pk["to_account"],
                    "City":            pk["to_city"],
                    "Amount (Rs.)":    pk["amount"],
                    "Transfer Time":   pk["split_time"],
                    "Final Dest":      pk["destination"],
                })
        st.dataframe(pd.DataFrame(pre_kp_rows), use_container_width=True, height=360, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — FIR BRIEF
# ─────────────────────────────────────────────────────────────────────────────
with tab_brief:
    st.markdown("### FIR-Ready Case Brief")
    st.markdown(_alert(
        "This document is <b>auto-generated</b> from correlated investigation data. "
        "All content must be reviewed and verified by the Investigating Officer before official filing.",
        "green"
    ), unsafe_allow_html=True)

    case_id_brief = _ac.get("case_id", "JMT-2023-0001")
    officer       = investigator_name or "[Investigating Officer]"
    l2_accused    = "\n".join(
        f"  {i+1:02d}. {m['holder_name']}  |  {m['mule_id']}  |  {m['city']}  |  Phone: {m['phone']}"
        for i, m in enumerate(l2.get("l2_mules", []))
    )

    brief_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║           FIRST INFORMATION REPORT (DRAFT — FOR REVIEW)         ║
╚══════════════════════════════════════════════════════════════════╝

  Case ID              : {case_id_brief}
  Date of Incident     : {_ac.get('incident_date')}
  Time of Incident     : {_ac.get('incident_time')}
  Investigating Officer: {officer}
  Generated By         : Cyber Fraud Investigation System (Auto)

══════════════════════════════════════════════════════════════════
  SECTION 1 — VICTIM DETAILS
══════════════════════════════════════════════════════════════════
  Full Name        : {vi.get('victim_name')}
  Phone Number     : {vi.get('phone')}
  City / State     : {vi.get('home_city')}, {vi.get('home_state')}
  Original IMEI    : {vi.get('original_imei')}
  SIM Provider     : {vi.get('sim_provider')}
  Bank             : {ua.get('bank_name')}
  Bank Account     : {ua.get('bank_account')}
  UPI ID           : {ua.get('upi_id')}
  Amount Stolen    : Rs. {txn.get('amount_debited',0):,}

══════════════════════════════════════════════════════════════════
  SECTION 2 — FRAUD PATTERN CLASSIFICATION
══════════════════════════════════════════════════════════════════
  Pattern          : {pt.get('pattern')}
  Risk Score       : {pt.get('risk_score')}/100
  Detection Flags  : {', '.join(pt.get('flags',[]))}
  Gang Involvement : {'YES — Organised criminal ring confirmed' if pt.get('gang_involved') else 'NOT CONFIRMED'}

══════════════════════════════════════════════════════════════════
  SECTION 3 — SIM SWAP EVIDENCE
══════════════════════════════════════════════════════════════════
  Status           : {sw.get('status')}
  Criminal IMEI    : {sw.get('criminal_imei')}  [NEW — fraudulently registered]
  Swap Timestamp   : {sw.get('swap_timestamp')}
  Swap Location    : {sw.get('swap_city')}, {sw.get('swap_state')}
  Tower ID         : {sw.get('swap_tower')}
  Victim City      : {sw.get('previous_city')}  [before swap]
  Distance         : {sw.get('distance_km')} km — physically impossible in 0 seconds
  UPI Accessed     : {sw.get('seconds_swap_to_upi')} seconds after SIM swap [AUTOMATED]

══════════════════════════════════════════════════════════════════
  SECTION 4 — ACCUSED PERSONS
══════════════════════════════════════════════════════════════════

  [A] KINGPIN (PRIMARY ACCUSED)
  ─────────────────────────────
  Name             : {kp.get('name')} (alias: {kp.get('alias')})
  Kingpin ID       : {kp.get('kingpin_id')}
  Phone            : {kp.get('phone')}
  UPI ID           : {kp.get('upi_id')}
  Bank             : {kp.get('bank_name')}
  Account          : {kp.get('bank_account')}
  City             : {kp.get('city')}, Jharkhand
  Total Victims    : {kp.get('total_victims_in_ring')}
  Total Amount     : Rs. {kp.get('total_amount_in_ring',0):,}
  Operation Time   : {kp.get('ring_operation_mins')} minutes

  [B] LEVEL 1 MULE (SECONDARY ACCUSED)
  ──────────────────────────────────────
  Name             : {l1.get('holder_name')}
  Mule ID          : {l1.get('mule_id')}
  Phone            : {l1.get('phone')}
  UPI ID           : {l1.get('upi_id')}
  Bank             : {l1.get('bank_name')}
  Account          : {l1.get('bank_account')}
  City             : {l1.get('city')}, Jharkhand
  Recruited By     : {l1.get('recruited_by')}
  Amount Received  : Rs. {l1.get('amount_received',0):,}

  [C] LEVEL 2 MULES ({l2.get('total_l2',0)} accounts — TERTIARY ACCUSED)
  ──────────────────────────────────────────────────────
{l2_accused}

══════════════════════════════════════════════════════════════════
  SECTION 5 — RECOMMENDED ACTIONS
══════════════════════════════════════════════════════════════════

  1. FREEZE ACCOUNTS IMMEDIATELY:
       - L1 Mule A/C : {l1.get('bank_account')}  ({l1.get('bank_name')})
       - Kingpin A/C  : {kp.get('bank_account')}  ({kp.get('bank_name')})
       - All 5 L2 mule accounts listed above.

  2. CDR REQUEST:
       Tower {sw.get('swap_tower')}, Jamtara — {sw.get('swap_timestamp')} ± 30 minutes.

  3. IMEI / TELECOM LOG:
       Request {vi.get('sim_provider')} for SIM swap approval records for
       number {vi.get('phone')} — identify retailer / CSC who processed it.

  4. LOOK-OUT NOTICE:
       {kp.get('name')} (alias {kp.get('alias')}) — last known: {kp.get('city')}, Jharkhand.

  5. ARREST WARRANT:
       L1 Mule {l1.get('holder_name')} — Phone: {l1.get('phone')} — Jamtara, Jharkhand.

  6. COORDINATION:
       Cyber Crime Cell, Jamtara + State Cyber Cell, Jharkhand Police HQ.

  7. LEGAL SECTIONS TO FILE UNDER:
       - IT Act Section 66C  : Identity theft
       - IT Act Section 66D  : Cheating by impersonation using computer resource
       - IPC Section 420     : Cheating and dishonestly inducing delivery of property
       - IPC Section 120B    : Criminal conspiracy
       - IT Act Section 43   : Damage to computer, computer system etc.

══════════════════════════════════════════════════════════════════
  NOTE: This brief is auto-generated by the Cyber Fraud
  Investigation System. All evidence references must be
  independently verified before official FIR filing.
══════════════════════════════════════════════════════════════════
"""

    c_brief, c_dl = st.columns([4, 1])
    with c_brief:
        st.text_area("Case Brief (editable before download)", value=brief_text.strip(), height=620, label_visibility="collapsed")
    with c_dl:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download FIR Brief",
            data=brief_text.encode("utf-8"),
            file_name=f"{case_id_brief}_FIR_brief.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )
        st.markdown(_card(f"""
        <div style='font-size:0.8rem; color:#8a9bb5;'>
            <b>Risk Score</b><br>
            <span style='font-size:1.5rem; font-weight:800; color:{score_color};'>{score}/100</span><br>
            {_badge(score_label, 'red' if score >= 80 else 'orange')}<br><br>
            <b>Pattern</b><br>
            <span style='font-size:0.75rem;'>SIM-Swap UPI Layered Mule</span><br><br>
            <b>Accused</b><br>
            1 Kingpin<br>
            1 L1 Mule<br>
            {l2.get('total_l2',0)} L2 Mules
        </div>
        """, "red"), unsafe_allow_html=True)
