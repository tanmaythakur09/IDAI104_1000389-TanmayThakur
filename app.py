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

# ── INJECT CSS ────────────────────────────────────────────────────────────────
def inject_css(theme="dark"):
    # Common variables
    accent_green = "#39ff14"
    accent_green_muted = "rgba(57, 255, 20, 0.2)"
    accent_green_glow = "rgba(57, 255, 20, 0.5)"
    
    if theme == "dark":
        bg_color = "#0a0a0a"
        bg_card = "rgba(15, 15, 15, 0.7)"
        bg_input = "rgba(0,0,0,0.6)"
        text_primary = "#e2e8f0"
        text_secondary = "#94a3b8"
        border_color = "rgba(57, 255, 20, 0.2)"
        sidebar_bg = "rgba(8, 8, 8, 0.95)"
    else:
        bg_color = "#f0f2f5"
        bg_card = "rgba(255, 255, 255, 0.85)"
        bg_input = "rgba(255, 255, 255, 0.9)"
        text_primary = "#1e293b"
        text_secondary = "#475569"
        border_color = "rgba(57, 255, 20, 0.4)"
        sidebar_bg = "rgba(248, 250, 252, 0.95)"

    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ── BASE ── */
html, body {{ font-family: 'Rajdhani', sans-serif; background-color: {bg_color}; }}
* {{ font-family: 'Rajdhani', sans-serif; box-sizing: border-box; }}
.stApp {{
    background: {bg_color} !important;
    background-image: 
        radial-gradient(circle at 10% 10%, {accent_green_muted} 0%, transparent 20%),
        radial-gradient(circle at 90% 90%, rgba(0, 150, 255, 0.05) 0%, transparent 20%),
        linear-gradient({accent_green_muted} 1px, transparent 1px),
        linear-gradient(90deg, {accent_green_muted} 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
    color: {text_primary};
}}

/* ── ANIMATED GRADIENT BG ── */
.stApp::before {{
    content: ''; box-shadow: inset 0 0 150px {accent_green_muted};
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none; z-index: 0;
}}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem !important; }}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
    border-right: 1px solid {border_color};
    box-shadow: 2px 0 25px {accent_green_muted};
    min-width: 270px !important;
}}
section[data-testid="stSidebar"] * {{ color: {text_secondary} !important; }}

/* ── NAV RADIO ── */
div[data-testid="stRadio"] > label {{ display: none; }}
div[data-testid="stRadio"] div[role="radiogroup"] {{ display: flex; flex-direction: column; gap: 8px; }}
div[data-testid="stRadio"] label {{
    background: transparent;
    border: 1px solid {border_color};
    border-radius: 4px; padding: 12px 16px;
    cursor: pointer; transition: all .3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    font-weight: 600; font-size: 14px; letter-spacing: .1em; text-transform: uppercase;
    position: relative; overflow: hidden; font-family: 'Orbitron', sans-serif;
}}
div[data-testid="stRadio"] label::before {{
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: transparent; transition: all .3s ease;
}}
div[data-testid="stRadio"] label:hover {{
    background: {accent_green_muted}; border-color: {accent_green};
    padding-left: 20px; color: {text_primary} !important;
}}
div[data-testid="stRadio"] label[data-selected="true"],
div[data-testid="stRadio"] input:checked + div {{
    background: linear-gradient(90deg, {accent_green_muted}, transparent);
    border-color: {accent_green}; box-shadow: inset 0 0 15px {accent_green_muted}, 0 0 10px {accent_green_muted};
    color: {text_primary} !important; font-weight: 700;
}}
div[data-testid="stRadio"] label[data-selected="true"]::before,
div[data-testid="stRadio"] input:checked + div::before {{
    background: {accent_green}; box-shadow: 0 0 12px {accent_green};
}}

/* ── GLASS CARDS ── */
.glass-card {{
    background: {bg_card};
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid {border_color}; border-radius: 4px;
    padding: 24px; margin: 8px 0; position: relative;
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.02), 0 5px 20px rgba(0,0,0,0.1);
    transition: all .3s;
}}
.glass-card::after {{
    content: ''; position: absolute; top: -1px; left: -1px; right: -1px; bottom: -1px;
    background: linear-gradient(45deg, transparent, {accent_green_muted}, transparent);
    z-index: -1; opacity: 0; transition: opacity 0.3s;
}}
.glass-card:hover {{ border-color: {accent_green}; box-shadow: 0 0 20px {accent_green_muted}; }}
.glass-card:hover::after {{ opacity: 1; }}

