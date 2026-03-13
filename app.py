"""
🏢 TechLift Elevator Monitoring System  v6.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Design : Deep Navy AI Dashboard · Glassmorphism cards · Dual-theme
Fonts  : Orbitron (headings) · Inter (body) · Rajdhani (metrics)
Colors : #020817 bg · #00D4FF cyan · #4F8EF7 blue · #7C3AED purple
New    : ✔ Working dark/light theme toggle
         ✔ Redesigned sidebar (logo + icon nav cards)
         ✔ Tooltips on key inputs
         ✔ Clearer prediction results layout
         ✔ Better spacing / visual hierarchy throughout
         ✔ Zero logic / ML changes
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

try:
    from sklearn.ensemble import RandomForestRegressor
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechLift | Elevator AI Monitor",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
_defaults = {"logged_in": False, "username": "", "theme": "dark"}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

USERS = {"admin": "elevate123", "tanmay": "1234", "engineer": "tech2024"}
ROLES = {"admin": "Administrator", "tanmay": "Sr. Engineer", "engineer": "Engineer"}

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS  — theme-aware, single source of truth
# ══════════════════════════════════════════════════════════════════════════════
# Accent palette (same in both modes)
CY   = "#00D4FF"   # neon cyan
BL   = "#4F8EF7"   # electric blue
PU   = "#7C3AED"   # purple glow
CRIT = "#EF4444"   # critical red
WARN = "#F59E0B"   # warning amber
OK   = "#10B981"   # healthy green

def _tokens(theme: str) -> dict:
    """Return theme-specific design tokens."""
    if theme == "dark":
        return dict(
            BG    = "#020817",
            CARD  = "rgba(15,23,42,0.80)",
            CARD2 = "rgba(15,23,42,0.95)",
            INP   = "rgba(15,23,42,0.92)",
            SBG   = "rgba(2,8,23,0.98)",
            T1    = "#E2E8F0",
            T2    = "#94A3B8",
            T3    = "#64748B",
            BORD  = "rgba(0,212,255,0.15)",
            BORD2 = "rgba(0,212,255,0.30)",
            SHA   = "rgba(0,0,0,0.60)",
            GRID  = "rgba(148,163,184,0.06)",
            ORBA  = "rgba(0,212,255,0.08)",   # orb a (cyan)
            ORBB  = "rgba(124,58,237,0.07)",  # orb b (purple)
            ORBC  = "rgba(79,142,247,0.05)",  # orb c (blue)
            INV   = "#020817",               # inverse (same as BG)
            SBTN_BG  = "rgba(239,68,68,0.06)",
            SBTN_COL = "#EF4444",
        )
    else:   # light
        return dict(
            BG    = "#F0F5FF",
            CARD  = "rgba(255,255,255,0.88)",
            CARD2 = "rgba(255,255,255,0.98)",
            INP   = "rgba(255,255,255,0.96)",
            SBG   = "rgba(240,245,255,0.99)",
            T1    = "#0F172A",
            T2    = "#475569",
            T3    = "#94A3B8",
            BORD  = "rgba(0,212,255,0.22)",
            BORD2 = "rgba(0,212,255,0.45)",
            SHA   = "rgba(15,23,42,0.10)",
            GRID  = "rgba(15,23,42,0.05)",
            ORBA  = "rgba(0,212,255,0.06)",
            ORBB  = "rgba(124,58,237,0.05)",
            ORBC  = "rgba(79,142,247,0.04)",
            INV   = "#F0F5FF",
            SBTN_BG  = "rgba(239,68,68,0.05)",
            SBTN_COL = "#DC2626",
        )

# ── CSS FACTORY ───────────────────────────────────────────────────────────────
def build_css(theme: str) -> str:
    t = _tokens(theme)
    BG=t["BG"]; CARD=t["CARD"]; CARD2=t["CARD2"]; INP=t["INP"]; SBG=t["SBG"]
    T1=t["T1"]; T2=t["T2"]; T3=t["T3"]
    BORD=t["BORD"]; BORD2=t["BORD2"]; SHA=t["SHA"]; GRID=t["GRID"]
    ORBA=t["ORBA"]; ORBB=t["ORBB"]; ORBC=t["ORBC"]; INV=t["INV"]
    SBTN_BG=t["SBTN_BG"]; SBTN_COL=t["SBTN_COL"]

    # muted/glow helpers
    CYm = "rgba(0,212,255,0.10)"
    CYg = "rgba(0,212,255,0.40)"
    BLm = "rgba(79,142,247,0.10)"
    PUm = "rgba(124,58,237,0.10)"

    return f"""
<style>
/* ── FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ── CSS VARS ── */
:root {{
  --cy:{CY}; --bl:{BL}; --pu:{PU}; --crit:{CRIT}; --warn:{WARN}; --ok:{OK};
  --bg:{BG}; --card:{CARD}; --card2:{CARD2}; --inp:{INP}; --sbg:{SBG};
  --t1:{T1}; --t2:{T2}; --t3:{T3};
  --bord:{BORD}; --bord2:{BORD2}; --sha:{SHA}; --grid:{GRID};
  --grad: linear-gradient(135deg, {CY} 0%, {BL} 100%);
  --grad-pu: linear-gradient(135deg, {CY} 0%, {PU} 100%);
  --grad-soft: linear-gradient(135deg, {CYm} 0%, {BLm} 100%);
  --fh: 'Orbitron', sans-serif;
  --fb: 'Inter', sans-serif;
  --fm: 'Rajdhani', sans-serif;
  --rad: 12px; --rad-sm: 8px; --rad-lg: 16px;
  --tr: 0.20s cubic-bezier(0.4, 0, 0.2, 1);
  --tr-slow: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* ── RESET ── */
*, *::before, *::after {{ box-sizing: border-box; }}

/* ── APP SHELL ── */
html, body {{ font-family: var(--fb); background: var(--bg); color: var(--t1); }}
.stApp {{
  min-height: 100vh;
  background:
    radial-gradient(ellipse 60% 50% at   3% 10%, {ORBA} 0%, transparent 60%),
    radial-gradient(ellipse 45% 40% at  97%  5%, {ORBB} 0%, transparent 55%),
    radial-gradient(ellipse 55% 45% at  88% 95%, {ORBC} 0%, transparent 55%),
    radial-gradient(ellipse 35% 30% at  15% 85%, {ORBB} 0%, transparent 50%),
    linear-gradient({GRID} 1px, transparent 1px),
    linear-gradient(90deg, {GRID} 1px, transparent 1px),
    {BG} !important;
  background-size:
    100% 100%, 100% 100%, 100% 100%, 100% 100%,
    36px 36px, 36px 36px, 100% 100% !important;
  color: var(--t1);
}}
/* subtle scanlines — dark only */
{"" if theme == "light" else """
.stApp::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:9998;
  background: repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.018) 3px,rgba(0,0,0,0.018) 4px);
}
"""}

/* ── HIDE CHROME ── */
#MainMenu, footer, header {{ visibility: hidden !important; }}
.block-container {{ padding-top: 1.2rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }}

/* ════════════════════════════════════
   SIDEBAR
════════════════════════════════════ */
section[data-testid="stSidebar"] {{
  background: var(--sbg) !important;
  backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px);
  border-right: 1px solid var(--bord) !important;
  box-shadow: 4px 0 50px rgba(0,212,255,0.05), 4px 0 20px var(--sha);
  min-width: 272px !important; max-width: 272px !important;
}}
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] .block-container {{ padding: 0 !important; }}

/* ── Logo / Brand ── */
.sb-logo {{
  display: flex; align-items: center; gap: 12px;
  padding: 22px 18px 18px;
  border-bottom: 1px solid var(--bord);
  background: linear-gradient(135deg, {CYm}, transparent);
  position: relative;
}}
.sb-logo::after {{
  content: ''; position: absolute; bottom: 0; left: 18px; right: 18px; height: 1px;
  background: var(--grad); opacity: .35;
}}
.sb-logo-icon {{
  width: 40px; height: 40px; border-radius: 10px;
  background: var(--grad);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
  box-shadow: 0 0 20px {CYm}, 0 4px 12px var(--sha);
}}
.sb-logo-text {{ flex: 1; }}
.sb-logo-title {{
  font-family: var(--fh); font-size: 13px; font-weight: 700;
  color: var(--t1); letter-spacing: .1em; text-transform: uppercase; line-height: 1;
}}
.sb-logo-sub {{
  font-family: var(--fb); font-size: 10px; font-weight: 400;
  color: var(--t2); letter-spacing: .08em; margin-top: 3px;
}}
.sb-version {{
  font-family: var(--fm); font-size: 10px; font-weight: 600;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
  letter-spacing: .06em;
}}

