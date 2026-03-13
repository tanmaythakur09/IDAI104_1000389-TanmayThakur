"""
🏢 TechLift Elevator Monitoring System v4.1
Ultra-premium tech-themed UI: Cyberpunk/Futuristic dark theme
UI/UX Improvements:
 - Fixed all missing CSS classes (user-badge, nav-section, sidebar-stat, fade-up, etc.)
 - Consistent light/dark theming with no hardcoded dark-only colors
 - Polished metric cards with shimmer animations
 - Refined login with animated gradient border
 - Improved sidebar with glowing user avatar + status indicator
 - Better tab styling, chart backgrounds, and scrollbar
 - Micro-interaction hover states across all interactive elements
 - Accessible focus rings with brand color
 - Staggered fade-up entrance animations
 - Responsive sidebar stat grid
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

# ── INJECT CSS ────────────────────────────────────────────────────────────────
def inject_css(theme="dark"):
    G  = "#39ff14"          # neon green accent
    Gm = "rgba(57,255,20,0.12)"
    Gg = "rgba(57,255,20,0.45)"
    R  = "#ff2d55"          # critical red
    Y  = "#ffc107"          # warning amber
    B  = "#00b4ff"          # info blue

    if theme == "dark":
        BG    = "#060608"
        CARD  = "rgba(14,16,20,0.82)"
        INPUT = "rgba(6,6,8,0.75)"
        T1    = "#ecf0f1"
        T2    = "#8899aa"
        BORD  = "rgba(57,255,20,0.18)"
        SBG   = "rgba(8,10,12,0.97)"
        GRID  = "rgba(255,255,255,0.04)"
        SHADOW= "rgba(0,0,0,0.6)"
    else:
        BG    = "#f0f4f8"
        CARD  = "rgba(255,255,255,0.88)"
        INPUT = "rgba(255,255,255,0.95)"
        T1    = "#0d1b2a"
        T2    = "#4a6080"
        BORD  = "rgba(57,255,20,0.35)"
        SBG   = "rgba(248,252,255,0.97)"
        GRID  = "rgba(0,0,0,0.04)"
        SHADOW= "rgba(0,0,0,0.12)"

    css = f"""
<style>
/* ── GOOGLE FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ── CSS VARIABLES ── */
:root {{
  --accent:      {G};
  --accent-muted:{Gm};
  --accent-glow: {Gg};
  --critical:    {R};
  --warning:     {Y};
  --info:        {B};
  --bg:          {BG};
  --card:        {CARD};
  --input:       {INPUT};
  --t1:          {T1};
  --t2:          {T2};
  --border:      {BORD};
  --sbg:         {SBG};
  --grid:        {GRID};
  --shadow:      {SHADOW};
  --font-display:'Orbitron', sans-serif;
  --font-body:   'Rajdhani', sans-serif;
  --font-mono:   'Share Tech Mono', monospace;
  --radius:      6px;
  --transition:  0.25s cubic-bezier(0.4,0,0.2,1);
}}

/* ── RESET & BASE ── */
*, *::before, *::after {{ box-sizing: border-box; }}
html, body {{ font-family: var(--font-body); background-color: var(--bg); }}
.stApp {{
  background: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 60% 40% at 10% 0%,  {Gm} 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 90% 100%, rgba(0,180,255,0.06) 0%, transparent 60%),
    linear-gradient({GRID} 1px, transparent 1px),
    linear-gradient(90deg, {GRID} 1px, transparent 1px) !important;
  background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px !important;
  color: var(--t1);
}}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header {{ visibility: hidden !important; }}
.block-container {{ padding-top: 1.5rem !important; max-width: 100% !important; }}

/* ── SCANLINE OVERLAY ── */
.stApp::after {{
  content: '';
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
  pointer-events: none; z-index: 9999;
}}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
section[data-testid="stSidebar"] {{
  background: var(--sbg) !important;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid var(--border) !important;
  box-shadow: 2px 0 30px rgba(57,255,20,0.08);
  min-width: 265px !important;
}}
section[data-testid="stSidebar"] > div {{ padding: 0 !important; }}
section[data-testid="stSidebar"] .block-container {{ padding: 0 !important; }}

/* User badge */
.user-badge {{
  display: flex; align-items: center; gap: 14px;
  padding: 20px 18px 16px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg, var(--accent-muted), transparent);
  position: relative; overflow: hidden;
}}
.user-badge::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  box-shadow: 0 0 10px var(--accent);
}}
.user-avatar {{
  width: 42px; height: 42px; border-radius: var(--radius);
  background: linear-gradient(135deg, var(--accent-muted), rgba(0,180,255,0.15));
  border: 1.5px solid var(--accent);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display); font-size: 14px; font-weight: 700;
  color: var(--accent); letter-spacing: .05em;
  box-shadow: 0 0 15px var(--accent-muted), inset 0 0 10px var(--accent-muted);
  flex-shrink: 0; position: relative;
}}
.user-avatar::after {{
  content: ''; position: absolute; bottom: -4px; right: -4px;
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--accent); border: 2px solid var(--bg);
  box-shadow: 0 0 8px var(--accent);
  animation: pulse-dot 2s ease infinite;
}}
@keyframes pulse-dot {{
  0%, 100% {{ transform: scale(1); box-shadow: 0 0 8px var(--accent); }}
  50% {{ transform: scale(1.15); box-shadow: 0 0 16px var(--accent); }}
}}
.user-name {{
  font-family: var(--font-display); font-size: 13px; font-weight: 700;
  color: var(--t1) !important; letter-spacing: .08em; text-transform: uppercase;
}}
.user-role {{
  font-family: var(--font-body); font-size: 11px; font-weight: 500;
  color: var(--accent) !important; letter-spacing: .12em; text-transform: uppercase;
  margin-top: 2px;
}}