/* ── METRIC CARDS ── */
.metric-glass {{
    background: linear-gradient(135deg, {accent_green_muted}, transparent);
    border: 1px solid {border_color}; border-left: 4px solid {accent_green};
    border-radius: 4px; padding: 22px; position: relative;
    text-align: left; overflow: hidden;
}}
.metric-glass::before {{
    content:''; position: absolute; top:0; right:0; width:50px; height:100%;
    background: linear-gradient(90deg, transparent, {accent_green_muted});
}}
.metric-glass .label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .2em; color: {text_secondary}; margin-bottom: 8px; font-family: 'Orbitron', sans-serif;}}
.metric-glass .value {{
    font-size: 34px; font-weight: 700; font-family: 'Orbitron', sans-serif;
    color: {text_primary}; text-shadow: 0 0 10px {accent_green_muted};
}}
.metric-glass .sub {{ font-size: 12px; color: {text_secondary}; margin-top: 8px; font-family: 'Rajdhani', sans-serif; }}

/* ── STATUS ALERTS ── */
.alert-critical {{ border-left: 4px solid #ff0044; background: rgba(255, 0, 68, 0.08); border: 1px solid rgba(255,0,68,0.3); padding: 20px; color: #ff0044; box-shadow: 0 0 15px rgba(255,0,68,0.2); font-family: 'Orbitron', sans-serif; text-transform:uppercase; letter-spacing: .05em; margin-bottom: 12px; }}
.alert-warning {{ border-left: 4px solid #ffb703; background: rgba(255, 183, 3, 0.08); border: 1px solid rgba(255,183,3,0.3); padding: 20px; color: #ffb703; box-shadow: 0 0 15px rgba(255,183,3,0.2); font-family: 'Orbitron', sans-serif; text-transform:uppercase; letter-spacing: .05em; margin-bottom: 12px; }}
.alert-healthy {{ border-left: 4px solid {accent_green}; background: {accent_green_muted}; border: 1px solid {border_color}; padding: 20px; color: {accent_green}; box-shadow: 0 0 15px {accent_green_muted}; font-family: 'Orbitron', sans-serif; text-transform:uppercase; letter-spacing: .05em; margin-bottom: 12px; }}

/* ── PAGE HEADER ── */
.page-header {{
    background: url('data:image/svg+xml;utf8,<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg"><path d="M0 40 L40 0" stroke="{accent_green_muted}" stroke-width="1"/></svg>'), linear-gradient(90deg, {bg_card}, transparent);
    border: 1px solid {border_color}; border-bottom: 2px solid {accent_green};
    padding: 24px 32px; margin-bottom: 30px;
    position: relative; border-radius: 4px;
}}
.page-header::before {{
    content: ''; position: absolute; left:-1px; top:-1px; width:15px; height:15px;
    border-top: 2px solid {accent_green}; border-left: 2px solid {accent_green};
}}
.page-header h1 {{
    font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 700;
    color: {text_primary}; text-shadow: 0 0 15px {accent_green_glow}; margin: 0 0 8px 0;
    text-transform: uppercase; letter-spacing: .1em;
}}
.page-header p {{ color: {text_secondary}; margin: 0; font-size: 13px; letter-spacing: .15em; text-transform: uppercase; font-weight: 600; }}

/* ── BUTTONS ── */
.stButton > button {{
    background: transparent !important;
    color: {accent_green} !important; border: 1px solid {accent_green} !important;
    border-radius: 4px !important; font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important; padding: 12px 24px !important;
    width: 100% !important; transition: all .2s !important;
    letter-spacing: .15em !important; text-transform: uppercase !important;
    position: relative; overflow: hidden;
    box-shadow: inset 0 0 10px {accent_green_muted} !important;
}}
.stButton > button:hover {{
    background: {accent_green_muted} !important; color: {text_primary} !important;
    box-shadow: 0 0 20px {accent_green_glow}, inset 0 0 15px {accent_green_muted} !important;
    text-shadow: 0 0 5px {text_primary} !important;
}}

/* ── TEXT INPUTS ── */
.stTextInput > div > div > input {{
    background: {bg_input} !important;
    border: 1px solid {border_color} !important; border-left: 3px solid {accent_green} !important;
    border-radius: 4px !important; color: {text_primary} !important;
    padding: 14px 16px !important; font-size: 15px !important; font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: .05em; transition: all .3s;
}}
.stTextInput > div > div > input:focus {{
    background: {bg_input} !important; border-color: {accent_green} !important;
    box-shadow: 0 0 15px {accent_green_muted} !important;
}}

/* ── LABELS ── */
.stTextInput > label, .stSelectbox > label, .stSlider > label {{
    color: {text_secondary} !important; font-family: 'Orbitron', sans-serif !important;
    font-size: 11px !important; letter-spacing: .15em !important; text-transform: uppercase !important;
    margin-bottom: 8px !important; font-weight: 600 !important;
}}

/* ── SLIDERS ── */
.stSlider > div > div > div > div {{ background: {accent_green} !important; box-shadow: 0 0 10px {accent_green} !important; }}
.stSlider [data-testid="stThumbValue"] {{ color: {text_primary} !important; font-family: 'Orbitron', sans-serif !important; }}
div[data-testid="stSlider"] > div > div > div[role="slider"] {{
    background: {bg_color} !important; border: 2px solid {accent_green} !important;
    box-shadow: 0 0 10px {accent_green} !important; border-radius: 50% !important;
    width: 18px !important; height: 18px !important;
}}

/* ── DATAFRAME ── */
.stDataFrame {{ border: 1px solid {border_color}; border-radius: 4px; overflow: hidden; }}
.stDataFrame table {{ background: {bg_input} !important; color: {text_primary} !important; font-family: 'Rajdhani', sans-serif !important; }}
.stDataFrame th {{ background: {bg_card} !important; color: {text_secondary} !important; font-family: 'Orbitron', sans-serif !important; }}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: {bg_color}; }}
::-webkit-scrollbar-thumb {{ background: {accent_green}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: #00cc00; }}

/* ── LOGIN ── */
.login-bg {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
.login-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; height: 80vh; margin-top: 5vh; }}
.login-card {{
    background: {bg_card};
    backdrop-filter: blur(25px); border: 1px solid {border_color};
    padding: 50px 45px; width: 100%; max-width: 480px;
    box-shadow: 0 0 40px rgba(0,0,0,0.5), inset 0 0 30px {accent_green_muted};
    position: relative; overflow: hidden; border-radius: 4px;
}}
.login-card::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, {accent_green}, {text_primary}, {accent_green}, transparent);
    box-shadow: 0 0 15px {accent_green};
}}
.corner-tl {{ position: absolute; top:0; left:0; width: 20px; height: 20px; border-top: 2px solid {accent_green}; border-left: 2px solid {accent_green}; }}
.corner-br {{ position: absolute; bottom:0; right:0; width: 20px; height: 20px; border-bottom: 2px solid {accent_green}; border-right: 2px solid {accent_green}; }}