/* ── User Badge ── */
.sb-user {{
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--bord);
  background: {CYm};
  position: relative;
}}
.sb-avatar {{
  width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0;
  background: linear-gradient(135deg, {CYm}, {PUm});
  border: 1.5px solid rgba(0,212,255,0.35);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--fh); font-size: 13px; font-weight: 700;
  color: {CY}; position: relative;
  box-shadow: 0 0 16px {CYm}, inset 0 0 10px {CYm};
}}
.sb-avatar::after {{
  content: ''; position: absolute; bottom: -4px; right: -4px;
  width: 10px; height: 10px; border-radius: 50%;
  background: {OK}; border: 2px solid var(--bg);
  box-shadow: 0 0 8px {OK}; animation: pulse-dot 2.5s ease infinite;
}}
@keyframes pulse-dot {{
  0%,100% {{ transform: scale(1); box-shadow: 0 0 8px {OK}; }}
  50%     {{ transform: scale(1.2); box-shadow: 0 0 14px {OK}; }}
}}
.sb-uname {{
  font-family: var(--fh); font-size: 11.5px; font-weight: 700;
  color: var(--t1); letter-spacing: .07em; text-transform: uppercase;
}}
.sb-urole {{
  font-family: var(--fb); font-size: 10px; font-weight: 500;
  color: {CY}; letter-spacing: .08em; margin-top: 2px; opacity: .85;
}}

/* ── Nav section label ── */
.sb-nav-label {{
  font-family: var(--fh); font-size: 8px; font-weight: 700;
  color: var(--t3); letter-spacing: .32em; text-transform: uppercase;
  padding: 16px 18px 6px;
}}
.sb-divider {{
  height: 1px; background: var(--bord); margin: 6px 12px;
}}

/* ── Radio Nav items ── */
div[data-testid="stRadio"] > label {{ display: none !important; }}
div[data-testid="stRadio"] div[role="radiogroup"] {{
  display: flex; flex-direction: column; gap: 3px; padding: 0 10px;
}}
div[data-testid="stRadio"] label {{
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: var(--rad-sm) !important;
  padding: 9px 12px 9px 14px !important;
  cursor: pointer; transition: all var(--tr) !important;
  font-weight: 500 !important; font-size: 11px !important;
  letter-spacing: .06em !important; text-transform: uppercase !important;
  font-family: var(--fh) !important; color: var(--t2) !important;
  position: relative !important; display: flex !important; align-items: center !important;
}}
div[data-testid="stRadio"] label::before {{
  content: ''; position: absolute; left: 0; top: 25%; bottom: 25%;
  width: 3px; border-radius: 0 3px 3px 0;
  background: transparent; transition: all var(--tr);
}}
div[data-testid="stRadio"] label:hover {{
  background: {CYm} !important;
  border-color: rgba(0,212,255,0.18) !important;
  color: var(--t1) !important; padding-left: 18px !important;
}}
div[data-testid="stRadio"] label:hover::before {{
  background: {CY}; box-shadow: 0 0 8px {CY};
}}
div[data-testid="stRadio"] label[data-selected="true"] {{
  background: linear-gradient(90deg, {CYm}, transparent 85%) !important;
  border-color: rgba(0,212,255,0.20) !important;
  border-left-color: {CY} !important;
  color: {CY} !important; font-weight: 600 !important;
  box-shadow: inset 0 0 20px {CYm} !important;
}}
div[data-testid="stRadio"] label[data-selected="true"]::before {{
  background: {CY}; box-shadow: 0 0 10px {CY};
}}

/* ── Sidebar quick stats ── */
.sb-stats {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 7px;
  padding: 4px 10px 10px;
}}
.sb-stat {{
  background: linear-gradient(135deg, {CYm}, {BLm});
  border: 1px solid var(--bord); border-radius: var(--rad-sm);
  padding: 11px 8px; text-align: center; transition: all var(--tr);
  cursor: default;
}}
.sb-stat:hover {{
  border-color: rgba(0,212,255,0.35);
  box-shadow: 0 0 18px {CYm};
  transform: translateY(-1px);
}}
.sb-stat-val {{
  font-family: var(--fm); font-size: 19px; font-weight: 700; line-height: 1;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}}
.sb-stat-lbl {{
  font-family: var(--fb); font-size: 9.5px; font-weight: 500;
  color: var(--t2); text-transform: uppercase; letter-spacing: .12em; margin-top: 4px;
}}

/* ── Sidebar logout button ── */
section[data-testid="stSidebar"] .stButton > button {{
  background: transparent !important; color: var(--t2) !important;
  border: 1px solid rgba(148,163,184,0.18) !important;
  border-radius: var(--rad-sm) !important;
  font-family: var(--fh) !important; font-size: 10px !important;
  font-weight: 600 !important; letter-spacing: .12em !important;
  text-transform: uppercase !important; padding: 7px 14px !important;
  width: auto !important; transition: all var(--tr) !important;
  box-shadow: none !important; margin: 0 10px 2px !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
  border-color: rgba(239,68,68,0.4) !important; color: {SBTN_COL} !important;
  background: {SBTN_BG} !important;
  box-shadow: 0 0 12px rgba(239,68,68,0.12) !important;
}}

/* ── Sidebar footer ── */
.sb-footer {{
  padding: 12px 18px 14px;
  border-top: 1px solid var(--bord);
  font-family: var(--fb); font-size: 9.5px; color: var(--t3);
  text-align: center; letter-spacing: .06em; line-height: 1.6;
}}

/* ════════════════════════════════════
   PAGE HEADER
════════════════════════════════════ */
.page-header {{
  background: var(--card);
  backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 20px 28px 16px; margin-bottom: 22px;
  position: relative; overflow: hidden;
  box-shadow: 0 4px 30px var(--sha);
  animation: fadeUp .4s ease both;
}}
.page-header::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: var(--grad); box-shadow: 0 0 20px rgba(0,212,255,0.5); opacity: .85;
}}
.page-header::after {{
  content: ''; position: absolute; top: 0; left: 0;
  width: 18px; height: 18px;
  border-top: 2px solid {CY}; border-left: 2px solid {CY};
}}
.page-header h1 {{
  font-family: var(--fh) !important; font-size: 19px !important;
  font-weight: 700 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; margin: 0 0 5px 0 !important;
  background: var(--grad) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important; background-clip: text !important;
}}
.page-header p {{
  color: var(--t2) !important; margin: 0 !important;
  font-family: var(--fb) !important; font-size: 12px !important;
  letter-spacing: .15em !important; text-transform: uppercase !important;
  font-weight: 500 !important;
}}
.ph-tag {{
  position: absolute; top: 16px; right: 20px;
  background: {CYm}; border: 1px solid rgba(0,212,255,0.22);
  border-radius: 20px; padding: 4px 12px;
  font-family: var(--fh); font-size: 9px; font-weight: 600;
  color: {CY}; letter-spacing: .14em; text-transform: uppercase;
  box-shadow: 0 0 10px {CYm};
}}
.ph-tag.warn {{ background: rgba(245,158,11,0.10); border-color: rgba(245,158,11,0.25); color: {WARN}; box-shadow: 0 0 10px rgba(245,158,11,0.15); }}
.ph-tag.crit {{ background: rgba(239,68,68,0.10); border-color: rgba(239,68,68,0.25); color: {CRIT}; box-shadow: 0 0 10px rgba(239,68,68,0.15); animation: crit-pulse 2.5s ease infinite; }}