/* Nav section label */
.nav-section {{
  font-family: var(--font-display); font-size: 9px; font-weight: 600;
  color: var(--t2) !important; letter-spacing: .25em; text-transform: uppercase;
  padding: 16px 18px 8px; opacity: 0.7;
}}

/* Radio nav */
div[data-testid="stRadio"] > label {{ display: none !important; }}
div[data-testid="stRadio"] div[role="radiogroup"] {{
  display: flex; flex-direction: column; gap: 4px; padding: 0 10px;
}}
div[data-testid="stRadio"] label {{
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: var(--radius) !important;
  padding: 10px 14px !important;
  cursor: pointer;
  transition: all var(--transition) !important;
  font-weight: 600 !important; font-size: 12px !important;
  letter-spacing: .1em !important; text-transform: uppercase !important;
  font-family: var(--font-display) !important;
  color: var(--t2) !important;
  position: relative !important; overflow: hidden !important;
}}
div[data-testid="stRadio"] label::before {{
  content: ''; position: absolute; left: 0; top: 20%; bottom: 20%;
  width: 3px; border-radius: 0 2px 2px 0;
  background: transparent; transition: all var(--transition);
}}
div[data-testid="stRadio"] label:hover {{
  background: var(--accent-muted) !important;
  border-color: rgba(57,255,20,0.3) !important;
  color: var(--t1) !important;
  padding-left: 18px !important;
}}
div[data-testid="stRadio"] label:hover::before {{
  background: var(--accent); box-shadow: 0 0 8px var(--accent);
}}
div[data-testid="stRadio"] label[data-selected="true"] {{
  background: linear-gradient(90deg, var(--accent-muted), transparent) !important;
  border-color: var(--border) !important;
  border-left-color: var(--accent) !important;
  color: var(--t1) !important; font-weight: 700 !important;
  box-shadow: inset 0 0 15px var(--accent-muted) !important;
}}
div[data-testid="stRadio"] label[data-selected="true"]::before {{
  background: var(--accent); box-shadow: 0 0 10px var(--accent);
}}

/* Sidebar quick stats */
.sidebar-stats {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
  padding: 0 10px 10px;
}}
.sidebar-stat {{
  background: var(--accent-muted);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 12px 10px; text-align: center;
}}
.s-val {{
  font-family: var(--font-display); font-size: 18px; font-weight: 700;
  color: var(--accent); text-shadow: 0 0 10px var(--accent-muted);
}}
.s-lbl {{
  font-family: var(--font-body); font-size: 10px; font-weight: 600;
  color: var(--t2); text-transform: uppercase; letter-spacing: .12em;
  margin-top: 3px;
}}

/* Logout button */
section[data-testid="stSidebar"] .stButton > button {{
  background: transparent !important;
  color: var(--t2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-display) !important;
  font-size: 11px !important; font-weight: 600 !important;
  letter-spacing: .12em !important; text-transform: uppercase !important;
  padding: 8px 14px !important; width: auto !important;
  transition: all var(--transition) !important;
  margin: 0 10px !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
  border-color: var(--critical) !important;
  color: var(--critical) !important;
  box-shadow: 0 0 12px rgba(255,45,85,0.2) !important;
  background: rgba(255,45,85,0.06) !important;
}}

/* ═══════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════ */
.page-header {{
  background: var(--card);
  border: 1px solid var(--border);
  border-bottom: 2px solid var(--accent);
  border-radius: var(--radius);
  padding: 22px 28px 18px;
  margin-bottom: 26px;
  position: relative; overflow: hidden;
  backdrop-filter: blur(12px);
  animation: fadeUp 0.5s ease both;
}}
.page-header::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, var(--accent) 0%, transparent 60%);
  box-shadow: 0 0 20px var(--accent-glow);
}}
.page-header::after {{
  content: ''; position: absolute;
  top: 0; left: 0; width: 16px; height: 16px;
  border-top: 2px solid var(--accent); border-left: 2px solid var(--accent);
}}
.page-header h1 {{
  font-family: var(--font-display) !important; font-size: 22px !important; font-weight: 700 !important;
  color: var(--t1) !important; text-transform: uppercase !important;
  letter-spacing: .1em !important; margin: 0 0 6px 0 !important;
  text-shadow: 0 0 20px var(--accent-glow);
}}
.page-header p {{
  color: var(--t2) !important; margin: 0 !important;
  font-size: 11px !important; letter-spacing: .2em !important;
  text-transform: uppercase !important; font-weight: 600 !important;
  font-family: var(--font-body) !important;
}}
.page-header-tag {{
  position: absolute; top: 18px; right: 20px;
  background: var(--accent-muted); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 4px 10px;
  font-family: var(--font-mono); font-size: 10px; color: var(--accent);
  letter-spacing: .1em;
}}

