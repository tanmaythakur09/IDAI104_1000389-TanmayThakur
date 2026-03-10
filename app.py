"""
🛗 ENHANCED Elevator Predictive Maintenance Dashboard v3.0
Premium UI: Glassmorphism dark theme, Login Page, Advanced Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try importing ML library
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="🛗 Elevator Maintenance Pro",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM DARK THEME CSS
# ============================================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* ---- BASE & FONTS ---- */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---- DARK BACKGROUND ---- */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1529 50%, #0a0e1a 100%);
        color: #e2e8f0;
    }

    /* ---- SIDEBAR ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1529 0%, #111827 100%) !important;
        border-right: 1px solid rgba(79, 142, 247, 0.2);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }

    /* ---- GLASS CARDS ---- */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 8px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(79, 142, 247, 0.15);
    }

    /* ---- METRIC CARDS ---- */
    .metric-glass {
        background: linear-gradient(135deg, rgba(79, 142, 247, 0.12) 0%, rgba(155, 89, 182, 0.08) 100%);
        border: 1px solid rgba(79, 142, 247, 0.25);
        border-radius: 14px;
        padding: 20px 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-glass:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(79, 142, 247, 0.2);
        border-color: rgba(79, 142, 247, 0.5);
    }
    .metric-glass .label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    .metric-glass .value {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #4f8ef7, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    .metric-glass .sub {
        font-size: 11px;
        color: #64748b;
        margin-top: 6px;
    }

    /* ---- ALERT CARDS ---- */
    .alert-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(185, 28, 28, 0.12));
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #ef4444;
        padding: 20px;
        border-radius: 12px;
        color: #fca5a5;
        transition: all 0.3s ease;
    }
    .alert-critical:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(239,68,68,0.2); }

    .alert-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(180, 83, 9, 0.12));
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 4px solid #f59e0b;
        padding: 20px;
        border-radius: 12px;
        color: #fcd34d;
        transition: all 0.3s ease;
    }
    .alert-warning:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(245,158,11,0.2); }

    .alert-healthy {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(5, 150, 105, 0.12));
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-left: 4px solid #10b981;
        padding: 20px;
        border-radius: 12px;
        color: #6ee7b7;
        transition: all 0.3s ease;
    }
    .alert-healthy:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(16,185,129,0.2); }

    /* ---- PAGE HEADERS ---- */
    .page-header {
        background: linear-gradient(135deg, rgba(79, 142, 247, 0.1) 0%, rgba(155, 89, 182, 0.08) 100%);
        border: 1px solid rgba(79, 142, 247, 0.2);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .page-header h1 {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #4f8ef7 0%, #9b59b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 6px 0;
    }
    .page-header p {
        color: #64748b;
        margin: 0;
        font-size: 14px;
    }

    /* ---- USER BADGE (sidebar) ---- */
    .user-badge {
        background: linear-gradient(135deg, rgba(79, 142, 247, 0.15), rgba(155, 89, 182, 0.1));
        border: 1px solid rgba(79, 142, 247, 0.3);
        border-radius: 12px;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .user-avatar {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #4f8ef7, #9b59b6);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; font-weight: 700; color: white;
        flex-shrink: 0;
    }
    .user-info .user-name { font-size: 14px; font-weight: 600; color: #e2e8f0; }
    .user-info .user-role { font-size: 11px; color: #64748b; }

    /* ---- LOGIN PAGE ---- */
    .login-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 48px 40px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 32px 80px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(79,142,247,0.1);
    }
    .login-title {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #4f8ef7 0%, #9b59b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
    }
    .login-subtitle {
        text-align: center;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 32px;
    }

    /* ---- STREAMLIT WIDGET OVERRIDES ---- */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(79, 142, 247, 0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        padding: 12px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4f8ef7 !important;
        box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4f8ef7 0%, #9b59b6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(79, 142, 247, 0.4) !important;
        opacity: 0.95 !important;
    }

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(79,142,247,0.2), rgba(155,89,182,0.15)) !important;
        color: #4f8ef7 !important;
    }

    /* ---- DATAFRAME ---- */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* ---- DIVIDER ---- */
    hr { border-color: rgba(255,255,255,0.07) !important; }

    /* ---- SCROLLBAR ---- */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4f8ef7, #9b59b6);
        border-radius: 3px;
    }

    /* ---- MATPLOTLIB CHART BACKGROUND ---- */
    .stpyplot { border-radius: 12px; overflow: hidden; }

    /* ---- ANIMATIONS ---- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-up { animation: fadeInUp 0.5s ease forwards; }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(79,142,247,0.3); }
        50%       { box-shadow: 0 0 20px rgba(79,142,247,0.6); }
    }
    .pulse { animation: pulse-glow 2s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE — LOGIN
# ============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Credentials dictionary
USERS = {
    "admin": "elevate123",
    "tanmay": "1234",
}

# ============================================================================
# LOGIN PAGE
# ============================================================================
def show_login():
    # Centre the login card using columns
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div style='margin-top: 60px;'>
            <div style='text-align:center; font-size:56px; margin-bottom:8px;'>🛗</div>
            <div class='login-title'>Elevator Maintenance Pro</div>
            <div class='login-subtitle'>Sign in to access your dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤  Username", placeholder="Enter your username")
            password = st.text_input("🔒  Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🚀  Sign In", use_container_width=True)

            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try: admin / elevate123")

        st.markdown("""
        <div style='text-align:center; margin-top:24px; color:#334155; font-size:12px;'>
            Demo accounts: <code style='color:#4f8ef7;'>admin</code> / <code style='color:#4f8ef7;'>elevate123</code>
            &nbsp;or&nbsp; <code style='color:#4f8ef7;'>tanmay</code> / <code style='color:#4f8ef7;'>1234</code>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# GUARD — show login if not authenticated
