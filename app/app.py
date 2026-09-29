import os
import tempfile

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image as PDFImage, Paragraph, SimpleDocTemplate, Spacer

from auth import authenticate_user, register_user
from database import (
    initialize_database,
    update_last_login,
    get_all_users,
    get_user_statistics,
    save_analysis,
    get_user_history,
)


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="InsightCivic AI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL DARK UI
# ============================================================

st.markdown(
    """
<style>
/* ==========================================================
   GLOBAL DARK SHELL — fixes Streamlit's default white canvas
   ========================================================== */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
    --bg: #070b12;
    --bg2: #0a101a;
    --panel: #0d1521;
    --panel2: #111c2b;
    --panel3: #152238;
    --line: #1d2a3c;
    --line2: #293950;
    --text: #f5f7fb;
    --text2: #c3cedd;
    --muted: #7d8ba0;
    --muted2: #5d6c82;
    --blue: #4d7cff;
    --blue2: #6e91ff;
    --green: #2fc49a;
    --amber: #f2b95f;
    --red: #ff7183;
    --shadow: 0 20px 60px rgba(0,0,0,.32);
}

html, body, #root,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
section.main,
section.main > div,
.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
}

body {
    overflow-x: hidden !important;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(77,124,255,.09), transparent 27%),
        radial-gradient(circle at 92% 8%, rgba(47,196,154,.045), transparent 23%),
        linear-gradient(180deg, #070b12 0%, #090e17 100%) !important;
    min-height: 100vh !important;
}

[data-testid="stHeader"] {
    background: rgba(7,11,18,.92) !important;
    border-bottom: 1px solid rgba(255,255,255,.025) !important;
}

[data-testid="stToolbar"] { visibility: hidden !important; }
#MainMenu, footer { visibility: hidden !important; }

.main .block-container {
    max-width: 1450px !important;
    padding: 2.25rem 2.6rem 5rem !important;
}

html, body, [class*="css"] {
    font-family: "DM Sans", "Segoe UI", sans-serif !important;
}

h1,h2,h3,h4,h5,h6 {
    font-family: "Manrope", "DM Sans", sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -.035em !important;
}

p, li, label, span { color: var(--text2); }

/* ==========================================================
   SIDEBAR
   ========================================================== */
section[data-testid="stSidebar"] {
    background: #080d16 !important;
    border-right: 1px solid #182436 !important;
    min-width: 245px !important;
}

section[data-testid="stSidebar"] > div {
    background: #080d16 !important;
    padding: 1.25rem .9rem 1rem !important;
}

section[data-testid="stSidebar"] * { color: var(--text2); }
section[data-testid="stSidebar"] hr { border-color: #1b283b !important; }

.brand {
    display:flex;
    align-items:center;
    gap:.72rem;
    padding:.15rem .35rem 1.05rem;
}
.brand-mark {
    width:40px;height:40px;border-radius:12px;
    display:flex;align-items:center;justify-content:center;
    background:linear-gradient(145deg,#4d7cff,#6f92ff);
    color:#fff !important;font-weight:800;
    box-shadow:0 10px 26px rgba(77,124,255,.25);
}
.brand-name { color:#fff !important;font-weight:800;font-size:.96rem; }
.brand-sub { color:#627188 !important;font-size:.62rem;margin-top:2px; }

.user-chip {
    display:flex;align-items:center;gap:.65rem;
    padding:.72rem;
    border:1px solid #1b293d;
    background:#0d1521;
    border-radius:12px;
    margin-bottom:1rem;
}
.avatar {
    width:34px;height:34px;border-radius:10px;
    display:flex;align-items:center;justify-content:center;
    background:#172641;color:#a9beff !important;font-weight:800;
}
.user-name { color:#fff !important;font-size:.78rem;font-weight:700; }
.user-role { color:#65748a !important;font-size:.62rem;margin-top:2px; }
.side-label {
    color:#5e6e85 !important;font-size:.58rem;font-weight:800;
    letter-spacing:.14em;text-transform:uppercase;
    margin:.8rem .45rem .4rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] { gap:.2rem; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius:10px !important;
    padding:.58rem .7rem !important;
    background:transparent !important;
    border:1px solid transparent !important;
    color:#8f9db1 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background:#101a29 !important;color:#fff !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background:linear-gradient(90deg,#142443,#102039) !important;
    border-color:#294476 !important;color:#fff !important;
    box-shadow:inset 3px 0 0 #4d7cff;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {
    color:#fff !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background:#0d1624 !important;
    border:1px solid #223149 !important;
    color:#bdc9d9 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background:#132034 !important;border-color:#344866 !important;
}

/* ==========================================================
   COMMON PAGE ELEMENTS
   ========================================================== */
.topbar {
    display:flex;justify-content:space-between;align-items:flex-start;
    gap:2rem;margin-bottom:1.65rem;
}
.page-kicker {
    color:#7090ff !important;font-size:.58rem;font-weight:800;
    letter-spacing:.16em;text-transform:uppercase;margin-bottom:.42rem;
}
.page-title {
    color:#fff !important;font-family:"Manrope",sans-serif;
    font-size:clamp(1.65rem,3vw,2.35rem);font-weight:800;
    line-height:1.08;letter-spacing:-.05em;
}
.page-desc {
    color:#7f8da2 !important;max-width:760px;margin-top:.48rem;
    font-size:.78rem;line-height:1.65;
}
.topbar-right {
    color:#66758b !important;font-size:.65rem;text-align:right;
    white-space:nowrap;padding-top:.28rem;
}
.section-title {
    color:#f3f6fb !important;font-family:"Manrope",sans-serif;
    font-size:.88rem;font-weight:800;margin:1.65rem 0 .72rem;
}

.card {
    background:linear-gradient(180deg,#101a29,#0d1521) !important;
    border:1px solid var(--line) !important;
    border-radius:15px !important;padding:1.1rem !important;
    box-shadow:0 10px 35px rgba(0,0,0,.16);
}
.card-tight {
    background:#0d1624 !important;border:1px solid var(--line) !important;
    border-radius:12px !important;padding:.78rem .95rem !important;
}
.stat-card {
    background:linear-gradient(180deg,#111c2d,#0d1521) !important;
    border:1px solid #1d2b40 !important;border-radius:14px !important;
    padding:1rem 1.05rem !important;min-height:105px;
    box-shadow:0 10px 30px rgba(0,0,0,.15);
}
.stat-label { color:#748399 !important;font-size:.62rem;font-weight:700; }
.stat-value {
    color:#fff !important;font-family:"Manrope",sans-serif;
    font-size:1.42rem;font-weight:800;margin-top:.25rem;
}
.stat-note { color:#596981 !important;font-size:.6rem;margin-top:.14rem; }

.feature {
    background:linear-gradient(180deg,#101a29,#0d1521) !important;
    border:1px solid #1c2a3e !important;border-radius:15px !important;
    padding:1.12rem !important;min-height:155px;
}
.feature-icon {
    width:37px;height:37px;border-radius:11px;
    background:rgba(77,124,255,.11);border:1px solid rgba(77,124,255,.18);
    color:#7897ff !important;display:flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;font-size:.95rem;
}
.feature-title { color:#f2f5fa !important;font-weight:800;font-size:.83rem; }
.feature-text { color:#75849a !important;font-size:.69rem;line-height:1.6;margin-top:.34rem; }

.workflow { display:flex;align-items:center;gap:.5rem;overflow-x:auto;padding-bottom:.25rem; }
.workflow-item {
    min-width:135px;padding:.72rem .8rem;background:#0d1624;
    border:1px solid #1e2d43;border-radius:11px;
}
.workflow-num { color:#6489ff !important;font-size:.56rem;font-weight:800; }
.workflow-name { color:#dce4ef !important;font-weight:700;font-size:.68rem;margin-top:.18rem; }

.notice {
    background:rgba(77,124,255,.045) !important;border:1px solid #20365c !important;
    border-radius:12px;padding:.9rem 1rem;color:#8190a7 !important;
    font-size:.7rem;line-height:1.6;
}

.risk-panel {
    background:linear-gradient(145deg,#111e32,#0d1521) !important;
    border:1px solid #263650 !important;border-radius:16px;padding:1.2rem;
    box-shadow:var(--shadow);min-height:190px;
}
.risk-eyebrow { color:#65758e !important;font-size:.57rem;font-weight:800;letter-spacing:.13em; }
.risk-level { font-family:"Manrope",sans-serif;font-size:1.8rem;font-weight:800;margin-top:.55rem; }
.risk-confidence { color:#77869d !important;font-size:.67rem;margin-top:.25rem; }
.risk-high { color:#ff7183 !important; }
.risk-medium { color:#f1b85f !important; }
.risk-low { color:#35c89e !important; }
.status-dot {
    display:inline-block;width:7px;height:7px;border-radius:50%;
    margin-right:7px;background:currentColor;box-shadow:0 0 12px currentColor;
}
.observation-title { color:#f1f5fb !important;font-weight:800;font-size:.82rem; }
.observation-sub { color:#718097 !important;font-size:.66rem;margin-top:.18rem; }

/* ==========================================================
   WIDGETS — every widget is dark
   ========================================================== */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stFileUploader"] label,
[data-testid="stDateInput"] label,
[data-testid="stNumberInput"] label {
    color:#8998ad !important;font-size:.63rem !important;font-weight:700 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    background:#0c1522 !important;border:1px solid #26364f !important;
    border-radius:9px !important;color:#f3f6fb !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within {
    border-color:#4d7cff !important;box-shadow:0 0 0 3px rgba(77,124,255,.1) !important;
}
input, textarea { color:#f3f6fb !important;-webkit-text-fill-color:#f3f6fb !important; }
input::placeholder, textarea::placeholder { color:#4e5d73 !important;-webkit-text-fill-color:#4e5d73 !important; }
div[data-baseweb="select"] span { color:#e8eef7 !important; }
div[role="listbox"], div[role="option"] { background:#0d1624 !important;color:#dce5f3 !important; }
div[role="option"]:hover { background:#16243a !important; }

.stButton > button, .stDownloadButton > button {
    min-height:39px !important;border-radius:9px !important;
    background:#0d1624 !important;border:1px solid #26364f !important;
    color:#e8eef7 !important;font-weight:700 !important;box-shadow:none !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background:#142136 !important;border-color:#3b4e6c !important;
    transform:translateY(-1px);
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
    background:linear-gradient(135deg,#4d7cff,#3e66df) !important;
    border-color:#4d7cff !important;color:#fff !important;
    box-shadow:0 8px 22px rgba(77,124,255,.18) !important;
}

button[data-baseweb="tab"] { color:#708097 !important;font-size:.68rem !important;font-weight:750 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#7393ff !important; }
div[data-baseweb="tab-highlight"] { background:#4d7cff !important;height:2px !important; }

[data-testid="stMetric"] {
    background:#0c1522 !important;border:1px solid #1c2a3e !important;
    border-radius:11px !important;padding:.7rem .78rem !important;
}
[data-testid="stMetricLabel"] { color:#74839a !important;font-size:.6rem !important; }
[data-testid="stMetricValue"] { color:#f4f7fb !important;font-weight:800 !important;font-size:1.1rem !important; }

[data-testid="stDataFrame"] {
    border:1px solid #1d2c41 !important;border-radius:12px !important;overflow:hidden !important;
    background:#0d1624 !important;
}

section[data-testid="stFileUploaderDropzone"] {
    background:#0c1522 !important;border:1px dashed #30435f !important;border-radius:11px !important;
}
section[data-testid="stFileUploaderDropzone"] * { color:#8998ad !important; }

[data-testid="stAlert"] { background:#101b2a !important;border-radius:10px !important; }
[data-testid="stExpander"] { background:#0d1624 !important;border:1px solid #1e2d42 !important;border-radius:11px !important; }
[data-testid="stExpander"] summary p { color:#dce5f3 !important; }
[data-testid="stMarkdownContainer"] a { color:#7897ff !important; }

/* ==========================================================
   LOGIN / REGISTER
   Uses :has() so Streamlit columns themselves become dark cards.
   This is the key fix for the white right-side area in the screenshot.
   ========================================================== */
.auth-marker { display:none !important; }

.auth-layout-marker ~ * { }

div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) {
    max-width:1160px !important;
    margin:3.5rem auto 2rem !important;
    gap:0 !important;
    align-items:stretch !important;
    background:transparent !important;
}

div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) > div[data-testid="stColumn"]:first-child {
    background:
        radial-gradient(circle at 84% 12%, rgba(77,124,255,.18), transparent 26%),
        radial-gradient(circle at 10% 92%, rgba(47,196,154,.06), transparent 24%),
        linear-gradient(145deg,#0b1423,#101d31 55%,#0b1526) !important;
    border:1px solid #1c2b40 !important;
    border-right:0 !important;
    border-radius:22px 0 0 22px !important;
    min-height:650px !important;
    padding:3.1rem !important;
    box-shadow:0 25px 80px rgba(0,0,0,.34) !important;
    position:relative !important;
    overflow:hidden !important;
}

div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) > div[data-testid="stColumn"]:last-child {
    background:#0a121e !important;
    border:1px solid #1c2b40 !important;
    border-radius:0 22px 22px 0 !important;
    min-height:650px !important;
    padding:3.1rem 3rem !important;
    box-shadow:25px 25px 80px rgba(0,0,0,.24) !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
}

.auth-logo {
    width:48px;height:48px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    background:linear-gradient(145deg,#4d7cff,#6f92ff);
    color:#fff !important;font-weight:900;font-size:1.05rem;
    box-shadow:0 12px 30px rgba(77,124,255,.25);
}
.auth-eyebrow {
    color:#7189c7 !important;font-size:.57rem;font-weight:800;
    letter-spacing:.17em;margin-top:2.7rem;
}
.auth-heading {
    color:#fff !important;font-family:"Manrope",sans-serif;
    font-size:clamp(2rem,3.4vw,2.85rem);line-height:1.04;
    letter-spacing:-.055em;font-weight:800;max-width:570px;margin-top:.55rem;
}
.auth-copy { color:#8392aa !important;font-size:.77rem;line-height:1.75;max-width:510px;margin-top:.9rem; }
.auth-points { display:grid;grid-template-columns:1fr 1fr;gap:.62rem;margin-top:1.8rem;max-width:560px; }
.auth-point {
    display:flex;gap:.5rem;align-items:flex-start;padding:.72rem;
    background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.055);
    border-radius:10px;color:#b8c5d8 !important;font-size:.66rem;line-height:1.4;
}
.auth-point b { color:#7091ff !important;font-size:.68rem; }
.auth-bottom { color:#4f5e74 !important;font-size:.58rem;margin-top:2rem; }
.auth-title { color:#f7faff !important;font-family:"Manrope",sans-serif;font-size:1.5rem;font-weight:800;letter-spacing:-.04em; }
.auth-sub { color:#718097 !important;font-size:.68rem;line-height:1.55;margin-top:.3rem;margin-bottom:1.15rem; }
.auth-footer { color:#4e5d73 !important;font-size:.58rem;text-align:center;margin-top:1rem; }

/* Keep the form widgets dark inside auth */
div[data-testid="stHorizontalBlock"]:has(.auth-right-marker) input {
    background:#0c1522 !important;
}

div[data-testid="stHorizontalBlock"]:has(.auth-right-marker) .stButton > button[kind="primary"] {
    min-height:42px !important;
    margin-top:.35rem !important;
}

/* ==========================================================
   MOBILE
   ========================================================== */
@media (max-width: 900px) {
    .main .block-container { padding:1.25rem 1rem 4rem !important; }
    .topbar { flex-direction:column;gap:.45rem; }
    .topbar-right { text-align:left; }
    div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) {
        margin:1rem auto !important;display:block !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) > div[data-testid="stColumn"]:first-child {
        border-right:1px solid #1c2b40 !important;border-radius:20px !important;
        min-height:420px !important;padding:2rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.auth-left-marker) > div[data-testid="stColumn"]:last-child {
        border-radius:20px !important;margin-top:1rem !important;
        min-height:430px !important;padding:2rem !important;
    }
    .auth-points { grid-template-columns:1fr; }
}
/* ==========================================================
   TYPOGRAPHY UPGRADE
   Larger, clearer and more readable UI
   ========================================================== */

/* ---------- GLOBAL ---------- */

html, body, [class*="css"] {
    font-size: 15px !important;
}

p, li, label, span {
    font-size: inherit;
}

/* ---------- SIDEBAR ---------- */

.brand-name {
    font-size: 1.02rem !important;
}

.brand-sub {
    font-size: .70rem !important;
}

.user-name {
    font-size: .88rem !important;
}

.user-role {
    font-size: .70rem !important;
}

.side-label {
    font-size: .68rem !important;
    letter-spacing: .13em !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: .68rem .78rem !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p,
section[data-testid="stSidebar"] div[role="radiogroup"] label span {
    font-size: .86rem !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    font-size: .84rem !important;
}

/* ---------- PAGE HEADER ---------- */

.page-kicker {
    font-size: .68rem !important;
    letter-spacing: .15em !important;
}

.page-title {
    font-size: clamp(1.9rem, 3vw, 2.6rem) !important;
    line-height: 1.08 !important;
}

.page-desc {
    font-size: .90rem !important;
    line-height: 1.7 !important;
}

.topbar-right {
    font-size: .72rem !important;
}

.section-title {
    font-size: 1.02rem !important;
    margin: 1.75rem 0 .82rem !important;
}

/* ---------- STAT CARDS ---------- */

.stat-card {
    padding: 1.15rem 1.2rem !important;
    min-height: 112px !important;
}

.stat-label {
    font-size: .72rem !important;
}

.stat-value {
    font-size: 1.58rem !important;
    margin-top: .32rem !important;
}

.stat-note {
    font-size: .68rem !important;
    margin-top: .18rem !important;
}

/* ---------- FEATURE CARDS ---------- */

.feature {
    padding: 1.25rem !important;
    min-height: 165px !important;
}

.feature-title {
    font-size: .94rem !important;
}

.feature-text {
    font-size: .78rem !important;
    line-height: 1.65 !important;
}

.feature-icon {
    font-size: 1.02rem !important;
}

/* ---------- WORKFLOW ---------- */

.workflow-item {
    min-width: 145px !important;
    padding: .82rem .9rem !important;
}

.workflow-num {
    font-size: .64rem !important;
}

.workflow-name {
    font-size: .76rem !important;
}

/* ---------- NOTICE ---------- */

.notice {
    font-size: .80rem !important;
    line-height: 1.7 !important;
}

/* ---------- RISK PANEL ---------- */

.risk-eyebrow {
    font-size: .64rem !important;
}

.risk-level {
    font-size: 2rem !important;
}

.risk-confidence {
    font-size: .76rem !important;
}

.observation-title {
    font-size: .92rem !important;
}

.observation-sub {
    font-size: .74rem !important;
}

/* ---------- STREAMLIT FORM LABELS ---------- */

[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stFileUploader"] label,
[data-testid="stDateInput"] label,
[data-testid="stNumberInput"] label {
    font-size: .78rem !important;
    font-weight: 700 !important;
}

/* ---------- INPUTS / SELECTBOXES ---------- */

div[data-baseweb="input"] input,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span,
textarea {
    font-size: .90rem !important;
}

div[data-baseweb="input"],
div[data-baseweb="select"] {
    min-height: 43px !important;
}

input::placeholder,
textarea::placeholder {
    font-size: .86rem !important;
}

/* ---------- BUTTONS ---------- */

.stButton > button,
.stDownloadButton > button {
    min-height: 43px !important;
    font-size: .84rem !important;
    font-weight: 700 !important;
}

/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    font-size: .82rem !important;
    font-weight: 700 !important;
    padding: .55rem .85rem !important;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"] {
    padding: .82rem .88rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: .72rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.22rem !important;
}

/* ---------- DATAFRAME ---------- */

[data-testid="stDataFrame"] {
    font-size: .84rem !important;
}

/* ---------- FILE UPLOADER ---------- */

section[data-testid="stFileUploaderDropzone"] {
    min-height: 110px !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    font-size: .78rem !important;
}

/* ---------- EXPANDERS / ALERTS ---------- */

[data-testid="stExpander"] summary p {
    font-size: .82rem !important;
}

[data-testid="stAlert"] {
    font-size: .82rem !important;
}

/* ---------- CAPTIONS ---------- */

[data-testid="stCaptionContainer"] {
    font-size: .76rem !important;
}

/* ---------- AUTH / LOGIN SCREEN ---------- */

.auth-eyebrow {
    font-size: .65rem !important;
}

.auth-heading {
    font-size: clamp(2.15rem, 3.5vw, 3rem) !important;
}

.auth-copy {
    font-size: .88rem !important;
    line-height: 1.8 !important;
}

.auth-point {
    font-size: .76rem !important;
    line-height: 1.5 !important;
    padding: .82rem !important;
}

.auth-point b {
    font-size: .78rem !important;
}

.auth-bottom {
    font-size: .66rem !important;
}

.auth-title {
    font-size: 1.68rem !important;
}

.auth-sub {
    font-size: .78rem !important;
    line-height: 1.65 !important;
}

.auth-footer {
    font-size: .65rem !important;
}

/* Login/register input text */
div[data-testid="stHorizontalBlock"]:has(.auth-right-marker) input {
    font-size: .90rem !important;
}

div[data-testid="stHorizontalBlock"]:has(.auth-right-marker) label {
    font-size: .78rem !important;
}

/* ---------- CARD TEXT ---------- */

.card {
    padding: 1.2rem !important;
}

.card-tight {
    padding: .9rem 1rem !important;
}

/* ---------- GENERAL MARKDOWN ---------- */

[data-testid="stMarkdownContainer"] p {
    font-size: .86rem;
    line-height: 1.65;
}

[data-testid="stMarkdownContainer"] li {
    font-size: .86rem;
    line-height: 1.65;
}

/* ---------- MOBILE ---------- */

@media (max-width: 900px) {

    html, body, [class*="css"] {
        font-size: 14px !important;
    }

    .page-title {
        font-size: 1.85rem !important;
    }

    .page-desc {
        font-size: .84rem !important;
    }

    .section-title {
        font-size: .98rem !important;
    }

    .stat-value {
        font-size: 1.45rem !important;
    }

    .feature-title {
        font-size: .90rem !important;
    }

    .feature-text {
        font-size: .76rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def page_header(kicker, title, description, right_text=None):
    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <div class="page-kicker">{kicker}</div>
                <div class="page-title">{title}</div>
                <div class="page-desc">{description}</div>
            </div>
            <div class="topbar-right">{right_text or ''}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def stat_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon, title, description):
    st.markdown(
        f"""
        <div class="feature">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_int(value, default=0):
    try:
        return int(float(value))
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def risk_class(risk):
    value = str(risk).lower()
    if value == "high":
        return "risk-high"
    if value == "medium":
        return "risk-medium"
    return "risk-low"


def style_chart(fig, ax):
    fig.patch.set_facecolor("#0d1624")
    ax.set_facecolor("#0d1624")

    # Larger chart typography
    ax.tick_params(
        colors="#8b9ab0",
        labelsize=10
    )

    ax.xaxis.label.set_color("#9aa8bb")
    ax.yaxis.label.set_color("#9aa8bb")

    ax.xaxis.label.set_fontsize(11)
    ax.yaxis.label.set_fontsize(11)

    ax.title.set_color("#edf2fa")
    ax.title.set_fontsize(13)
    ax.title.set_fontweight("bold")

    for spine in ax.spines.values():
        spine.set_color("#26364f")

    ax.grid(
        axis="y",
        color="#1d2a3d",
        alpha=.65,
        linewidth=.7
    )


# ============================================================
# DATABASE / FILES
# ============================================================

try:
    initialize_database()
except Exception as e:
    st.error("The application could not initialize its database.")
    st.exception(e)
    st.stop()

APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_PATH)
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "emergency_risk_model.pkl")
DATA_PATH = os.path.join(PROJECT_ROOT, "data_processed", "final_emergency_hourly_dataset.csv")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error("Unable to load the trained emergency risk model.")
    st.caption("Check that models/emergency_risk_model.pkl exists.")
    st.exception(e)
    st.stop()

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error("Unable to load the emergency dataset.")
    st.caption("Check that data_processed/final_emergency_hourly_dataset.csv exists.")
    st.exception(e)
    st.stop()


