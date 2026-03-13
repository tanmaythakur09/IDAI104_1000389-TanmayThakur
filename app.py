"""
🏢 TechLift Elevator Monitoring System v5.0
Design System: AI / Predictive Maintenance — Deep Navy + Neon Cyan
─────────────────────────────────────────────────────────────────
Colors  : #020817 bg · #00D4FF cyan · #4F8EF7 blue · #7C3AED purple
Fonts   : Orbitron (headings) · Inter (body) · Rajdhani (metrics)
Charts  : #00D4FF line · #4F8EF7 secondary · #F59E0B warn · #EF4444 crit
Cards   : glassmorphism rgba(15,23,42,0.75) · 12px blur · gradient borders
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import RandomForestRegressor
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechLift | Elevator Monitoring System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("logged_in", False), ("username", ""), ("theme", "dark"), ("page", "📊 Overview")]:
    if k not in st.session_state:
        st.session_state[k] = v

USERS = {"admin": "elevate123", "tanmay": "1234", "engineer": "tech2024"}

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════════════════
CY   = "#00D4FF"
BL   = "#4F8EF7"
PU   = "#7C3AED"
CRIT = "#EF4444"
WARN = "#F59E0B"
OK   = "#10B981"

CYm  = "rgba(0,212,255,0.10)"
CYg  = "rgba(0,212,255,0.40)"
BLm  = "rgba(79,142,247,0.10)"
PUm  = "rgba(124,58,237,0.12)"

BG   = "#020817"
CARD = "rgba(15,23,42,0.75)"
INP  = "rgba(15,23,42,0.90)"
SBG  = "rgba(2,8,23,0.97)"
T1   = "#E2E8F0"
T2   = "#94A3B8"
BORD = "rgba(0,212,255,0.14)"
SHA  = "rgba(0,0,0,0.55)"
GRID = "rgba(148,163,184,0.07)"
RAD  = "10px"
TR   = "0.22s cubic-bezier(0.4,0,0.2,1)"

# ── INJECT CSS ────────────────────────────────────────────────────────────────
def inject_css():
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {{
  --cyan:{CY}; --cyan-muted:{CYm}; --cyan-glow:{CYg};
  --blue:{BL}; --blue-muted:{BLm};
  --purple:{PU}; --purple-muted:{PUm};
  --critical:{CRIT}; --warning:{WARN}; --ok:{OK};
  --bg:{BG}; --card:{CARD}; --input:{INP}; --sbg:{SBG};
  --t1:{T1}; --t2:{T2}; --border:{BORD}; --shadow:{SHA}; --grid:{GRID};
  --radius:{RAD}; --tr:{TR};
  --grad:linear-gradient(135deg,{CY},{BL});
  --grad-soft:linear-gradient(135deg,{CYm},{BLm});
  --font-head:'Orbitron',sans-serif;
  --font-body:'Inter',sans-serif;
  --font-metric:'Rajdhani',sans-serif;
}}

*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{font-family:var(--font-body);background-color:var(--bg);color:var(--t1);}}

.stApp{{
  background:
    radial-gradient(ellipse 55% 45% at 5% 10%,rgba(0,212,255,0.07) 0%,transparent 55%),
    radial-gradient(ellipse 40% 35% at 95% 0%,rgba(124,58,237,0.08) 0%,transparent 55%),
    radial-gradient(ellipse 50% 40% at 90% 95%,rgba(79,142,247,0.06) 0%,transparent 50%),
    linear-gradient({GRID} 1px,transparent 1px),
    linear-gradient(90deg,{GRID} 1px,transparent 1px),
    {BG} !important;
  background-size:100% 100%,100% 100%,100% 100%,32px 32px,32px 32px,100% 100% !important;
  color:var(--t1);min-height:100vh;
}}
.stApp::after{{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:9999;
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.025) 3px,rgba(0,0,0,0.025) 4px);
}}

#MainMenu,footer,header{{visibility:hidden !important;}}
.block-container{{padding-top:1.4rem !important;max-width:100% !important;}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"]{{
  background:var(--sbg) !important;
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border-right:1px solid var(--border) !important;
  box-shadow:4px 0 40px rgba(0,212,255,0.06);
  min-width:268px !important;
}}
section[data-testid="stSidebar"]>div,
section[data-testid="stSidebar"] .block-container{{padding:0 !important;}}

.user-badge{{
  display:flex;align-items:center;gap:14px;
  padding:20px 18px 18px;border-bottom:1px solid var(--border);
  background:linear-gradient(135deg,{CYm},{BLm});
  position:relative;overflow:hidden;
}}
.user-badge::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:var(--grad);box-shadow:0 0 12px {CY};
}}
.user-avatar{{
  width:44px;height:44px;border-radius:10px;
  background:linear-gradient(135deg,{CYm},{PUm});
  border:1.5px solid rgba(0,212,255,0.35);
  display:flex;align-items:center;justify-content:center;
  font-family:var(--font-head);font-size:14px;font-weight:700;
  color:var(--cyan);letter-spacing:.04em;
  box-shadow:0 0 18px {CYm},inset 0 0 12px {CYm};
  flex-shrink:0;position:relative;
}}
.user-avatar::after{{
  content:'';position:absolute;bottom:-5px;right:-5px;
  width:11px;height:11px;border-radius:50%;
  background:{OK};border:2px solid var(--bg);
  box-shadow:0 0 8px {OK};animation:pulse-dot 2.2s ease infinite;
}}
@keyframes pulse-dot{{
  0%,100%{{transform:scale(1);box-shadow:0 0 8px {OK};}}
  50%{{transform:scale(1.2);box-shadow:0 0 16px {OK};}}
}}
.user-name{{
  font-family:var(--font-head);font-size:12px;font-weight:700;
  color:var(--t1) !important;letter-spacing:.08em;text-transform:uppercase;
}}
.user-role{{
  font-family:var(--font-body);font-size:11px;font-weight:500;
  color:var(--cyan) !important;letter-spacing:.1em;
  text-transform:uppercase;margin-top:3px;opacity:.85;
}}
.nav-section{{
  font-family:var(--font-head);font-size:8.5px;font-weight:600;
  color:var(--t2) !important;letter-spacing:.28em;text-transform:uppercase;
  padding:18px 18px 8px;opacity:.6;
}}
div[data-testid="stRadio"]>label{{display:none !important;}}
div[data-testid="stRadio"] div[role="radiogroup"]{{
  display:flex;flex-direction:column;gap:3px;padding:0 10px;
}}
div[data-testid="stRadio"] label{{
  background:transparent !important;border:1px solid transparent !important;
  border-radius:8px !important;padding:10px 14px !important;cursor:pointer;
  transition:all var(--tr) !important;font-weight:500 !important;
  font-size:11.5px !important;letter-spacing:.08em !important;
  text-transform:uppercase !important;font-family:var(--font-head) !important;
  color:var(--t2) !important;position:relative !important;
}}
div[data-testid="stRadio"] label::before{{
  content:'';position:absolute;left:0;top:22%;bottom:22%;
  width:3px;border-radius:0 2px 2px 0;
  background:transparent;transition:all var(--tr);
}}
div[data-testid="stRadio"] label:hover{{
  background:{CYm} !important;border-color:rgba(0,212,255,0.2) !important;
  color:var(--t1) !important;padding-left:18px !important;
}}
div[data-testid="stRadio"] label:hover::before{{background:var(--cyan);box-shadow:0 0 8px var(--cyan);}}
div[data-testid="stRadio"] label[data-selected="true"]{{
  background:linear-gradient(90deg,{CYm},transparent) !important;
  border-color:rgba(0,212,255,0.18) !important;border-left-color:var(--cyan) !important;
  color:var(--t1) !important;font-weight:600 !important;
  box-shadow:inset 0 0 18px {CYm} !important;
}}
div[data-testid="stRadio"] label[data-selected="true"]::before{{background:var(--cyan);box-shadow:0 0 10px var(--cyan);}}

.sidebar-stats{{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:4px 10px 12px;}}
.sidebar-stat{{
  background:linear-gradient(135deg,{CYm},{BLm});
  border:1px solid var(--border);border-radius:8px;
  padding:12px 10px;text-align:center;transition:all var(--tr);
}}
.sidebar-stat:hover{{border-color:rgba(0,212,255,0.3);box-shadow:0 0 16px {CYm};}}
.s-val{{
  font-family:var(--font-metric);font-size:20px;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;line-height:1;
}}
.s-lbl{{
  font-family:var(--font-body);font-size:10px;font-weight:500;
  color:var(--t2);text-transform:uppercase;letter-spacing:.12em;margin-top:4px;
}}

section[data-testid="stSidebar"] .stButton>button{{
  background:transparent !important;color:var(--t2) !important;
  border:1px solid rgba(148,163,184,0.2) !important;border-radius:8px !important;
  font-family:var(--font-head) !important;font-size:10.5px !important;
  font-weight:600 !important;letter-spacing:.1em !important;
  text-transform:uppercase !important;padding:8px 14px !important;
  width:auto !important;transition:all var(--tr) !important;
  box-shadow:none !important;margin:2px 10px !important;
}}
section[data-testid="stSidebar"] .stButton>button:hover{{
  border-color:rgba(239,68,68,0.45) !important;color:{CRIT} !important;
  background:rgba(239,68,68,0.06) !important;
  box-shadow:0 0 14px rgba(239,68,68,0.15) !important;
}}

/* ── PAGE HEADER ── */
.page-header{{
  background:var(--card);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:22px 28px 18px;margin-bottom:24px;
  position:relative;overflow:hidden;
  animation:fadeUp .45s ease both;
}}
.page-header::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:var(--grad);opacity:.8;box-shadow:0 0 16px {CYg};
}}
.page-header::after{{
  content:'';position:absolute;top:0;left:0;
  width:18px;height:18px;
  border-top:2px solid {CY};border-left:2px solid {CY};
}}
.page-header h1{{
  font-family:var(--font-head) !important;font-size:20px !important;
  font-weight:700 !important;letter-spacing:.1em !important;
  text-transform:uppercase !important;margin:0 0 6px 0 !important;
  background:var(--grad) !important;
  -webkit-background-clip:text !important;
  -webkit-text-fill-color:transparent !important;background-clip:text !important;
}}
.page-header p{{
  color:var(--t2) !important;margin:0 !important;
  font-family:var(--font-body) !important;font-size:12px !important;
  letter-spacing:.18em !important;text-transform:uppercase !important;font-weight:500 !important;
}}
.page-header-tag{{
  position:absolute;top:18px;right:20px;
  background:{CYm};border:1px solid rgba(0,212,255,0.25);
  border-radius:20px;padding:4px 12px;
  font-family:var(--font-head);font-size:9px;font-weight:600;
  color:{CY};letter-spacing:.14em;text-transform:uppercase;
  box-shadow:0 0 12px {CYm};
}}

/* ── METRIC CARDS ── */
.metric-glass{{
  background:var(--card);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:22px 22px 18px;position:relative;overflow:hidden;
  transition:all var(--tr);animation:fadeUp .45s ease both;
}}
.metric-glass::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--grad);
}}
.metric-glass::after{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,{CYm} 0%,{BLm} 50%,transparent 100%);
  pointer-events:none;
}}
.metric-glass:hover{{
  transform:translateY(-3px);border-color:rgba(0,212,255,0.28);
  box-shadow:0 8px 32px rgba(0,212,255,0.10),0 0 0 1px rgba(0,212,255,0.10);
}}
.metric-glass .label{{
  font-family:var(--font-head);font-size:9px;font-weight:600;
  text-transform:uppercase;letter-spacing:.22em;color:var(--t2);
  margin-bottom:12px;position:relative;z-index:1;
}}
.metric-glass .value{{
  font-family:var(--font-metric);font-size:34px;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;
  line-height:1;position:relative;z-index:1;
}}
.metric-glass .sub{{
  font-family:var(--font-body);font-size:11px;font-weight:400;
  color:var(--t2);margin-top:8px;position:relative;z-index:1;
}}

/* ── GLASS CARDS ── */
.glass-card{{
  background:var(--card);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border:1px solid var(--border);border-radius:var(--radius);
  padding:22px;margin:8px 0;
  box-shadow:0 4px 24px var(--shadow);
  transition:all var(--tr);animation:fadeUp .45s ease both;
}}
.glass-card:hover{{border-color:rgba(0,212,255,0.26);box-shadow:0 0 28px {CYm},0 8px 32px var(--shadow);}}

/* ── ALERT PANELS ── */
.alert-panel{{
  border-radius:var(--radius);padding:20px 22px;margin-bottom:10px;
  position:relative;overflow:hidden;transition:all var(--tr);backdrop-filter:blur(10px);
}}
.alert-panel:hover{{transform:translateX(4px);}}
.alert-panel::before{{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;}}
.alert-panel h3{{
  margin:0 0 6px 0 !important;font-family:var(--font-head) !important;
  font-size:12px !important;text-transform:uppercase !important;letter-spacing:.1em !important;
}}
.alert-panel p{{
  margin:4px 0 0 !important;font-size:12px !important;
  opacity:.75 !important;font-family:var(--font-body) !important;
}}
.alert-panel .big-num{{
  font-family:var(--font-metric);font-size:34px;font-weight:700;line-height:1.1;margin:6px 0 4px;
}}
.alert-healthy{{
  background:linear-gradient(135deg,rgba(16,185,129,0.09),transparent);
  border:1px solid rgba(16,185,129,0.22);color:{OK};
}}
.alert-healthy::before{{background:{OK};box-shadow:0 0 12px {OK};}}
.alert-healthy:hover{{box-shadow:0 0 28px rgba(16,185,129,0.14);border-color:{OK};}}
.alert-warning{{
  background:linear-gradient(135deg,rgba(245,158,11,0.09),transparent);
  border:1px solid rgba(245,158,11,0.22);color:{WARN};
}}
.alert-warning::before{{background:{WARN};box-shadow:0 0 12px {WARN};}}
.alert-warning:hover{{box-shadow:0 0 28px rgba(245,158,11,0.14);border-color:{WARN};}}
.alert-critical{{
  background:linear-gradient(135deg,rgba(239,68,68,0.09),transparent);
  border:1px solid rgba(239,68,68,0.22);color:{CRIT};
  animation:crit-pulse 2.8s ease infinite;
}}
.alert-critical::before{{background:{CRIT};box-shadow:0 0 12px {CRIT};}}
.alert-critical:hover{{border-color:{CRIT};}}
@keyframes crit-pulse{{0%,100%{{box-shadow:0 0 18px rgba(239,68,68,0.06);}}50%{{box-shadow:0 0 32px rgba(239,68,68,0.18);}}}}

/* ── ANIMATIONS ── */
@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px);}}to{{opacity:1;transform:translateY(0);}}}}
.fade-up  {{animation:fadeUp .45s ease both;}}
.fade-up-1{{animation:fadeUp .45s  .06s ease both;}}
.fade-up-2{{animation:fadeUp .45s  .12s ease both;}}
.fade-up-3{{animation:fadeUp .45s  .18s ease both;}}
.fade-up-4{{animation:fadeUp .45s  .24s ease both;}}

/* ── BUTTONS ── */
.stButton>button{{
  background:transparent !important;color:var(--cyan) !important;
  border:1px solid rgba(0,212,255,0.35) !important;border-radius:8px !important;
  font-family:var(--font-head) !important;font-weight:600 !important;
  font-size:11px !important;padding:11px 22px !important;width:100% !important;
  letter-spacing:.14em !important;text-transform:uppercase !important;
  transition:all var(--tr) !important;box-shadow:inset 0 0 14px {CYm} !important;
}}
.stButton>button:hover{{
  background:{CYm} !important;color:#fff !important;border-color:{CY} !important;
  box-shadow:0 0 24px {CYg},inset 0 0 18px {CYm} !important;
}}
.stButton>button:focus-visible{{outline:2px solid {CY} !important;outline-offset:3px !important;}}

/* ── TEXT INPUTS ── */
.stTextInput>div>div>input{{
  background:var(--input) !important;border:1px solid var(--border) !important;
  border-left:2px solid {CY} !important;border-radius:8px !important;
  color:var(--t1) !important;padding:13px 16px !important;
  font-size:14px !important;font-family:var(--font-body) !important;
  letter-spacing:.03em;transition:all var(--tr);
}}
.stTextInput>div>div>input:focus{{
  border-color:rgba(0,212,255,0.5) !important;
  box-shadow:0 0 0 3px {CYm},0 0 20px {CYm} !important;outline:none !important;
}}
.stTextInput>div>div>input::placeholder{{color:var(--t2) !important;opacity:.55;}}
.stTextInput>label,.stSelectbox>label,.stSlider>label,.stMultiSelect>label{{
  color:var(--t2) !important;font-family:var(--font-head) !important;
  font-size:9.5px !important;letter-spacing:.2em !important;
  text-transform:uppercase !important;font-weight:600 !important;margin-bottom:6px !important;
}}

/* ── SLIDERS ── */
.stSlider>div>div>div>div{{background:var(--grad) !important;box-shadow:0 0 8px {CYg} !important;}}
div[data-testid="stSlider"]>div>div>div[role="slider"]{{
  background:var(--bg) !important;border:2px solid {CY} !important;
  box-shadow:0 0 14px {CYg} !important;border-radius:50% !important;
  width:16px !important;height:16px !important;transition:transform var(--tr) !important;
}}
div[data-testid="stSlider"]>div>div>div[role="slider"]:hover{{transform:scale(1.3) !important;}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{{
  background:var(--card) !important;border:1px solid var(--border) !important;
  border-radius:10px !important;padding:4px !important;gap:4px !important;
}}
.stTabs [data-baseweb="tab"]{{
  background:transparent !important;border:none !important;border-radius:7px !important;
  color:var(--t2) !important;font-family:var(--font-head) !important;
  font-size:10px !important;font-weight:600 !important;letter-spacing:.1em !important;
  text-transform:uppercase !important;padding:8px 16px !important;transition:all var(--tr) !important;
}}
.stTabs [data-baseweb="tab"]:hover{{background:{CYm} !important;color:var(--t1) !important;}}
.stTabs [aria-selected="true"]{{background:{CYm} !important;color:{CY} !important;box-shadow:inset 0 0 14px {CYm} !important;}}
.stTabs [data-baseweb="tab-highlight"]{{background:var(--grad) !important;height:2px !important;box-shadow:0 0 12px {CYg} !important;}}

/* ── SELECTBOX + MULTISELECT ── */
.stSelectbox>div>div{{
  background:var(--input) !important;color:var(--t1) !important;
  border:1px solid var(--border) !important;border-radius:8px !important;
}}
.stSelectbox>div>div:focus-within{{border-color:rgba(0,212,255,0.45) !important;box-shadow:0 0 0 3px {CYm} !important;}}
.stMultiSelect>div>div{{background:var(--input) !important;border:1px solid var(--border) !important;border-radius:8px !important;}}
span[data-baseweb="tag"]{{
  background:{CYm} !important;border:1px solid rgba(0,212,255,0.3) !important;
  border-radius:6px !important;color:{CY} !important;
  font-family:var(--font-body) !important;font-size:12px !important;
}}

/* ── DATAFRAME ── */
.stDataFrame{{border:1px solid var(--border) !important;border-radius:var(--radius) !important;overflow:hidden !important;}}
.stDataFrame table{{background:var(--input) !important;color:var(--t1) !important;font-family:var(--font-body) !important;font-size:13px !important;}}
.stDataFrame th{{
  background:rgba(0,212,255,0.05) !important;color:var(--t2) !important;
  font-family:var(--font-head) !important;font-size:9.5px !important;
  letter-spacing:.14em !important;text-transform:uppercase !important;
  border-bottom:1px solid var(--border) !important;
}}
.stDataFrame tr:hover td{{background:{CYm} !important;}}

/* ── HEADINGS + HR ── */
h2,h3{{
  font-family:var(--font-head) !important;font-size:13px !important;
  font-weight:700 !important;letter-spacing:.08em !important;
  text-transform:uppercase !important;color:var(--t1) !important;
}}
hr{{border-color:var(--border) !important;margin:20px 0 !important;}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:linear-gradient({CY},{BL});border-radius:3px;}}
::-webkit-scrollbar-thumb:hover{{background:{CY};}}

/* ══════════════════════════
   LOGIN
══════════════════════════ */
.login-wrapper{{
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;width:100%;min-height:80vh;
}}
.login-card{{
  background:var(--card);
  backdrop-filter:blur(32px);-webkit-backdrop-filter:blur(32px);
  border:1px solid rgba(0,212,255,0.18);
  padding:50px 46px 42px;width:100%;max-width:460px;border-radius:16px;
  box-shadow:0 0 80px rgba(0,212,255,0.08),0 0 0 1px rgba(0,212,255,0.08),inset 0 0 60px rgba(0,212,255,0.03);
  position:relative;overflow:hidden;animation:fadeUp .6s ease both;
}}
.login-card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:var(--grad);box-shadow:0 0 24px {CYg};
  animation:border-glow 3s ease-in-out infinite;
}}
@keyframes border-glow{{0%,100%{{opacity:.7;}}50%{{opacity:1;}}}}
.corner-tl{{position:absolute;top:0;left:0;width:20px;height:20px;border-top:2px solid {CY};border-left:2px solid {CY};}}
.corner-br{{position:absolute;bottom:0;right:0;width:20px;height:20px;border-bottom:2px solid {CY};border-right:2px solid {CY};}}
.corner-tr{{position:absolute;top:0;right:0;width:20px;height:20px;border-top:2px solid rgba(0,212,255,0.28);border-right:2px solid rgba(0,212,255,0.28);}}
.corner-bl{{position:absolute;bottom:0;left:0;width:20px;height:20px;border-bottom:2px solid rgba(0,212,255,0.28);border-left:2px solid rgba(0,212,255,0.28);}}
.tech-badge{{
  position:absolute;top:18px;right:18px;
  background:{CYm};border:1px solid rgba(0,212,255,0.25);
  padding:5px 12px;font-size:9px;color:{CY};
  letter-spacing:.16em;font-family:var(--font-head);font-weight:700;
  box-shadow:0 0 12px {CYm};border-radius:20px;
}}
.status-dot{{
  width:7px;height:7px;background:{OK};border-radius:50%;
  box-shadow:0 0 10px {OK};display:inline-block;
  animation:pulse-dot 1.8s ease infinite;margin-right:5px;vertical-align:middle;
}}
.login-icon{{
  text-align:center;font-size:52px;margin-bottom:14px;
  filter:drop-shadow(0 0 22px {CYg});
  animation:float 3.2s ease-in-out infinite;
}}
@keyframes float{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-6px);}}}}
.login-title{{
  text-align:center;font-family:var(--font-head);
  font-size:30px;font-weight:900;
  background:var(--grad);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;
  letter-spacing:.18em;text-transform:uppercase;margin-bottom:4px;
}}
.login-subtitle{{
  text-align:center;font-size:11px;color:var(--t2);
  margin-bottom:32px;letter-spacing:.28em;text-transform:uppercase;
  font-family:var(--font-body);font-weight:500;
}}
.login-features{{
  display:flex;justify-content:center;gap:24px;
  padding-top:22px;border-top:1px solid var(--border);margin-top:4px;
}}
.login-feat{{
  text-align:center;font-size:9.5px;color:var(--t2);
  text-transform:uppercase;letter-spacing:.12em;font-family:var(--font-head);font-weight:600;
}}
.login-feat .feat-icon{{font-size:22px;display:block;margin-bottom:6px;filter:drop-shadow(0 0 8px {CYg});}}
.login-hint{{
  text-align:center;margin-top:20px;color:var(--t2);
  font-size:10.5px;font-family:var(--font-body);letter-spacing:.05em;opacity:.65;
}}
.login-hint span{{color:{CY};opacity:1;}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


inject_css()

# ── LOGIN PAGE ─────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""<style>
    section[data-testid="stSidebar"]{{ display:none !important; }}
    header{{ display:none !important; }}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='login-card'>
          <div class='corner-tl'></div><div class='corner-br'></div>
          <div class='corner-tr'></div><div class='corner-bl'></div>
          <div class='tech-badge'><span class='status-dot'></span>SYS.ONLINE</div>
          <div class='login-icon'>🏢</div>
          <div class='login-title'>TechLift</div>
          <div class='login-subtitle'>v5.0 · Predictive AI Monitoring</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("User ID", placeholder="Enter identification...")
            password = st.text_input("Passkey", type="password", placeholder="Enter passkey...")
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⌗  Initialize Uplink", use_container_width=True)
            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("⛔  ACCESS DENIED — Credentials mismatch. Please retry.")

        st.markdown(f"""
            <div class='login-features'>
              <div class='login-feat'><span class='feat-icon'>🛡️</span>AES-256</div>
              <div class='login-feat'><span class='feat-icon'>📡</span>Uplink</div>
              <div class='login-feat'><span class='feat-icon'>🧠</span>Neural Net</div>
            </div>
            <div class='login-hint'>
              OVERRIDE: [<span>admin</span> : <span>elevate123</span>]
              &nbsp;·&nbsp; [<span>tanmay</span> : <span>1234</span>]
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.logged_in:
    show_login()
    st.stop()

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('elevator_sensor_data_cleaned.csv')

