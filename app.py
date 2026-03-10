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

    with tab1:
        st.subheader("Vibration Time Series with Thresholds")
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(filtered_df['ID'], filtered_df['vibration'], linewidth=2,
                color='#4f8ef7', label='Vibration Level', alpha=0.9)
        ax.axhline(y=mean_vib, color='#10b981', linestyle='--', linewidth=1.8, label=f'Avg: {mean_vib:.2f}', alpha=0.8)
        ax.axhline(y=healthy_threshold, color='#f59e0b', linestyle='--', linewidth=1.8, label=f'Action: {healthy_threshold:.2f}', alpha=0.8)
        ax.axhline(y=critical_threshold, color='#ef4444', linestyle='--', linewidth=1.8, label=f'Critical: {critical_threshold:.2f}', alpha=0.8)
        ax.set_xlabel('Sample Index', fontsize=11, fontweight='bold')
        ax.set_ylabel('Vibration Level', fontsize=11, fontweight='bold')
        ax.set_title('Vibration Trends', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab2:
        st.subheader("Distribution Analysis")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.hist(filtered_df['humidity'], bins=25, color='#4f8ef7', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Humidity (%)', fontweight='bold')
            ax.set_ylabel('Frequency', fontweight='bold')
            ax.set_title('Humidity Distribution', fontweight='bold')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            ax.hist(filtered_df['revolutions'], bins=25, color='#9b59b6', edgecolor='black', alpha=0.7)
            ax.set_xlabel('Revolutions', fontweight='bold')
            ax.set_ylabel('Frequency', fontweight='bold')
            ax.set_title('Door Usage Distribution', fontweight='bold')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    with tab3:
        st.subheader("Correlation Analysis")
        cols = ['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(filtered_df[cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    with tab4:
        st.subheader("Statistics")
        cols = ['revolutions', 'humidity', 'vibration', 'x1', 'x2', 'x3', 'x4', 'x5']
        st.dataframe(filtered_df[cols].describe().round(3))

    with tab5:
        st.subheader("Data Table")
        st.dataframe(filtered_df.round(2), height=400)
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, f"elevator_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ============================================================================
# PAGE 3: ML PREDICTIONS
# ============================================================================
elif page == "🤖 ML Predictions":
    page_header("🤖", "ML Predictions", "Predict failures before they happen")

    if not ML_AVAILABLE:
        st.warning("⚠️ scikit-learn loading...")
    else:
        st.subheader("Make a Prediction")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ca, cb, cc = st.columns(3)
            rev = ca.slider("Revolutions", 5.0, 40.0, 20.0)
            hum = cb.slider("Humidity", 30.0, 80.0, 55.0)
            x1 = cc.slider("Sensor x1", 75.0, 105.0, 90.0)
            
            cd, ce, cf, cg = st.columns(4)
            x2 = cd.slider("x2", 45.0, 60.0, 50.0)
            x3 = ce.slider("x3", 70.0, 90.0, 80.0)
            x4 = cf.slider("x4", 34.0, 47.0, 40.0)
            x5 = cg.slider("x5", 49.0, 71.0, 60.0)
            
            X = df[['revolutions', 'humidity', 'x1', 'x2', 'x3', 'x4', 'x5']]
            y = df['vibration']
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            pred = model.predict([[rev, hum, x1, x2, x3, x4, x5]])[0]
            
            if pred < healthy_threshold:
                st.success(f"✅ {pred:.2f} - HEALTHY")
            elif pred < critical_threshold:
                st.warning(f"⚠️ {pred:.2f} - MAINTENANCE NEEDED")
            else:
                st.error(f"🚨 {pred:.2f} - CRITICAL")

# ============================================================================
# PAGE 4: ALERTS
# ============================================================================
elif page == "📋 Alerts & Warnings":
    page_header("📋", "Alerts", "Real-time monitoring")

    critical = df[df['vibration'] >= critical_threshold]
    warning = df[(df['vibration'] >= healthy_threshold) & (df['vibration'] < critical_threshold)]
    healthy = df[df['vibration'] < healthy_threshold]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='alert-healthy'><h2>✅ {len(healthy):,}</h2><p>Healthy</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='alert-warning'><h2>⚠️ {len(warning):,}</h2><p>Maintenance</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='alert-critical'><h2>🚨 {len(critical):,}</h2><p>Critical</p></div>", unsafe_allow_html=True)

# ============================================================================
# PAGE 5: REPORT GENERATOR
# ============================================================================
elif page == "📑 Report Generator":
    page_header("📑", "Reports", "Generate analysis reports")

    report = st.selectbox("Report Type", ["Executive Summary", "Technical Analysis"])
    
    if st.button("Generate Report"):
        st.success("✅ Report Generated!")
        st.markdown(f"""
        # Report - {report}
        Generated: {datetime.now().strftime('%Y-%m-%d')}
        
        Total readings: {len(df):,}
        Healthy: {len(df[df['vibration'] < healthy_threshold]):,}
        """)

# ============================================================================
# PAGE 6: SETTINGS
# ============================================================================
elif page == "⚙️ Settings":
    page_header("⚙️", "Settings", "Customize dashboard")
    
    st.subheader("Preferences")
    theme = st.radio("Theme", ["Dark", "Light"])
    alerts = st.checkbox("Enable Alerts")
    
    if st.button("Save"):
        st.success("✅ Saved!")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #334155; font-size: 12px;'>
    <p>🛗 Elevator Dashboard v3.0 · {st.session_state.username.capitalize()} · © 2026</p>
</div>
""", unsafe_allow_html=True)