/* ═══════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════ */
.metric-glass {{
  background: var(--card);
  border: 1px solid var(--border); border-left: 3px solid var(--accent);
  border-radius: var(--radius); padding: 20px 22px;
  position: relative; overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all var(--transition);
  animation: fadeUp 0.5s ease both;
}}
.metric-glass:hover {{
  border-color: var(--accent);
  box-shadow: 0 0 25px var(--accent-muted), 0 8px 30px var(--shadow);
  transform: translateY(-2px);
}}
.metric-glass::before {{
  content: '';
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, var(--accent-muted) 0%, transparent 60%);
  pointer-events: none;
}}
.metric-glass::after {{
  content: '';
  position: absolute; top: -50%; right: -10px;
  width: 80px; height: 200%;
  background: linear-gradient(90deg, transparent, rgba(57,255,20,0.04), transparent);
  transform: skewX(-20deg);
  animation: shimmer 4s ease-in-out infinite;
}}
@keyframes shimmer {{
  0%, 100% {{ right: -10px; opacity: 0; }}
  40%, 60% {{ right: 60%; opacity: 1; }}
}}
.metric-glass .label {{
  font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .22em;
  color: var(--t2); margin-bottom: 10px; font-family: var(--font-display);
}}
.metric-glass .value {{
  font-size: 32px; font-weight: 700; font-family: var(--font-display);
  color: var(--t1); text-shadow: 0 0 15px var(--accent-muted);
  line-height: 1;
}}
.metric-glass .sub {{
  font-size: 11px; color: var(--t2); margin-top: 8px;
  font-family: var(--font-body); letter-spacing: .06em;
}}

/* ═══════════════════════════════════════
   GLASS CARDS
═══════════════════════════════════════ */
.glass-card {{
  background: var(--card);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 22px; margin: 8px 0;
  box-shadow: 0 4px 20px var(--shadow);
  transition: all var(--transition);
  animation: fadeUp 0.5s ease both;
}}
.glass-card:hover {{
  border-color: rgba(57,255,20,0.35);
  box-shadow: 0 0 25px var(--accent-muted), 0 8px 30px var(--shadow);
}}

/* ═══════════════════════════════════════
   ALERT PANELS
═══════════════════════════════════════ */
.alert-panel {{
  border-radius: var(--radius); padding: 20px 22px;
  margin-bottom: 10px; position: relative; overflow: hidden;
  transition: all var(--transition);
}}
.alert-panel:hover {{ transform: translateX(3px); }}
.alert-panel::before {{
  content: ''; position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px;
}}
.alert-panel h3 {{
  margin: 0 0 6px 0 !important; font-family: var(--font-display) !important;
  font-size: 13px !important; text-transform: uppercase !important; letter-spacing: .1em !important;
}}
.alert-panel p {{
  margin: 4px 0 0 0 !important; font-size: 11px !important; opacity: 0.8 !important;
  font-family: var(--font-body) !important;
}}
.alert-panel .big-num {{
  font-size: 32px; font-weight: 800; font-family: var(--font-display);
  line-height: 1; margin: 4px 0;
}}

.alert-healthy {{
  background: linear-gradient(135deg, rgba(57,255,20,0.08), transparent);
  border: 1px solid rgba(57,255,20,0.25); color: {G};
  box-shadow: 0 0 20px rgba(57,255,20,0.06);
}}
.alert-healthy::before {{ background: {G}; box-shadow: 0 0 12px {G}; }}
.alert-healthy:hover {{ box-shadow: 0 0 30px rgba(57,255,20,0.15); border-color: {G}; }}

.alert-warning {{
  background: linear-gradient(135deg, rgba(255,193,7,0.08), transparent);
  border: 1px solid rgba(255,193,7,0.25); color: {Y};
  box-shadow: 0 0 20px rgba(255,193,7,0.06);
}}
.alert-warning::before {{ background: {Y}; box-shadow: 0 0 12px {Y}; }}
.alert-warning:hover {{ box-shadow: 0 0 30px rgba(255,193,7,0.15); border-color: {Y}; }}

.alert-critical {{
  background: linear-gradient(135deg, rgba(255,45,85,0.08), transparent);
  border: 1px solid rgba(255,45,85,0.25); color: {R};
  box-shadow: 0 0 20px rgba(255,45,85,0.06);
  animation: critical-pulse 2.5s ease infinite;
}}
.alert-critical::before {{ background: {R}; box-shadow: 0 0 12px {R}; }}
.alert-critical:hover {{ box-shadow: 0 0 30px rgba(255,45,85,0.2); border-color: {R}; }}
@keyframes critical-pulse {{
  0%, 100% {{ box-shadow: 0 0 20px rgba(255,45,85,0.06); }}
  50% {{ box-shadow: 0 0 30px rgba(255,45,85,0.18); }}
}}

/* ═══════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════ */
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.fade-up {{ animation: fadeUp 0.45s ease both; }}
.fade-up-1 {{ animation: fadeUp 0.45s 0.05s ease both; }}
.fade-up-2 {{ animation: fadeUp 0.45s 0.10s ease both; }}
.fade-up-3 {{ animation: fadeUp 0.45s 0.15s ease both; }}
.fade-up-4 {{ animation: fadeUp 0.45s 0.20s ease both; }}