# ============================================================
# SESSION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# AUTH SCREEN
# ============================================================

if not st.session_state.logged_in:
    left, right = st.columns([1.08, .92], gap="small")

    with left:
        st.markdown('<div class="auth-layout-marker auth-left-marker"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="auth-logo">◆</div>
            <div class="auth-eyebrow">CIVIC INTELLIGENCE PLATFORM</div>
            <div class="auth-heading">Urban risk intelligence, built for clarity.</div>
            <div class="auth-copy">
                InsightCivic AI turns historical civic and environmental observations
                into structured analysis, model-assisted risk classification and reviewable reports.
            </div>
            <div class="auth-points">
                <div class="auth-point"><b>01</b><span>Historical civic data exploration</span></div>
                <div class="auth-point"><b>02</b><span>Random Forest risk classification</span></div>
                <div class="auth-point"><b>03</b><span>Analysis history and PDF reporting</span></div>
                <div class="auth-point"><b>04</b><span>Role-based administrative access</span></div>
            </div>
            <div class="auth-bottom">INSIGHTCIVIC AI · DECISION SUPPORT</div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="auth-layout-marker auth-right-marker"></div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">Welcome back</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-sub">Sign in to continue to your civic intelligence workspace.</div>',
            unsafe_allow_html=True,
        )

        login_tab, register_tab = st.tabs(["Sign in", "Create account"])

        with login_tab:
            login_username = st.text_input(
                "Username", placeholder="Enter your username", key="login_username"
            )
            login_password = st.text_input(
                "Password", placeholder="Enter your password", type="password", key="login_password"
            )

            if st.button("Sign in  →", type="primary", use_container_width=True, key="login_button"):
                username_value = login_username.strip()
                if not username_value or not login_password:
                    st.warning("Please enter both username and password.")
                else:
                    try:
                        user = authenticate_user(username_value, login_password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = dict(user)
                            update_last_login(user["id"])
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                    except Exception as e:
                        st.error("Unable to process the login.")
                        st.exception(e)

        with register_tab:
            register_username = st.text_input(
                "Username", placeholder="Choose a username", key="register_username"
            )
            register_email = st.text_input(
                "Email", placeholder="Enter your email", key="register_email"
            )
            register_password = st.text_input(
                "Password", placeholder="Minimum 6 characters", type="password", key="register_password"
            )
            register_confirm = st.text_input(
                "Confirm password", placeholder="Re-enter your password", type="password", key="register_confirm"
            )

            if st.button("Create account  →", type="primary", use_container_width=True, key="register_button"):
                username_value = register_username.strip()
                email_value = register_email.strip()
                if not username_value or not email_value or not register_password:
                    st.warning("Please fill in all fields.")
                elif register_password != register_confirm:
                    st.error("Passwords do not match.")
                elif len(register_password) < 6:
                    st.warning("Password must contain at least 6 characters.")
                else:
                    try:
                        created = register_user(username_value, email_value, register_password)
                        if created:
                            st.success("Account created. You can now sign in.")
                        else:
                            st.error("Username or email already exists.")
                    except Exception as e:
                        st.error("Unable to create the account.")
                        st.exception(e)

        st.markdown(
            '<div class="auth-footer">Secure account access · Analytical decision support</div>',
            unsafe_allow_html=True,
        )

    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

current_user = st.session_state.user
if not current_user:
    st.session_state.logged_in = False
    st.rerun()

current_role = str(current_user.get("role", "user")).lower()
username_display = current_user.get("username", "User")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    initials = str(username_display).strip()[:1].upper() or "U"

    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-mark">◆</div>
            <div><div class="brand-name">InsightCivic AI</div><div class="brand-sub">Civic intelligence platform</div></div>
        </div>
        <div class="user-chip">
            <div class="avatar">{initials}</div>
            <div><div class="user-name">{username_display}</div><div class="user-role">{current_role.title()} account</div></div>
        </div>
        <div class="side-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    navigation_options = ["Overview", "Risk Analysis", "Dataset Explorer", "My History"]
    if current_role == "admin":
        navigation_options.append("Admin Panel")

    section = st.radio(
        "Navigation",
        navigation_options,
        label_visibility="collapsed",
        format_func=lambda x: {
            "Overview": "⌂  Overview",
            "Risk Analysis": "◉  Risk Analysis",
            "Dataset Explorer": "▦  Dataset Explorer",
            "My History": "◷  My History",
            "Admin Panel": "⚙  Admin Panel",
        }.get(x, x),
    )

    st.divider()

    if st.button("Sign out", use_container_width=True, key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.markdown(
        '<div style="color:#52627a;font-size:.6rem;line-height:1.55;margin:.8rem .4rem;">'
        'Model outputs are analytical decision support and should be reviewed in context.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW
# ============================================================

if section == "Overview":
    page_header(
        "COMMAND CENTER",
        f"Welcome back, {username_display}.",
        "A concise view of your civic-risk workspace, dataset health and analysis capabilities.",
        f"{df.shape[0]:,} records available",
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1: stat_card("Dataset records", f"{df.shape[0]:,}", "Current working dataset")
    with c2: stat_card("Data fields", f"{df.shape[1]}", "Available columns")
    with c3: stat_card("Missing values", f"{int(df.isnull().sum().sum()):,}", "Across current dataset")
    with c4: stat_card("Model", "Random Forest", "Loaded and ready")

    section_title("Workspace capabilities")
    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        feature_card("◉", "Risk analysis", "Select a date and hour, inspect the observation and review the trained model classification.")
    with f2:
        feature_card("▦", "Dataset explorer", "Inspect the working dataset and preview another CSV without replacing the application's source data.")
    with f3:
        feature_card("◷", "Analysis history", "Save analyses to your account and revisit previous observations, classifications and model details.")

    section_title("Analysis pipeline")
    workflow = [("01", "Dataset"), ("02", "Observation"), ("03", "Features"), ("04", "Random Forest"), ("05", "Risk class"), ("06", "Report")]
    st.markdown(
        '<div class="workflow">' + ''.join(
            f'<div class="workflow-item"><div class="workflow-num">{n}</div><div class="workflow-name">{name}</div></div>'
            for n, name in workflow
        ) + '</div>', unsafe_allow_html=True
    )

    section_title("Responsible use")
    st.markdown(
        '<div class="notice"><b style="color:#dbe7ff;">Decision support, not certainty.</b> '
        'InsightCivic AI uses historical observations and a trained classification model to support analysis. '
        'A model output is not a guarantee that a real-world emergency will occur, and feature importance does not establish causation.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif section == "Risk Analysis":
    page_header(
        "RISK INTELLIGENCE",
        "Analyze a civic observation.",
        "Choose a date and hour to inspect the observation, model classification, visual evidence and report.",
        "Model-assisted analysis",
    )

    required_columns = ["date", "hour", "crime_count", "crash_count", "PRCP", "TAVG", "is_peak_hour", "emergency_risk_score"]
    missing_columns = [c for c in required_columns if c not in df.columns]
    if missing_columns:
        st.error("The dataset is missing required columns.")
        st.write(missing_columns)
        st.stop()

    available_dates = df["date"].dropna().unique().tolist()
    available_hours = sorted(df["hour"].dropna().unique().tolist())
    if not available_dates or not available_hours:
        st.warning("The dataset does not contain valid date or hour values.")
        st.stop()

    selector1, selector2 = st.columns([1.5, 1], gap="medium")
    with selector1:
        selected_date = st.selectbox("Observation date", available_dates, key="risk_date")
    with selector2:
        selected_hour = st.selectbox("Hour", available_hours, key="risk_hour")

    sample = df[(df["date"] == selected_date) & (df["hour"] == selected_hour)]
    if sample.empty:
        st.warning("No observation was found for this date and hour.")
        st.stop()

    row = sample.iloc[0]
    features = ["crime_count", "crash_count", "PRCP", "TAVG", "is_peak_hour"]

    try:
        model_input = sample[features]
        prediction = model.predict(model_input)[0]
        prediction_text = str(prediction)
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(model_input)[0]
            confidence = float(max(probabilities)) * 100
        else:
            confidence = 0.0
    except Exception as e:
        st.error("The trained model could not process this observation.")
        st.exception(e)
        st.stop()

    section_title("Classification")
    r1, r2 = st.columns([.8, 1.8], gap="medium")

    with r1:
        st.markdown(
            f"""
            <div class="risk-panel">
                <div class="risk-eyebrow">MODEL CLASSIFICATION</div>
                <div class="risk-level {risk_class(prediction_text)}"><span class="status-dot"></span>{prediction_text.upper()}</div>
                <div class="risk-confidence">Model probability score: <b style="color:#dce5f3;">{confidence:.2f}%</b></div>
                <div style="height:1px;background:#1c2a3e;margin:1rem 0;"></div>
                <div class="observation-sub">Selected observation<br><b style="color:#dce5f3;">{selected_date}</b> <span style="color:#53627a;">·</span> <b style="color:#dce5f3;">{selected_hour}:00</b></div>
            </div>
            """, unsafe_allow_html=True
        )

    with r2:
        st.markdown(
            '<div class="card"><div class="observation-title">Selected observation</div>'
            '<div class="observation-sub">Input values used by the trained model for this classification.</div></div>',
            unsafe_allow_html=True,
        )
        m1, m2, m3, m4, m5 = st.columns(5, gap="small")
        with m1: st.metric("Crime", safe_int(row["crime_count"]))
        with m2: st.metric("Crashes", safe_int(row["crash_count"]))
        with m3: st.metric("Rainfall", f"{safe_float(row['PRCP']):.2f}")
        with m4: st.metric("Temperature", f"{safe_float(row['TAVG']):.2f}")
        with m5: st.metric("Peak hour", safe_int(row["is_peak_hour"]))

    section_title("Visual evidence")
    day_data = df[df["date"] == selected_date]
    risk_values = pd.to_numeric(day_data["emergency_risk_score"], errors="coerce").dropna()
    selected_score_series = pd.to_numeric(pd.Series([row["emergency_risk_score"]]), errors="coerce")
    selected_score = float(selected_score_series.iloc[0]) if not selected_score_series.empty and pd.notna(selected_score_series.iloc[0]) else 0.0

    chart1, chart2 = st.columns(2, gap="medium")
    with chart1:
        st.markdown('<div class="card-tight"><b style="color:#eef3fb;">Daily risk-score distribution</b><br><span style="color:#687892;font-size:.62rem;">Selected observation shown against the same day.</span></div>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(6.5, 3.6))
        ax1.hist(risk_values, bins=15, color="#4d7cff", alpha=.72, edgecolor="#101a2a")
        ax1.axvline(selected_score, color="#f1b657", linestyle="--", linewidth=2)
        ax1.set_xlabel("Emergency Risk Score", fontsize=11)
        ax1.set_ylabel("Frequency", fontsize=11)
        ax1.set_title("Daily Risk Score Distribution", pad=12, fontsize=13, fontweight="bold")
        style_chart(fig1, ax1); fig1.tight_layout(); st.pyplot(fig1, use_container_width=True); plt.close(fig1)

    with chart2:
        st.markdown('<div class="card-tight"><b style="color:#eef3fb;">Crime vs crash relationship</b><br><span style="color:#687892;font-size:.62rem;">Selected observation is highlighted.</span></div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6.5, 3.6))
        ax2.scatter(day_data["crime_count"], day_data["crash_count"], alpha=.55, color="#6d91ff", edgecolors="none")
        ax2.scatter(safe_float(row["crime_count"]), safe_float(row["crash_count"]), s=180, marker="*", color="#f1b657", edgecolors="#fff", linewidths=.6)
        ax2.set_xlabel("Crime Count", fontsize=11)
        ax2.set_ylabel("Crash Count", fontsize=11)
        ax2.set_title("Crime and Crash Relationship", pad=12, fontsize=13, fontweight="bold")
        style_chart(fig2, ax2); fig2.tight_layout(); st.pyplot(fig2, use_container_width=True); plt.close(fig2)

    section_title("Model explanation")
    top_feature = "Not available"
    importance_df = None
    try:
        importances = model.feature_importances_
        feature_importance_dict = dict(zip(features, importances))
        top_feature = max(feature_importance_dict, key=feature_importance_dict.get)
        importance_df = pd.DataFrame({
            "Feature": [k.replace("_", " ").title() for k in feature_importance_dict],
            "Importance": [round(float(v), 4) for v in feature_importance_dict.values()],
        }).sort_values("Importance", ascending=False)
        e1, e2 = st.columns([1, 1.2], gap="medium")
        with e1: st.dataframe(importance_df, use_container_width=True, hide_index=True)
        with e2:
            st.markdown(
                f'<div class="card" style="min-height:150px;"><div class="page-kicker">TOP FEATURE</div>'
                f'<div style="color:#fff;font-family:Manrope;font-size:1.3rem;font-weight:800;margin:.3rem 0;">{top_feature.replace("_", " ").title()}</div>'
                '<div style="color:#77869d;font-size:.7rem;line-height:1.65;">Feature importance indicates how influential an input was within the trained model. It does not establish that the feature causes risk.</div></div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.info("Feature importance is not available for this model.")

    section_title("Actions")
    a1, a2 = st.columns(2, gap="medium")
    with a1:
        if st.button("Save analysis", type="primary", use_container_width=True, key="save_analysis_button"):
            try:
                save_analysis(
                    user_id=current_user["id"], analysis_date=selected_date, analysis_hour=selected_hour,
                    crime_count=row["crime_count"], crash_count=row["crash_count"], rainfall=row["PRCP"],
                    temperature=row["TAVG"], peak_hour=row["is_peak_hour"], risk_level=prediction_text,
                    confidence=confidence, top_factor=top_feature,
                )
                st.success("Analysis saved successfully.")
            except Exception as e:
                st.error("The analysis could not be saved."); st.exception(e)
    with a2:
        generate_pdf = st.button("Generate PDF report", use_container_width=True, key="generate_pdf_button")

    if generate_pdf:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                chart1_path = os.path.join(temp_dir, "risk_distribution.png")
                chart2_path = os.path.join(temp_dir, "crime_vs_crash.png")
                report_path = os.path.join(temp_dir, "InsightCivic_AI_Report.pdf")

                fig_pdf1, ax_pdf1 = plt.subplots(figsize=(7, 4))
                ax_pdf1.hist(risk_values, bins=15, color="#4d7cff", alpha=.72, edgecolor="#101a2a")
                ax_pdf1.axvline(selected_score, color="#f1b657", linestyle="--", linewidth=2)
                ax_pdf1.set_xlabel("Emergency Risk Score"); ax_pdf1.set_ylabel("Frequency"); ax_pdf1.set_title("Daily Risk Score Distribution")
                style_chart(fig_pdf1, ax_pdf1); fig_pdf1.tight_layout(); fig_pdf1.savefig(chart1_path, dpi=160, bbox_inches="tight", facecolor="#0d1624"); plt.close(fig_pdf1)

                fig_pdf2, ax_pdf2 = plt.subplots(figsize=(7, 4))
                ax_pdf2.scatter(day_data["crime_count"], day_data["crash_count"], alpha=.55, color="#6d91ff", edgecolors="none")
                ax_pdf2.scatter(safe_float(row["crime_count"]), safe_float(row["crash_count"]), s=180, marker="*", color="#f1b657", edgecolors="#fff", linewidths=.6)
                ax_pdf2.set_xlabel("Crime Count"); ax_pdf2.set_ylabel("Crash Count"); ax_pdf2.set_title("Crime and Crash Relationship")
                style_chart(fig_pdf2, ax_pdf2); fig_pdf2.tight_layout(); fig_pdf2.savefig(chart2_path, dpi=160, bbox_inches="tight", facecolor="#0d1624"); plt.close(fig_pdf2)

                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                "InsightTitle",
                parent=styles["Title"],
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
                textColor=colors.HexColor("#3867e8"),
                fontSize=24,
                leading=29,
                spaceAfter=10
            )
                heading_style = ParagraphStyle(
                "InsightHeading",
                parent=styles["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=15,
                leading=19,
                spaceBefore=8,
                spaceAfter=8,
                textColor=colors.HexColor("#3867e8")
)
                normal_style = ParagraphStyle(
                "InsightNormal",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=11.5,
                leading=17,
                textColor=colors.HexColor("#202733"),
)
                story = [
                    Paragraph("InsightCivic AI", title_style),
                    Paragraph("Civic Risk Analysis Report", heading_style), Spacer(1, .2*inch),
                    Paragraph(f"<b>Date:</b> {selected_date}", normal_style),
                    Paragraph(f"<b>Hour:</b> {selected_hour}", normal_style),
                    Paragraph(f"<b>Risk Classification:</b> {prediction_text}", normal_style),
                    Paragraph(f"<b>Model Probability Score:</b> {confidence:.2f}%", normal_style), Spacer(1, .2*inch),
                    Paragraph("Selected Observation", heading_style),
                    Paragraph(
                        f"Crime Count: {safe_int(row['crime_count'])}<br/>Crash Count: {safe_int(row['crash_count'])}<br/>"
                        f"Rainfall: {safe_float(row['PRCP']):.2f}<br/>Temperature: {safe_float(row['TAVG']):.2f}<br/>Peak Hour: {safe_int(row['is_peak_hour'])}", normal_style),
                    Spacer(1, .2*inch), Paragraph("Model Explanation", heading_style),
                    Paragraph(f"Highest model feature importance: {top_feature.replace('_',' ').title()}", normal_style),
                    Spacer(1, .2*inch), PDFImage(chart1_path, width=6.5*inch, height=3.7*inch), Spacer(1, .15*inch),
                    PDFImage(chart2_path, width=6.5*inch, height=3.7*inch), Spacer(1, .15*inch),
                    Paragraph("Responsible Use: This report is intended for analytical and decision-support purposes. The model probability score should not be interpreted as the probability of a real-world emergency.", normal_style),
                ]
                document = SimpleDocTemplate(report_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
                document.build(story)
                with open(report_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
            st.success("PDF report generated successfully.")
            st.download_button("Download InsightCivic AI report", data=pdf_bytes, file_name="InsightCivic_AI_Report.pdf", mime="application/pdf", use_container_width=True, key="download_pdf_button")
        except Exception as e:
            st.error("The PDF report could not be generated."); st.exception(e)


# ============================================================
# DATASET EXPLORER
# ============================================================

elif section == "Dataset Explorer":
    page_header("DATA EXPLORER", "Inspect the working dataset.", "Review the application's current data and preview another CSV without replacing the main source.", f"{df.shape[0]:,} rows")
    s1, s2, s3 = st.columns(3, gap="medium")
    with s1: stat_card("Rows", f"{df.shape[0]:,}", "Current dataset")
    with s2: stat_card("Columns", f"{df.shape[1]}", "Available fields")
    with s3: stat_card("Missing values", f"{int(df.isnull().sum().sum()):,}", "Across all columns")

    section_title("Dataset preview")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    section_title("Preview another CSV")
    st.caption("Uploaded files are previewed only and do not replace the application's main dataset.")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], key="csv_uploader")
    if uploaded_file is not None:
        try:
            new_df = pd.read_csv(uploaded_file)
            st.success(f"{uploaded_file.name} uploaded successfully.")
            u1, u2, u3 = st.columns(3, gap="medium")
            with u1: stat_card("Rows", f"{new_df.shape[0]:,}", "Uploaded file")
            with u2: stat_card("Columns", f"{new_df.shape[1]}", "Uploaded file")
            with u3: stat_card("Missing values", f"{int(new_df.isnull().sum().sum()):,}", "Uploaded file")
            st.dataframe(new_df.head(20), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error("The uploaded file could not be read as a CSV."); st.exception(e)


# ============================================================
# HISTORY
# ============================================================

elif section == "My History":
    page_header("PERSONAL HISTORY", "Saved analyses", "Review observations previously saved from your account.", "Account-level records")
    try:
        history = get_user_history(current_user["id"])
    except Exception as e:
        st.error("Could not load your analysis history."); st.exception(e); st.stop()

    if history:
        history_data = []
        for record in history:
            try: confidence_text = f"{float(record.get('confidence', 0)):.2f}%"
            except Exception: confidence_text = str(record.get("confidence", 0))
            history_data.append({
                "Date": record.get("analysis_date"), "Hour": record.get("analysis_hour"),
                "Crime": record.get("crime_count"), "Crashes": record.get("crash_count"),
                "Rainfall": record.get("rainfall"), "Temperature": record.get("temperature"),
                "Peak Hour": record.get("peak_hour"), "Risk": record.get("risk_level"),
                "Score": confidence_text, "Top Factor": record.get("top_factor"), "Saved At": record.get("created_at"),
            })
        history_df = pd.DataFrame(history_data)
        high_count = int((history_df["Risk"].astype(str).str.lower() == "high").sum())
        medium_count = int((history_df["Risk"].astype(str).str.lower() == "medium").sum())
        h1, h2, h3 = st.columns(3, gap="medium")
        with h1: stat_card("Total analyses", len(history_df), "Saved to your account")
        with h2: stat_card("High classifications", high_count, "Historical saved records")
        with h3: stat_card("Medium classifications", medium_count, "Historical saved records")
        section_title("Analysis records")
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="card"><b style="color:#f1f5fb;">No saved analyses yet.</b><br><span style="color:#687892;font-size:.7rem;">Run an observation from Risk Analysis and save it to build your history.</span></div>', unsafe_allow_html=True)


# ============================================================
# ADMIN PANEL
# ============================================================

elif section == "Admin Panel":
    page_header("ADMINISTRATION", "User administration", "Administrative overview of registered InsightCivic AI users.", "Restricted workspace")
    if current_role != "admin":
        st.error("Access denied. Administrator privileges are required.")
        st.stop()

    try:
        statistics = get_user_statistics()
    except Exception as e:
        st.error("Could not load user statistics."); st.exception(e); st.stop()

    a1, a2, a3 = st.columns(3, gap="medium")
    with a1: stat_card("Total users", statistics.get("total_users", 0), "Registered accounts")
    with a2: stat_card("Administrators", statistics.get("total_admins", 0), "Privileged accounts")
    with a3: stat_card("Regular users", statistics.get("total_regular_users", 0), "Standard accounts")

    section_title("Registered users")
    try:
        users = get_all_users()
    except Exception as e:
        st.error("Could not load registered users."); st.exception(e); st.stop()

    if users:
        users_df = pd.DataFrame([
            {
                "ID": user.get("id"), "Username": user.get("username"), "Email": user.get("email"),
                "Role": user.get("role"), "Created At": user.get("created_at"), "Last Login": user.get("last_login") or "Never",
            }
            for user in users
        ])
        st.dataframe(users_df, use_container_width=True, hide_index=True)
    else:
        st.info("No registered users found.")

else:
    st.warning("Please select a section from the sidebar.")