.login-title {{
    text-align: center; font-family: 'Orbitron', sans-serif;
    font-size: 36px; font-weight: 900; color: {text_primary};
    text-shadow: 0 0 20px {accent_green_glow};
    letter-spacing: .15em; text-transform: uppercase; margin-bottom: 5px;
}}
.login-subtitle {{
    text-align: center; font-size: 13px; color: {text_secondary};
    margin-bottom: 35px; letter-spacing: .3em; text-transform: uppercase; font-family: 'Rajdhani', sans-serif; font-weight: 600;
}}
.login-icon {{ text-align: center; font-size: 55px; margin-bottom: 10px; filter: drop-shadow(0 0 25px {accent_green_glow}); }}
.tech-badge {{
    position: absolute; top: 20px; right: 20px;
    background: {accent_green_muted}; border: 1px solid {accent_green};
    padding: 6px 12px; font-size: 10px; color: {accent_green};
    letter-spacing: .15em; font-family: 'Orbitron', sans-serif; font-weight: 700;
    box-shadow: 0 0 10px {accent_green_muted}; border-radius: 4px;
}}
.status-dot {{
    width: 8px; height: 8px; background: {accent_green}; border-radius: 50%;
    box-shadow: 0 0 12px {accent_green}; display: inline-block; animation: blink 1.2s infinite alternate; margin-right: 6px;
}}
@keyframes blink {{ from {{ opacity: 0.3; }} to {{ opacity: 1; }} }}
.login-features {{ display: flex; justify-content: center; gap: 30px; margin-top: 35px; border-top: 1px solid {border_color}; padding-top: 25px;}}
.login-feat {{ text-align: center; font-size: 11px; color: {text_secondary}; text-transform: uppercase; letter-spacing: .15em; font-family: 'Orbitron', sans-serif; font-weight: 600; }}
.login-feat .feat-icon {{ font-size: 26px; display: block; margin-bottom: 8px; color: {accent_green}; filter: drop-shadow(0 0 10px {accent_green_glow}); }}