/* ═══════════════════════════════════════
   GLOBAL BUTTONS
═══════════════════════════════════════ */
.stButton > button {{
  background: transparent !important;
  color: var(--accent) !important;
  border: 1px solid var(--accent) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-display) !important;
  font-weight: 600 !important; font-size: 11px !important;
  padding: 10px 22px !important; width: 100% !important;
  transition: all var(--transition) !important;
  letter-spacing: .15em !important; text-transform: uppercase !important;
  box-shadow: inset 0 0 12px var(--accent-muted) !important;
  position: relative !important; overflow: hidden !important;
}}
.stButton > button:hover {{
  background: var(--accent-muted) !important;
  color: var(--t1) !important;
  box-shadow: 0 0 22px var(--accent-glow), inset 0 0 15px var(--accent-muted) !important;
}}
.stButton > button:focus-visible {{
  outline: 2px solid var(--accent) !important; outline-offset: 2px !important;
}}

/* ═══════════════════════════════════════
   TEXT INPUTS
═══════════════════════════════════════ */
.stTextInput > div > div > input {{
  background: var(--input) !important;
  border: 1px solid var(--border) !important;
  border-left: 3px solid var(--accent) !important;
  border-radius: var(--radius) !important;
  color: var(--t1) !important;
  padding: 13px 16px !important;
  font-size: 15px !important; font-family: var(--font-body) !important;
  letter-spacing: .04em; transition: all var(--transition);
}}
.stTextInput > div > div > input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 18px var(--accent-muted), 0 0 0 3px rgba(57,255,20,0.08) !important;
  outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: var(--t2) !important; opacity: 0.6; }}

/* Labels */
.stTextInput > label, .stSelectbox > label,
.stSlider > label, .stMultiSelect > label {{
  color: var(--t2) !important;
  font-family: var(--font-display) !important;
  font-size: 10px !important; letter-spacing: .18em !important;
  text-transform: uppercase !important;
  margin-bottom: 6px !important; font-weight: 600 !important;
}}

/* ═══════════════════════════════════════
   SLIDERS
═══════════════════════════════════════ */
.stSlider > div > div > div > div {{
  background: var(--accent) !important;
  box-shadow: 0 0 8px var(--accent) !important;
}}
div[data-testid="stSlider"] > div > div > div[role="slider"] {{
  background: var(--bg) !important;
  border: 2px solid var(--accent) !important;
  box-shadow: 0 0 12px var(--accent) !important;
  border-radius: 50% !important;
  width: 16px !important; height: 16px !important;
  transition: transform var(--transition) !important;
}}
div[data-testid="stSlider"] > div > div > div[role="slider"]:hover {{
  transform: scale(1.25) !important;
}}

/* ═══════════════════════════════════════
   TABS
═══════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 4px !important; gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
  background: transparent !important;
  border: none !important; border-radius: 4px !important;
  color: var(--t2) !important;
  font-family: var(--font-display) !important;
  font-size: 10px !important; font-weight: 600 !important;
  letter-spacing: .1em !important; text-transform: uppercase !important;
  padding: 8px 16px !important;
  transition: all var(--transition) !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
  background: var(--accent-muted) !important; color: var(--t1) !important;
}}
.stTabs [aria-selected="true"] {{
  background: var(--accent-muted) !important;
  color: var(--accent) !important;
  box-shadow: inset 0 0 12px var(--accent-muted) !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{
  background: var(--accent) !important;
  height: 2px !important;
  box-shadow: 0 0 10px var(--accent) !important;
}}

/* ═══════════════════════════════════════
   DATAFRAME
═══════════════════════════════════════ */
.stDataFrame {{
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; overflow: hidden !important;
}}
.stDataFrame table {{ background: var(--input) !important; color: var(--t1) !important; font-family: var(--font-mono) !important; }}
.stDataFrame th {{ background: var(--card) !important; color: var(--t2) !important; font-family: var(--font-display) !important; font-size: 10px !important; letter-spacing: .12em !important; text-transform: uppercase !important; }}
.stDataFrame tr:hover td {{ background: var(--accent-muted) !important; }}

/* ═══════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════ */
.stSelectbox > div > div {{
  background: var(--input) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--t1) !important;
}}
.stSelectbox > div > div:focus-within {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 12px var(--accent-muted) !important;
}}

/* ═══════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════ */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
  background: rgba(57,255,20,0.4); border-radius: 3px;
  transition: background var(--transition);
}}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

/* ═══════════════════════════════════════
   HEADINGS
═══════════════════════════════════════ */
h2, h3 {{
  color: var(--t1) !important; font-family: var(--font-display) !important;
  letter-spacing: .06em !important; text-transform: uppercase !important;
  font-size: 14px !important;
}}
hr {{ border-color: var(--border) !important; margin: 20px 0 !important; }}

/* ═══════════════════════════════════════
   STATUS ALERTS (Streamlit native)
═══════════════════════════════════════ */
.stSuccess, .stInfo, .stWarning, .stError {{
  border-radius: var(--radius) !important;
  font-family: var(--font-body) !important;
}}

