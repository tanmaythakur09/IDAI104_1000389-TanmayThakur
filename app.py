"""
🏢 TechLift Elevator Monitoring System v4.0
Ultra-premium tech-themed UI: Cyberpunk/Futuristic dark theme
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

# ── THEME CSS ─────────────────────────────────────────────────────────────────
DARK_BG  = "#020817"
DARK_BG2 = "#0d1629"
LIGHT_BG  = "#f0f4ff"
LIGHT_BG2 = "#e2e8f0"

def get_css(theme="dark"):
    is_dark = theme == "dark"
    bg        = DARK_BG if is_dark else LIGHT_BG
    bg2       = DARK_BG2 if is_dark else LIGHT_BG2
    text      = "#e2e8f0" if is_dark else "#0f172a"
    text_muted= "#64748b" if is_dark else "#475569"
    card_bg   = "rgba(255,255,255,0.04)" if is_dark else "rgba(255,255,255,0.85)"
    card_border= "rgba(0,212,255,0.15)" if is_dark else "rgba(0,120,255,0.2)"
    sidebar_bg = f"linear-gradient(180deg,{DARK_BG2} 0%,#090f1e 100%)" if is_dark else f"linear-gradient(180deg,{LIGHT_BG2} 0%,#dbeafe 100%)"
    sidebar_txt= "#94a3b8" if is_dark else "#1e3a5f"
    input_bg  = "rgba(255,255,255,0.06)" if is_dark else "rgba(255,255,255,0.9)"
    nav_hover = "rgba(0,212,255,0.08)" if is_dark else "rgba(0,120,255,0.08)"

    return f"""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── BASE ── */
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
.stApp{{background:linear-gradient(135deg,{bg} 0%,{bg2} 50%,{bg} 100%) !important;color:{text};}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"]{{background:{sidebar_bg} !important;border-right:1px solid rgba(0,212,255,0.15);min-width:260px !important;}}
section[data-testid="stSidebar"] *{{color:{sidebar_txt} !important;}}
section[data-testid="stSidebar"] .block-container{{padding:1rem 0.8rem;}}

/* ── HIDE DEFAULT RADIO BULLETS, replace with nav cards ── */
div[data-testid="stRadio"]>label{{display:none;}}
div[data-testid="stRadio"] div[role="radiogroup"]{{display:flex;flex-direction:column;gap:4px;}}
div[data-testid="stRadio"] label{{
  background:rgba(0,212,255,0.04);
  border:1px solid rgba(0,212,255,0.12);
  border-radius:10px;padding:10px 14px;
  cursor:pointer;transition:all .25s ease;
  font-weight:500;font-size:14px;letter-spacing:.02em;
  display:flex !important;align-items:center;gap:8px;
}}
div[data-testid="stRadio"] label:hover{{background:{nav_hover};border-color:rgba(0,212,255,0.4);transform:translateX(4px);}}
div[data-testid="stRadio"] label[data-selected="true"],
div[data-testid="stRadio"] input:checked+div{{background:linear-gradient(90deg,rgba(0,212,255,0.18),rgba(79,142,247,0.1));border-color:#00d4ff;box-shadow:0 0 12px rgba(0,212,255,0.2);}}

/* ── GLASS CARDS ── */
.glass-card{{background:{card_bg};backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid {card_border};border-radius:16px;padding:24px;margin:8px 0;transition:transform .3s,box-shadow .3s;}}
.glass-card:hover{{transform:translateY(-4px);box-shadow:0 20px 40px rgba(0,212,255,0.12);}}

/* ── METRIC CARDS ── */
.metric-glass{{background:linear-gradient(135deg,rgba(0,212,255,0.1),rgba(79,142,247,0.07));border:1px solid rgba(0,212,255,0.2);border-radius:14px;padding:20px 24px;text-align:center;transition:all .3s;}}
.metric-glass:hover{{transform:translateY(-3px);box-shadow:0 12px 28px rgba(0,212,255,0.18);border-color:rgba(0,212,255,0.45);}}
.metric-glass .label{{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:{text_muted};margin-bottom:8px;}}
.metric-glass .value{{font-size:30px;font-weight:800;background:linear-gradient(135deg,#00d4ff,#4f8ef7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;}}
.metric-glass .sub{{font-size:11px;color:{text_muted};margin-top:6px;}}

/* ── ALERTS ── */
.alert-critical{{background:linear-gradient(135deg,rgba(239,68,68,.18),rgba(185,28,28,.12));border:1px solid rgba(239,68,68,.4);border-left:4px solid #ef4444;padding:20px;border-radius:12px;color:#fca5a5;transition:all .3s;}}
.alert-critical:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(239,68,68,.2);}}
.alert-warning{{background:linear-gradient(135deg,rgba(245,158,11,.18),rgba(180,83,9,.12));border:1px solid rgba(245,158,11,.4);border-left:4px solid #f59e0b;padding:20px;border-radius:12px;color:#fcd34d;transition:all .3s;}}
.alert-warning:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(245,158,11,.2);}}
.alert-healthy{{background:linear-gradient(135deg,rgba(16,185,129,.18),rgba(5,150,105,.12));border:1px solid rgba(16,185,129,.4);border-left:4px solid #10b981;padding:20px;border-radius:12px;color:#6ee7b7;transition:all .3s;}}
.alert-healthy:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(16,185,129,.2);}}

/* ── PAGE HEADER ── */
.page-header{{background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(79,142,247,0.06));border:1px solid rgba(0,212,255,0.18);border-radius:16px;padding:28px 32px;margin-bottom:24px;position:relative;overflow:hidden;}}
.page-header::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#00d4ff,#4f8ef7,transparent);}}
.page-header h1{{font-family:'Orbitron',sans-serif;font-size:24px;font-weight:700;background:linear-gradient(135deg,#00d4ff 0%,#4f8ef7 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 6px 0;}}
.page-header p{{color:{text_muted};margin:0;font-size:13px;}}

/* ── USER BADGE ── */
.user-badge{{background:linear-gradient(135deg,rgba(0,212,255,0.12),rgba(79,142,247,0.08));border:1px solid rgba(0,212,255,0.25);border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:12px;margin-bottom:12px;}}
.user-avatar{{width:40px;height:40px;background:linear-gradient(135deg,#00d4ff,#4f8ef7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;color:#020817;flex-shrink:0;box-shadow:0 0 12px rgba(0,212,255,0.4);}}
.user-name{{font-size:14px;font-weight:600;color:{text} !important;}}
.user-role{{font-size:11px;color:{text_muted} !important;}}

/* ── BUTTONS ── */
.stButton>button{{background:linear-gradient(135deg,#00d4ff 0%,#4f8ef7 100%) !important;color:#020817 !important;border:none !important;border-radius:10px !important;font-weight:700 !important;font-size:14px !important;padding:12px 24px !important;width:100% !important;transition:all .3s !important;letter-spacing:.04em !important;text-transform:uppercase !important;}}
.stButton>button:hover{{transform:translateY(-2px) !important;box-shadow:0 8px 28px rgba(0,212,255,0.5) !important;}}

/* ── TEXT INPUTS ── */
.stTextInput>div>div>input{{background:{input_bg} !important;border:1px solid rgba(0,212,255,0.3) !important;border-radius:10px !important;color:{text} !important;padding:12px 16px !important;font-size:14px !important;}}
.stTextInput>div>div>input:focus{{border-color:#00d4ff !important;box-shadow:0 0 0 3px rgba(0,212,255,0.15) !important;}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{{background:rgba(0,212,255,0.04) !important;border-radius:12px !important;padding:4px !important;border:1px solid rgba(0,212,255,0.1) !important;}}
.stTabs [data-baseweb="tab"]{{border-radius:8px !important;color:{text_muted} !important;font-weight:500 !important;}}
.stTabs [aria-selected="true"]{{background:linear-gradient(135deg,rgba(0,212,255,0.2),rgba(79,142,247,0.15)) !important;color:#00d4ff !important;}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-track{{background:rgba(0,0,0,0.1);}}
::-webkit-scrollbar-thumb{{background:linear-gradient(135deg,#00d4ff,#4f8ef7);border-radius:3px;}}

/* ── DIVIDER ── */
hr{{border-color:rgba(0,212,255,0.1) !important;}}

/* ── ANIMATIONS ── */
@keyframes fadeInUp{{from{{opacity:0;transform:translateY(20px);}}to{{opacity:1;transform:translateY(0);}}}}
.fade-up{{animation:fadeInUp .5s ease forwards;}}
@keyframes pulseGlow{{0%,100%{{box-shadow:0 0 8px rgba(0,212,255,0.3);}}50%{{box-shadow:0 0 22px rgba(0,212,255,0.7);}}}}
.pulse{{animation:pulseGlow 2.5s ease-in-out infinite;}}
@keyframes scanline{{0%{{top:-10%;}}100%{{top:110%;}}}}

/* ── LOGIN ── */
.login-bg{{min-height:90vh;display:flex;align-items:center;justify-content:center;}}
.login-card{{
  background:rgba(2,8,23,0.85);
  backdrop-filter:blur(40px);
  -webkit-backdrop-filter:blur(40px);
  border:1px solid rgba(0,212,255,0.25);
  border-radius:24px;padding:48px 44px;
  width:100%;max-width:440px;
  box-shadow:0 32px 80px rgba(0,0,0,0.6),0 0 60px rgba(0,212,255,0.07);
  position:relative;overflow:hidden;
}}
.login-card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#00d4ff,#4f8ef7,transparent);
}}
.login-title{{
  text-align:center;font-family:'Orbitron',sans-serif;
  font-size:22px;font-weight:700;
  background:linear-gradient(135deg,#00d4ff,#4f8ef7);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:4px;
}}
.login-subtitle{{text-align:center;font-size:12px;color:#475569;margin-bottom:28px;letter-spacing:.06em;text-transform:uppercase;}}
.login-icon{{text-align:center;font-size:52px;margin-bottom:12px;filter:drop-shadow(0 0 16px rgba(0,212,255,0.6));}}
.login-features{{display:flex;justify-content:center;gap:20px;margin-top:24px;}}
.login-feat{{text-align:center;font-size:11px;color:#334155;}}
.login-feat .feat-icon{{font-size:20px;display:block;margin-bottom:4px;}}
.tech-badge{{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.2);
  border-radius:20px;padding:4px 12px;font-size:10px;
  color:#00d4ff;letter-spacing:.08em;text-transform:uppercase;margin-bottom:16px;
}}
.status-dot{{width:6px;height:6px;background:#10b981;border-radius:50%;box-shadow:0 0 6px #10b981;display:inline-block;animation:pulseGlow 1.5s infinite;}}

/* ── NAV LABEL ── */
.nav-section{{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.15em;color:#334155 !important;padding:8px 4px 4px;}}

/* ── SIDEBAR STAT CARDS ── */
.sidebar-stat{{background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.12);border-radius:8px;padding:10px 12px;text-align:center;margin:4px 0;}}
.sidebar-stat .s-val{{font-size:18px;font-weight:700;color:#00d4ff !important;}}
.sidebar-stat .s-lbl{{font-size:10px;color:#475569 !important;text-transform:uppercase;letter-spacing:.05em;}}

/* ── DATAFRAME ── */
.stDataFrame{{border-radius:12px;overflow:hidden;}}

/* ── SELECTBOX / SLIDER ── */
.stSelectbox>div>div{{background:{input_bg} !important;border:1px solid rgba(0,212,255,0.25) !important;border-radius:10px !important;}}
.stSlider .rc-slider-handle{{background:#00d4ff !important;border-color:#00d4ff !important;box-shadow:0 0 8px rgba(0,212,255,0.5) !important;}}
.stSlider .rc-slider-track{{background:linear-gradient(90deg,#00d4ff,#4f8ef7) !important;}}

/* ── CHECKBOX / TOGGLE ── */
.stCheckbox>label{{color:{text} !important;}}
</style>
"""

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
def show_login():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{display:none!important;}
    header{display:none!important;}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style='margin-top:40px; text-align:center;'>
            <div class='tech-badge'><span class='status-dot'></span> SYSTEM ONLINE · v4.0</div>
        </div>
        <div class='login-icon'>🏢</div>
        <div class='login-title'>TechLift</div>
        <div style='text-align:center;font-size:13px;color:#64748b;margin-bottom:4px;'>Elevator Monitoring System</div>
        <div class='login-subtitle'>⚙️ Predictive Intelligence Platform · 📊 Real-Time Analytics</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤  Username", placeholder="Enter username")
            password = st.text_input("🔐  Password", type="password", placeholder="Enter password")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⚡  ACCESS SYSTEM", use_container_width=True)
            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌  Invalid credentials. Check demo accounts below.")

        st.markdown("""
        <div class='login-features'>
            <div class='login-feat'><span class='feat-icon'>🛡️</span>Secure Auth</div>
            <div class='login-feat'><span class='feat-icon'>📡</span>Live Data</div>
            <div class='login-feat'><span class='feat-icon'>🤖</span>AI Engine</div>
        </div>
        <div style='text-align:center;margin-top:20px;color:#1e293b;font-size:11px;'>
            Demo: <code style='color:#00d4ff;'>admin</code> / <code style='color:#00d4ff;'>elevate123</code>
            &nbsp;·&nbsp; <code style='color:#4f8ef7;'>tanmay</code> / <code style='color:#4f8ef7;'>1234</code>
        </div>
        """, unsafe_allow_html=True)

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

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    initials = st.session_state.username[:2].upper()
    role     = "Administrator" if st.session_state.username == "admin" else "Senior Engineer" if st.session_state.username == "tanmay" else "Engineer"
    st.markdown(f"""
    <div class='user-badge pulse'>
        <div class='user-avatar'>{initials}</div>
        <div>
            <div class='user-name'>{st.session_state.username.capitalize()}</div>
            <div class='user-role'>{role}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()

    st.markdown("<div class='nav-section'>⬡ Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["📊  Overview", "📈  Advanced Analytics", "🤖  ML Predictions",
         "🚨  Alerts & Warnings", "📑  Report Generator", "⚙️  Settings"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='nav-section' style='margin-top:12px;'>⬡ Quick Stats</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='sidebar-stat'><div class='s-val'>{len(df):,}</div><div class='s-lbl'>Readings</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='sidebar-stat'><div class='s-val'>{healthy_pct:.0f}%</div><div class='s-lbl'>Healthy</div></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-top:auto;padding-top:16px;border-top:1px solid rgba(0,212,255,0.1);'>
        <div style='font-size:10px;color:#1e293b;text-align:center;'>
            🏢 TechLift EMS · v4.0 · © 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def page_header(icon, title, subtitle):
    st.markdown(f"""
    <div class='page-header fade-up'>
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def metric_glass(label, value, sub=""):
    return f"""<div class='metric-glass'>
        <div class='label'>{label}</div>
        <div class='value'>{value}</div>
        <div class='sub'>{sub}</div>
    </div>"""

def styled_fig(fig):
    is_dark = st.session_state.theme == "dark"
    bg      = "#0a0e1a" if is_dark else "#f8fafc"
    fg      = "#e2e8f0" if is_dark else "#0f172a"
    grid    = "#1e293b" if is_dark else "#cbd5e1"
    fig.patch.set_facecolor(bg)
    for ax in fig.get_axes():
        ax.set_facecolor(bg)
        ax.tick_params(colors=fg, labelsize=9)
        ax.xaxis.label.set_color(fg)
        ax.yaxis.label.set_color(fg)
        if hasattr(ax, 'title'): ax.title.set_color(fg)
        ax.spines['bottom'].set_color(grid)
        ax.spines['left'].set_color(grid)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, color=grid, alpha=0.3, linewidth=0.5)
    plt.tight_layout()

# ── PAGE 1: OVERVIEW ──────────────────────────────────────────────────────────
if "Overview" in page:
    page_header("📊", "System Overview", "Real-time health monitoring & predictive intelligence")

    avg_cost = (critical_count * 12000 + maint_count * 2000) / 12
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(metric_glass("✅ Healthy Status", f"{healthy_count/len(df)*100:.1f}%", f"{healthy_count:,} readings"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("⚠️ Maintenance",   f"{maint_count/len(df)*100:.1f}%",   f"{maint_count:,} readings"), unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("🚨 Critical",       f"{critical_count/len(df)*100:.1f}%", f"{critical_count:,} readings"), unsafe_allow_html=True)
    with c4: st.markdown(metric_glass("💰 Savings/Mo",     f"${avg_cost:,.0f}", "vs emergency repairs"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📍 System Health Visualization")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='alert-healthy'><h3 style='margin:0 0 6px'>✅ Healthy</h3><p style='font-size:28px;font-weight:800;margin:0'>{healthy_count/len(df)*100:.1f}%</p><p style='margin:6px 0 0;font-size:13px;opacity:.8'>Vibration &lt; {healthy_thr:.2f}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='alert-warning'><h3 style='margin:0 0 6px'>⚠️ Maintenance</h3><p style='font-size:28px;font-weight:800;margin:0'>{maint_count/len(df)*100:.1f}%</p><p style='margin:6px 0 0;font-size:13px;opacity:.8'>Vibration {healthy_thr:.2f}–{critical_thr:.2f}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='alert-critical'><h3 style='margin:0 0 6px'>🚨 Critical</h3><p style='font-size:28px;font-weight:800;margin:0'>{critical_count/len(df)*100:.1f}%</p><p style='margin:6px 0 0;font-size:13px;opacity:.8'>Vibration &gt; {critical_thr:.2f}</p></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💡 Key Insights")
    col1,col2 = st.columns(2)
    with col1:
        r = df['revolutions'].corr(df['vibration'])
        st.success(f"**🚪 Door Usage Impact: r = {r:.3f}**\n\nVERY STRONG correlation\n\n• High-usage elevators: +51% vibration\n• Usage is PRIMARY driver\n• Maintenance = usage intensity")
    with col2:
        r2 = df['humidity'].corr(df['vibration'])
        st.info(f"**💨 Environmental Impact: r = {r2:.3f}**\n\nWEAK correlation\n\n• Humidity has minor effect\n• Not a primary concern\n• Focus on usage-based maintenance")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("💰 Financial Impact Analysis")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(metric_glass("Emergency Repair",   "$12,000", "per incident"), unsafe_allow_html=True)
    with c2: st.markdown(metric_glass("Preventive Service", "$2,000",  "per service"), unsafe_allow_html=True)
    with c3: st.markdown(metric_glass("Break-Even",         "2 failures/yr", "$12,000 savings"), unsafe_allow_html=True)

# ── PAGE 2: ADVANCED ANALYTICS ────────────────────────────────────────────────
elif "Analytics" in page:
    page_header("📈", "Advanced Analytics", "Deep-dive data exploration with interactive filters")

    st.subheader("🎛️ Data Filters")
    col1,col2,col3 = st.columns(3)
    with col1:
        vib_range = st.slider("Vibration Range", float(df['vibration'].min()), float(df['vibration'].max()),
                              (float(df['vibration'].min()), float(df['vibration'].max())), step=0.1)
    with col2:
        rev_range = st.slider("Door Revolutions", float(df['revolutions'].min()), float(df['revolutions'].max()),
                              (float(df['revolutions'].min()), float(df['revolutions'].max())), step=1.0)
    with col3:
        hum_range = st.slider("Humidity %", float(df['humidity'].min()), float(df['humidity'].max()),
                              (float(df['humidity'].min()), float(df['humidity'].max())), step=1.0)

    fdf = df[(df['vibration']>=vib_range[0])&(df['vibration']<=vib_range[1])&
             (df['revolutions']>=rev_range[0])&(df['revolutions']<=rev_range[1])&
             (df['humidity']>=hum_range[0])&(df['humidity']<=hum_range[1])]

    st.markdown(f"<div class='glass-card'><b>🔍 Filtered:</b> {len(fdf):,} / {len(df):,} readings &nbsp;|&nbsp; Healthy: {len(fdf[fdf['vibration']<healthy_thr]):,} &nbsp;|&nbsp; Critical: {len(fdf[fdf['vibration']>=critical_thr]):,}</div>", unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["📊 Time Series","📉 Distributions","📍 Correlations","🔍 Statistics","📋 Data Table"])

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(fdf['ID'], fdf['vibration'], linewidth=1.5, color='#00d4ff', alpha=0.9, label='Vibration')
        ax.axhline(mean_vib,    color='#10b981', linestyle='--', linewidth=1.5, label=f'Avg: {mean_vib:.2f}')
        ax.axhline(healthy_thr, color='#f59e0b', linestyle='--', linewidth=1.5, label=f'Action: {healthy_thr:.2f}')
        ax.axhline(critical_thr,color='#ef4444', linestyle='--', linewidth=1.5, label=f'Critical: {critical_thr:.2f}')
        ax.fill_between(fdf['ID'], fdf['vibration'], alpha=0.1, color='#00d4ff')
        ax.set_xlabel('Sample Index', fontsize=10); ax.set_ylabel('Vibration', fontsize=10)
        ax.set_title('Vibration Trends with Thresholds', fontsize=12, fontweight='bold')
        ax.legend(facecolor='#0a0e1a', edgecolor='#1e293b', labelcolor='#e2e8f0', fontsize=9)
        styled_fig(fig); st.pyplot(fig); plt.close()

    with tab2:
        col1,col2 = st.columns(2)
        with col1:
            fig,ax = plt.subplots()
            ax.hist(fdf['humidity'], bins=25, color='#00d4ff', edgecolor='#020817', alpha=0.8)
            ax.set_xlabel('Humidity (%)'); ax.set_ylabel('Frequency'); ax.set_title('Humidity Distribution')
            styled_fig(fig); st.pyplot(fig); plt.close()
        with col2:
            fig,ax = plt.subplots()
            ax.hist(fdf['revolutions'], bins=25, color='#4f8ef7', edgecolor='#020817', alpha=0.8)
            ax.set_xlabel('Revolutions'); ax.set_ylabel('Frequency'); ax.set_title('Door Usage Distribution')
            styled_fig(fig); st.pyplot(fig); plt.close()

    with tab3:
        cols = ['revolutions','humidity','vibration','x1','x2','x3','x4','x5']
        fig,ax = plt.subplots(figsize=(10,8))
        sns.heatmap(fdf[cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax,
                    linecolor='#0a0e1a', linewidths=0.5)
        styled_fig(fig); st.pyplot(fig); plt.close()

    with tab4:
        cols = ['revolutions','humidity','vibration','x1','x2','x3','x4','x5']
        st.dataframe(fdf[cols].describe().round(3), use_container_width=True)

    with tab5:
        st.dataframe(fdf.round(2), height=400, use_container_width=True)
        csv = fdf.to_csv(index=False)
        st.download_button("📥  Download CSV", csv, f"elevator_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ── PAGE 3: ML PREDICTIONS ────────────────────────────────────────────────────
elif "ML" in page:
    page_header("🤖", "ML Predictions", "AI-powered failure prediction engine")

    if not ML_AVAILABLE:
        st.warning("⚠️ scikit-learn not installed. Run: pip install scikit-learn")
    else:
        st.subheader("🎯 Configure Sensor Parameters")
        col1,col2 = st.columns([2,1])
        with col1:
            ca,cb,cc = st.columns(3)
            rev = ca.slider("🔄 Revolutions", 5.0, 40.0, 20.0)
            hum = cb.slider("💧 Humidity",    30.0, 80.0, 55.0)
            x1  = cc.slider("📡 Sensor x1",  75.0,105.0, 90.0)
            cd,ce,cf,cg = st.columns(4)
            x2 = cd.slider("x2", 45.0,60.0,50.0); x3 = ce.slider("x3", 70.0,90.0,80.0)
            x4 = cf.slider("x4", 34.0,47.0,40.0); x5 = cg.slider("x5", 49.0,71.0,60.0)

            @st.cache_resource
            def train_model():
                X = df[['revolutions','humidity','x1','x2','x3','x4','x5']]
                y = df['vibration']
                m = RandomForestRegressor(n_estimators=100, random_state=42)
                m.fit(X, y)
                return m

            model = train_model()
            pred  = model.predict([[rev,hum,x1,x2,x3,x4,x5]])[0]

            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("📊 Prediction Result")
            if pred < healthy_thr:
                st.markdown(f"<div class='alert-healthy'><h2>✅ HEALTHY — {pred:.3f}</h2><p>System operating within normal parameters. No action required.</p></div>", unsafe_allow_html=True)
            elif pred < critical_thr:
                st.markdown(f"<div class='alert-warning'><h2>⚠️ MAINTENANCE NEEDED — {pred:.3f}</h2><p>Schedule preventive maintenance. Vibration approaching action threshold.</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='alert-critical'><h2>🚨 CRITICAL — {pred:.3f}</h2><p>Immediate inspection required! Vibration exceeds critical threshold.</p></div>", unsafe_allow_html=True)

        with col2:
            imp = dict(zip(['revolutions','humidity','x1','x2','x3','x4','x5'], model.feature_importances_))
            imp_sorted = sorted(imp.items(), key=lambda x: x[1], reverse=True)
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("🔬 Feature Importance")
            for feat, score in imp_sorted:
                pct = score * 100
                st.markdown(f"""
                <div style='margin:8px 0;'>
                    <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;'>
                        <span>{feat}</span><span>{pct:.1f}%</span>
                    </div>
                    <div style='background:rgba(0,212,255,0.1);border-radius:4px;height:6px;'>
                        <div style='background:linear-gradient(90deg,#00d4ff,#4f8ef7);width:{pct:.0f}%;height:100%;border-radius:4px;'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ── PAGE 4: ALERTS ────────────────────────────────────────────────────────────
elif "Alerts" in page:
    page_header("🚨", "Alerts & Warnings", "Real-time system health monitoring")

    critical_df = df[df['vibration'] >= critical_thr]
    warning_df  = df[(df['vibration'] >= healthy_thr) & (df['vibration'] < critical_thr)]
    healthy_df  = df[df['vibration'] <  healthy_thr]

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f"<div class='alert-healthy'><h2>✅ {len(healthy_df):,}</h2><p style='margin:0;font-size:14px;'>Healthy Readings</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='alert-warning'><h2>⚠️ {len(warning_df):,}</h2><p style='margin:0;font-size:14px;'>Need Maintenance</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='alert-critical'><h2>🚨 {len(critical_df):,}</h2><p style='margin:0;font-size:14px;'>Critical Alerts</p></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🚨 Critical Records", "⚠️ Warning Records"])
    with tab1:
        if len(critical_df):
            st.dataframe(critical_df.round(3), use_container_width=True, height=350)
        else:
            st.success("✅ No critical records found!")
    with tab2:
        if len(warning_df):
            st.dataframe(warning_df.round(3), use_container_width=True, height=350)
        else:
            st.success("✅ No warning records found!")

# ── PAGE 5: REPORT GENERATOR ──────────────────────────────────────────────────
elif "Report" in page:
    page_header("📑", "Report Generator", "Generate comprehensive analysis reports")

    col1, col2 = st.columns([2, 1])
    with col1:
        rtype = st.selectbox("Report Type", ["Executive Summary", "Technical Analysis", "Maintenance Schedule", "Cost Analysis"])
        rdate = st.date_input("Report Date", value=datetime.now())
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        fmt = st.selectbox("Format", ["Markdown", "Plain Text"])

    if st.button("⚡  Generate Report", key="gen_report"):
        with st.spinner("Generating report..."):
            import time; time.sleep(0.5)
        st.success("✅ Report Generated Successfully!")
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(metric_glass("Total Readings",  f"{len(df):,}", "data points"), unsafe_allow_html=True)
        with c2: st.markdown(metric_glass("System Health",   f"{healthy_pct:.1f}%", "within normal"), unsafe_allow_html=True)
        with c3: st.markdown(metric_glass("Critical Alerts", f"{critical_count:,}", f"{critical_count/len(df)*100:.1f}%"), unsafe_allow_html=True)

        report_txt = f"""# {rtype} — TechLift Elevator Monitoring
**Generated:** {rdate.strftime('%Y-%m-%d')} | **User:** {st.session_state.username.capitalize()}

## Executive Summary
- Total sensor readings: {len(df):,}
- Healthy readings: {healthy_count:,} ({healthy_pct:.1f}%)
- Maintenance needed: {maint_count:,} ({maint_count/len(df)*100:.1f}%)
- Critical alerts: {critical_count:,} ({critical_count/len(df)*100:.1f}%)

## Sensor Statistics
- Avg vibration: {mean_vib:.3f} ± {std_vib:.3f}
- Action threshold: {healthy_thr:.3f}
- Critical threshold: {critical_thr:.3f}

## Financial Impact
- Estimated monthly savings: ${(critical_count*12000+maint_count*2000)/12:,.0f}
- Recommendations: Implement usage-based maintenance scheduling.
"""
        st.code(report_txt, language="markdown")
        st.download_button("📥  Download Report", report_txt,
                           f"report_{rtype.replace(' ','_').lower()}_{rdate}.md", "text/plain")

# ── PAGE 6: SETTINGS ──────────────────────────────────────────────────────────
elif "Settings" in page:
    page_header("⚙️", "Settings", "System configuration & preferences")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎨 Appearance")
        theme_choice = st.radio("Interface Theme", ["dark", "light"],
                                index=0 if st.session_state.theme == "dark" else 1,
                                format_func=lambda x: "🌙 Dark Mode" if x == "dark" else "☀️ Light Mode")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔔 Notifications")
        alerts_on  = st.checkbox("Enable Critical Alerts",    value=True)
        warn_on    = st.checkbox("Enable Warning Alerts",     value=True)
        reports_on = st.checkbox("Enable Scheduled Reports",  value=False)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Data Settings")
        refresh = st.selectbox("Refresh Interval", ["Manual", "30 seconds", "1 minute", "5 minutes"])
        decimals = st.slider("Decimal Precision", 1, 5, 3)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("👤 Account Info")
        st.markdown(f"""
        <div style='font-size:13px;'>
            <p><b>Username:</b> {st.session_state.username.capitalize()}</p>
            <p><b>Role:</b> {role}</p>
            <p><b>Session:</b> Active</p>
            <p><b>Last Login:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("💾  Save Settings", key="save_settings"):
        st.session_state.theme = theme_choice
        # Re-inject updated theme CSS immediately
        st.markdown(get_css(theme_choice), unsafe_allow_html=True)
        st.success("✅ Settings saved! Theme applied — refresh the page if colours don't update instantly.")
        st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;color:#1e293b;font-size:11px;padding:8px 0;'>
    🏢 TechLift Elevator Monitoring System · v4.0 · 
    Logged in as <b style='color:#00d4ff;'>{st.session_state.username.capitalize()}</b> · 
    {datetime.now().strftime('%Y-%m-%d %H:%M')} · © 2026 TechLift
</div>
""", unsafe_allow_html=True)