/* ════════════════════════════════════
   KPI / METRIC CARDS
════════════════════════════════════ */
.metric-card {{
  background: var(--card);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 20px 20px 16px; position: relative; overflow: hidden;
  transition: all var(--tr-slow); animation: fadeUp .45s ease both;
  box-shadow: 0 2px 20px var(--sha);
}}
.metric-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: var(--grad);
}}
.metric-card::after {{
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(135deg, {CYm} 0%, {BLm} 60%, transparent 100%);
}}
.metric-card:hover {{
  transform: translateY(-4px); border-color: rgba(0,212,255,0.30);
  box-shadow: 0 12px 40px rgba(0,212,255,0.10), 0 0 0 1px rgba(0,212,255,0.12);
}}
.mc-icon {{
  font-size: 22px; margin-bottom: 10px; display: block;
  position: relative; z-index: 1;
}}
.mc-label {{
  font-family: var(--fh); font-size: 8.5px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .24em;
  color: var(--t2); margin-bottom: 8px;
  position: relative; z-index: 1;
}}
.mc-value {{
  font-family: var(--fm); font-size: 36px; font-weight: 700; line-height: 1;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
  position: relative; z-index: 1;
}}
.mc-value.ok   {{ background: linear-gradient(135deg,{OK},{CY}) !important; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }}
.mc-value.warn {{ background: linear-gradient(135deg,{WARN},#FBBF24) !important; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }}
.mc-value.crit {{ background: linear-gradient(135deg,{CRIT},#F87171) !important; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }}
.mc-sub {{
  font-family: var(--fb); font-size: 11px; font-weight: 400;
  color: var(--t2); margin-top: 6px; position: relative; z-index: 1;
}}
.mc-trend {{
  position: absolute; top: 16px; right: 16px; z-index: 2;
  font-family: var(--fm); font-size: 12px; font-weight: 600;
  padding: 2px 8px; border-radius: 20px;
}}
.mc-trend.up   {{ background: rgba(16,185,129,0.12); color: {OK}; border: 1px solid rgba(16,185,129,0.2); }}
.mc-trend.down {{ background: rgba(239,68,68,0.12); color: {CRIT}; border: 1px solid rgba(239,68,68,0.2); }}

/* ════════════════════════════════════
   GLASS SECTION CARDS
════════════════════════════════════ */
.glass-card {{
  background: var(--card);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 22px; margin: 6px 0;
  box-shadow: 0 4px 28px var(--sha);
  transition: border-color var(--tr), box-shadow var(--tr);
  animation: fadeUp .4s ease both;
}}
.glass-card:hover {{
  border-color: rgba(0,212,255,0.24);
  box-shadow: 0 0 32px {CYm}, 0 8px 32px var(--sha);
}}
.glass-card-title {{
  font-family: var(--fh); font-size: 11px; font-weight: 700;
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--t1); margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}}
.glass-card-title::after {{
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--bord), transparent);
}}

/* ════════════════════════════════════
   STATUS / ALERT PANELS
════════════════════════════════════ */
.status-panel {{
  border-radius: var(--rad); padding: 18px 20px;
  margin-bottom: 8px; position: relative; overflow: hidden;
  transition: all var(--tr); backdrop-filter: blur(10px);
}}
.status-panel:hover {{ transform: translateX(3px); }}
.status-panel::before {{
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
  border-radius: 0 2px 2px 0;
}}
.sp-header {{
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 4px;
}}
.sp-title {{
  font-family: var(--fh); font-size: 11.5px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .1em;
}}
.sp-pct {{
  font-family: var(--fm); font-size: 32px; font-weight: 700; line-height: 1.1;
}}
.sp-meta {{
  font-family: var(--fb); font-size: 11px; opacity: .72; margin-top: 3px;
}}
.sp-bar {{
  width: 100%; height: 4px; background: rgba(255,255,255,0.08);
  border-radius: 2px; margin-top: 10px; overflow: hidden;
}}
.sp-bar-fill {{ height: 100%; border-radius: 2px; transition: width .8s ease; }}

.sp-ok   {{ background: linear-gradient(135deg,rgba(16,185,129,.09),transparent); border:1px solid rgba(16,185,129,.22); color:{OK}; }}
.sp-ok::before   {{ background:{OK}; box-shadow:0 0 12px {OK}; }}
.sp-ok:hover     {{ box-shadow:0 0 24px rgba(16,185,129,.14); border-color:{OK}; }}
.sp-warn {{ background: linear-gradient(135deg,rgba(245,158,11,.09),transparent); border:1px solid rgba(245,158,11,.22); color:{WARN}; }}
.sp-warn::before {{ background:{WARN}; box-shadow:0 0 12px {WARN}; }}
.sp-warn:hover   {{ box-shadow:0 0 24px rgba(245,158,11,.14); border-color:{WARN}; }}
.sp-crit {{ background: linear-gradient(135deg,rgba(239,68,68,.09),transparent); border:1px solid rgba(239,68,68,.22); color:{CRIT}; animation:crit-pulse 2.8s ease infinite; }}
.sp-crit::before {{ background:{CRIT}; box-shadow:0 0 12px {CRIT}; }}
.sp-crit:hover   {{ box-shadow:0 0 32px rgba(239,68,68,.20); border-color:{CRIT}; }}
@keyframes crit-pulse {{ 0%,100%{{box-shadow:0 0 16px rgba(239,68,68,.06);}} 50%{{box-shadow:0 0 32px rgba(239,68,68,.18);}} }}

/* ════════════════════════════════════
   INSIGHT / INFO CARDS
════════════════════════════════════ */
.insight-card {{
  background: var(--card);
  border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 18px 20px; transition: all var(--tr);
  position: relative; overflow: hidden;
}}
.insight-card:hover {{ border-color: var(--bord2); box-shadow: 0 0 24px {CYm}; }}
.ic-badge {{
  display: inline-flex; align-items: center; gap: 6px;
  font-family: var(--fh); font-size: 9px; font-weight: 700;
  letter-spacing: .18em; text-transform: uppercase;
  padding: 4px 10px; border-radius: 20px; margin-bottom: 12px;
}}
.ic-badge.strong {{ background:rgba(16,185,129,.1); color:{OK}; border:1px solid rgba(16,185,129,.25); }}
.ic-badge.weak   {{ background:{CYm}; color:{CY}; border:1px solid rgba(0,212,255,.25); }}
.ic-title {{
  font-family: var(--fh); font-size: 12px; font-weight: 700;
  color: var(--t1); letter-spacing: .06em; margin-bottom: 8px;
}}
.ic-body {{ font-family: var(--fb); font-size: 13px; color: var(--t2); line-height: 1.6; }}
.ic-stat {{
  display: flex; align-items: baseline; gap: 6px; margin-top: 10px;
  font-family: var(--fm); font-size: 28px; font-weight: 700;
  background: var(--grad); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; background-clip: text;
}}
.ic-stat span {{ font-family: var(--fb); font-size: 12px; color: var(--t2); -webkit-text-fill-color: var(--t2); }}

/* ════════════════════════════════════
   FINANCIAL TABLE CARDS
════════════════════════════════════ */
.fin-card {{
  background: var(--card); border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 20px; text-align: center; transition: all var(--tr-slow);
}}
.fin-card:hover {{ transform: translateY(-3px); border-color: var(--bord2); box-shadow: 0 8px 30px {CYm}; }}
.fin-card-icon {{ font-size: 26px; margin-bottom: 10px; display: block; }}
.fin-card-label {{ font-family: var(--fh); font-size: 9px; font-weight: 600; color: var(--t2); letter-spacing: .2em; text-transform: uppercase; margin-bottom: 6px; }}
.fin-card-value {{ font-family: var(--fm); font-size: 30px; font-weight: 700; background: var(--grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
.fin-card-sub {{ font-family: var(--fb); font-size: 11px; color: var(--t3); margin-top: 4px; }}

/* ════════════════════════════════════
   ANIMATIONS
════════════════════════════════════ */
@keyframes fadeUp {{ from{{ opacity:0; transform:translateY(14px); }} to{{ opacity:1; transform:translateY(0); }} }}
@keyframes fadeIn {{ from{{ opacity:0; }} to{{ opacity:1; }} }}
@keyframes slideRight {{ from{{ transform:translateX(-8px); opacity:0; }} to{{ transform:translateX(0); opacity:1; }} }}
.fade-up   {{ animation: fadeUp .40s ease both; }}
.fade-up-1 {{ animation: fadeUp .40s .06s ease both; }}
.fade-up-2 {{ animation: fadeUp .40s .12s ease both; }}
.fade-up-3 {{ animation: fadeUp .40s .18s ease both; }}
.fade-up-4 {{ animation: fadeUp .40s .24s ease both; }}

/* ════════════════════════════════════
   BUTTONS
════════════════════════════════════ */
.stButton > button {{
  background: transparent !important; color: {CY} !important;
  border: 1px solid rgba(0,212,255,0.32) !important; border-radius: var(--rad-sm) !important;
  font-family: var(--fh) !important; font-weight: 600 !important;
  font-size: 10.5px !important; padding: 11px 24px !important;
  width: 100% !important; letter-spacing: .16em !important;
  text-transform: uppercase !important; transition: all var(--tr) !important;
  box-shadow: inset 0 0 16px {CYm} !important; position: relative !important;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, {CYm}, {BLm}) !important;
  color: #fff !important; border-color: {CY} !important;
  box-shadow: 0 0 28px rgba(0,212,255,0.30), inset 0 0 20px {CYm} !important;
  transform: translateY(-1px) !important;
}}
.stButton > button:active {{ transform: translateY(0px) !important; }}
.stButton > button:focus-visible {{ outline: 2px solid {CY} !important; outline-offset: 3px !important; }}

/* ════════════════════════════════════
   TEXT INPUTS
════════════════════════════════════ */
.stTextInput > div > div > input {{
  background: var(--inp) !important; color: var(--t1) !important;
  border: 1px solid var(--bord) !important; border-left: 2px solid {CY} !important;
  border-radius: var(--rad-sm) !important;
  padding: 12px 16px !important; font-size: 14px !important;
  font-family: var(--fb) !important; transition: all var(--tr);
}}
.stTextInput > div > div > input:focus {{
  border-color: rgba(0,212,255,0.50) !important;
  box-shadow: 0 0 0 3px {CYm}, 0 0 18px {CYm} !important; outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: var(--t2) !important; opacity: .5; }}

/* ── Form labels ── */
.stTextInput > label, .stSelectbox > label,
.stSlider > label, .stMultiSelect > label,
.stNumberInput > label {{
  color: var(--t2) !important; font-family: var(--fh) !important;
  font-size: 9px !important; letter-spacing: .22em !important;
  text-transform: uppercase !important; font-weight: 700 !important;
  margin-bottom: 5px !important;
}}

/* ── Help text / tooltips ── */
.stTextInput > div > div > div[data-testid="InputInstructions"],
.stSlider small, .element-container .stMarkdown small {{
  color: var(--t3) !important; font-family: var(--fb) !important;
  font-size: 10.5px !important; font-style: italic;
}}

/* ════════════════════════════════════
   SLIDERS
════════════════════════════════════ */
.stSlider > div > div > div > div {{
  background: var(--grad) !important; box-shadow: 0 0 8px rgba(0,212,255,0.35) !important;
}}
div[data-testid="stSlider"] > div > div > div[role="slider"] {{
  background: var(--bg) !important; border: 2px solid {CY} !important;
  box-shadow: 0 0 14px rgba(0,212,255,0.50) !important;
  border-radius: 50% !important; width: 16px !important; height: 16px !important;
  transition: transform var(--tr) !important;
}}
div[data-testid="stSlider"] > div > div > div[role="slider"]:hover {{
  transform: scale(1.35) !important;
  box-shadow: 0 0 20px rgba(0,212,255,0.65) !important;
}}

/* ════════════════════════════════════
   TABS
════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
  background: var(--card) !important; border: 1px solid var(--bord) !important;
  border-radius: 10px !important; padding: 4px !important; gap: 3px !important;
}}
.stTabs [data-baseweb="tab"] {{
  background: transparent !important; border: none !important;
  border-radius: 7px !important; color: var(--t2) !important;
  font-family: var(--fh) !important; font-size: 9.5px !important;
  font-weight: 600 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; padding: 8px 14px !important;
  transition: all var(--tr) !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ background: {CYm} !important; color: var(--t1) !important; }}
.stTabs [aria-selected="true"] {{
  background: {CYm} !important; color: {CY} !important;
  box-shadow: inset 0 0 14px {CYm} !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{
  background: var(--grad) !important; height: 2px !important;
  box-shadow: 0 0 12px rgba(0,212,255,0.45) !important;
}}

/* ════════════════════════════════════
   SELECTBOX / MULTISELECT
════════════════════════════════════ */
.stSelectbox > div > div {{
  background: var(--inp) !important; color: var(--t1) !important;
  border: 1px solid var(--bord) !important; border-radius: var(--rad-sm) !important;
}}
.stSelectbox > div > div:focus-within {{
  border-color: rgba(0,212,255,0.45) !important; box-shadow: 0 0 0 3px {CYm} !important;
}}
.stMultiSelect > div > div {{
  background: var(--inp) !important; border: 1px solid var(--bord) !important;
  border-radius: var(--rad-sm) !important;
}}
span[data-baseweb="tag"] {{
  background: {CYm} !important; border: 1px solid rgba(0,212,255,0.30) !important;
  border-radius: 6px !important; color: {CY} !important;
  font-family: var(--fb) !important; font-size: 12px !important;
}}

/* ════════════════════════════════════
   DATAFRAME
════════════════════════════════════ */
.stDataFrame {{
  border: 1px solid var(--bord) !important; border-radius: var(--rad) !important;
  overflow: hidden !important;
}}
.stDataFrame table {{
  background: var(--inp) !important; color: var(--t1) !important;
  font-family: var(--fb) !important; font-size: 12.5px !important;
}}
.stDataFrame th {{
  background: rgba(0,212,255,0.05) !important; color: var(--t2) !important;
  font-family: var(--fh) !important; font-size: 9px !important;
  letter-spacing: .16em !important; text-transform: uppercase !important;
  border-bottom: 1px solid var(--bord) !important; padding: 10px 12px !important;
}}
.stDataFrame td {{ padding: 8px 12px !important; border-bottom: 1px solid rgba(148,163,184,0.06) !important; }}
.stDataFrame tr:hover td {{ background: {CYm} !important; }}

/* ════════════════════════════════════
   STREAMLIT NATIVE ALERTS
════════════════════════════════════ */
.stSuccess, .stInfo, .stWarning, .stError {{
  border-radius: var(--rad-sm) !important;
  font-family: var(--fb) !important; font-size: 13px !important;
  border-left-width: 3px !important;
}}

/* ════════════════════════════════════
   TYPOGRAPHY
════════════════════════════════════ */
h2, h3 {{
  font-family: var(--fh) !important; font-size: 12px !important;
  font-weight: 700 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; color: var(--t1) !important;
  margin-bottom: 12px !important;
}}
p {{ font-family: var(--fb) !important; font-size: 14px !important; color: var(--t1) !important; }}
hr {{ border-color: var(--bord) !important; margin: 18px 0 !important; }}

/* ════════════════════════════════════
   SCROLLBAR
════════════════════════════════════ */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: linear-gradient({CY},{BL}); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {CY}; }}

/* ════════════════════════════════════
   SETTINGS — THEME TOGGLE CARD
════════════════════════════════════ */
.theme-toggle-card {{
  background: var(--card); border: 1px solid var(--bord); border-radius: var(--rad);
  padding: 20px; display: flex; gap: 12px; margin-top: 6px;
}}
.theme-option {{
  flex: 1; border: 1px solid var(--bord); border-radius: var(--rad-sm);
  padding: 14px 12px; text-align: center; cursor: pointer;
  transition: all var(--tr); font-family: var(--fh); font-size: 10px;
  font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
  color: var(--t2);
}}
.theme-option:hover {{ border-color: var(--bord2); color: var(--t1); }}
.theme-option.active {{ background: {CYm}; border-color: {CY}; color: {CY}; box-shadow: inset 0 0 16px {CYm}; }}
.theme-icon {{ font-size: 22px; display: block; margin-bottom: 8px; }}

/* ════════════════════════════════════
   DATA KV TABLE (settings / info)
════════════════════════════════════ */
.kv-table {{ width:100%; border-collapse:collapse; font-family:var(--fm); }}
.kv-table tr {{ border-bottom:1px solid var(--bord); }}
.kv-table tr:last-child {{ border-bottom:none; }}
.kv-table td {{ padding:9px 4px; font-size:13px; }}
.kv-table td:first-child {{ color:var(--t2); letter-spacing:.06em; text-transform:uppercase; font-size:11px; font-family:var(--fh); padding-right:16px; }}
.kv-table td:last-child {{ color:var(--t1); font-weight:600; text-align:right; }}

/* ════════════════════════════════════
   LOGIN PAGE
════════════════════════════════════ */
.login-outer {{
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; width:100%; min-height:82vh;
}}
.login-card {{
  background: var(--card2);
  backdrop-filter:blur(36px); -webkit-backdrop-filter:blur(36px);
  border:1px solid rgba(0,212,255,0.20); border-radius:20px;
  padding:52px 48px 44px; width:100%; max-width:460px;
  box-shadow:0 0 100px rgba(0,212,255,0.07), 0 30px 80px var(--sha),
             inset 0 0 60px rgba(0,212,255,0.025);
  position:relative; overflow:hidden; animation:fadeUp .55s ease both;
}}
.login-card::before {{
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:var(--grad); box-shadow:0 0 28px rgba(0,212,255,0.55);
  animation:border-glow 3.5s ease-in-out infinite;
}}
@keyframes border-glow {{ 0%,100%{{opacity:.65;}} 50%{{opacity:1;}} }}
.lc-corner {{ position:absolute; width:20px; height:20px; }}
.lc-corner.tl {{ top:0; left:0;  border-top:2px solid {CY}; border-left:2px solid {CY}; }}
.lc-corner.br {{ bottom:0; right:0; border-bottom:2px solid {CY}; border-right:2px solid {CY}; }}
.lc-corner.tr {{ top:0; right:0; border-top:2px solid rgba(0,212,255,.25); border-right:2px solid rgba(0,212,255,.25); }}
.lc-corner.bl {{ bottom:0; left:0; border-bottom:2px solid rgba(0,212,255,.25); border-left:2px solid rgba(0,212,255,.25); }}
.lc-badge {{
  position:absolute; top:18px; right:18px;
  background:{CYm}; border:1px solid rgba(0,212,255,.25);
  padding:4px 12px; font-size:8.5px; color:{CY};
  letter-spacing:.18em; font-family:var(--fh); font-weight:700;
  box-shadow:0 0 10px {CYm}; border-radius:20px;
}}
.online-dot {{
  width:7px; height:7px; background:{OK}; border-radius:50%;
  box-shadow:0 0 10px {OK}; display:inline-block;
  animation:pulse-dot 1.8s ease infinite; margin-right:4px; vertical-align:middle;
}}
.lc-icon {{
  text-align:center; font-size:54px; margin-bottom:14px;
  filter:drop-shadow(0 0 24px rgba(0,212,255,0.45));
  animation:float 3.5s ease-in-out infinite;
}}
@keyframes float {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(-7px);}} }}
.lc-title {{
  text-align:center; font-family:var(--fh); font-size:28px; font-weight:900;
  background:var(--grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; letter-spacing:.2em; text-transform:uppercase; margin-bottom:4px;
}}
.lc-sub {{
  text-align:center; font-size:10.5px; color:var(--t2);
  margin-bottom:30px; letter-spacing:.28em; text-transform:uppercase;
  font-family:var(--fb); font-weight:500;
}}
.lc-feats {{
  display:flex; justify-content:center; gap:20px;
  padding-top:20px; border-top:1px solid var(--bord); margin-top:4px;
}}
.lc-feat {{
  text-align:center; font-size:9px; color:var(--t2);
  text-transform:uppercase; letter-spacing:.12em; font-family:var(--fh); font-weight:600;
}}
.lc-feat .fi {{ font-size:20px; display:block; margin-bottom:5px; filter:drop-shadow(0 0 7px rgba(0,212,255,.45)); }}
.lc-hint {{
  text-align:center; margin-top:18px; color:var(--t3);
  font-size:10px; font-family:var(--fb); letter-spacing:.05em;
}}
.lc-hint span {{ color:{CY}; }}
</style>
"""

def inject_css(theme: str):
    st.markdown(build_css(theme), unsafe_allow_html=True)

inject_css(st.session_state.theme)

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""<style>
    section[data-testid="stSidebar"]{{ display:none !important; }}
    header{{ display:none !important; }}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.15, 1])
    with col:
        st.markdown("<div class='login-outer'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='login-card'>
          <div class='lc-corner tl'></div><div class='lc-corner br'></div>
          <div class='lc-corner tr'></div><div class='lc-corner bl'></div>
          <div class='lc-badge'><span class='online-dot'></span>SYS.ONLINE</div>
          <div class='lc-icon'>🏢</div>
          <div class='lc-title'>TechLift</div>
          <div class='lc-sub'>v6.0 · Predictive AI Monitoring Core</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("User ID", placeholder="Enter your identification…")
            password = st.text_input("Access Key", type="password", placeholder="Enter your passkey…")
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⌗  Initialize Uplink", use_container_width=True)
            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username  = username
                    st.rerun()
                else:
                    st.error("⛔  Access denied — invalid credentials. Please retry.")

        st.markdown(f"""
          <div class='lc-feats'>
            <div class='lc-feat'><span class='fi'>🛡️</span>AES-256</div>
            <div class='lc-feat'><span class='fi'>📡</span>Uplink</div>
            <div class='lc-feat'><span class='fi'>🧠</span>AI Core</div>
          </div>
          <div class='lc-hint'>
            OVERRIDE: [<span>admin</span> : <span>elevate123</span>] ·
            [<span>tanmay</span> : <span>1234</span>]
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
    return pd.read_csv("elevator_sensor_data_cleaned.csv")

df            = load_data()
mean_vib      = df["vibration"].mean()
std_vib       = df["vibration"].std()
healthy_thr   = mean_vib + std_vib
critical_thr  = mean_vib + 2 * std_vib
healthy_count = len(df[df["vibration"] < healthy_thr])
maint_count   = len(df[(df["vibration"] >= healthy_thr) & (df["vibration"] < critical_thr)])
critical_count= len(df[df["vibration"] >= critical_thr])
healthy_pct   = healthy_count / len(df) * 100

role = ROLES.get(st.session_state.username, "Engineer")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    initials = st.session_state.username[:2].upper()

    # ── App Brand ──
    st.markdown(f"""
    <div class='sb-logo'>
      <div class='sb-logo-icon'>🏢</div>
      <div class='sb-logo-text'>
        <div class='sb-logo-title'>TechLift</div>
        <div class='sb-logo-sub'>Elevator AI Monitor</div>
      </div>
      <div class='sb-version'>v6.0</div>
    </div>
    """, unsafe_allow_html=True)

    # ── User ──
    st.markdown(f"""
    <div class='sb-user'>
      <div class='sb-avatar'>{initials}</div>
      <div>
        <div class='sb-uname'>{st.session_state.username.capitalize()}</div>
        <div class='sb-urole'>{role}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:8px 10px 2px;'>", unsafe_allow_html=True)
    if st.button("🚪  Sign Out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown("<div class='sb-nav-label'>Main Navigation</div>", unsafe_allow_html=True)
    page = st.radio("nav", [
        "📊  Overview",
        "📈  Advanced Analytics",
        "🤖  ML Predictions",
        "🚨  Alerts & Warnings",
        "📑  Report Generator",
        "⚙️  Settings",
    ], label_visibility="collapsed")

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Quick stats ──
    st.markdown("<div class='sb-nav-label'>Live Stats</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='sb-stats'>
      <div class='sb-stat'>
        <div class='sb-stat-val'>{len(df):,}</div>
        <div class='sb-stat-lbl'>Readings</div>
      </div>
      <div class='sb-stat'>
        <div class='sb-stat-val'>{healthy_pct:.0f}%</div>
        <div class='sb-stat-lbl'>Healthy</div>
      </div>
      <div class='sb-stat'>
        <div class='sb-stat-val' style='background:linear-gradient(135deg,{CRIT},{WARN});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>{critical_count:,}</div>
        <div class='sb-stat-lbl'>Critical</div>
      </div>
      <div class='sb-stat'>
        <div class='sb-stat-val' style='background:linear-gradient(135deg,{WARN},{BL});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>{maint_count:,}</div>
        <div class='sb-stat-lbl'>Maint.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown(f"""
    <div class='sb-footer'>
      TechLift EMS · v6.0<br>© 2026 · All rights reserved
    </div>
    """, unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def page_header(icon: str, title: str, subtitle: str, tag: str = None, tag_type: str = ""):
    tag_class = f"ph-tag {tag_type}".strip() if tag else ""
    tag_html  = f"<div class='{tag_class}'>{tag}</div>" if tag else ""
    st.markdown(f"""
    <div class='page-header fade-up'>
      {tag_html}
      <h1>{icon} {title}</h1>
      <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def metric_card(icon, label, value, sub="", delay="", color_cls=""):
    style = f"animation-delay:{delay}" if delay else ""
    val_cls = f"mc-value {color_cls}".strip()
    return f"""<div class='metric-card' style='{style}'>
      <span class='mc-icon'>{icon}</span>
      <div class='mc-label'>{label}</div>
      <div class='{val_cls}'>{value}</div>
      <div class='mc-sub'>{sub}</div>
    </div>"""

def status_panel(cls, icon, title, pct, count, thr_text, fill_color):
    return f"""<div class='status-panel {cls}'>
      <div class='sp-header'>
        <div class='sp-title'>{icon} {title}</div>
      </div>
      <div class='sp-pct'>{pct:.1f}%</div>
      <div class='sp-meta'>{count:,} readings &nbsp;·&nbsp; {thr_text}</div>
      <div class='sp-bar'><div class='sp-bar-fill' style='width:{pct:.1f}%;background:{fill_color};'></div></div>
    </div>"""

def styled_fig(fig, theme: str):
    """Apply the AI tech palette to every matplotlib figure."""
    t   = _tokens(theme)
    BG  = t["BG"]
    T2v = t["T2"]
    T1v = t["T1"]
    fig.patch.set_facecolor("#00000000")
    for ax in fig.get_axes():
        ax.set_facecolor("#00000000")
        ax.tick_params(colors=T2v, labelsize=8.5, which="both")
        ax.xaxis.label.set_color(T2v); ax.xaxis.label.set_fontsize(10)
        ax.yaxis.label.set_color(T2v); ax.yaxis.label.set_fontsize(10)
        if ax.get_title():
            ax.title.set_color(T1v); ax.title.set_fontsize(11)
        for sp in ["bottom", "left"]:
            ax.spines[sp].set_color((0.580, 0.639, 0.722, 0.35)); ax.spines[sp].set_linewidth(0.7)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(True, color=(0.580, 0.639, 0.722, 0.12), alpha=1, linewidth=0.5, linestyle="--")
    plt.tight_layout(pad=1.8)

THM = st.session_state.theme   # shorthand used by chart calls

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    page_header("📊", "System Overview",
                "Real-time elevator health · Predictive intelligence · Anomaly detection",
                tag="● LIVE", tag_type="")

    avg_cost = (critical_count * 12_000 + maint_count * 2_000) / 12

    # ── KPI row ──
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric_card("✅", "Healthy Status",  f"{healthy_pct:.1f}%",         f"{healthy_count:,} readings",   "0.05s", "ok"),   unsafe_allow_html=True)
    with c2: st.markdown(metric_card("⚠️", "Needs Maintenance",f"{maint_count/len(df)*100:.1f}%", f"{maint_count:,} readings", "0.10s", "warn"), unsafe_allow_html=True)
    with c3: st.markdown(metric_card("🚨", "Critical State",  f"{critical_count/len(df)*100:.1f}%", f"{critical_count:,} readings","0.15s","crit"),unsafe_allow_html=True)
    with c4: st.markdown(metric_card("💰", "Monthly Savings", f"${avg_cost:,.0f}",             "vs reactive repairs",          "0.20s", ""),     unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Status panels ──
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(status_panel("sp-ok",   "✅", "Healthy",     healthy_pct,                    healthy_count,  f"Vibration &lt; {healthy_thr:.2f}",                           OK  ), unsafe_allow_html=True)
    with col2: st.markdown(status_panel("sp-warn", "⚠️", "Maintenance", maint_count/len(df)*100,         maint_count,   f"{healthy_thr:.2f} – {critical_thr:.2f}",                     WARN), unsafe_allow_html=True)
    with col3: st.markdown(status_panel("sp-crit", "🚨", "Critical",    critical_count/len(df)*100,      critical_count,f"Vibration &gt; {critical_thr:.2f}",                           CRIT), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Insights ──
    st.markdown("<div class='glass-card-title fade-up'>💡 Key Insights</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    r  = df["revolutions"].corr(df["vibration"])
    r2 = df["humidity"].corr(df["vibration"])
    with col1:
        st.markdown(f"""
        <div class='insight-card fade-up-1'>
          <div class='ic-badge strong'>● Very Strong Correlation</div>
          <div class='ic-title'>🚪 Door Usage → Vibration</div>
          <div class='ic-stat'>r = {r:.3f} <span>/ 1.0 max</span></div>
          <div class='ic-body'>High-usage elevators show up to +51% vibration.
          Door revolutions is the <strong>primary driver</strong> — schedule maintenance based on usage intensity.</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='insight-card fade-up-2'>
          <div class='ic-badge weak'>◌ Weak Correlation</div>
          <div class='ic-title'>💧 Humidity → Vibration</div>
          <div class='ic-stat'>r = {r2:.3f} <span>/ 1.0 max</span></div>
          <div class='ic-body'>Ambient humidity has minimal influence on vibration.
          Environmental factors are <strong>not a primary concern</strong> — focus maintenance budget on usage-based scheduling.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Financial ──
    st.markdown("<div class='glass-card-title fade-up'>💰 Financial Impact Analysis</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class='fin-card fade-up-1'>
          <span class='fin-card-icon'>🛠️</span>
          <div class='fin-card-label'>Emergency Repair</div>
          <div class='fin-card-value'>$12,000</div>
          <div class='fin-card-sub'>per unplanned incident</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='fin-card fade-up-2'>
          <span class='fin-card-icon'>🔧</span>
          <div class='fin-card-label'>Preventive Service</div>
          <div class='fin-card-value'>$2,000</div>
          <div class='fin-card-sub'>per scheduled service</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='fin-card fade-up-3'>
          <span class='fin-card-icon'>📈</span>
          <div class='fin-card-label'>Estimated Savings / Mo</div>
          <div class='fin-card-value'>${avg_cost:,.0f}</div>
          <div class='fin-card-sub'>break-even at 2 failures/yr</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ADVANCED ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in page:
    page_header("📈", "Advanced Analytics",
                "Interactive data exploration with real-time filtering",
                tag="INTERACTIVE")

    # ── Filters ──
    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card-title'>🎛️ Data Filters</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        vib_range = st.slider("Vibration Range",
            float(df["vibration"].min()), float(df["vibration"].max()),
            (float(df["vibration"].min()), float(df["vibration"].max())),
            step=0.1, help="Filter readings by vibration sensor value")
    with col2:
        rev_range = st.slider("Door Revolutions",
            float(df["revolutions"].min()), float(df["revolutions"].max()),
            (float(df["revolutions"].min()), float(df["revolutions"].max())),
            step=1.0, help="Filter by number of door open/close cycles")
    with col3:
        hum_range = st.slider("Humidity %",
            float(df["humidity"].min()), float(df["humidity"].max()),
            (float(df["humidity"].min()), float(df["humidity"].max())),
            step=1.0, help="Filter by ambient humidity percentage")
    st.markdown("</div>", unsafe_allow_html=True)

    fdf = df[
        (df["vibration"]   >= vib_range[0]) & (df["vibration"]   <= vib_range[1]) &
        (df["revolutions"] >= rev_range[0]) & (df["revolutions"] <= rev_range[1]) &
        (df["humidity"]    >= hum_range[0]) & (df["humidity"]    <= hum_range[1])
    ]
    fh = len(fdf[fdf["vibration"] < healthy_thr])
    fc = len(fdf[fdf["vibration"] >= critical_thr])

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric_card("🔍","Filtered Readings",f"{len(fdf):,}",f"of {len(df):,} total","",""),unsafe_allow_html=True)
    with c2: st.markdown(metric_card("✅","Filtered Healthy",f"{fh:,}","","","ok"),unsafe_allow_html=True)
    with c3: st.markdown(metric_card("🚨","Filtered Critical",f"{fc:,}","","","crit"),unsafe_allow_html=True)
    with c4: st.markdown(metric_card("📊","Filter Coverage",f"{len(fdf)/len(df)*100:.1f}%","of dataset","",""),unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Time Series", "📉 Distributions", "📍 Correlations", "🔍 Statistics", "📋 Data Table"])

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5), facecolor="none")
        ax.plot(fdf["ID"], fdf["vibration"], linewidth=1.3, color=CY, alpha=0.88, label="Vibration")
        ax.axhline(mean_vib,    color=OK,   linestyle="--", linewidth=1.4, label=f"Mean ({mean_vib:.2f})",    alpha=0.8)
        ax.axhline(healthy_thr, color=WARN, linestyle="--", linewidth=1.4, label=f"Warn ({healthy_thr:.2f})", alpha=0.8)
        ax.axhline(critical_thr,color=CRIT, linestyle="--", linewidth=1.4, label=f"Crit ({critical_thr:.2f})",alpha=0.8)
        ax.fill_between(fdf["ID"], healthy_thr, critical_thr,        alpha=0.04, color=WARN)
        ax.fill_between(fdf["ID"], critical_thr, fdf["vibration"].max(), alpha=0.04, color=CRIT)
        ax.set_xlabel("Reading ID"); ax.set_ylabel("Vibration")
        t_val = _tokens(THM)
        ax.legend(loc="upper right", fontsize=8.5, facecolor=t_val["BG"],
                  edgecolor=(0.0, 0.831, 1.0, 0.25), labelcolor=t_val["T2"])
        styled_fig(fig, THM)
        st.pyplot(fig, transparent=True); plt.close()

    with tab2:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor="none")
        for ax, col, clr in zip(axes, ["vibration","revolutions","humidity"], [CY, BL, PU]):
            ax.hist(fdf[col], bins=40, color=clr, alpha=0.72, edgecolor="none")
            ax.set_title(col.capitalize(), fontsize=11, pad=8)
            ax.set_xlabel(col); ax.set_ylabel("Count")
        styled_fig(fig, THM)
        st.pyplot(fig, transparent=True); plt.close()

    with tab3:
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="none")
        corr = fdf[["vibration","revolutions","humidity"]].corr()
        cmap = sns.diverging_palette(220, 20, as_cmap=True)
        sns.heatmap(corr, ax=ax, annot=True, fmt=".3f", cmap=cmap,
                    linewidths=0.5, linecolor=(0.580, 0.639, 0.722, 0.20),
                    cbar_kws={"shrink": 0.8},
                    annot_kws={"size": 11, "color": _tokens(THM)["T1"]})
        ax.set_title("Correlation Matrix", fontsize=12, pad=12)
        styled_fig(fig, THM)
        st.pyplot(fig, transparent=True); plt.close()

    with tab4:
        stats = fdf[["vibration","revolutions","humidity"]].describe().round(4)
        st.dataframe(stats, use_container_width=True)

    with tab5:
        st.dataframe(fdf.head(500), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — ML PREDICTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif "ML" in page:
    page_header("🤖", "ML Predictions",
                "Random Forest predictive maintenance engine",
                tag="AI CORE", tag_type="")

    if not ML_AVAILABLE:
        st.error("scikit-learn is not installed. Run: **pip install scikit-learn**")
        st.stop()

    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card-title'>⚙️ Model Hyperparameters</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: n_est  = st.slider("Number of Trees",  10,  300, 100, step=10,  help="More trees = better accuracy but slower training")
    with col2: t_size = st.slider("Test Split %",     10,   40,  20, step=5,   help="Percentage of data held out for model evaluation")
    with col3: m_dep  = st.slider("Max Tree Depth",    2,   20,   8, step=1,   help="Deeper trees capture more patterns but may overfit")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀  Train Random Forest Model"):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score

        X = df[["revolutions","humidity"]]
        y = df["vibration"]
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=t_size/100, random_state=42)

        with st.spinner("⚙️ Training model — please wait…"):
            mdl = RandomForestRegressor(n_estimators=n_est, max_depth=m_dep, random_state=42, n_jobs=-1)
            mdl.fit(X_tr, y_tr)
            y_pred = mdl.predict(X_te)

        rmse = np.sqrt(mean_squared_error(y_te, y_pred))
        r2   = r2_score(y_te, y_pred)
        mae  = np.mean(np.abs(y_te - y_pred))
        r2_cls = "ok" if r2 >= 0.85 else ("warn" if r2 >= 0.6 else "crit")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>📊 Model Performance</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(metric_card("🎯","R² Score",    f"{r2:.4f}",   "Variance explained",      "", r2_cls), unsafe_allow_html=True)
        with c2: st.markdown(metric_card("📏","RMSE",        f"{rmse:.4f}", "Root mean squared error", "", ""),     unsafe_allow_html=True)
        with c3: st.markdown(metric_card("📐","MAE",         f"{mae:.4f}",  "Mean absolute error",     "", ""),     unsafe_allow_html=True)
        with c4: st.markdown(metric_card("🔢","Test Samples",f"{len(X_te):,}",f"{t_size}% of data",   "", ""),     unsafe_allow_html=True)

        # ── R² quality banner ──
        if r2 >= 0.85:
            st.success(f"✅ Excellent model — R² = {r2:.4f}. The model explains {r2*100:.1f}% of vibration variance.")
        elif r2 >= 0.6:
            st.warning(f"⚠️ Moderate model — R² = {r2:.4f}. Consider adding more features or tuning hyperparameters.")
        else:
            st.error(f"🚨 Weak model — R² = {r2:.4f}. The current features may not be sufficient for accurate prediction.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>📉 Visual Diagnostics</div>", unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="none")
        axes[0].scatter(y_te, y_pred, color=CY, alpha=0.30, s=10, edgecolors="none", label="Predictions")
        mn = min(y_te.min(), y_pred.min()); mx = max(y_te.max(), y_pred.max())
        axes[0].plot([mn,mx],[mn,mx], color=CRIT, linestyle="--", linewidth=1.5, alpha=0.8, label="Perfect fit")
        axes[0].set_xlabel("Actual Vibration"); axes[0].set_ylabel("Predicted Vibration")
        axes[0].set_title("Actual vs Predicted")
        t_v = _tokens(THM)
        axes[0].legend(fontsize=9, facecolor=t_v["BG"], edgecolor=(0.0, 0.831, 1.0, 0.25), labelcolor=t_v["T2"])

        fi = pd.Series(mdl.feature_importances_, index=X.columns).sort_values(ascending=True)
        bars = axes[1].barh(fi.index, fi.values, color=[BL, CY], alpha=0.82)
        axes[1].set_title("Feature Importance"); axes[1].set_xlabel("Importance Score")
        for bar, val in zip(bars, fi.values):
            axes[1].text(val + 0.002, bar.get_y() + bar.get_height()/2,
                         f"{val:.3f}", va="center", fontsize=9, color=t_v["T2"])

        styled_fig(fig, THM)
        st.pyplot(fig, transparent=True); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — ALERTS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Alerts" in page:
    tag_type = "crit" if critical_count > 0 else ""
    page_header("🚨", "Alerts & Warnings",
                "Real-time threshold monitoring and anomaly detection",
                tag=f"{'🔴' if critical_count else '🟢'} {critical_count} ACTIVE",
                tag_type=tag_type)

    # ── Critical ──
    critical_df = df[df["vibration"] >= critical_thr].copy()
    st.markdown("<div class='glass-card-title fade-up'>🔴 Critical Readings</div>", unsafe_allow_html=True)
    if not critical_df.empty:
        st.markdown(f"""
        <div class='status-panel sp-crit fade-up-1' style='margin-bottom:16px;'>
          <div class='sp-header'>
            <div class='sp-title'>🚨 {len(critical_df)} Critical Readings Detected</div>
          </div>
          <div class='sp-meta'>Vibration exceeds threshold {critical_thr:.4f} — Immediate inspection required on affected units</div>
        </div>""", unsafe_allow_html=True)
        st.dataframe(critical_df.head(100), use_container_width=True)
    else:
        st.success("✅ No critical readings detected. All units operating within safe parameters.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Maintenance ──
    maint_df = df[(df["vibration"] >= healthy_thr) & (df["vibration"] < critical_thr)]
    st.markdown("<div class='glass-card-title fade-up-1'>🟡 Maintenance Readings</div>", unsafe_allow_html=True)
    if not maint_df.empty:
        st.markdown(f"""
        <div class='status-panel sp-warn fade-up-2' style='margin-bottom:16px;'>
          <div class='sp-header'>
            <div class='sp-title'>⚠️ {len(maint_df)} Readings Flagged for Maintenance</div>
          </div>
          <div class='sp-meta'>Vibration between {healthy_thr:.4f} and {critical_thr:.4f} — Schedule preventive service</div>
        </div>""", unsafe_allow_html=True)
        st.dataframe(maint_df.head(100), use_container_width=True)
    else:
        st.success("✅ No maintenance readings detected. No preventive service currently required.")

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif "Report" in page:
    page_header("📑", "Report Generator",
                "Automated diagnostic report compilation and export",
                tag="EXPORT READY")

    st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card-title'>📋 Report Configuration</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1: report_title = st.text_input("Report Title", value="TechLift Elevator Health Report")
    with col2: report_date  = st.text_input("Report Date",  value=datetime.now().strftime("%Y-%m-%d"))

    include_sections = st.multiselect(
        "Sections to Include",
        ["Executive Summary","Health Overview","Critical Incidents",
         "Financial Analysis","Correlation Analysis","Recommendations"],
        default=["Executive Summary","Health Overview","Critical Incidents","Recommendations"],
        help="Select which sections to include in the generated report"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("📄  Generate Report"):
        lines = [f"# {report_title}",
                 f"**Generated:** {report_date} &nbsp;|&nbsp; **System:** TechLift EMS v6.0",
                 "---"]
        if "Executive Summary" in include_sections:
            lines += ["## Executive Summary",
                f"Analyzed **{len(df):,} sensor readings**. System health: "
                f"**{healthy_pct:.1f}% healthy**, {maint_count/len(df)*100:.1f}% maintenance, "
                f"{critical_count/len(df)*100:.1f}% critical.", ""]
        if "Health Overview" in include_sections:
            lines += ["## Health Overview",
                f"- **Healthy:** {healthy_count:,} ({healthy_count/len(df)*100:.1f}%)",
                f"- **Maintenance:** {maint_count:,} ({maint_count/len(df)*100:.1f}%)",
                f"- **Critical:** {critical_count:,} ({critical_count/len(df)*100:.1f}%)", ""]
        if "Critical Incidents" in include_sections:
            lines += ["## Critical Incidents",
                f"Threshold: vibration > **{critical_thr:.4f}**",
                f"Total critical readings: **{critical_count:,}**", ""]
        if "Financial Analysis" in include_sections:
            avg = (critical_count*12000 + maint_count*2000) / 12
            lines += ["## Financial Analysis",
                "- Emergency repair cost: **$12,000** / incident",
                "- Preventive service cost: **$2,000** / service",
                f"- Estimated monthly savings via predictive maintenance: **${avg:,.0f}**", ""]
        if "Correlation Analysis" in include_sections:
            rc = df["revolutions"].corr(df["vibration"])
            rh = df["humidity"].corr(df["vibration"])
            lines += ["## Correlation Analysis",
                f"- Door revolutions ↔ vibration: **r = {rc:.4f}** (Very strong)",
                f"- Humidity ↔ vibration: **r = {rh:.4f}** (Weak)", ""]
        if "Recommendations" in include_sections:
            lines += ["## Recommendations",
                "1. Prioritize inspection for all critical vibration readings immediately",
                "2. Schedule preventive maintenance for high-revolution elevators",
                "3. Implement usage-based maintenance scheduling",
                "4. Monitor door revolutions as the primary health indicator", ""]

        md = "\n".join(lines)
        st.markdown("<div class='glass-card fade-up' style='margin-top:16px;'>", unsafe_allow_html=True)
        st.markdown(md)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("⬇️  Download Report (.md)", md,
                           file_name=f"techlift_report_{report_date}.md", mime="text/markdown")

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Settings" in page:
    page_header("⚙️", "Settings",
                "Application configuration, preferences, and system info",
                tag="CONFIG")

    col1, col2 = st.columns(2)

    with col1:
        # ── Theme toggle ──
        st.markdown("<div class='glass-card fade-up'>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>🎨 Appearance</div>", unsafe_allow_html=True)

        dark_active  = "active" if st.session_state.theme == "dark"  else ""
        light_active = "active" if st.session_state.theme == "light" else ""

        st.markdown(f"""
        <div class='theme-toggle-card'>
          <div class='theme-option {dark_active}' id='th-dark'>
            <span class='theme-icon'>🌙</span>Dark Mode
          </div>
          <div class='theme-option {light_active}' id='th-light'>
            <span class='theme-icon'>☀️</span>Light Mode
          </div>
        </div>
        """, unsafe_allow_html=True)

        new_theme = st.radio(
            "Select theme",
            ["dark", "light"],
            index=0 if st.session_state.theme == "dark" else 1,
            horizontal=True,
            label_visibility="collapsed",
        )
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

        st.markdown("<br><div style='font-family:var(--fb);font-size:12px;color:var(--t2);'>", unsafe_allow_html=True)
        st.caption("ℹ️ Theme change applies immediately to all pages and persists for your session.")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ── Alert thresholds ──
        st.markdown("<div class='glass-card fade-up-1'>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>📊 Alert Thresholds</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <table class='kv-table'>
          <tr><td>Mean Vibration</td><td style='color:{CY};'>{mean_vib:.4f}</td></tr>
          <tr><td>Std Deviation</td><td style='color:{CY};'>{std_vib:.4f}</td></tr>
          <tr><td>Healthy Threshold</td><td style='color:{OK};'>&lt; {healthy_thr:.4f}</td></tr>
          <tr><td>Warning Threshold</td><td style='color:{WARN};'>{healthy_thr:.4f} – {critical_thr:.4f}</td></tr>
          <tr><td>Critical Threshold</td><td style='color:{CRIT};'>&gt; {critical_thr:.4f}</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # ── User profile ──
        st.markdown("<div class='glass-card fade-up-2'>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>👤 User Profile</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <table class='kv-table'>
          <tr><td>User ID</td>   <td style='color:{CY};'>{st.session_state.username}</td></tr>
          <tr><td>Role</td>      <td style='color:{CY};'>{role}</td></tr>
          <tr><td>Session</td>   <td style='color:{OK};'>● Active</td></tr>
          <tr><td>Uplink</td>    <td style='color:{OK};'>● Connected</td></tr>
          <tr><td>Theme</td>     <td style='color:{CY};'>{st.session_state.theme.capitalize()}</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Dataset info ──
        st.markdown("<div class='glass-card fade-up-3'>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>📦 Dataset</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <table class='kv-table'>
          <tr><td>Rows</td>     <td style='color:{CY};'>{len(df):,}</td></tr>
          <tr><td>Columns</td>  <td style='color:{CY};'>{len(df.columns)}</td></tr>
          <tr><td>Source</td>   <td style='color:{BL};font-size:10.5px;'>elevator_sensor_data_cleaned.csv</td></tr>
          <tr><td>Cached</td>   <td style='color:{OK};'>● Yes (@st.cache_data)</td></tr>
          <tr><td>ML Engine</td><td style='color:{""+OK if ML_AVAILABLE else CRIT};'>{"● sklearn available" if ML_AVAILABLE else "✗ Not installed"}</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── System status ──
        st.markdown("<div class='glass-card fade-up-4'>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card-title'>🖥️ System Status</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <table class='kv-table'>
          <tr><td>Version</td>    <td style='color:{CY};'>v6.0</td></tr>
          <tr><td>Streamlit</td>  <td style='color:{OK};'>● Running</td></tr>
          <tr><td>Data Cache</td> <td style='color:{OK};'>● Active</td></tr>
          <tr><td>Auth</td>       <td style='color:{OK};'>● Session valid</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