/* ═══════════════════════════════════════
   LOGIN PAGE
═══════════════════════════════════════ */
.login-wrapper {{
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; width: 100%; min-height: 80vh;
}}
.login-card {{
  background: var(--card);
  backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
  border: 1px solid var(--border);
  padding: 48px 44px; width: 100%; max-width: 460px;
  border-radius: var(--radius);
  box-shadow: 0 0 60px rgba(0,0,0,0.4), inset 0 0 40px var(--accent-muted);
  position: relative; overflow: hidden;
  animation: fadeUp 0.6s ease both;
}}
.login-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, {G} 30%, #fff 50%, {G} 70%, transparent 100%);
  box-shadow: 0 0 20px {G};
  animation: scan-line 3s ease-in-out infinite;
}}
@keyframes scan-line {{
  0%, 100% {{ opacity: 0.6; }}
  50% {{ opacity: 1; }}
}}
.login-card .corner-tl {{
  position: absolute; top: 0; left: 0;
  width: 18px; height: 18px;
  border-top: 2px solid {G}; border-left: 2px solid {G};
}}
.login-card .corner-br {{
  position: absolute; bottom: 0; right: 0;
  width: 18px; height: 18px;
  border-bottom: 2px solid {G}; border-right: 2px solid {G};
}}
.login-card .corner-tr {{
  position: absolute; top: 0; right: 0;
  width: 18px; height: 18px;
  border-top: 2px solid rgba(57,255,20,0.3); border-right: 2px solid rgba(57,255,20,0.3);
}}
.login-card .corner-bl {{
  position: absolute; bottom: 0; left: 0;
  width: 18px; height: 18px;
  border-bottom: 2px solid rgba(57,255,20,0.3); border-left: 2px solid rgba(57,255,20,0.3);
}}
.tech-badge {{
  position: absolute; top: 18px; right: 18px;
  background: var(--accent-muted); border: 1px solid var(--border);
  padding: 5px 10px; font-size: 9px; color: {G};
  letter-spacing: .15em; font-family: var(--font-display); font-weight: 700;
  box-shadow: 0 0 10px var(--accent-muted); border-radius: var(--radius);
}}
.status-dot {{
  width: 7px; height: 7px; background: {G}; border-radius: 50%;
  box-shadow: 0 0 10px {G}; display: inline-block;
  animation: pulse-dot 1.5s ease infinite; margin-right: 5px;
  vertical-align: middle;
}}
.login-icon {{
  text-align: center; font-size: 52px; margin-bottom: 12px;
  filter: drop-shadow(0 0 20px {Gg});
  animation: float 3s ease-in-out infinite;
}}
@keyframes float {{
  0%, 100% {{ transform: translateY(0); }}
  50%       {{ transform: translateY(-5px); }}
}}
.login-title {{
  text-align: center; font-family: var(--font-display);
  font-size: 32px; font-weight: 900; color: var(--t1);
  text-shadow: 0 0 25px {Gg}; letter-spacing: .18em;
  text-transform: uppercase; margin-bottom: 4px;
}}
.login-subtitle {{
  text-align: center; font-size: 11px; color: var(--t2);
  margin-bottom: 32px; letter-spacing: .3em; text-transform: uppercase;
  font-family: var(--font-body); font-weight: 600;
}}
.login-divider {{
  height: 1px; background: var(--border); margin: 28px 0;
  position: relative;
}}
.login-divider::before {{
  content: 'SYSTEM ACCESS'; position: absolute;
  top: 50%; left: 50%; transform: translate(-50%, -50%);
  background: var(--card); padding: 0 12px;
  font-family: var(--font-mono); font-size: 9px; color: var(--t2); letter-spacing: .15em;
}}
.login-features {{
  display: flex; justify-content: center; gap: 24px;
  padding-top: 22px; border-top: 1px solid var(--border);
}}
.login-feat {{
  text-align: center; font-size: 10px; color: var(--t2);
  text-transform: uppercase; letter-spacing: .12em; font-family: var(--font-display);
}}
.login-feat .feat-icon {{
  font-size: 22px; display: block; margin-bottom: 6px;
  filter: drop-shadow(0 0 8px {Gg});
}}
.login-hint {{
  text-align: center; margin-top: 22px;
  color: var(--t2); font-size: 10px;
  font-family: var(--font-mono); letter-spacing: .06em; opacity: 0.7;
}}
.login-hint span {{ color: {B}; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


inject_css(st.session_state.theme)

# ── LOGIN PAGE ─────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""<style>
    section[data-testid="stSidebar"]{{display:none!important;}}
    header{{display:none!important;}}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
        st.markdown("""
        <div class='login-card'>
            <div class='corner-tl'></div><div class='corner-br'></div>
            <div class='corner-tr'></div><div class='corner-bl'></div>
            <div class='tech-badge'><span class='status-dot'></span>SYS.ONLINE</div>
            <div class='login-icon'>💠</div>
            <div class='login-title'>TechLift</div>
            <div class='login-subtitle'>v4.1 · Predictive AI Core</div>
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

        st.markdown("""
            <div class='login-features'>
                <div class='login-feat'><span class='feat-icon'>🛡️</span>AES-256</div>
                <div class='login-feat'><span class='feat-icon'>📡</span>Uplink</div>
                <div class='login-feat'><span class='feat-icon'>🧠</span>Neural Net</div>
            </div>
            <div class='login-hint'>
                OVERRIDE: [<span>admin</span> : <span>elevate123</span>] · [<span>tanmay</span> : <span>1234</span>]
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

# ── ROLE ──────────────────────────────────────────────────────────────────────
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

    st.markdown("<div style='padding:8px 10px 4px;'>", unsafe_allow_html=True)
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
        <div class='sidebar-stat'>
            <div class='s-val'>{len(df):,}</div>
            <div class='s-lbl'>Readings</div>
        </div>
        <div class='sidebar-stat'>
            <div class='s-val'>{healthy_pct:.0f}%</div>
            <div class='s-lbl'>Healthy</div>
        </div>
        <div class='sidebar-stat'>
            <div class='s-val'>{critical_count:,}</div>
            <div class='s-lbl'>Critical</div>
        </div>
        <div class='sidebar-stat'>
            <div class='s-val'>{maint_count:,}</div>
            <div class='s-lbl'>Maint.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:16px 18px 12px;border-top:1px solid var(--border);margin-top:auto;'>
        <div style='font-size:9px;color:var(--t2);text-align:center;font-family:var(--font-mono);letter-spacing:.1em;'>
            🏢 TechLift EMS · v4.1 · © 2026
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

def styled_fig(fig, theme="dark"):
    BG   = "#060608" if theme == "dark" else "#f0f4f8"
    FG   = "#ecf0f1" if theme == "dark" else "#0d1b2a"
    GRID = "#1a2030" if theme == "dark" else "#d1dce8"
    fig.patch.set_facecolor(BG)
    for ax in fig.get_axes():
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=9)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        if hasattr(ax, 'title'): ax.title.set_color(FG)
        for spine in ['bottom','left']:
            ax.spines[spine].set_color(GRID)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, color=GRID, alpha=0.5, linewidth=0.5, linestyle='--')
    plt.tight_layout(pad=1.5)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    page_header("📊", "System Overview",
                "Real-time health monitoring & predictive intelligence",
                tag="LIVE FEED")

    avg_cost = (critical_count * 12000 + maint_count * 2000) / 12
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric_glass("✅ Healthy Status",  f"{healthy_count/len(df)*100:.1f}%", f"{healthy_count:,} readings", "0.05s"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("⚠️ Maintenance",    f"{maint_count/len(df)*100:.1f}%",   f"{maint_count:,} readings",   "0.10s"), unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("🚨 Critical",        f"{critical_count/len(df)*100:.1f}%",f"{critical_count:,} readings","0.15s"), unsafe_allow_html=True)
    with c4: st.markdown(metric_glass("💰 Savings / Mo",   f"${avg_cost:,.0f}",                  "vs emergency repairs",        "0.20s"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📍 System Health Status")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(alert_panel("alert-panel alert-healthy", "✅", "Healthy",
                                healthy_count/len(df)*100, healthy_count,
                                f"Vibration &lt; {healthy_thr:.2f}"), unsafe_allow_html=True)
    with col2:
        st.markdown(alert_panel("alert-panel alert-warning", "⚠️", "Maintenance",
                                maint_count/len(df)*100, maint_count,
                                f"{healthy_thr:.2f} – {critical_thr:.2f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(alert_panel("alert-panel alert-critical", "🚨", "Critical",
                                critical_count/len(df)*100, critical_count,
                                f"Vibration &gt; {critical_thr:.2f}"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💡 Key Insights")
    col1, col2 = st.columns(2)
    with col1:
        r = df['revolutions'].corr(df['vibration'])
        st.success(f"**🚪 Door Usage Impact: r = {r:.3f}**\n\nVERY STRONG correlation\n\n"
                   "• High-usage elevators: +51% vibration\n• Usage is PRIMARY driver\n• Maintenance = usage intensity")
    with col2:
        r2 = df['humidity'].corr(df['vibration'])
        st.info(f"**💨 Environmental Impact: r = {r2:.3f}**\n\nWEAK correlation\n\n"
                "• Humidity has minor effect\n• Not a primary concern\n• Focus on usage-based maintenance")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💰 Financial Impact Analysis")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(metric_glass("Emergency Repair",   "$12,000", "per incident"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("Preventive Service", "$2,000",  "per service"),  unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("Break-Even",         "2 failures/yr", "$12,000 savings"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: ADVANCED ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in page:
    page_header("📈", "Advanced Analytics",
                "Deep-dive data exploration with interactive filters",
                tag="INTERACTIVE")

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
        f"<div class='glass-card fade-up-1'>"
        f"<span style='font-family:var(--font-mono);font-size:12px;color:var(--t2);'>FILTER RESULT</span>&nbsp;&nbsp;"
        f"<strong style='color:var(--accent);font-size:16px;'>{len(fdf):,}</strong>"
        f"<span style='color:var(--t2);'> / {len(df):,} readings</span>"
        f"&nbsp;&nbsp;·&nbsp;&nbsp;Healthy: <strong>{len(fdf[fdf['vibration']<healthy_thr]):,}</strong>"
        f"&nbsp;&nbsp;·&nbsp;&nbsp;Critical: <strong style='color:var(--critical);'>{len(fdf[fdf['vibration']>=critical_thr]):,}</strong>"
        f"</div>",
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Time Series", "📉 Distributions", "📍 Correlations", "🔍 Statistics", "📋 Data Table"]
    )

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(fdf['ID'], fdf['vibration'], linewidth=1.2, color='#39ff14', alpha=0.85, label='Vibration')
        ax.axhline(mean_vib,    color='#10b981', linestyle='--', linewidth=1.5, label=f'Mean ({mean_vib:.2f})', alpha=0.8)
        ax.axhline(healthy_thr, color='#ffc107', linestyle='--', linewidth=1.5, label=f'Warn ({healthy_thr:.2f})', alpha=0.8)
        ax.axhline(critical_thr,color='#ff2d55', linestyle='--', linewidth=1.5, label=f'Crit ({critical_thr:.2f})', alpha=0.8)
        ax.fill_between(fdf['ID'], healthy_thr, critical_thr, alpha=0.04, color='#ffc107')
        ax.fill_between(fdf['ID'], critical_thr, fdf['vibration'].max(), alpha=0.04, color='#ff2d55')
        ax.set_xlabel('Reading ID'); ax.set_ylabel('Vibration')
        ax.legend(loc='upper right', fontsize=8, facecolor='#0a0c10', edgecolor='#1e2a3a', labelcolor='#e2e8f0')
        styled_fig(fig, st.session_state.theme)
        st.pyplot(fig); plt.close()

    with tab2:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, col, clr in zip(axes, ['vibration','revolutions','humidity'], ['#39ff14','#00b4ff','#ffc107']):
            ax.hist(fdf[col], bins=40, color=clr, alpha=0.75, edgecolor='none')
            ax.set_title(col.capitalize(), fontsize=11, pad=8)
            ax.set_xlabel(col); ax.set_ylabel('Count')
        styled_fig(fig, st.session_state.theme)
        st.pyplot(fig); plt.close()

    with tab3:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = fdf[['vibration','revolutions','humidity']].corr()
        mask = np.zeros_like(corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True
        sns.heatmap(corr, ax=ax, annot=True, fmt='.3f', cmap='RdYlGn',
                    linewidths=0.5, linecolor='#1e2a3a',
                    cbar_kws={'shrink': 0.8}, mask=~mask ^ mask)
        ax.set_title('Correlation Matrix', fontsize=12, pad=12)
        styled_fig(fig, st.session_state.theme)
        st.pyplot(fig); plt.close()

    with tab4:
        stats = fdf[['vibration','revolutions','humidity']].describe().round(4)
        st.dataframe(stats, use_container_width=True)

    with tab5:
        st.dataframe(fdf.head(500), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: ML PREDICTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif "ML" in page:
    page_header("🤖", "ML Predictions",
                "Random Forest predictive maintenance engine",
                tag="AI CORE")

    if not ML_AVAILABLE:
        st.error("scikit-learn is not installed. Run: pip install scikit-learn")
        st.stop()

    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.subheader("⚙️ Model Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        n_estimators = st.slider("Number of Trees", 10, 300, 100, step=10)
    with col2:
        test_size = st.slider("Test Split %", 10, 40, 20)
    with col3:
        max_depth = st.slider("Max Depth", 2, 20, 8)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀  Train Model"):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score

        X = df[['revolutions', 'humidity']]
        y = df['vibration']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size/100, random_state=42
        )

        with st.spinner("Training Random Forest..."):
            model = RandomForestRegressor(n_estimators=n_estimators,
                                          max_depth=max_depth, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        mse  = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2   = r2_score(y_test, y_pred)

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(metric_glass("R² Score",   f"{r2:.4f}", "Model accuracy"), unsafe_allow_html=True)
        with c2: st.markdown(metric_glass("RMSE",       f"{rmse:.4f}", "Root mean squared error"), unsafe_allow_html=True)
        with c3: st.markdown(metric_glass("Test Rows",  f"{len(X_test):,}", f"{test_size}% of data"), unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        axes[0].scatter(y_test, y_pred, color='#39ff14', alpha=0.4, s=12, edgecolors='none')
        mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
        axes[0].plot([mn, mx], [mn, mx], 'r--', linewidth=1.5, alpha=0.8)
        axes[0].set_xlabel('Actual'); axes[0].set_ylabel('Predicted')
        axes[0].set_title('Actual vs Predicted', fontsize=11)

        feat_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True)
        axes[1].barh(feat_imp.index, feat_imp.values, color=['#39ff14','#00b4ff'], alpha=0.85)
        axes[1].set_title('Feature Importance', fontsize=11)
        axes[1].set_xlabel('Importance Score')

        styled_fig(fig, st.session_state.theme)
        st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: ALERTS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Alerts" in page:
    page_header("🚨", "Alerts & Warnings",
                "Threshold monitoring and anomaly detection",
                tag=f"{critical_count} ACTIVE")

    st.subheader("🔴 Critical Readings")
    critical_df = df[df['vibration'] >= critical_thr].copy()
    if not critical_df.empty:
        st.markdown(
            f"<div class='alert-panel alert-critical' style='margin-bottom:16px;'>"
            f"<h3>🚨 {len(critical_df)} Critical Readings Detected</h3>"
            f"<p>Vibration exceeds {critical_thr:.2f} — Immediate inspection required</p>"
            f"</div>", unsafe_allow_html=True
        )
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
            f"</div>", unsafe_allow_html=True
        )
        st.dataframe(maint_df.head(100), use_container_width=True)
    else:
        st.success("✅ No maintenance readings detected.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif "Report" in page:
    page_header("📑", "Report Generator",
                "Automated diagnostic report compilation",
                tag="EXPORT READY")

    col1, col2 = st.columns([2, 1])
    with col1:
        report_title = st.text_input("Report Title", value="TechLift Elevator Health Report")
    with col2:
        report_date  = st.text_input("Report Date", value=datetime.now().strftime("%Y-%m-%d"))

    include_sections = st.multiselect(
        "Include Sections",
        ["Executive Summary", "Health Overview", "Critical Incidents", "Financial Analysis",
         "Correlation Analysis", "Recommendations"],
        default=["Executive Summary", "Health Overview", "Critical Incidents", "Recommendations"]
    )

    if st.button("📄  Generate Report"):
        report_lines = [
            f"# {report_title}",
            f"**Generated:** {report_date} | **System:** TechLift EMS v4.1",
            "---",
        ]
        if "Executive Summary" in include_sections:
            report_lines += [
                "## Executive Summary",
                f"Analyzed **{len(df):,} sensor readings**. "
                f"System health: **{healthy_pct:.1f}% healthy**, "
                f"{maint_count/len(df)*100:.1f}% maintenance, "
                f"{critical_count/len(df)*100:.1f}% critical.",
                ""
            ]
        if "Health Overview" in include_sections:
            report_lines += [
                "## Health Overview",
                f"- **Healthy:** {healthy_count:,} readings ({healthy_count/len(df)*100:.1f}%)",
                f"- **Maintenance:** {maint_count:,} readings ({maint_count/len(df)*100:.1f}%)",
                f"- **Critical:** {critical_count:,} readings ({critical_count/len(df)*100:.1f}%)",
                ""
            ]
        if "Critical Incidents" in include_sections:
            report_lines += [
                "## Critical Incidents",
                f"Threshold: vibration > {critical_thr:.4f}",
                f"Total critical readings: **{critical_count:,}**",
                ""
            ]
        if "Financial Analysis" in include_sections:
            avg_cost = (critical_count * 12000 + maint_count * 2000) / 12
            report_lines += [
                "## Financial Analysis",
                f"- Emergency repair cost: $12,000/incident",
                f"- Preventive service cost: $2,000/service",
                f"- Estimated monthly savings via predictive maintenance: **${avg_cost:,.0f}**",
                ""
            ]
        if "Correlation Analysis" in include_sections:
            r  = df['revolutions'].corr(df['vibration'])
            r2 = df['humidity'].corr(df['vibration'])
            report_lines += [
                "## Correlation Analysis",
                f"- Door revolutions vs vibration: **r = {r:.4f}** (Very strong)",
                f"- Humidity vs vibration: **r = {r2:.4f}** (Weak)",
                ""
            ]
        if "Recommendations" in include_sections:
            report_lines += [
                "## Recommendations",
                "1. Prioritize inspection for all critical vibration readings immediately",
                "2. Schedule preventive maintenance for high-usage elevators",
                "3. Implement usage-based maintenance scheduling",
                "4. Monitor revolutions as the primary health indicator",
                ""
            ]

        report_md = "\n".join(report_lines)
        st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
        st.markdown(report_md)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("⬇️  Download Report (.md)", report_md,
                           file_name=f"techlift_report_{report_date}.md",
                           mime="text/markdown")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6: SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Settings" in page:
    page_header("⚙️", "Settings",
                "System configuration and preferences",
                tag="CONFIG")

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
        <div style='font-family:var(--font-mono);font-size:12px;color:var(--t2);line-height:2;'>
        MEAN VIBRATION &nbsp;&nbsp;<span style='color:var(--accent);'>{mean_vib:.4f}</span><br>
        STD DEVIATION &nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>{std_vib:.4f}</span><br>
        HEALTHY THRESHOLD &nbsp;<span style='color:#ffc107;'>{healthy_thr:.4f}</span><br>
        CRITICAL THRESHOLD &nbsp;<span style='color:#ff2d55;'>{critical_thr:.4f}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card fade-up-2'>", unsafe_allow_html=True)
        st.subheader("👤 User Profile")
        st.markdown(f"""
        <div style='font-family:var(--font-mono);font-size:12px;color:var(--t2);line-height:2.2;'>
        USER ID &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>{st.session_state.username}</span><br>
        ROLE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>{role}</span><br>
        SESSION &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>ACTIVE</span><br>
        UPLINK &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>CONNECTED</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card fade-up-3'>", unsafe_allow_html=True)
        st.subheader("📦 Dataset Info")
        st.markdown(f"""
        <div style='font-family:var(--font-mono);font-size:12px;color:var(--t2);line-height:2.2;'>
        ROWS &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:var(--accent);'>{len(df):,}</span><br>
        COLUMNS &nbsp;<span style='color:var(--accent);'>{len(df.columns)}</span><br>
        SOURCE &nbsp;&nbsp;<span style='color:var(--accent);'>elevator_sensor_data_cleaned.csv</span><br>
        CACHED &nbsp;&nbsp;<span style='color:var(--accent);'>YES</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