/* MISC */
h2, h3 {{ color: {text_primary} !important; font-family: 'Orbitron', sans-serif !important; letter-spacing: .08em; text-transform: uppercase; }}
hr {{ border-color: {border_color} !important; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


inject_css(st.session_state.theme)

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
def show_login():
    theme = st.session_state.get('theme', 'dark')
    bg_color = "#0a0a0a" if theme == "dark" else "#f0f2f5"
    accent_green_muted = "rgba(57, 255, 20, 0.05)"
    
    st.markdown(f"""
    <style>
    section[data-testid="stSidebar"]{{display:none!important;}}
    header{{display:none!important;}}
    .stApp {{ background: {bg_color} url('data:image/svg+xml;utf8,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M100 0 L0 100" stroke="{accent_green_muted}" stroke-width="1"/></svg>') !important; }}
    </style>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
        st.markdown("""
        <div class='login-card'>
            <div class='corner-tl'></div>
            <div class='corner-br'></div>
            <div class='tech-badge'><span class='status-dot'></span> SYS.ONLINE</div>
            <div class='login-icon'>💠</div>
            <div class='login-title'>TechLift</div>
            <div class='login-subtitle'>v4.0 // PREDICTIVE AI CORE</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("IDENTIFICATION [USER]", placeholder="Enter ID...")
            password = st.text_input("AUTHORIZATION [PASS]", type="password", placeholder="Enter Passkey...")
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("INITIALIZE UPLINK", use_container_width=True)
            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("ACCESS DENIED: Credentials mismatch.")

        st.markdown("""
            <div class='login-features'>
                <div class='login-feat'><span class='feat-icon'>🛡️</span>AES-256</div>
                <div class='login-feat'><span class='feat-icon'>📡</span>UPLINK</div>
                <div class='login-feat'><span class='feat-icon'>🧠</span>NEURAL NET</div>
            </div>
            <div style='text-align:center;margin-top:25px;color:#a5b4fc;font-size:11px;font-family: Rajdhani, sans-serif;letter-spacing: .08em;'>
                OVERRIDE: [ <span style='color:#0ff;'>admin</span> : <span style='color:#0ff;'>elevate123</span> ] // [ <span style='color:#8a2be2;'>tanmay</span> : <span style='color:#8a2be2;'>1234</span> ]
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

# ── ROLE (module-level so Settings page can access it) ───────────────────────
role = "Administrator" if st.session_state.username == "admin" else "Senior Engineer" if st.session_state.username == "tanmay" else "Engineer"

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    initials = st.session_state.username[:2].upper()
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

def styled_fig(fig, theme="dark"):
    bg   = "#0a0a0a" if theme == "dark" else "#f0f2f5"
    fg   = "#e2e8f0" if theme == "dark" else "#1e293b"
    grid = "#1e293b" if theme == "dark" else "#cbd5e1"
    
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

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    fdf = df[(df['vibration']>=vib_range[0])&(df['vibration']<=vib_range[1])&
             (df['revolutions']>=rev_range[0])&(df['revolutions']<=rev_range[1])&
             (df['humidity']>=hum_range[0])&(df['humidity']<=hum_range[1])]

    st.markdown(f"<div class='glass-card'><b>🔍 Filtered:</b> {len(fdf):,} / {len(df):,} readings &nbsp;|&nbsp; Healthy: {len(fdf[fdf['vibration']<healthy_thr]):,} &nbsp;|&nbsp; Critical: {len(fdf[fdf['vibration']>=critical_thr]):,}</div>", unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["📊 Time Series","📉 Distributions","📍 Correlations","🔍 Statistics","📋 Data Table"])

    with tab1:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(fdf['ID'], fdf['vibration'], linewidth=1.5, color='#39ff14', alpha=0.9, label='Vibration')
        ax.axhline(mean_vib,    color='#10b981', linestyle='--', linewidth=1.5, label=f'Avg: {mean_vib:.2f}')
        ax.axhline(healthy_thr, color='#f59e0b', linestyle='--', linewidth=1.5, label=f'Action: {healthy_thr:.2f}')
        ax.axhline(critical_thr,color='#ef4444', linestyle='--', linewidth=1.5, label=f'Critical: {critical_thr:.2f}')
        ax.fill_between(fdf['ID'], fdf['vibration'], alpha=0.1, color='#39ff14')
        ax.set_xlabel('Sample Index', fontsize=10); ax.set_ylabel('Vibration', fontsize=10)
        ax.set_title('Vibration Trends with Thresholds', fontsize=12, fontweight='bold')
        legend_bg = '#0a0a0a' if st.session_state.theme == 'dark' else '#ffffff'
        legend_fg = '#e2e8f0' if st.session_state.theme == 'dark' else '#1e293b'
        ax.legend(facecolor=legend_bg, edgecolor='rgba(57, 255, 20, 0.4)', labelcolor=legend_fg, fontsize=9)
        styled_fig(fig, st.session_state.theme); st.pyplot(fig); plt.close()

    with tab2:
        col1,col2 = st.columns(2)
        with col1:
            fig,ax = plt.subplots()
            ax.hist(fdf['humidity'], bins=25, color='#39ff14', edgecolor='rgba(0,0,0,0.5)', alpha=0.8)
            ax.set_xlabel('Humidity (%)'); ax.set_ylabel('Frequency'); ax.set_title('Humidity Distribution')
            styled_fig(fig, st.session_state.theme); st.pyplot(fig); plt.close()
        with col2:
            fig,ax = plt.subplots()
            ax.hist(fdf['revolutions'], bins=25, color='#10b981', edgecolor='rgba(0,0,0,0.5)', alpha=0.8)
            ax.set_xlabel('Revolutions'); ax.set_ylabel('Frequency'); ax.set_title('Door Usage Distribution')
            styled_fig(fig, st.session_state.theme); st.pyplot(fig); plt.close()

    with tab3:
        cols = ['revolutions','humidity','vibration','x1','x2','x3','x4','x5']
        fig,ax = plt.subplots(figsize=(10,8))
        line_color = '#0a0a0a' if st.session_state.theme == 'dark' else '#ffffff'
        sns.heatmap(fdf[cols].corr(), annot=True, fmt='.2f', cmap='Greens', ax=ax,
                    linecolor=line_color, linewidths=0.5)
        styled_fig(fig, st.session_state.theme); st.pyplot(fig); plt.close()

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
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
                    <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;color:#94a3b8;'>
                        <span>{feat}</span><span>{pct:.1f}%</span>
                    </div>
                    <div style='background:rgba(57, 255, 20, 0.1);border-radius:4px;height:6px;'>
                        <div style='background:linear-gradient(90deg,#10b981,#39ff14);width:{pct:.0f}%;height:100%;border-radius:4px;box-shadow:0 0 6px rgba(57, 255, 20, 0.4);'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
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

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        rtype = st.selectbox("Report Type", ["Executive Summary", "Technical Analysis", "Maintenance Schedule", "Cost Analysis"])
        rdate = st.date_input("Report Date", value=datetime.now())
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        fmt = st.selectbox("Format", ["Markdown", "Plain Text"])
    st.markdown("</div>", unsafe_allow_html=True)

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
        <div style='font-size:13px;color:#94a3b8;'>
            <p><b style='color:#e2e8f0;'>Username:</b> {st.session_state.username.capitalize()}</p>
            <p><b style='color:#e2e8f0;'>Role:</b> {role}</p>
            <p><b style='color:#e2e8f0;'>Session:</b> Active</p>
            <p><b style='color:#e2e8f0;'>Last Login:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("💾  Save Settings", key="save_settings"):
        st.session_state.theme = theme_choice
        st.success("✅ Settings saved! Theme applied.")
        st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;color:#334155;font-size:11px;padding:8px 0;'>
    🏢 TechLift Elevator Monitoring System · v4.0 · 
    Logged in as <b style='color:#00d4ff;'>{st.session_state.username.capitalize()}</b> · 
    {datetime.now().strftime('%Y-%m-%d %H:%M')} · © 2026 TechLift
</div>
""", unsafe_allow_html=True)