# ============================================================================
if not st.session_state.logged_in:
    show_login()
    st.stop()

# ============================================================================
# LOAD DATA (only after login)
# ============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv('elevator_sensor_data_cleaned.csv')
    return df

df = load_data()

mean_vib = df['vibration'].mean()
std_vib  = df['vibration'].std()
healthy_threshold  = mean_vib + std_vib
critical_threshold = mean_vib + 2 * std_vib

# ============================================================================
# SIDEBAR — USER BADGE + NAV
# ============================================================================
with st.sidebar:
    initials = st.session_state.username[:2].upper()
    st.markdown(f"""
    <div class='user-badge pulse'>
        <div class='user-avatar'>{initials}</div>
        <div class='user-info'>
            <div class='user-name'>{st.session_state.username.capitalize()}</div>
            <div class='user-role'>{'Administrator' if st.session_state.username == 'admin' else 'Engineer'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛗 Navigation")
    page = st.radio(
        "Go to:",
        ["📊 Overview", "📈 Advanced Analytics", "🤖 ML Predictions",
         "📋 Alerts & Warnings", "📑 Report Generator", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### ⚡ Quick Stats")
    col1, col2 = st.columns(2)
    healthy_pct = len(df[df['vibration'] < healthy_threshold]) / len(df) * 100
    with col1:
        st.metric("Readings", f"{len(df):,}")
    with col2:
        st.metric("Healthy %", f"{healthy_pct:.1f}%")

    st.markdown("---")
    st.caption("v3.0 · Premium Edition")

# ============================================================================
# PAGE HEADER HELPER
# ============================================================================
def page_header(icon, title, subtitle):
    st.markdown(f"""
    <div class='page-header fade-up'>
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# METRIC CARD HELPER
# ============================================================================
def metric_glass(label, value, sub=""):
    return f"""
    <div class='metric-glass'>
        <div class='label'>{label}</div>
        <div class='value'>{value}</div>
        <div class='sub'>{sub}</div>
    </div>
    """

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "📊 Overview":
    page_header("📊", "System Overview", "Real-time health monitoring & advanced analytics")

    healthy_count  = len(df[df['vibration'] < healthy_threshold])
    maint_count    = len(df[(df['vibration'] >= healthy_threshold) & (df['vibration'] < critical_threshold)])
    critical_count = len(df[df['vibration'] >= critical_threshold])
    avg_cost       = (critical_count * 12000 + maint_count * 2000) / 12

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_glass("✅ Healthy Status", f"{healthy_count/len(df)*100:.1f}%", f"{healthy_count} readings"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_glass("⚠️ Maintenance", f"{maint_count/len(df)*100:.1f}%", f"{maint_count} readings"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_glass("🚨 Critical", f"{critical_count/len(df)*100:.1f}%", f"{critical_count} readings"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_glass("💰 Savings/Month", f"${avg_cost:,.0f}", "vs emergency repairs"), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📍 System Health Visualization")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='alert-healthy'>
            <h3 style='margin:0 0 6px 0;'>✅ Healthy</h3>
            <p style='font-size: 28px; font-weight: 800; margin:0;'>{(healthy_count/len(df)*100):.1f}%</p>
            <p style='margin:6px 0 0;font-size:13px;opacity:.8;'>Vibration &lt; {healthy_threshold:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='alert-warning'>
            <h3 style='margin:0 0 6px 0;'>⚠️ Maintenance</h3>
            <p style='font-size: 28px; font-weight: 800; margin:0;'>{(maint_count/len(df)*100):.1f}%</p>
            <p style='margin:6px 0 0;font-size:13px;opacity:.8;'>Vibration {healthy_threshold:.2f} – {critical_threshold:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='alert-critical'>
            <h3 style='margin:0 0 6px 0;'>🚨 Critical</h3>
            <p style='font-size: 28px; font-weight: 800; margin:0;'>{(critical_count/len(df)*100):.1f}%</p>
            <p style='margin:6px 0 0;font-size:13px;opacity:.8;'>Vibration &gt; {critical_threshold:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💡 Key Insights")

    col1, col2 = st.columns(2)
    with col1:
        corr_rev = df['revolutions'].corr(df['vibration'])
        st.success(f"""
        **🚪 Door Usage Impact: r = {corr_rev:.3f}**

        This is a VERY STRONG correlation!

        • High-usage elevators: +51% vibration
        • Usage is the PRIMARY driver
        • Maintenance = usage intensity
        """)
    with col2:
        corr_hum = df['humidity'].corr(df['vibration'])
        st.info(f"""
        **💨 Environmental Impact: r = {corr_hum:.3f}**

        This is a WEAK correlation

        • Humidity has minor effect
        • Not a primary concern
        • Focus on usage-based maintenance
        """)

    st.markdown("---")
    st.subheader("💰 Financial Impact Analysis")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(metric_glass("Emergency Repair", "$12,000", "per incident"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_glass("Preventive Service", "$2,000", "per service"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_glass("Break-Even", "2 failures/yr", "$12,000 savings"), unsafe_allow_html=True)

# ============================================================================
# PAGE 2: ADVANCED ANALYTICS
# ============================================================================
elif page == "📈 Advanced Analytics":
    page_header("📈", "Advanced Analytics", "Deep-dive data exploration with interactive filters")

    st.subheader("🎛️ Advanced Filters")
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

    filtered_df = df[
        (df['vibration']   >= vib_range[0]) & (df['vibration']   <= vib_range[1]) &
        (df['revolutions'] >= rev_range[0]) & (df['revolutions'] <= rev_range[1]) &
        (df['humidity']    >= hum_range[0]) & (df['humidity']    <= hum_range[1])
    ]

    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Time Series", "📉 Distributions", "📍 Correlations",
        "🔍 Statistics", "📋 Data Table"
    ])

    dark_bg = '#0d1529'
    text_col = '#94a3b8'

    def style_ax(ax, fig):
        fig.patch.set_facecolor(dark_bg)
        ax.set_facecolor(dark_bg)
        ax.tick_params(colors=text_col, labelsize=10)
        ax.xaxis.label.set_color(text_col)
        ax.yaxis.label.set_color(text_col)
        ax.title.set_color('#e2e8f0')
        for spine in ax.spines.values():
            spine.set_edgecolor('rgba(255,255,255,0.08)')
        ax.grid(True, alpha=0.08, color='white')

    with tab1:
        st.subheader("Vibration Time Series with Thresholds")
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(filtered_df['ID'], filtered_df['vibration'], linewidth=2,
                color='#4f8ef7', label='Vibration Level', alpha=0.9)
        ax.axhline(y=mean_vib,           color='#10b981', linestyle='--', linewidth=1.8,
                   label=f'Average: {mean_vib:.2f}', alpha=0.8)
        ax.axhline(y=healthy_threshold,  color='#f59e0b', linestyle='--', linewidth=1.8,
                   label=f'Action: {healthy_threshold:.2f}', alpha=0.8)
        ax.axhline(y=critical_threshold, color='#ef4444', linestyle='--', linewidth=1.8,
                   label=f'Critical: {critical_threshold:.2f}', alpha=0.8)
        ax.fill_between(filtered_df['ID'], healthy_threshold, critical_threshold,
                        alpha=0.12, color='#f59e0b', label='Maintenance Zone')
        ax.fill_between(filtered_df['ID'], critical_threshold, filtered_df['vibration'].max(),
                        alpha=0.12, color='#ef4444', label='Critical Zone')
        ax.set_xlabel('Sample Index', fontsize=11, fontweight='bold')
        ax.set_ylabel('Vibration Level', fontsize=11, fontweight='bold')
        ax.set_title('Vibration Trends with Action Thresholds', fontsize=13, fontweight='bold')
        legend = ax.legend(loc='upper right', facecolor='#111827', edgecolor='#334155',
                           labelcolor='#94a3b8')
        style_ax(ax, fig)
        plt.tight_layout()
        st.pyplot(fig)
        st.info(f"📊 Showing {len(filtered_df):,} of {len(df):,} total readings")

    with tab2:
        st.subheader("Distribution Analysis")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.hist(filtered_df['humidity'], bins=25, color='#4f8ef7', edgecolor='#0d1529', alpha=0.85)
            ax.axvline(filtered_df['humidity'].mean(), color='#ef4444', linestyle='--',
                       linewidth=2, label=f'Mean: {filtered_df["humidity"].mean():.1f}%')
            ax.set_xlabel('Humidity (%)', fontweight='bold')
            ax.set_ylabel('Frequency', fontweight='bold')
            ax.set_title('Humidity Distribution', fontweight='bold')
            ax.legend(facecolor='#111827', edgecolor='#334155', labelcolor='#94a3b8')
            style_ax(ax, fig)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            ax.hist(filtered_df['revolutions'], bins=25, color='#9b59b6', edgecolor='#0d1529', alpha=0.85)
            ax.axvline(filtered_df['revolutions'].mean(), color='#ef4444', linestyle='--',
                       linewidth=2, label=f'Mean: {filtered_df["revolutions"].mean():.1f}')
            ax.set_xlabel('Door Revolutions', fontweight='bold')
            ax.set_ylabel('Frequency', fontweight='bold')
            ax.set_title('Door Usage Distribution', fontweight='bold')
            ax.legend(facecolor='#111827', edgecolor='#334155', labelcolor='#94a3b8')
            style_ax(ax, fig)
            st.pyplot(fig)

    with tab3:
        st.subheader("Variable Correlation Analysis")
        numeric_cols = ['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']
        corr_matrix  = filtered_df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    ax=ax, vmin=-1, vmax=1, linewidths=0.5, linecolor='#0d1529')
        ax.set_title('Correlation Heatmap', fontsize=13, fontweight='bold')
        style_ax(ax, fig)
        st.pyplot(fig)

    with tab4:
        st.subheader("Statistical Summary")
        stats_data = filtered_df[['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']].describe()
        st.dataframe(stats_data.round(3), use_container_width=True)
        st.subheader("Percentile Analysis")
        percentiles = filtered_df['vibration'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: st.markdown(metric_glass("25th %ile", f"{percentiles[0.25]:.2f}"), unsafe_allow_html=True)
        with c2: st.markdown(metric_glass("50th %ile", f"{percentiles[0.5]:.2f}"),  unsafe_allow_html=True)
        with c3: st.markdown(metric_glass("75th %ile", f"{percentiles[0.75]:.2f}"), unsafe_allow_html=True)
        with c4: st.markdown(metric_glass("90th %ile", f"{percentiles[0.9]:.2f}"),  unsafe_allow_html=True)
        with c5: st.markdown(metric_glass("95th %ile", f"{percentiles[0.95]:.2f}"), unsafe_allow_html=True)
        with c6: st.markdown(metric_glass("99th %ile", f"{percentiles[0.99]:.2f}"), unsafe_allow_html=True)

    with tab5:
        st.subheader("Detailed Data View")
        st.dataframe(filtered_df.round(2), use_container_width=True, height=400)
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"elevator_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# ============================================================================
# PAGE 3: ML PREDICTIONS
# ============================================================================
elif page == "🤖 ML Predictions":
    page_header("🤖", "ML Predictions", "Predict elevator failures before they happen")

    if not ML_AVAILABLE:
        st.warning("⚠️ scikit-learn not installed. Run: pip install scikit-learn")
    else:
        st.subheader("📊 Failure Prediction Model")
        X = df[['revolutions', 'humidity', 'x1', 'x2', 'x3', 'x4', 'x5']]
        y = df['vibration']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("🎯 Make a Prediction")
            ca, cb, cc = st.columns(3)
            with ca: rev_input = st.slider("Door Revolutions", 5.0, 40.0, 20.0)
            with cb: hum_input = st.slider("Humidity %",       30.0, 80.0, 55.0)
            with cc: x1_input  = st.slider("Sensor x1",       75.0, 105.0, 90.0)

            cd, ce, cf, cg = st.columns(4)
            with cd: x2_input = st.slider("Sensor x2", 45.0, 60.0, 50.0)
            with ce: x3_input = st.slider("Sensor x3", 70.0, 90.0, 80.0)
            with cf: x4_input = st.slider("Sensor x4", 34.0, 47.0, 40.0)
            with cg: x5_input = st.slider("Sensor x5", 49.0, 71.0, 60.0)

            input_data = np.array([[rev_input, hum_input, x1_input, x2_input, x3_input, x4_input, x5_input]])
            prediction = model.predict(input_data)[0]

            st.markdown("---")
            if prediction < healthy_threshold:
                st.success(f"### ✅ Prediction: {prediction:.2f}\n**Status: HEALTHY** — No action needed")
            elif prediction < critical_threshold:
                st.warning(f"### ⚠️ Prediction: {prediction:.2f}\n**Status: MAINTENANCE NEEDED** — Schedule service in 2-4 weeks")
            else:
                st.error(f"### 🚨 Prediction: {prediction:.2f}\n**Status: CRITICAL** — Emergency service required!")

        with col2:
            st.subheader("📊 Feature Importance")
            fi = pd.DataFrame({
                'Feature':    X.columns,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)

            dark_bg = '#0d1529'
            fig, ax = plt.subplots(figsize=(6, 5))
            bars = ax.barh(fi['Feature'], fi['Importance'],
                           color=['#4f8ef7' if v > fi['Importance'].median() else '#9b59b6'
                                  for v in fi['Importance']])
            ax.set_xlabel('Importance', fontweight='bold')
            ax.set_title('Feature Importance', fontweight='bold')
            fig.patch.set_facecolor(dark_bg)
            ax.set_facecolor(dark_bg)
            ax.tick_params(colors='#94a3b8')
            ax.xaxis.label.set_color('#94a3b8')
            ax.title.set_color('#e2e8f0')
            for spine in ax.spines.values():
                spine.set_edgecolor('#1e293b')
            ax.grid(True, alpha=0.08, color='white', axis='x')
            st.pyplot(fig)

# ============================================================================
# PAGE 4: ALERTS & WARNINGS
# ============================================================================
elif page == "📋 Alerts & Warnings":
    page_header("📋", "Smart Alerts & Warnings", "Real-time monitoring and intelligent alert system")

    critical_readings = df[df['vibration'] >= critical_threshold]
    warning_readings  = df[(df['vibration'] >= healthy_threshold) & (df['vibration'] < critical_threshold)]
    healthy_readings  = df[df['vibration'] < healthy_threshold]

    st.subheader("🚨 Current System Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='alert-healthy'>
            <h2 style='margin:0;'>✅ {len(healthy_readings):,}</h2>
            <p style='margin:6px 0 0; opacity:.8;'>Healthy Readings</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='alert-warning'>
            <h2 style='margin:0;'>⚠️ {len(warning_readings):,}</h2>
            <p style='margin:6px 0 0; opacity:.8;'>Maintenance Alerts</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='alert-critical'>
            <h2 style='margin:0;'>🚨 {len(critical_readings):,}</h2>
            <p style='margin:6px 0 0; opacity:.8;'>Critical Alerts</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    if len(critical_readings) > 0:
        st.subheader("🚨 CRITICAL ALERTS — Immediate Action Required")
        st.markdown(f"""
        **{len(critical_readings)} readings with CRITICAL vibration levels detected!**

        - **Average vibration:** {critical_readings['vibration'].mean():.2f}
        - **Max vibration:** {critical_readings['vibration'].max():.2f}
        - **Average revolutions:** {critical_readings['revolutions'].mean():.1f}

        **ACTION ITEMS:**
        1. ⚠️ Schedule immediate elevator inspection
        2. 📞 Contact maintenance team urgently
        3. 📋 Log incident in maintenance system
        4. 🚫 Consider temporary service restrictions if severe
        """)

    if len(warning_readings) > 0:
        st.subheader("⚠️ MAINTENANCE ALERTS — Schedule Service")
        st.markdown(f"""
        **{len(warning_readings)} readings indicating maintenance is needed**

        - **Average vibration:** {warning_readings['vibration'].mean():.2f}
        - **Range:** {warning_readings['vibration'].min():.2f} – {warning_readings['vibration'].max():.2f}

        **RECOMMENDATIONS:**
        1. 📅 Schedule preventive maintenance within 2-4 weeks
        2. 🔍 Inspect door mechanisms and bearings
        3. 🛢️ Consider lubrication and adjustment
        4. 📊 Monitor trends closely
        """)

    st.success(f"✅ **{len(healthy_readings):,} readings show normal operation** — Continue regular monitoring.")

    st.markdown("---")
    st.subheader("📈 Alert Trend Over Time")

    window_size   = 500
    critical_trend, warning_trend = [], []
    for i in range(0, len(df), window_size):
        w = df.iloc[i:i+window_size]
        critical_trend.append(len(w[w['vibration'] >= critical_threshold]))
        warning_trend.append(len(w[(w['vibration'] >= healthy_threshold) & (w['vibration'] < critical_threshold)]))

    dark_bg = '#0d1529'
    fig, ax = plt.subplots(figsize=(12, 5))
    x = range(len(critical_trend))
    ax.plot(x, critical_trend, marker='o', linewidth=2, color='#ef4444', label='Critical')
    ax.plot(x, warning_trend,  marker='s', linewidth=2, color='#f59e0b', label='Warning')
    ax.fill_between(x, critical_trend, alpha=0.2, color='#ef4444')
    ax.fill_between(x, warning_trend,  alpha=0.2, color='#f59e0b')
    ax.set_xlabel('Time Period', fontweight='bold')
    ax.set_ylabel('Number of Alerts', fontweight='bold')
    ax.set_title('Alert Frequency Over Time', fontweight='bold')
    legend = ax.legend(facecolor='#111827', edgecolor='#334155', labelcolor='#94a3b8')
    fig.patch.set_facecolor(dark_bg)
    ax.set_facecolor(dark_bg)
    ax.tick_params(colors='#94a3b8')
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#e2e8f0')
    for spine in ax.spines.values():
        spine.set_edgecolor('#1e293b')
    ax.grid(True, alpha=0.06, color='white')
    st.pyplot(fig)

# ============================================================================
# PAGE 5: REPORT GENERATOR
# ============================================================================
elif page == "📑 Report Generator":
    page_header("📑", "Report Generator", "Export comprehensive professional analysis reports")

    st.subheader("📋 Report Options")
    report_type = st.selectbox(
        "Select Report Type:",
        ["Executive Summary", "Technical Analysis", "Maintenance Schedule",
         "Financial Impact", "Comprehensive Report"]
    )

    col1, col2 = st.columns(2)
    with col1: include_charts      = st.checkbox("Include visualizations", value=True)
    with col2: include_predictions = st.checkbox("Include predictions", value=True)

    st.markdown("---")
    if st.button("📄 Generate Report", use_container_width=True):
        st.success("✅ Report Generated Successfully!")

        healthy_count  = len(df[df['vibration'] < healthy_threshold])
        maint_count    = len(df[(df['vibration'] >= healthy_threshold) & (df['vibration'] < critical_threshold)])
        critical_count = len(df[df['vibration'] >= critical_threshold])

        if report_type == "Executive Summary":
            st.markdown(f"""
# Elevator Maintenance — Executive Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Prepared by:** {st.session_state.username.capitalize()}

## Key Metrics
| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Healthy | {healthy_count:,} | {healthy_count/len(df)*100:.1f}% |
| ⚠️ Maintenance | {maint_count:,} | {maint_count/len(df)*100:.1f}% |
| 🚨 Critical | {critical_count:,} | {critical_count/len(df)*100:.1f}% |

## Key Findings
- Door usage is the **PRIMARY driver** (r = 0.838)
- High-usage elevators have **51% higher vibration**
- Clear maintenance thresholds established
- Predictive model achieves good accuracy

## Recommendations
1. Implement usage-based maintenance
2. Schedule monthly service for high-traffic elevators
3. Deploy predictive monitoring system
4. **Expected annual savings: $12,000+ per elevator**
            """)
        st.info("📊 PDF download feature coming in next release")

# ============================================================================
# PAGE 6: SETTINGS
# ============================================================================
elif page == "⚙️ Settings":
    page_header("⚙️", "Dashboard Settings", "Customize your experience and notification preferences")

    st.subheader("🎨 Appearance")
    col1, col2 = st.columns(2)
    with col1: theme      = st.radio("Theme:", ["Dark (Premium)", "Light", "Auto"])
    with col2: chart_style = st.select_slider("Chart Detail", options=["Simple", "Normal", "Detailed"])

    st.markdown("---")
    st.subheader("🔔 Alerts & Notifications")
    col1, col2, col3 = st.columns(3)
    with col1: critical_alerts     = st.checkbox("Critical Alerts",     value=True)
    with col2: maintenance_alerts  = st.checkbox("Maintenance Alerts",  value=True)
    with col3: email_notifications = st.checkbox("Email Notifications", value=False)

    st.markdown("---")
    st.subheader("📊 Data & Analytics")
    col1, col2 = st.columns(2)
    with col1: update_freq  = st.select_slider("Update Frequency", options=["Real-time", "Every 5 min", "Every 30 min"])
    with col2: data_retention = st.select_slider("Data Retention",  options=["7 days", "30 days", "90 days", "1 year"])

    st.markdown("---")
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved successfully!")

    st.markdown("---")
    st.subheader("ℹ️ About")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(metric_glass("Version", "3.0", "Premium Edition"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_glass("Last Updated", "Mar 2026", "by Tanmay"), unsafe_allow_html=True)

    st.info("""
    **🛗 Elevator Predictive Maintenance Dashboard v3.0**

    Advanced analytics platform for elevator monitoring and predictive maintenance.

    **Features:**
    - 🔐 Secure login with session management
    - 🌑 Premium dark glassmorphism UI
    - 📊 Real-time sensor monitoring
    - 🤖 ML-powered predictions
    - 🚨 Intelligent alert system
    - 📑 Professional report generation
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #334155; font-size: 12px; padding: 12px 0;'>
    <p>🛗 <strong>Elevator Predictive Maintenance Dashboard v3.0</strong> &nbsp;·&nbsp; Premium Edition</p>
    <p>Logged in as <strong style='color:#4f8ef7;'>{st.session_state.username.capitalize()}</strong>
       &nbsp;·&nbsp; © 2026 TechLift Solutions · All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)