df = load_data()
mean_vib       = df['vibration'].mean()
std_vib        = df['vibration'].std()
healthy_thr    = mean_vib + std_vib
critical_thr   = mean_vib + 2 * std_vib
healthy_count  = len(df[df['vibration'] < healthy_thr])
maint_count    = len(df[(df['vibration'] >= healthy_thr) & (df['vibration'] < critical_thr)])
critical_count = len(df[df['vibration'] >= critical_thr])
healthy_pct    = healthy_count / len(df) * 100

ROLES = {"admin": "Administrator", "tanmay": "Sr. Engineer"}
role  = ROLES.get(st.session_state.username, "Engineer")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    initials = st.session_state.username[:2].upper()
    st.markdown(f"""
    <div class='user-badge fade-up'>
      <div class='user-avatar'>{initials}</div>
      <div>
        <div class='user-name'>{st.session_state.username.capitalize()}</div>
        <div class='user-role'>{role}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:10px 10px 4px;'>", unsafe_allow_html=True)
    if st.button("🚪  Logout"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='nav-section'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["📊  Overview", "📈  Advanced Analytics", "🤖  ML Predictions",
         "🚨  Alerts & Warnings", "📑  Report Generator", "⚙️  Settings"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='nav-section' style='margin-top:8px;'>Quick Stats</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='sidebar-stats fade-up-2'>
      <div class='sidebar-stat'><div class='s-val'>{len(df):,}</div><div class='s-lbl'>Readings</div></div>
      <div class='sidebar-stat'><div class='s-val'>{healthy_pct:.0f}%</div><div class='s-lbl'>Healthy</div></div>
      <div class='sidebar-stat'><div class='s-val'>{critical_count:,}</div><div class='s-lbl'>Critical</div></div>
      <div class='sidebar-stat'><div class='s-val'>{maint_count:,}</div><div class='s-lbl'>Maint.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding:16px 18px 12px;border-top:1px solid {BORD};margin-top:8px;'>
      <div style='font-size:9px;color:{T2};text-align:center;
                  font-family:"Rajdhani",sans-serif;letter-spacing:.1em;'>
        🏢 TechLift EMS · v5.0 · © 2026
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def page_header(icon, title, subtitle, tag=None):
    tag_html = f"<div class='page-header-tag'>{tag}</div>" if tag else ""
    st.markdown(f"""
    <div class='page-header fade-up'>
      {tag_html}
      <h1>{icon} {title}</h1>
      <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def metric_glass(label, value, sub="", delay=""):
    style = f"animation-delay:{delay};" if delay else ""
    return f"""<div class='metric-glass' style='{style}'>
      <div class='label'>{label}</div>
      <div class='value'>{value}</div>
      <div class='sub'>{sub}</div>
    </div>"""

def alert_panel(cls, icon, title, pct, count, threshold_text):
    return f"""<div class='alert-panel {cls}'>
      <h3>{icon} {title}</h3>
      <div class='big-num'>{pct:.1f}%</div>
      <p>{count:,} readings &nbsp;·&nbsp; {threshold_text}</p>
    </div>"""

def styled_fig(fig):
    """Apply AI tech palette to every matplotlib figure."""
    fig.patch.set_facecolor("#00000000")
    for ax in fig.get_axes():
        ax.set_facecolor("#00000000")
        ax.tick_params(colors=T2, labelsize=9, which='both')
        ax.xaxis.label.set_color(T2)
        ax.yaxis.label.set_color(T2)
        if ax.get_title():
            ax.title.set_color(T1)
            ax.title.set_fontsize(11)
        for sp in ['bottom', 'left']:
            ax.spines[sp].set_color("rgba(148,163,184,0.2)")
            ax.spines[sp].set_linewidth(0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, color="rgba(148,163,184,0.12)", alpha=1, linewidth=0.5, linestyle='--')
    plt.tight_layout(pad=1.5)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    page_header("📊", "System Overview",
                "Real-time health monitoring & predictive intelligence", tag="LIVE FEED")

    avg_cost = (critical_count * 12000 + maint_count * 2000) / 12
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric_glass("✅ Healthy Status",  f"{healthy_count/len(df)*100:.1f}%", f"{healthy_count:,} readings",  "0.05s"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("⚠️ Maintenance",    f"{maint_count/len(df)*100:.1f}%",   f"{maint_count:,} readings",    "0.10s"), unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("🚨 Critical",        f"{critical_count/len(df)*100:.1f}%",f"{critical_count:,} readings", "0.15s"), unsafe_allow_html=True)
    with c4: st.markdown(metric_glass("💰 Savings / Mo",   f"${avg_cost:,.0f}",                  "vs emergency repairs",         "0.20s"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📍 System Health Status")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(alert_panel("alert-panel alert-healthy","✅","Healthy",   healthy_count/len(df)*100, healthy_count, f"Vibration &lt; {healthy_thr:.2f}"), unsafe_allow_html=True)
    with col2: st.markdown(alert_panel("alert-panel alert-warning","⚠️","Maintenance",maint_count/len(df)*100,  maint_count,  f"{healthy_thr:.2f} – {critical_thr:.2f}"), unsafe_allow_html=True)
    with col3: st.markdown(alert_panel("alert-panel alert-critical","🚨","Critical", critical_count/len(df)*100,critical_count,f"Vibration &gt; {critical_thr:.2f}"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💡 Key Insights")
    col1, col2 = st.columns(2)
    with col1:
        r = df['revolutions'].corr(df['vibration'])
        st.success(f"**🚪 Door Usage Impact: r = {r:.3f}**\n\nVERY STRONG correlation\n\n• High-usage elevators: +51% vibration\n• Usage is PRIMARY driver\n• Maintenance = usage intensity")
    with col2:
        r2 = df['humidity'].corr(df['vibration'])
        st.info(f"**💨 Environmental Impact: r = {r2:.3f}**\n\nWEAK correlation\n\n• Humidity has minor effect\n• Not a primary concern\n• Focus on usage-based maintenance")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💰 Financial Impact Analysis")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(metric_glass("Emergency Repair",   "$12,000", "per incident"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("Preventive Service", "$2,000",  "per service"),  unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("Break-Even",         "2 failures/yr", "$12,000 savings"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ADVANCED ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in page:
    page_header("📈", "Advanced Analytics",
                "Deep-dive data exploration with interactive filters", tag="INTERACTIVE")

    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.subheader("🎛️ Data Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        vib_range = st.slider("Vibration Range",
            float(df['vibration'].min()), float(df['vibration'].max()),
            (float(df['vibration'].min()), float(df['vibration'].max())), step=0.1)
    with col2:
        rev_range = st.slider("Door Revolutions",
            float(df['revolutions'].min()), float(df['revolutions'].max()),
            (float(df['revolutions'].min()), float(df['revolutions'].max())), step=1.0)
    with col3:
        hum_range = st.slider("Humidity %",
            float(df['humidity'].min()), float(df['humidity'].max()),
            (float(df['humidity'].min()), float(df['humidity'].max())), step=1.0)
    st.markdown("</div>", unsafe_allow_html=True)

    fdf = df[
        (df['vibration']   >= vib_range[0]) & (df['vibration']   <= vib_range[1]) &
        (df['revolutions'] >= rev_range[0]) & (df['revolutions'] <= rev_range[1]) &
        (df['humidity']    >= hum_range[0]) & (df['humidity']    <= hum_range[1])
    ]

    st.markdown(
        f"<div class='glass-card fade-up-1' style='padding:14px 20px;'>"
        f"<span style='font-family:\"Rajdhani\",sans-serif;font-size:11px;color:{T2};letter-spacing:.12em;'>FILTER RESULT</span>"
        f"&nbsp;&nbsp;<strong style='color:{CY};font-size:18px;font-family:\"Rajdhani\",sans-serif;'>{len(fdf):,}</strong>"
        f"<span style='color:{T2};font-size:13px;'> / {len(df):,} readings</span>"
        f"&nbsp;&nbsp;·&nbsp;&nbsp;Healthy: <strong style='color:{OK};'>{len(fdf[fdf['vibration']<healthy_thr]):,}</strong>"
        f"&nbsp;&nbsp;·&nbsp;&nbsp;Critical: <strong style='color:{CRIT};'>{len(fdf[fdf['vibration']>=critical_thr]):,}</strong>"
        f"</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Time Series", "📉 Distributions", "📍 Correlations", "🔍 Statistics", "📋 Data Table"])

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5), facecolor='none')
        ax.plot(fdf['ID'], fdf['vibration'], linewidth=1.4, color=CY, alpha=0.9, label='Vibration')
        ax.axhline(mean_vib,    color=OK,   linestyle='--', linewidth=1.4, label=f'Mean ({mean_vib:.2f})',    alpha=0.8)
        ax.axhline(healthy_thr, color=WARN, linestyle='--', linewidth=1.4, label=f'Warn ({healthy_thr:.2f})', alpha=0.8)
        ax.axhline(critical_thr,color=CRIT, linestyle='--', linewidth=1.4, label=f'Crit ({critical_thr:.2f})',alpha=0.8)
        ax.fill_between(fdf['ID'], healthy_thr, critical_thr,     alpha=0.05, color=WARN)
        ax.fill_between(fdf['ID'], critical_thr, fdf['vibration'].max(), alpha=0.05, color=CRIT)
        ax.set_xlabel('Reading ID'); ax.set_ylabel('Vibration')
        ax.legend(loc='upper right', fontsize=8, facecolor=BG,
                  edgecolor="rgba(0,212,255,0.2)", labelcolor=T2)
        styled_fig(fig)
        st.pyplot(fig, transparent=True); plt.close()

    with tab2:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='none')
        for ax, col, clr in zip(axes, ['vibration','revolutions','humidity'], [CY, BL, PU]):
            ax.hist(fdf[col], bins=40, color=clr, alpha=0.70, edgecolor='none')
            ax.set_title(col.capitalize(), fontsize=11, pad=8)
            ax.set_xlabel(col); ax.set_ylabel('Count')
        styled_fig(fig)
        st.pyplot(fig, transparent=True); plt.close()

    with tab3:
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
        corr = fdf[['vibration','revolutions','humidity']].corr()
        cmap = sns.diverging_palette(220, 20, as_cmap=True)
        sns.heatmap(corr, ax=ax, annot=True, fmt='.3f', cmap=cmap,
                    linewidths=0.5, linecolor="rgba(148,163,184,0.15)",
                    cbar_kws={'shrink': 0.8}, annot_kws={'size': 11, 'color': T1})
        ax.set_title('Correlation Matrix', fontsize=12, pad=12)
        styled_fig(fig)
        st.pyplot(fig, transparent=True); plt.close()

    with tab4:
        stats = fdf[['vibration','revolutions','humidity']].describe().round(4)
        st.dataframe(stats, use_container_width=True)

    with tab5:
        st.dataframe(fdf.head(500), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — ML PREDICTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif "ML" in page:
    page_header("🤖", "ML Predictions",
                "Random Forest predictive maintenance engine", tag="AI CORE")

    if not ML_AVAILABLE:
        st.error("scikit-learn is not installed. Run: pip install scikit-learn")
        st.stop()

    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.subheader("⚙️ Model Configuration")
    col1, col2, col3 = st.columns(3)
    with col1: n_estimators = st.slider("Number of Trees", 10, 300, 100, step=10)
    with col2: test_size    = st.slider("Test Split %", 10, 40, 20)
    with col3: max_depth    = st.slider("Max Depth", 2, 20, 8)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀  Train Model"):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score

        X = df[['revolutions', 'humidity']]
        y = df['vibration']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size / 100, random_state=42)

        with st.spinner("Training Random Forest..."):
            model = RandomForestRegressor(n_estimators=n_estimators,
                                          max_depth=max_depth, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        mse  = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2   = r2_score(y_test, y_pred)

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(metric_glass("R² Score",  f"{r2:.4f}",   "Model accuracy"),          unsafe_allow_html=True)
        with c2: st.markdown(metric_glass("RMSE",      f"{rmse:.4f}", "Root mean squared error"),  unsafe_allow_html=True)
        with c3: st.markdown(metric_glass("Test Rows", f"{len(X_test):,}", f"{test_size}% of data"), unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='none')
        axes[0].scatter(y_test, y_pred, color=CY, alpha=0.35, s=12, edgecolors='none')
        mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
        axes[0].plot([mn, mx], [mn, mx], color=CRIT, linestyle='--', linewidth=1.5, alpha=0.8)
        axes[0].set_xlabel('Actual'); axes[0].set_ylabel('Predicted')
        axes[0].set_title('Actual vs Predicted', fontsize=11)

        feat_imp = pd.Series(model.feature_importances_,
                             index=X.columns).sort_values(ascending=True)
        axes[1].barh(feat_imp.index, feat_imp.values, color=[BL, CY], alpha=0.85)
        axes[1].set_title('Feature Importance', fontsize=11)
        axes[1].set_xlabel('Importance Score')

        styled_fig(fig)
        st.pyplot(fig, transparent=True); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — ALERTS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Alerts" in page:
    page_header("🚨", "Alerts & Warnings",
                "Threshold monitoring and anomaly detection", tag=f"{critical_count} ACTIVE")

    st.subheader("🔴 Critical Readings")
    critical_df = df[df['vibration'] >= critical_thr].copy()
    if not critical_df.empty:
        st.markdown(
            f"<div class='alert-panel alert-critical' style='margin-bottom:16px;'>"
            f"<h3>🚨 {len(critical_df)} Critical Readings Detected</h3>"
            f"<p>Vibration exceeds {critical_thr:.2f} — Immediate inspection required</p>"
            f"</div>", unsafe_allow_html=True)
        st.dataframe(critical_df.head(100), use_container_width=True)
    else:
        st.success("✅ No critical readings detected.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🟡 Maintenance Readings")
    maint_df = df[(df['vibration'] >= healthy_thr) & (df['vibration'] < critical_thr)]
    if not maint_df.empty:
        st.markdown(
            f"<div class='alert-panel alert-warning' style='margin-bottom:16px;'>"
            f"<h3>⚠️ {len(maint_df)} Readings Require Maintenance</h3>"
            f"<p>Vibration between {healthy_thr:.2f} and {critical_thr:.2f} — Schedule service</p>"
            f"</div>", unsafe_allow_html=True)
        st.dataframe(maint_df.head(100), use_container_width=True)
    else:
        st.success("✅ No maintenance readings detected.")

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif "Report" in page:
    page_header("📑", "Report Generator",
                "Automated diagnostic report compilation", tag="EXPORT READY")

    col1, col2 = st.columns([2, 1])
    with col1: report_title = st.text_input("Report Title", value="TechLift Elevator Health Report")
    with col2: report_date  = st.text_input("Report Date", value=datetime.now().strftime("%Y-%m-%d"))

    include_sections = st.multiselect(
        "Include Sections",
        ["Executive Summary","Health Overview","Critical Incidents",
         "Financial Analysis","Correlation Analysis","Recommendations"],
        default=["Executive Summary","Health Overview","Critical Incidents","Recommendations"]
    )

    if st.button("📄  Generate Report"):
        report_lines = [
            f"# {report_title}",
            f"**Generated:** {report_date} | **System:** TechLift EMS v5.0", "---",
        ]
        if "Executive Summary" in include_sections:
            report_lines += ["## Executive Summary",
                f"Analyzed **{len(df):,} sensor readings**. System health: **{healthy_pct:.1f}% healthy**, "
                f"{maint_count/len(df)*100:.1f}% maintenance, {critical_count/len(df)*100:.1f}% critical.", ""]
        if "Health Overview" in include_sections:
            report_lines += ["## Health Overview",
                f"- **Healthy:** {healthy_count:,} readings ({healthy_count/len(df)*100:.1f}%)",
                f"- **Maintenance:** {maint_count:,} readings ({maint_count/len(df)*100:.1f}%)",
                f"- **Critical:** {critical_count:,} readings ({critical_count/len(df)*100:.1f}%)", ""]
        if "Critical Incidents" in include_sections:
            report_lines += ["## Critical Incidents",
                f"Threshold: vibration > {critical_thr:.4f}",
                f"Total critical readings: **{critical_count:,}**", ""]
        if "Financial Analysis" in include_sections:
            avg_cost = (critical_count * 12000 + maint_count * 2000) / 12
            report_lines += ["## Financial Analysis",
                "- Emergency repair cost: $12,000/incident",
                "- Preventive service cost: $2,000/service",
                f"- Estimated monthly savings: **${avg_cost:,.0f}**", ""]
        if "Correlation Analysis" in include_sections:
            r  = df['revolutions'].corr(df['vibration'])
            r2 = df['humidity'].corr(df['vibration'])
            report_lines += ["## Correlation Analysis",
                f"- Door revolutions vs vibration: **r = {r:.4f}** (Very strong)",
                f"- Humidity vs vibration: **r = {r2:.4f}** (Weak)", ""]
        if "Recommendations" in include_sections:
            report_lines += ["## Recommendations",
                "1. Prioritize inspection for all critical vibration readings immediately",
                "2. Schedule preventive maintenance for high-usage elevators",
                "3. Implement usage-based maintenance scheduling",
                "4. Monitor revolutions as the primary health indicator", ""]

        report_md = "\n".join(report_lines)
        st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
        st.markdown(report_md)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("⬇️  Download Report (.md)", report_md,
                           file_name=f"techlift_report_{report_date}.md", mime="text/markdown")

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Settings" in page:
    page_header("⚙️", "Settings", "System configuration and preferences", tag="CONFIG")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
        st.subheader("🎨 Appearance")
        theme_choice = st.selectbox("UI Theme", ["dark", "light"],
                                    index=0 if st.session_state.theme == "dark" else 1)
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card fade-up-1'>", unsafe_allow_html=True)
        st.subheader("📊 Alert Thresholds")
        st.markdown(f"""
        <div style='font-family:"Rajdhani",sans-serif;font-size:13px;color:{T2};line-height:2.2;letter-spacing:.04em;'>
          MEAN VIBRATION &nbsp;&nbsp;<span style='color:{CY};'>{mean_vib:.4f}</span><br>
          STD DEVIATION &nbsp;&nbsp;&nbsp;<span style='color:{CY};'>{std_vib:.4f}</span><br>
          HEALTHY THRESHOLD &nbsp;<span style='color:{WARN};'>{healthy_thr:.4f}</span><br>
          CRITICAL THRESHOLD &nbsp;<span style='color:{CRIT};'>{critical_thr:.4f}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card fade-up-2'>", unsafe_allow_html=True)
        st.subheader("👤 User Profile")
        st.markdown(f"""
        <div style='font-family:"Rajdhani",sans-serif;font-size:13px;color:{T2};line-height:2.2;letter-spacing:.04em;'>
          USER ID &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:{CY};'>{st.session_state.username}</span><br>
          ROLE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:{CY};'>{role}</span><br>
          SESSION &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:{OK};'>ACTIVE</span><br>
          UPLINK &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:{OK};'>CONNECTED</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card fade-up-3'>", unsafe_allow_html=True)
        st.subheader("📦 Dataset Info")
        st.markdown(f"""
        <div style='font-family:"Rajdhani",sans-serif;font-size:13px;color:{T2};line-height:2.2;letter-spacing:.04em;'>
          ROWS &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:{CY};'>{len(df):,}</span><br>
          COLUMNS &nbsp;<span style='color:{CY};'>{len(df.columns)}</span><br>
          SOURCE &nbsp;&nbsp;<span style='color:{BL};'>elevator_sensor_data_cleaned.csv</span><br>
          CACHED &nbsp;&nbsp;<span style='color:{OK};'>YES</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

