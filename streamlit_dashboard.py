#!/usr/bin/env python3
"""
Rajasthan Royals War-Room Interactive Dashboard (SupeRR Selector Season 2 — Round 1 V5)
Author: Adhwaith K P / RR Sports Data Science Team
Features:
  - Dark Midnight & Neon Royals Pink War-Room Theme (#0A0E1A, #131D31, #254AA5, #EA1A85)
  - 3-Way Target Pool Routing:
      1. Option A: IPL-Proven Released Pool (V5 Official — Recommended)
      2. Option B: Global T20I Extended Pool (Scouting Gems & Free Agents)
      3. List A: All-Player Benchmark Pool (Includes Retained Stars)
  - Dedicated IPL 2027 Auction War-Room Tab with 10-Franchise Financial Matrix & RR ₹27.05 Cr Shopping Plan
  - Real-time Exponential Recency Weighting Engine with dynamic multi-season interpolation
  - Interactive Plotly dark quadrant scatter plots, Scout Spotlights, and Head-to-Head comparators
  - Full mathematical architecture documentation with LaTeX formulas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="RR War-Room | SupeRR Selector Season 2",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Rajasthan Royals Midnight War-Room Theme (#0A0E1A, #131D31, #254AA5, #EA1A85, #38BDF8)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background adjustments */
    .stApp {
        background-color: #0A0E1A;
        color: #F8FAFC;
    }
    
    /* Executive Main Header */
    .main-header {
        background: linear-gradient(135deg, #071026 0%, #152A68 50%, #831843 100%);
        border: 1px solid rgba(234, 26, 133, 0.35);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(234, 26, 133, 0.15);
        padding: 2.2rem 2.6rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    /* Sleek Dark Metric Cards */
    .metric-card {
        background: #111C30;
        border: 1px solid #1E2E4A;
        border-top: 4px solid #EA1A85;
        border-radius: 12px;
        padding: 1.3rem;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(234, 26, 133, 0.25);
    }
    .metric-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0.3rem 0;
        letter-spacing: -0.5px;
    }
    .metric-sub {
        font-size: 0.86rem;
        color: #38BDF8;
        font-weight: 600;
    }
    
    /* Section Banner */
    .section-banner {
        background: #111C30;
        border-left: 5px solid #EA1A85;
        border-top: 1px solid #1E2E4A;
        border-right: 1px solid #1E2E4A;
        border-bottom: 1px solid #1E2E4A;
        border-radius: 0 12px 12px 0;
        padding: 1.1rem 1.5rem;
        margin: 1.2rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    
    /* Recency Badge */
    .recency-badge {
        display: inline-block;
        background: linear-gradient(135deg, #254AA5 0%, #EA1A85 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 10px rgba(234, 26, 133, 0.3);
    }
    
    /* Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #131E33;
        border-radius: 8px;
        padding: 10px 20px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid #1E2E4A;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #254AA5 0%, #EA1A85 100%) !important;
        color: #FFFFFF !important;
        border-color: #EA1A85 !important;
        box-shadow: 0 2px 12px rgba(234, 26, 133, 0.35);
    }
    
    /* Scout Spotlight Cards */
    .scout-card {
        background: #111C30;
        border: 1px solid #1E2E4A;
        border-left: 5px solid #38BDF8;
        border-radius: 12px;
        padding: 1.3rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
    }
    
    /* War-room plan card */
    .plan-card {
        background: #111C30;
        border: 1px solid #1E2E4A;
        border-top: 4px solid #254AA5;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main Title & Subtitle Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <div style="display: inline-block; background: rgba(255,255,255,0.15); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.6rem; border: 1px solid rgba(255,255,255,0.2);">
                Official Hackathon Round 1 Submission System • V5 Official
            </div>
            <h1 style="margin:0; font-size: 2.35rem; font-weight: 800; letter-spacing: -0.5px;">
                👑 RAJASTHAN ROYALS WAR-ROOM
            </h1>
            <h3 style="margin:0.3rem 0 0 0; font-size: 1.15rem; font-weight: 500; color: #F1F5F9; opacity: 0.95;">
                Context-Aware Pressure & Exponential Recency Engine (V5) • Official 10-Team IPL 2027 Roster Integration
            </h3>
            <p style="margin:0.7rem 0 0 0; font-size: 0.88rem; color: #CBD5E1; opacity: 0.9; max-width: 980px; line-height: 1.5;">
                Synthesizing 200,999 deliveries across 883 matches. Integrates official IPL 2027 retention/trade lists (184 locked players excluded), Rajasthan Royals' ₹27.05 Cr purse with 6 open slots (3 overseas), 6 contextual leverage multipliers, and exponential recency time-decay.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA LOADERS & CACHING (Option A, Option B, List A Benchmark)
# ==============================================================================
@st.cache_data
def load_all_datasets():
    # Helper to resolve file paths across root and /new
    def get_path(f):
        if os.path.exists(f):
            return f
        if os.path.exists(os.path.join('new', f)):
            return os.path.join('new', f)
        return f

    bat_opt_a = pd.read_csv(get_path('v5_official_released_ipl_batters.csv'))
    bowl_opt_a = pd.read_csv(get_path('v5_official_released_ipl_bowlers.csv'))
    bat_opt_b = pd.read_csv(get_path('v5_all_available_auction_batters.csv'))
    bowl_opt_b = pd.read_csv(get_path('v5_all_available_auction_bowlers.csv'))
    bat_list_a = pd.read_csv(get_path('v4_recency_top_batters.csv'))
    bowl_list_a = pd.read_csv(get_path('v4_recency_top_bowlers.csv'))
    bat_yearly = pd.read_csv(get_path('bat_yearly_pressure.csv'))
    bowl_yearly = pd.read_csv(get_path('bowl_yearly_pressure.csv'))

    # Standardize auction status column across all datasets
    for df in [bat_opt_a, bat_opt_b, bat_list_a]:
        if 'official_2027_status' in df.columns:
            df['auction_status'] = df['official_2027_status']
        elif 'ipl_2026_team' in df.columns:
            df['auction_status'] = df['ipl_2026_team']
        else:
            df['auction_status'] = "Free Agent / Pool"

    for df in [bowl_opt_a, bowl_opt_b, bowl_list_a]:
        if 'official_2027_status' in df.columns:
            df['auction_status'] = df['official_2027_status']
        elif 'ipl_2026_team' in df.columns:
            df['auction_status'] = df['ipl_2026_team']
        else:
            df['auction_status'] = "Free Agent / Pool"

    return bat_opt_a, bowl_opt_a, bat_opt_b, bowl_opt_b, bat_list_a, bowl_list_a, bat_yearly, bowl_yearly

try:
    bat_a_pool, bowl_a_pool, bat_b_pool, bowl_b_pool, bat_bench, bowl_bench, bat_yr_df, bowl_yr_df = load_all_datasets()
except Exception as e:
    st.error(f"Error loading CSV files: {e}. Please ensure superr_selector_v5_official_retentions_pipeline.py has run.")
    st.stop()

# ==============================================================================
# SESSION STATE INITIALIZATION & PRESET CALLBACKS
# ==============================================================================
DEFAULT_ROSTER_MODE = "Option A: IPL-Proven Released Pool (V5 Official — Recommended)"
DEFAULT_MIN_P_BALLS = 70
DEFAULT_MIN_REC_BALLS = 30
DEFAULT_RECENCY_MULT = 1.00
DEFAULT_W_SR_ECON = 0.25
DEFAULT_W_AVG_SR = 0.20
DEFAULT_W_REC = 0.15
DEFAULT_W_BND = 0.15
DEFAULT_W_DOT = 0.10
DEFAULT_W_LIFT = 0.10

if 'roster_mode' not in st.session_state:
    st.session_state['roster_mode'] = DEFAULT_ROSTER_MODE
if 'min_p_balls' not in st.session_state:
    st.session_state['min_p_balls'] = DEFAULT_MIN_P_BALLS
if 'min_rec_balls' not in st.session_state:
    st.session_state['min_rec_balls'] = DEFAULT_MIN_REC_BALLS
if 'recency_mult' not in st.session_state:
    st.session_state['recency_mult'] = DEFAULT_RECENCY_MULT
if 'w_sr_econ' not in st.session_state:
    st.session_state['w_sr_econ'] = DEFAULT_W_SR_ECON
if 'w_avg_sr' not in st.session_state:
    st.session_state['w_avg_sr'] = DEFAULT_W_AVG_SR
if 'w_rec' not in st.session_state:
    st.session_state['w_rec'] = DEFAULT_W_REC
if 'w_bnd' not in st.session_state:
    st.session_state['w_bnd'] = DEFAULT_W_BND
if 'w_dot' not in st.session_state:
    st.session_state['w_dot'] = DEFAULT_W_DOT
if 'w_lift' not in st.session_state:
    st.session_state['w_lift'] = DEFAULT_W_LIFT

def reset_to_opt_a():
    st.session_state['roster_mode'] = "Option A: IPL-Proven Released Pool (V5 Official — Recommended)"
    st.session_state['min_p_balls'] = 70
    st.session_state['min_rec_balls'] = 30
    st.session_state['recency_mult'] = 1.00
    st.session_state['w_sr_econ'] = 0.25
    st.session_state['w_avg_sr'] = 0.20
    st.session_state['w_rec'] = 0.15
    st.session_state['w_bnd'] = 0.15
    st.session_state['w_dot'] = 0.10
    st.session_state['w_lift'] = 0.10

def reset_to_opt_b():
    st.session_state['roster_mode'] = "Option B: Global T20I Extended Pool (Scouting Gems & Free Agents)"
    st.session_state['min_p_balls'] = 80
    st.session_state['min_rec_balls'] = 40
    st.session_state['recency_mult'] = 1.00
    st.session_state['w_sr_econ'] = 0.25
    st.session_state['w_avg_sr'] = 0.20
    st.session_state['w_rec'] = 0.15
    st.session_state['w_bnd'] = 0.15
    st.session_state['w_dot'] = 0.10
    st.session_state['w_lift'] = 0.10

def reset_to_list_a():
    st.session_state['roster_mode'] = "List A: All-Player Benchmark Pool (Includes Retained Stars)"
    st.session_state['min_p_balls'] = 120
    st.session_state['min_rec_balls'] = 50
    st.session_state['recency_mult'] = 1.00
    st.session_state['w_sr_econ'] = 0.25
    st.session_state['w_avg_sr'] = 0.20
    st.session_state['w_rec'] = 0.15
    st.session_state['w_bnd'] = 0.15
    st.session_state['w_dot'] = 0.10
    st.session_state['w_lift'] = 0.10

# ==============================================================================
# SIDEBAR CONTROLS & BENCHMARK RESET BUTTONS
# ==============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/300px-Rajasthan_Royals_Logo.svg.png", width=120)
st.sidebar.markdown("## ⚙️ War-Room Controls")

# Benchmark Calibration Reset Section
st.sidebar.markdown("### 🔄 Preset Calibration Resets")
st.sidebar.caption("Click to instantly snap all sliders and meters to the exact calibration values:")

st.sidebar.button(
    "👑 Reset to Option A (IPL-Proven Targets)",
    on_click=reset_to_opt_a,
    help="Snaps to calibrated Option A: IPL-Proven Released Veterans (Travis Head, Karun Nair, Mustafizur, Wanindu, etc.)",
    use_container_width=True,
    type="primary"
)

st.sidebar.button(
    "🌐 Reset to Option B (Global Pool)",
    on_click=reset_to_opt_b,
    help="Snaps to Option B: Global Free Agents & Associates included.",
    use_container_width=True
)

st.sidebar.button(
    "🏆 Reset to List A Benchmark",
    on_click=reset_to_list_a,
    help="Resets meters to evaluate the full benchmark including 184 retained franchise stars (Kohli, Bumrah, Narine).",
    use_container_width=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 1. Select Target Pool")
roster_mode = st.sidebar.radio(
    "Evaluation Target Pool:",
    options=[
        "Option A: IPL-Proven Released Pool (V5 Official — Recommended)",
        "Option B: Global T20I Extended Pool (Scouting Gems & Free Agents)",
        "List A: All-Player Benchmark Pool (Includes Retained Stars)"
    ],
    key='roster_mode',
    help="Option A is strictly IPL-proven released players. Option B includes uncapped/Associate gems. List A evaluates all active players."
)

# Pool routing
if "Option A" in roster_mode:
    curr_bat_meta = bat_a_pool.copy()
    curr_bowl_meta = bowl_a_pool.copy()
    pool_badge = "Officially Released IPL Veterans & Capped Free Agents (184 Retained Stars Excluded)"
    pool_title = "Option A: IPL-Proven Released Pool (V5 Official)"
elif "Option B" in roster_mode:
    curr_bat_meta = bat_b_pool.copy()
    curr_bowl_meta = bowl_b_pool.copy()
    pool_badge = "Global T20I Pool (Includes Uncapped / Associate Gems, 184 Retained Stars Excluded)"
    pool_title = "Option B: Global T20I Extended Pool"
else:
    curr_bat_meta = bat_bench.copy()
    curr_bowl_meta = bowl_bench.copy()
    pool_badge = "Unrestricted All-Player Benchmark (Evaluates Retained Franchise Cores like Bumrah, Kohli & Narine)"
    pool_title = "List A: All-Player Overall Benchmark"

st.sidebar.markdown("---")
st.sidebar.markdown("### 2. Sample Size Thresholds")
min_p_balls = st.sidebar.slider(
    "Min Career Pressure Balls",
    min_value=30, max_value=250,
    step=10,
    key='min_p_balls',
    help="Minimum deliveries faced or bowled under base pressure situations (P_base = 1)."
)
min_rec_balls = st.sidebar.slider(
    "Min 2025–2026 Pressure Balls",
    min_value=15, max_value=120,
    step=5,
    key='min_rec_balls',
    help="Minimum deliveries in recent high-recency seasons (2025–2026) to prevent small-sample distortion."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 3. ⏳ Exponential Recency Weighting Multiplier")
recency_mult = st.sidebar.slider(
    "Exponential Recency Scale (M_recency)",
    min_value=0.00, max_value=2.00,
    step=0.05,
    key='recency_mult',
    help="Scales exponential recency decay across seasons 2022-2026. At 1.00x: 2026 = 1.50x, 2025 = 1.25x, 2024 = 0.90x, 2023 = 0.65x, 2022 = 0.45x. At 0.00x: Flat weighting."
)

# Compute dynamic yearly weights
base_recency_map = {2026: 1.50, 2025: 1.25, 2024: 0.90, 2023: 0.65, 2022: 0.45}
active_recency_map = {
    y: max(0.05, round(1.0 + recency_mult * (base_recency_map[y] - 1.0), 3))
    for y in base_recency_map
}

# Mini-visualizer in sidebar showing active multipliers
st.sidebar.caption(f"**Active Season Multipliers (Recency Scale: {recency_mult:.2f}×):**")
rec_cols = st.sidebar.columns(5)
rec_cols[0].metric("2022", f"{active_recency_map[2022]:.2f}×")
rec_cols[1].metric("2023", f"{active_recency_map[2023]:.2f}×")
rec_cols[2].metric("2024", f"{active_recency_map[2024]:.2f}×")
rec_cols[3].metric("2025", f"{active_recency_map[2025]:.2f}×")
rec_cols[4].metric("2026", f"{active_recency_map[2026]:.2f}×")

ratio_26_22 = active_recency_map[2026] / active_recency_map[2022] if active_recency_map[2022] > 0 else 99.0
st.sidebar.caption(f"⚡ **Recency Advantage Ratio (2026 vs 2022):** **{ratio_26_22:.2f}×**")

st.sidebar.markdown("---")
st.sidebar.markdown("### 4. Dynamic Z-Score Model Weights")
st.sidebar.caption("Adjust component weights to simulate custom franchise war-room preferences:")
w_sr_econ = st.sidebar.slider("Career Pressure SR / Economy", 0.10, 0.40, step=0.05, key='w_sr_econ')
w_avg_sr = st.sidebar.slider("Career Pressure Avg / Bowling SR", 0.10, 0.40, step=0.05, key='w_avg_sr')
w_rec = st.sidebar.slider("2025–26 Recency SR / Economy", 0.05, 0.30, step=0.05, key='w_rec')
w_bnd = st.sidebar.slider("Boundary % Impact", 0.05, 0.25, step=0.05, key='w_bnd')
w_dot = st.sidebar.slider("Dot Ball % Control", 0.05, 0.25, step=0.05, key='w_dot')
w_lift = st.sidebar.slider("Clutch Elevation (Δ SR / Δ Econ)", 0.05, 0.25, step=0.05, key='w_lift')

# ==============================================================================
# REAL-TIME DYNAMIC RECENCY ENGINE & METRIC RECALCULATION
# ==============================================================================
# 1. Batters dynamic calculation
bat_yr = bat_yr_df.copy()
bat_yr['m_dyn'] = bat_yr['year'].map(active_recency_map).fillna(1.0)
bat_yr['w_balls'] = bat_yr['wc_balls'] * bat_yr['m_dyn']
bat_yr['w_runs'] = bat_yr['wc_runs'] * bat_yr['m_dyn']
bat_yr['w_outs'] = bat_yr['wc_outs'] * bat_yr['m_dyn']
bat_yr['w_bnd'] = bat_yr['wc_bnd'] * bat_yr['m_dyn']
bat_yr['w_dot'] = bat_yr['wc_dot'] * bat_yr['m_dyn']

bat_dyn_agg = bat_yr.groupby('striker_id').agg(
    w_balls=('w_balls', 'sum'),
    w_runs=('w_runs', 'sum'),
    w_outs=('w_outs', 'sum'),
    w_bnd=('w_bnd', 'sum'),
    w_dot=('w_dot', 'sum')
).reset_index()

bat_dyn_agg['wp_sr'] = (bat_dyn_agg['w_runs'] / np.maximum(bat_dyn_agg['w_balls'], 1) * 100).round(1)
bat_dyn_agg['wp_avg'] = (bat_dyn_agg['w_runs'] / np.maximum(bat_dyn_agg['w_outs'], 1)).round(1)
bat_dyn_agg['wp_bnd_pct'] = (bat_dyn_agg['w_bnd'] / np.maximum(bat_dyn_agg['w_balls'], 1) * 100).round(1)
bat_dyn_agg['wp_dot_pct'] = (bat_dyn_agg['w_dot'] / np.maximum(bat_dyn_agg['w_balls'], 1) * 100).round(1)

# Merge with active pool metadata
bat_strip_cols = ['wp_sr', 'wp_avg', 'wp_bnd_pct', 'wp_dot_pct', 'sr_lift', 'bpi_auction', 'bpi_v4', 'bpi_v5']
bat_base_cols = [c for c in curr_bat_meta.columns if c not in bat_strip_cols]
bat_active = curr_bat_meta[bat_base_cols].drop_duplicates('striker_id').merge(bat_dyn_agg, on='striker_id', how='inner')
bat_active['sr_lift'] = (bat_active['wp_sr'] - bat_active['base_sr']).round(1)

# 2. Bowlers dynamic calculation
bowl_yr = bowl_yr_df.copy()
bowl_yr['m_dyn'] = bowl_yr['year'].map(active_recency_map).fillna(1.0)
bowl_yr['w_balls'] = bowl_yr['wc_balls'] * bowl_yr['m_dyn']
bowl_yr['w_runs'] = bowl_yr['wc_runs'] * bowl_yr['m_dyn']
bowl_yr['w_wkts'] = bowl_yr['wc_wkts'] * bowl_yr['m_dyn']
bowl_yr['w_dot'] = bowl_yr['wc_dot'] * bowl_yr['m_dyn']
bowl_yr['w_bnd'] = bowl_yr['wc_bnd'] * bowl_yr['m_dyn']

bowl_dyn_agg = bowl_yr.groupby('bowler_id').agg(
    w_balls=('w_balls', 'sum'),
    w_runs=('w_runs', 'sum'),
    w_wkts=('w_wkts', 'sum'),
    w_dot=('w_dot', 'sum'),
    w_bnd=('w_bnd', 'sum')
).reset_index()

bowl_dyn_agg['wp_econ'] = (bowl_dyn_agg['w_runs'] / np.maximum(bowl_dyn_agg['w_balls'], 1) * 6.0).round(2)
bowl_dyn_agg['wp_sr'] = (bowl_dyn_agg['w_balls'] / np.maximum(bowl_dyn_agg['w_wkts'], 1)).round(1)
bowl_dyn_agg['wp_dot_pct'] = (bowl_dyn_agg['w_dot'] / np.maximum(bowl_dyn_agg['w_balls'], 1) * 100).round(1)
bowl_dyn_agg['wp_bnd_pct'] = (bowl_dyn_agg['w_bnd'] / np.maximum(bowl_dyn_agg['w_balls'], 1) * 100).round(1)

bowl_strip_cols = ['wp_econ', 'wp_sr', 'wp_dot_pct', 'wp_bnd_pct', 'econ_drop', 'bopi_auction', 'bopi_v4', 'bopi_v5']
bowl_base_cols = [c for c in curr_bowl_meta.columns if c not in bowl_strip_cols]
bowl_active = curr_bowl_meta[bowl_base_cols].drop_duplicates('bowler_id').merge(bowl_dyn_agg, on='bowler_id', how='inner')
bowl_active['econ_drop'] = (bowl_active['wp_econ'] - bowl_active['base_econ']).round(2)

# Apply sample size filters
bat_filt = bat_active[
    (bat_active['p_balls'] >= min_p_balls) &
    (bat_active['rec_p_balls'] >= min_rec_balls)
].copy()

bowl_filt = bowl_active[
    (bowl_active['p_balls'] >= min_p_balls) &
    (bowl_active['rec_p_balls'] >= min_rec_balls)
].copy()

# Dynamic BPI computation
if not bat_filt.empty:
    for col in ['wp_sr', 'wp_avg', 'wp_bnd_pct', 'wp_dot_pct', 'sr_lift', 'rec_p_sr', 'avg_pressure_intensity']:
        std = bat_filt[col].std()
        bat_filt[col + '_dyn_z'] = (bat_filt[col] - bat_filt[col].mean()) / (std if std != 0 and pd.notna(std) else 1)
    
    bat_filt['dynamic_bpi'] = (
        w_sr_econ * bat_filt['wp_sr_dyn_z'] +
        w_avg_sr * bat_filt['wp_avg_dyn_z'] +
        w_rec * bat_filt['rec_p_sr_dyn_z'] +
        w_bnd * bat_filt['wp_bnd_pct_dyn_z'] -
        w_dot * bat_filt['wp_dot_pct_dyn_z'] +
        w_lift * bat_filt['sr_lift_dyn_z'] +
        0.05 * bat_filt['avg_pressure_intensity_dyn_z']
    ).round(3)
    bat_filt = bat_filt.sort_values('dynamic_bpi', ascending=False).reset_index(drop=True)

# Dynamic BoPI computation
if not bowl_filt.empty:
    for col in ['wp_econ', 'wp_sr', 'wp_dot_pct', 'wp_bnd_pct', 'econ_drop', 'rec_p_econ', 'avg_pressure_intensity']:
        std = bowl_filt[col].std()
        bowl_filt[col + '_dyn_z'] = (bowl_filt[col] - bowl_filt[col].mean()) / (std if std != 0 and pd.notna(std) else 1)
    
    # In official methodology: For bowlers, Dot Ball Chokehold is primary (+0.15) and Boundary Suppression is (-0.10)
    # (Batters have Boundary +0.15 and Dot -0.10). Ensure bowler weights respect official pipeline calibration:
    bowl_w_dot = w_bnd if w_bnd == DEFAULT_W_BND and w_dot == DEFAULT_W_DOT else w_dot
    bowl_w_bnd = w_dot if w_bnd == DEFAULT_W_BND and w_dot == DEFAULT_W_DOT else w_bnd

    bowl_filt['dynamic_bopi'] = (
        -w_sr_econ * bowl_filt['wp_econ_dyn_z'] -
        w_avg_sr * bowl_filt['wp_sr_dyn_z'] -
        w_rec * bowl_filt['rec_p_econ_dyn_z'] +
        bowl_w_dot * bowl_filt['wp_dot_pct_dyn_z'] -
        bowl_w_bnd * bowl_filt['wp_bnd_pct_dyn_z'] -
        w_lift * bowl_filt['econ_drop_dyn_z'] +
        0.05 * bowl_filt['avg_pressure_intensity_dyn_z']
    ).round(3)
    bowl_filt = bowl_filt.sort_values('dynamic_bopi', ascending=False).reset_index(drop=True)

# ==============================================================================
# MAIN PAGE EXECUTIVE SCOPE & KPI OVERVIEW CARDS
# ==============================================================================
st.markdown(f"""
<div class="section-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <strong style="color: #38BDF8; font-size: 1.05rem;">Active Target Pool:</strong> 
            <span style="font-weight:700; color: #F8FAFC;">{pool_title}</span><br/>
            <span style="font-size: 0.88rem; color: #94A3B8;">
                <strong>Filter Scope:</strong> {pool_badge} &bull; 
                <strong>Qualified Candidates:</strong> <span style="color:#38BDF8;font-weight:700;">{len(bat_filt)} Batters</span> &bull; <span style="color:#EA1A85;font-weight:700;">{len(bowl_filt)} Bowlers</span> | 
                <strong>Thresholds:</strong> Career P-Balls &ge; {min_p_balls}, 2025–26 P-Balls &ge; {min_rec_balls}
            </span>
        </div>
        <div style="text-align:right;">
            <span class="recency-badge">⏳ Recency Decay: {recency_mult:.2f}× Active ({active_recency_map[2026]:.2f}× in 2026 vs {active_recency_map[2022]:.2f}× in 2022)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4 Key War-Room Metrics
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1:
    top_bat_name = bat_filt.iloc[0]['striker_name'] if not bat_filt.empty else "N/A"
    top_bat_score = bat_filt.iloc[0]['dynamic_bpi'] if not bat_filt.empty else 0.0
    top_bat_team = bat_filt.iloc[0]['auction_status'] if not bat_filt.empty else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🏏 Top Clutch Batter</div>
        <div class="metric-value">{top_bat_name}</div>
        <div class="metric-sub">BPI: +{top_bat_score:.3f} • {top_bat_team}</div>
    </div>
    """, unsafe_allow_html=True)

with col_k2:
    top_bowl_name = bowl_filt.iloc[0]['bowler_name'] if not bowl_filt.empty else "N/A"
    top_bowl_score = bowl_filt.iloc[0]['dynamic_bopi'] if not bowl_filt.empty else 0.0
    top_bowl_team = bowl_filt.iloc[0]['auction_status'] if not bowl_filt.empty else ""
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #38BDF8;">
        <div class="metric-title">🎯 Top Clutch Bowler</div>
        <div class="metric-value">{top_bowl_name}</div>
        <div class="metric-sub" style="color:#EA1A85;">BoPI: +{top_bowl_score:.3f} • {top_bowl_team}</div>
    </div>
    """, unsafe_allow_html=True)

with col_k3:
    avg_rec_sr = bat_filt['rec_p_sr'].mean() if not bat_filt.empty else 0.0
    avg_base_sr = bat_filt['base_sr'].mean() if not bat_filt.empty else 0.0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">⚡ Pool 2025–26 P-Strike Rate</div>
        <div class="metric-value">{avg_rec_sr:.1f}</div>
        <div class="metric-sub">Baseline Par: {avg_base_sr:.1f} (Lift: +{avg_rec_sr - avg_base_sr:.1f})</div>
    </div>
    """, unsafe_allow_html=True)

with col_k4:
    avg_rec_econ = bowl_filt['rec_p_econ'].mean() if not bowl_filt.empty else 0.0
    avg_base_econ = bowl_filt['base_econ'].mean() if not bowl_filt.empty else 0.0
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: #38BDF8;">
        <div class="metric-title">🛡️ Pool 2025–26 P-Economy</div>
        <div class="metric-value">{avg_rec_econ:.2f} <span style="font-size:0.95rem;font-weight:600;color:#94A3B8;">RPO</span></div>
        <div class="metric-sub" style="color:#EA1A85;">Baseline Par: {avg_base_econ:.2f} RPO (Δ {avg_rec_econ - avg_base_econ:+.2f})</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ==============================================================================
# TAB NAVIGATION
# ==============================================================================
tab_warroom, tab_bat, tab_bowl, tab_recency, tab_charts, tab_compare, tab_math = st.tabs([
    "💰 IPL 2027 Auction War-Room",
    "🏏 Batters Leaderboard (Top 10)",
    "🎯 Bowlers Leaderboard (Top 10)",
    "⏳ Exponential Recency Engine",
    "📊 Publication Quadrants",
    "🔍 Head-to-Head Comparison",
    "📐 Mathematical Architecture"
])

# ------------------------------------------------------------------------------
# TAB 1: IPL 2027 AUCTION WAR-ROOM & RR SHOPPING PLAN
# ------------------------------------------------------------------------------
with tab_warroom:
    st.markdown("### 💰 Rajasthan Royals IPL 2027 Auction War-Room Strategy")
    st.markdown("""
    **Official 10-Team Context:** Following official franchise retentions, trades, and releases, Rajasthan Royals enters the IPL 2027 Mega-Auction with **₹27.05 Crore** remaining purse and **6 Open Slots (3 Overseas, 3 Indian)**.
    """)

    col_rr1, col_rr2, col_rr3, col_rr4 = st.columns(4)
    col_rr1.metric("RR Remaining Purse", "₹27.05 Cr", "Mid-Table Flexibility")
    col_rr2.metric("RR Open Slots", "6 Slots", "3 Overseas • 3 Indian")
    col_rr3.metric("RR Traded In", "Shami & Siddharth", "From Lucknow Super Giants")
    col_rr4.metric("RR Key Released", "Hetmyer, Deshpande, Milne", "Burger, Maphaka, Sen")

    st.markdown("---")
    st.markdown("#### 📋 Official 10-Franchise Financials, Purses & Open Slots Matrix")

    franchise_data = pd.DataFrame([
        {"Franchise": "Lucknow Super Giants (LSG)", "Remaining Purse (₹ Cr)": 47.45, "Retained": 18, "Open Slots": 7, "OS Slots": 3, "Confirmed Retained Core": "Pooran, Kuldeep Yadav, Marsh, Markram, Curran, Mayank Yadav, Bishnoi", "Notable Released": "Mohammed Shami (Traded to RR), M. Siddharth (Traded to RR)"},
        {"Franchise": "Kolkata Knight Riders (KKR)", "Remaining Purse (₹ Cr)": 41.65, "Retained": 17, "Open Slots": 8, "OS Slots": 3, "Confirmed Retained Core": "Cameron Green, Narine, Rinku Singh, Chakravarthy, Harshit Rana, Finn Allen", "Notable Released": "Mustafizur Rahman, Pathirana, Rahane, Akash Deep, Starc"},
        {"Franchise": "Sunrisers Hyderabad (SRH)", "Remaining Purse (₹ Cr)": 40.15, "Retained": 18, "Open Slots": 7, "OS Slots": 3, "Confirmed Retained Core": "Pat Cummins, Abhishek Sharma, Klaasen, Ishan Kishan, Nitish Reddy", "Notable Released": "Travis Head, Gerald Coetzee, Kamindu Mendis, Jaydev Unadkat"},
        {"Franchise": "Delhi Capitals (DC)", "Remaining Purse (₹ Cr)": 39.50, "Retained": 16, "Open Slots": 9, "OS Slots": 4, "Confirmed Retained Core": "Rishabh Pant, Axar Patel, KL Rahul, Tristan Stubbs, Jake Fraser-McGurk", "Notable Released": "Pathum Nissanka, Karun Nair, Mitchell Starc, Nitish Rana"},
        {"Franchise": "Mumbai Indians (MI)", "Remaining Purse (₹ Cr)": 32.60, "Retained": 16, "Open Slots": 9, "OS Slots": 2, "Confirmed Retained Core": "Rohit, Surya, Bumrah, Tilak Varma, Arshdeep Singh, De Kock, Rickelton, Santner", "Notable Released": "Trent Boult, Deepak Chahar, Allah Ghazanfar, Keshav Maharaj"},
        {"Franchise": "Chennai Super Kings (CSK)", "Remaining Purse (₹ Cr)": 28.05, "Retained": 19, "Open Slots": 6, "OS Slots": 2, "Confirmed Retained Core": "Ruturaj Gaikwad (c), Sanju Samson, Noor Ahmad, Dube, Livingstone, Conway", "Notable Released": "MS Dhoni (Mentor), Matt Henry, Spencer Johnson, Akash Madhwal"},
        {"Franchise": "Rajasthan Royals (RR)", "Remaining Purse (₹ Cr)": 27.05, "Retained": 19, "Open Slots": 6, "OS Slots": 3, "Confirmed Retained Core": "Riyan Parag (c), Yashasvi Jaiswal, Dhruv Jurel, Sooryavanshi, Archer, Shami, Jadeja", "Notable Released": "Hetmyer, Deshpande, Milne, Burger, Maphaka, Kuldeep Sen"},
        {"Franchise": "Punjab Kings (PBKS)", "Remaining Purse (₹ Cr)": 18.60, "Retained": 19, "Open Slots": 6, "OS Slots": 2, "Confirmed Retained Core": "Shreyas Iyer (c), Hardik Pandya, Prabhsimran, Shashank, Stoinis, Jansen, Chahal", "Notable Released": "Lockie Ferguson, Mitchell Owen, Nehal Wadhera, Praveen Dubey"},
        {"Franchise": "Royal Challengers Bengaluru (RCB)", "Remaining Purse (₹ Cr)": 14.15, "Retained": 20, "Open Slots": 5, "OS Slots": 1, "Confirmed Retained Core": "Virat Kohli, Rajat Patidar (c), Phil Salt, Jitesh Sharma, Padikkal, Hazlewood", "Notable Released": "Glenn Maxwell, Faf du Plessis, Dinesh Karthik (Retired)"},
        {"Franchise": "Gujarat Titans (GT)", "Remaining Purse (₹ Cr)": 8.75, "Retained": 22, "Open Slots": 3, "OS Slots": 2, "Confirmed Retained Core": "Shubman Gill, Sai Sudharsan, Rashid Khan, Jos Buttler, Siraj, Rabada, Prasidh", "Notable Released": "M Shahrukh Khan, Kane Williamson, Matthew Wade"}
    ])
    st.dataframe(franchise_data, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🎯 Rajasthan Royals 6-Slot Shopping Plan (Allocating ₹27.05 Cr Purse)")
    st.markdown("""
    Based on Rajasthan Royals' released personnel (Hetmyer, Deshpande, Milne, Burger, Maphaka, Sen), here is the quantitative acquisition blueprint derived from our V5 pressure engine:
    """)

    rr_shopping_plan = pd.DataFrame([
        {
            "Slot #": "Slot 1 (OS #1)",
            "Target Role (Replacing Released RR Player)": "Left-Arm Death Pacer (Replaces Burger / Maphaka)",
            "Primary Target": "Mustafizur Rahman (Rel. KKR)",
            "Backup Target": "Matheesha Pathirana (Rel. KKR) / Spencer Johnson",
            "Key Pressure Metric (V5)": "Mustafizur: 5.56 Econ (22 Wkts) | Pathirana: 16.3% Bnd (51 P-Wkts)",
            "Target Bid Cap": "₹6.50 Cr – ₹8.50 Cr"
        },
        {
            "Slot #": "Slot 2 (OS #2)",
            "Target Role (Replacing Released RR Player)": "Overseas Finisher / Top-Order (Replaces Hetmyer)",
            "Primary Target": "David Miller / Travis Head",
            "Backup Target": "Pathum Nissanka (Rel. DC)",
            "Key Pressure Metric (V5)": "Head: 180.9 Rec SR | Miller: 995 P-Balls",
            "Target Bid Cap": "₹6.00 Cr – ₹8.00 Cr"
        },
        {
            "Slot #": "Slot 3 (OS #3)",
            "Target Role (Replacing Released RR Player)": "Overseas Attacking Spinner (Replaces Bishnoi / Puthur)",
            "Primary Target": "Wanindu Hasaranga (Rel. LSG)",
            "Backup Target": "Akeal Hosein / Mujeeb Ur Rahman",
            "Key Pressure Metric (V5)": "Hasaranga: 80 P-Wkts | Hosein: 6.71 Econ",
            "Target Bid Cap": "₹4.50 Cr – ₹6.00 Cr"
        },
        {
            "Slot #": "Slot 4 (IND #1)",
            "Target Role (Replacing Released RR Player)": "Indian Middle-Order Anchor/Hitter (Domestic Depth)",
            "Primary Target": "Karun Nair (Rel. DC)",
            "Backup Target": "Sarfaraz Khan (Rel. CSK)",
            "Key Pressure Metric (V5)": "Nair: +1.970 BPI, 178.8 SR, 61.1 Avg",
            "Target Bid Cap": "₹2.00 Cr – ₹3.50 Cr"
        },
        {
            "Slot #": "Slot 5 (IND #2)",
            "Target Role (Replacing Released RR Player)": "Indian Power Finisher (No. 6/7 Impact)",
            "Primary Target": "M Shahrukh Khan (Rel. GT)",
            "Backup Target": "Abishek Porel / Nitish Rana",
            "Key Pressure Metric (V5)": "Shahrukh: 164.4 Pressure SR in 2025–26",
            "Target Bid Cap": "₹1.50 Cr – ₹2.50 Cr"
        },
        {
            "Slot #": "Slot 6 (IND #3)",
            "Target Role (Replacing Released RR Player)": "Uncapped Death/PP Pacer (Replaces Deshpande / Sen)",
            "Primary Target": "Sakib Hussain (Rel. SRH)",
            "Backup Target": "Praful Hinge / Akash Madhwal",
            "Key Pressure Metric (V5)": "Sakib: 7.65 Rec Econ (-1.11 RPO Drop) | Hinge: -1.47 Drop",
            "Target Bid Cap": "₹0.30 Cr – ₹0.80 Cr"
        }
    ])
    st.table(rr_shopping_plan)

    col_w1, col_w2 = st.columns([1.2, 1])
    with col_w1:
        st.markdown("#### 👑 Projected Rajasthan Royals Best XII for IPL 2027")
        best_xii = [
            ("1. Yashasvi Jaiswal", "Indian Opener (Retained Core)"),
            ("2. Vaibhav Sooryavanshi", "Young Indian Attacking Opener (Retained Core)"),
            ("3. Riyan Parag (c)", "Captain & Dynamic Middle-Order Anchor (Retained Core)"),
            ("4. Dhruv Jurel (wk)", "Clutch Wicketkeeper Finisher (Retained Core)"),
            ("5. Karun Nair / Sarfaraz Khan", "Auction Target: Proven Indian Clutch Batting Anchor"),
            ("6. David Miller / Travis Head", "Auction Target (OS): High-Caliber Finisher / Power Hitter"),
            ("7. Ravindra Jadeja", "Elite Indian All-Rounder (Retained Core)"),
            ("8. Wanindu Hasaranga / Akeal Hosein", "Auction Target (OS): Attacking Leg-Spinner / Bowling All-Rounder"),
            ("9. Jofra Archer (OS)", "Elite Overseas Express Pacer (Retained Core)"),
            ("10. Mohammed Shami", "Veteran Indian Seam Leader (Traded In from LSG)"),
            ("11. Mustafizur Rahman / Spencer Johnson (OS)", "Auction Target (OS): Elite Death Bowling Specialist"),
            ("12. Sandeep Sharma / Sakib Hussain / Praful Hinge (Impact)", "Impact Player: Swing & Death Specialist")
        ]
        for name, role in best_xii:
            st.markdown(f"- **{name}** — *{role}*")

    with col_w2:
        st.markdown("#### 📊 RR Purse Allocation Visualization (₹27.05 Cr)")
        budget_items = {
            "Mustafizur (OS Death)": 7.50,
            "Miller / Head (OS Finisher)": 7.00,
            "Hasaranga (OS Spinner)": 5.00,
            "Karun Nair (IND Anchor)": 2.75,
            "Shahrukh Khan (IND Finisher)": 2.00,
            "Sakib Hussain (Uncapped Pacer)": 0.55,
            "Tactical Bidding Buffer": 2.25
        }
        fig_donut = px.pie(
            names=list(budget_items.keys()),
            values=list(budget_items.values()),
            hole=0.45,
            color_discrete_sequence=['#254AA5', '#EA1A85', '#38BDF8', '#8B5CF6', '#F59E0B', '#10B981', '#64748B']
        )
        fig_donut.update_layout(
            height=340,
            template='plotly_dark',
            paper_bgcolor='rgba(17, 28, 48, 0.8)',
            plot_bgcolor='rgba(17, 28, 48, 0.8)',
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.caption("Total Projected Spend: **₹24.80 Cr** | Tactical Reserve Buffer: **₹2.25 Cr**")

# ------------------------------------------------------------------------------
# TAB 2: BATTERS LEADERBOARD
# ------------------------------------------------------------------------------
with tab_bat:
    st.markdown(f"### 🏏 {pool_title} — Top Batting Performers Under Pressure")
    st.markdown("""
    **Understanding Batting Metrics:**
    - **Pressure SR ($SR_{\\text{wp}}$):** Strike rate under game-leverage pressure (collapses, death overs, steep chases) weighted dynamically by ball degradation, venue par, away hostility, elite opposition, and exponential recency.
    - **2025–26 P-SR:** Raw pressure strike rate over the most recent 24-month window (2025–2026 seasons).
    - **Δ SR Lift:** Strike rate elevation under pressure compared to career baseline ($SR_{\\text{wp}} - SR_{\\text{base}}$). Positive numbers prove clutch acceleration.
    - **BPI Score:** Composite Batting Pressure Index calculated from standardized multi-factor Z-scores.
    """)

    top10_bat = bat_filt.head(10).copy()
    top10_bat.insert(0, 'Rank', [f"#{i+1}" for i in range(len(top10_bat))])

    display_cols_bat = [
        'Rank', 'striker_name', 'auction_status', 'p_balls', 'rec_p_balls',
        'base_sr', 'wp_sr', 'rec_p_sr', 'sr_lift', 'wp_avg', 'rec_p_avg',
        'wp_bnd_pct', 'wp_dot_pct', 'dynamic_bpi'
    ]

    st.dataframe(
        top10_bat[display_cols_bat].rename(columns={
            'striker_name': 'Batter Name',
            'auction_status': 'Auction Status / Team',
            'p_balls': 'Career P-Balls',
            'rec_p_balls': '2025-26 P-Balls',
            'base_sr': 'Base SR',
            'wp_sr': 'Pressure SR (Weighted)',
            'rec_p_sr': '2025-26 P-SR',
            'sr_lift': 'Δ SR Lift',
            'wp_avg': 'Pressure Avg',
            'rec_p_avg': '2025-26 P-Avg',
            'wp_bnd_pct': 'Boundary %',
            'wp_dot_pct': 'Dot %',
            'dynamic_bpi': 'BPI Index'
        }),
        use_container_width=True,
        hide_index=True
    )

    # Scout Spotlight Card for #1 Batter
    if not top10_bat.empty:
        b1 = top10_bat.iloc[0]
        st.markdown(f"""
        <div class="scout-card">
            <h4 style="margin:0 0 0.5rem 0; color:#38BDF8;">
                🌟 War-Room Scout Spotlight: #{b1['Rank']} {b1['striker_name']} ({b1['auction_status']})
            </h4>
            <p style="margin:0; font-size:0.92rem; color:#E2E8F0; line-height:1.5;">
                <strong>Primary Auction Recommendation:</strong> {b1['striker_name']} records an outstanding 
                <strong style="color:#EA1A85;">+{b1['dynamic_bpi']:.3f} BPI score</strong>, elevating strike rate from {b1['base_sr']:.1f} at baseline to 
                <strong style="color:#38BDF8;">{b1['wp_sr']:.1f}</strong> under pressure (a massive <strong style="color:#4ADE80;">{b1['sr_lift']:+.1f} Δ SR Lift</strong>). 
                In 2025–2026 pressure situations, he maintains a <strong>{b1['rec_p_sr']:.1f} SR</strong> with an elite 
                <strong>{b1['wp_avg']:.1f} average</strong> and {b1['wp_bnd_pct']:.1f}% boundary percentage across {int(b1['p_balls'])} pressure deliveries.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Scatter Quadrant
    fig_bat = px.scatter(
        bat_filt,
        x='base_sr',
        y='rec_p_sr',
        size='rec_p_balls',
        color='dynamic_bpi',
        color_continuous_scale=['#00F2FE', '#3B82F6', '#8B5CF6', '#EC4899', '#EA1A85'],
        hover_name='striker_name',
        hover_data=['auction_status', 'wp_sr', 'sr_lift', 'wp_avg', 'rec_p_avg'],
        labels={
            'base_sr': 'Career Baseline Strike Rate',
            'rec_p_sr': '2025–2026 Pressure Strike Rate',
            'dynamic_bpi': 'BPI Score',
            'rec_p_balls': '2025–26 P-Balls'
        },
        title=f"🏏 Batters Quadrant: Career Baseline SR vs. 2025–26 Pressure SR ({pool_title})"
    )
    fig_bat.add_hline(y=bat_filt['rec_p_sr'].mean(), line_dash="dash", line_color="#38BDF8", annotation_text="Pool Pressure Mean", annotation_position="bottom right")
    fig_bat.add_vline(x=bat_filt['base_sr'].mean(), line_dash="dash", line_color="#EA1A85", annotation_text="Pool Base Mean", annotation_position="top left")
    fig_bat.update_layout(
        height=520,
        template='plotly_dark',
        paper_bgcolor='rgba(17, 28, 48, 0.8)',
        plot_bgcolor='rgba(17, 28, 48, 0.8)'
    )
    st.plotly_chart(fig_bat, use_container_width=True)

    # Download CSV
    csv_bat = top10_bat[display_cols_bat].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top 10 Batters CSV",
        data=csv_bat,
        file_name="rr_top10_batters_v5.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 3: BOWLERS LEADERBOARD
# ------------------------------------------------------------------------------
with tab_bowl:
    st.markdown(f"### 🎯 {pool_title} — Top Bowling Performers Under Pressure")
    st.markdown("""
    **Understanding Bowling Metrics:**
    - **Pressure Economy ($\\text{Econ}_{\\text{wp}}$):** Economy rate under high leverage (powerplay collapse, death overs, defending small totals) weighted by venue par, dew/wet-ball physics, away hostility, elite striker matchups, and exponential recency. (Lower is better).
    - **2025–26 P-Econ:** Economy rate conceded under pressure in the most recent 2025–2026 seasons.
    - **Δ Econ Drop:** Economy difference relative to baseline ($\\text{Econ}_{\\text{wp}} - \\text{Econ}_{\\text{base}}$). Negative values indicate that a bowler tightens up and restricts runs even harder when the game is on the line.
    - **BoPI Score:** Composite Bowling Pressure Index derived from standardized multi-factor Z-scores (Higher is better).
    """)

    top10_bowl = bowl_filt.head(10).copy()
    top10_bowl.insert(0, 'Rank', [f"#{i+1}" for i in range(len(top10_bowl))])

    display_cols_bowl = [
        'Rank', 'bowler_name', 'auction_status', 'p_balls', 'rec_p_balls', 'rec_p_wkts',
        'base_econ', 'wp_econ', 'rec_p_econ', 'econ_drop', 'wp_sr', 'rec_p_sr',
        'wp_dot_pct', 'wp_bnd_pct', 'dynamic_bopi'
    ]

    st.dataframe(
        top10_bowl[display_cols_bowl].rename(columns={
            'bowler_name': 'Bowler Name',
            'auction_status': 'Auction Status / Team',
            'p_balls': 'Career P-Balls',
            'rec_p_balls': '2025-26 P-Balls',
            'rec_p_wkts': '2025-26 P-Wkts',
            'base_econ': 'Base Econ',
            'wp_econ': 'Pressure Econ (Weighted)',
            'rec_p_econ': '2025-26 P-Econ',
            'econ_drop': 'Δ Econ Drop',
            'wp_sr': 'Pressure SR',
            'rec_p_sr': '2025-26 P-SR',
            'wp_dot_pct': 'Dot %',
            'wp_bnd_pct': 'Boundary %',
            'dynamic_bopi': 'BoPI Index'
        }),
        use_container_width=True,
        hide_index=True
    )

    # Scout Spotlight Card for #1 Bowler
    if not top10_bowl.empty:
        bw1 = top10_bowl.iloc[0]
        st.markdown(f"""
        <div class="scout-card" style="border-left-color: #EA1A85;">
            <h4 style="margin:0 0 0.5rem 0; color:#EA1A85;">
                🌟 War-Room Scout Spotlight: #{bw1['Rank']} {bw1['bowler_name']} ({bw1['auction_status']})
            </h4>
            <p style="margin:0; font-size:0.92rem; color:#E2E8F0; line-height:1.5;">
                <strong>Primary Auction Recommendation:</strong> {bw1['bowler_name']} earns the 
                <strong style="color:#38BDF8;">#{bw1['Rank']} ranking with a +{bw1['dynamic_bopi']:.3f} BoPI score</strong>. 
                Under extreme pressure situations, he concedes just <strong style="color:#4ADE80;">{bw1['wp_econ']:.2f} RPO</strong> (tightening down from {bw1['base_econ']:.2f} baseline economy, an impressive <strong>{bw1['econ_drop']:+.2f} economy drop</strong>). 
                Across {int(bw1['p_balls'])} career pressure deliveries and {int(bw1['rec_p_balls'])} recent 2025–2026 pressure balls, he yields a stellar 
                <strong>{bw1['rec_p_econ']:.2f} RPO</strong> and {bw1['wp_dot_pct']:.1f}% dot-ball chokehold.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Scatter Quadrant
    fig_bowl = px.scatter(
        bowl_filt,
        x='base_econ',
        y='rec_p_econ',
        size='rec_p_balls',
        color='dynamic_bopi',
        color_continuous_scale=['#00F2FE', '#3B82F6', '#8B5CF6', '#EC4899', '#EA1A85'],
        hover_name='bowler_name',
        hover_data=['auction_status', 'wp_econ', 'econ_drop', 'rec_p_wkts', 'wp_dot_pct'],
        labels={
            'base_econ': 'Career Baseline Economy (RPO)',
            'rec_p_econ': '2025–2026 Pressure Economy (RPO)',
            'dynamic_bopi': 'BoPI Score',
            'rec_p_balls': '2025–26 P-Balls'
        },
        title=f"🎯 Bowlers Quadrant: Baseline Econ vs. 2025–26 Pressure Econ ({pool_title})"
    )
    fig_bowl.add_hline(y=bowl_filt['rec_p_econ'].mean(), line_dash="dash", line_color="#38BDF8", annotation_text="Pool Pressure Mean", annotation_position="bottom right")
    fig_bowl.add_vline(x=bowl_filt['base_econ'].mean(), line_dash="dash", line_color="#EA1A85", annotation_text="Pool Base Mean", annotation_position="top left")
    fig_bowl.update_layout(
        height=520,
        template='plotly_dark',
        paper_bgcolor='rgba(17, 28, 48, 0.8)',
        plot_bgcolor='rgba(17, 28, 48, 0.8)'
    )
    st.plotly_chart(fig_bowl, use_container_width=True)

    # Download CSV
    csv_bowl = top10_bowl[display_cols_bowl].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top 10 Bowlers CSV",
        data=csv_bowl,
        file_name="rr_top10_bowlers_v5.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 4: EXPONENTIAL RECENCY ENGINE EXPLAINED & INTERACTIVE VISUALIZER
# ------------------------------------------------------------------------------
with tab_recency:
    st.markdown("### ⏳ Interactive Exponential Recency Weighting Architecture")
    st.markdown("""
    Modern T20 franchise analytics suffers when relying purely on career aggregates: a batter who dominated in 2022 but declined in 2025–2026 is often overvalued, while a rapidly ascending young clutch specialist is overlooked.
    
    To solve this, our **V5 Recency Engine** couples contextual scoreboard physics with a continuous exponential time-decay function:
    """)

    col_r1, col_r2 = st.columns([1.2, 1])
    with col_r1:
        st.latex(r"W_{\text{final}} = W_{\text{context}} \times M_{\text{recency}}(t)")
        st.markdown("""
        Where $M_{\text{recency}}(t)$ assigns exponential weight to match deliveries based on proximity to the present:
        - **2026 Season:** Multiplier = **1.50×** (Peak weight for immediate form)
        - **2025 Season:** Multiplier = **1.25×** (Strong weight for recent tactical meta)
        - **2024 Season:** Multiplier = **0.90×** (Slight dampening)
        - **2023 Season:** Multiplier = **0.65×** (Substantial historical discount)
        - **2022 Season:** Multiplier = **0.45×** (Long-term baseline discount)
        
        **Dynamic Recency Scaling Formula:**
        """)
        st.latex(r"M_{\text{active}}(y) = \max\left(0.05, \, 1.0 + \lambda \cdot [M_{\text{benchmark}}(y) - 1.0]\right)")
        st.markdown(f"""
        With current **Recency Scale $\\lambda = {recency_mult:.2f}\\times$**:
        - A delivery bowled in 2026 carries **{active_recency_map[2026]:.2f}×** weight.
        - A delivery bowled in 2022 carries **{active_recency_map[2022]:.2f}×** weight.
        - **Recency Leverage Ratio:** 2026 clutch deliveries are weighted **{ratio_26_22:.2f}× more heavily** than 2022 deliveries!
        """)

    with col_r2:
        # Plot active exponential decay curve
        years_list = [2022, 2023, 2024, 2025, 2026]
        weights_list = [active_recency_map[y] for y in years_list]
        bench_weights = [base_recency_map[y] for y in years_list]

        fig_rec = go.Figure()
        fig_rec.add_trace(go.Bar(
            x=years_list,
            y=weights_list,
            marker_color=['#00F2FE', '#3B82F6', '#8B5CF6', '#EC4899', '#EA1A85'],
            name="Active Weight",
            text=[f"{w:.2f}×" for w in weights_list],
            textposition='auto'
        ))
        fig_rec.add_trace(go.Scatter(
            x=years_list,
            y=bench_weights,
            mode='lines+markers',
            name="Benchmark (1.00×)",
            line=dict(color='#F8FAFC', dash='dash', width=2),
            marker=dict(size=7, color='#F8FAFC')
        ))
        fig_rec.update_layout(
            title=f"Exponential Recency Weight by Season (Scale: {recency_mult:.2f}×)",
            xaxis_title="Match Season (Year)",
            yaxis_title="Delivery Weight Multiplier",
            height=360,
            template='plotly_dark',
            paper_bgcolor='rgba(17, 28, 48, 0.8)',
            plot_bgcolor='rgba(17, 28, 48, 0.8)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_rec, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔬 How Changing Recency Weighting Modifies Player Rankings Live")
    st.markdown(f"""
    Because all 200,999 deliveries are partitioned across seasons and pressure contexts, moving the sidebar's **Recency Multiplier slider** recalculates each player's weighted deliveries ($W_{{\\text{{balls}}}}$, $W_{{\\text{{runs}}}}$, $W_{{\\text{{wkts}}}}$) dynamically in real time:
    - **At $\\lambda = 0.00\\times$ (Flat Weighting):** Eliminates recency decay entirely. All years carry equal 1.00× weight.
    - **At $\\lambda = 1.00\\times$ (Benchmark Default):** The exact calibrated exponential weights applied in our V5 pipeline.
    - **At $\\lambda = 2.00\\times$ (Aggressive Decay):** Drastically magnifies 2025–2026 performances (2026 = 2.00×), penalizing aging stars whose clutch stats occurred in 2022–2023.
    """)

# ------------------------------------------------------------------------------
# TAB 5: PUBLICATION QUADRANT CHARTS
# ------------------------------------------------------------------------------
with tab_charts:
    st.markdown("### 📊 Publication-Grade 220 DPI Quadrant Scatter Visualizations")
    st.markdown("""
    Below are the high-resolution publication charts generated by our pipeline. 
    These plots divide the player pool into four distinct tactical quadrants:
    - **Upper Right (Elite Clutch Accelerators / Restrictors):** High baseline competency combined with high clutch elevation. This is Rajasthan Royals' primary auction target zone.
    - **Upper Left (Emerging Pressure Specialists):** Modest baseline volume but explosive performance during collapse and death overs.
    - **Lower Right (High Baseline, Pressure Decelerators):** Accumulators who score heavily in low-pressure conditions but struggle when required run rates spike.
    - **Lower Left (Unviable Targets):** Low baseline and low pressure performance.
    """)

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.markdown("#### 🏏 Released Batters: Baseline SR vs. 2025–26 Pressure SR")
        img_bat_path = 'v5_released_bat_chart.png' if os.path.exists('v5_released_bat_chart.png') else ('list_b_bat_chart.png' if os.path.exists('list_b_bat_chart.png') else os.path.join('new', 'v5_released_bat_chart.png'))
        if os.path.exists(img_bat_path):
            st.image(img_bat_path, caption="V5 Released Batters Quadrant (220 DPI Plot)", use_container_width=True)
        else:
            st.info("Chart will appear after pipeline executes.")

    with col_img2:
        st.markdown("#### 🎯 Released Bowlers: Baseline Econ vs. 2025–26 Pressure Econ")
        img_bowl_path = 'v5_released_bowl_chart.png' if os.path.exists('v5_released_bowl_chart.png') else ('list_b_bowl_chart.png' if os.path.exists('list_b_bowl_chart.png') else os.path.join('new', 'v5_released_bowl_chart.png'))
        if os.path.exists(img_bowl_path):
            st.image(img_bowl_path, caption="V5 Released Bowlers Quadrant (220 DPI Plot)", use_container_width=True)
        else:
            st.info("Chart will appear after pipeline executes.")

# ------------------------------------------------------------------------------
# TAB 6: HEAD-TO-HEAD CANDIDATE COMPARISON
# ------------------------------------------------------------------------------
with tab_compare:
    st.markdown("### 🔍 Head-to-Head Candidate Comparison")
    st.markdown("Compare any two shortlisted targets side-by-side across all career baseline, pressure, and recent form metrics:")

    compare_type = st.radio("Select Discipline to Compare:", ["Batters", "Bowlers"], horizontal=True)

    if compare_type == "Batters":
        bat_names = bat_filt['striker_name'].tolist()
        if len(bat_names) >= 2:
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                p1_name = st.selectbox("Select Target Batter 1:", bat_names, index=0)
            with col_c2:
                p2_name = st.selectbox("Select Target Batter 2:", bat_names, index=1 if len(bat_names) > 1 else 0)

            p1_data = bat_filt[bat_filt['striker_name'] == p1_name].iloc[0]
            p2_data = bat_filt[bat_filt['striker_name'] == p2_name].iloc[0]

            comp_df = pd.DataFrame({
                "Metric": [
                    "Auction Status / Franchise", "BPI Score", "Career P-Balls", "2025-26 P-Balls",
                    "Base Strike Rate", "Pressure SR (Weighted)", "2025-26 Pressure SR",
                    "Δ SR Lift (Clutch Elevation)", "Pressure Average", "2025-26 Pressure Avg",
                    "Boundary %", "Dot Ball %"
                ],
                f"Candidate 1: {p1_name}": [
                    p1_data['auction_status'], f"+{p1_data['dynamic_bpi']:.3f}", f"{int(p1_data['p_balls'])}",
                    f"{int(p1_data['rec_p_balls'])}", f"{p1_data['base_sr']:.1f}", f"{p1_data['wp_sr']:.1f}",
                    f"{p1_data['rec_p_sr']:.1f}", f"{p1_data['sr_lift']:+.1f}", f"{p1_data['wp_avg']:.1f}",
                    f"{p1_data['rec_p_avg']:.1f}", f"{p1_data['wp_bnd_pct']:.1f}%", f"{p1_data['wp_dot_pct']:.1f}%"
                ],
                f"Candidate 2: {p2_name}": [
                    p2_data['auction_status'], f"+{p2_data['dynamic_bpi']:.3f}", f"{int(p2_data['p_balls'])}",
                    f"{int(p2_data['rec_p_balls'])}", f"{p2_data['base_sr']:.1f}", f"{p2_data['wp_sr']:.1f}",
                    f"{p2_data['rec_p_sr']:.1f}", f"{p2_data['sr_lift']:+.1f}", f"{p2_data['wp_avg']:.1f}",
                    f"{p2_data['rec_p_avg']:.1f}", f"{p2_data['wp_bnd_pct']:.1f}%", f"{p2_data['wp_dot_pct']:.1f}%"
                ]
            })
            st.table(comp_df)
        else:
            st.warning("Not enough batters meet current filter thresholds to compare.")
    else:
        bowl_names = bowl_filt['bowler_name'].tolist()
        if len(bowl_names) >= 2:
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                b1_name = st.selectbox("Select Target Bowler 1:", bowl_names, index=0)
            with col_c2:
                b2_name = st.selectbox("Select Target Bowler 2:", bowl_names, index=1 if len(bowl_names) > 1 else 0)

            b1_data = bowl_filt[bowl_filt['bowler_name'] == b1_name].iloc[0]
            b2_data = bowl_filt[bowl_filt['bowler_name'] == b2_name].iloc[0]

            comp_bowl_df = pd.DataFrame({
                "Metric": [
                    "Auction Status / Franchise", "BoPI Score", "Career P-Balls", "2025-26 P-Balls",
                    "2025-26 P-Wickets", "Base Economy (RPO)", "Pressure Economy (Weighted)",
                    "2025-26 Pressure Economy", "Δ Econ Drop (Restriction)", "Pressure Strike Rate",
                    "2025-26 Pressure SR", "Dot Ball %", "Boundary %"
                ],
                f"Candidate 1: {b1_name}": [
                    b1_data['auction_status'], f"+{b1_data['dynamic_bopi']:.3f}", f"{int(b1_data['p_balls'])}",
                    f"{int(b1_data['rec_p_balls'])}", f"{int(b1_data['rec_p_wkts'])}", f"{b1_data['base_econ']:.2f}",
                    f"{b1_data['wp_econ']:.2f}", f"{b1_data['rec_p_econ']:.2f}", f"{b1_data['econ_drop']:+.2f}",
                    f"{b1_data['wp_sr']:.1f}", f"{b1_data['rec_p_sr']:.1f}", f"{b1_data['wp_dot_pct']:.1f}%", f"{b1_data['wp_bnd_pct']:.1f}%"
                ],
                f"Candidate 2: {b2_name}": [
                    b2_data['auction_status'], f"+{b2_data['dynamic_bopi']:.3f}", f"{int(b2_data['p_balls'])}",
                    f"{int(b2_data['rec_p_balls'])}", f"{int(b2_data['rec_p_wkts'])}", f"{b2_data['base_econ']:.2f}",
                    f"{b2_data['wp_econ']:.2f}", f"{b2_data['rec_p_econ']:.2f}", f"{b2_data['econ_drop']:+.2f}",
                    f"{b2_data['wp_sr']:.1f}", f"{b2_data['rec_p_sr']:.1f}", f"{b2_data['wp_dot_pct']:.1f}%", f"{b2_data['wp_bnd_pct']:.1f}%"
                ]
            })
            st.table(comp_bowl_df)
        else:
            st.warning("Not enough bowlers meet current filter thresholds to compare.")

# ------------------------------------------------------------------------------
# TAB 7: MATHEMATICAL ARCHITECTURE
# ------------------------------------------------------------------------------
with tab_math:
    st.markdown("### 📐 Complete Mathematical Specification (V5 Engine)")
    st.markdown("""
    The SupeRR Selector V5 Framework evaluates every delivery through a multi-tiered hierarchy of match leverage, physical dynamics, and temporal recency:
    """)

    st.markdown("#### 1. Base Scoreboard Leverage Filter ($P_{\\text{base}}$)")
    st.markdown("""
    To eliminate dead-rubber stat-padding and non-competitive deliveries, $P_{\\text{base}} = 1$ is activated strictly under four critical conditions:
    """)
    st.latex(r"""
    P_{\text{base}} = 
    \begin{cases}
    1 & \text{if Powerplay Collapse: } (\text{over} \le 6 \land \text{wkts} \ge 2) \lor (\text{over} \in [7, 12] \land \text{wkts} \ge 3) \\
    1 & \text{if 1st Innings Death Overs: } (\text{innings} = 1 \land \text{over} \ge 16 \land \text{wkts} \le 7) \\
    1 & \text{if 2nd Innings Death Chase: } (\text{innings} = 2 \land \text{over} \ge 16 \land \text{runs\_needed} > 0 \land \text{rrr} \in [7.5, 22.0] \land \text{wkts} \le 8) \\
    1 & \text{if High-Leverage Steep Chase: } (\text{innings} = 2 \land \text{runs\_needed} > 0 \land \text{rrr} \in [9.5, 20.0] \land \text{wkts} \le 8) \\
    0 & \text{otherwise (Garbage time excluded)}
    \end{cases}
    """)

    st.markdown("#### 2. The 6-Factor Multiplicative Context Architecture")
    st.latex(r"""
    W_{\text{context, bat}} = P_{\text{base}} \times M_{\text{level}} \times M_{\text{venue, bat}} \times M_{\text{away, bat}} \times M_{\text{opp, bat}} \times M_{\text{ball, bat}} \times M_{\text{inn}}
    """)
    st.latex(r"""
    W_{\text{context, bowl}} = P_{\text{base}} \times M_{\text{level}} \times M_{\text{venue, bowl}} \times M_{\text{away, bowl}} \times M_{\text{opp, bowl}} \times M_{\text{ball, bowl}} \times M_{\text{inn}}
    """)

    st.markdown("""
    - **Match Stakes ($M_{\\text{level}}$):** $1.30$ for IPL Playoffs/Finals, $1.22$ for World Cup/Asia Cup Knockouts, $1.18$ for IPL League matches, $1.05$ for Bilateral T20Is.
    - **Venue Pitch Par ($M_{\\text{venue}}$):** Normalized against global RPO:
    """)
    st.latex(r"M_{\text{venue, bat}} = \text{clip}\left(\frac{\text{RPO}_{\text{global}}}{\text{RPO}_{\text{venue}}}, \, 0.90, \, 1.15\right), \quad M_{\text{venue, bowl}} = \text{clip}\left(\frac{\text{RPO}_{\text{venue}}}{\text{RPO}_{\text{global}}}, \, 0.90, \, 1.15\right)")
    st.markdown("""
    - **Away Hostility ($M_{\\text{away}}$):** $1.12$ when playing against host team at their fortress, $1.00$ otherwise.
    - **Elite Opposition Matchup ($M_{\\text{opp}}$):** $1.18$ when facing top-30% bowlers (Econ $\\le 30\\text{th percentile}$ or Wkts $\\ge 30$) or top-30% batters (SR $\\ge 70\\text{th percentile}$ or Runs $\\ge 600$).
    - **Dew & Ball Physics ($M_{\\text{ball}}$):**
      - Batters: $1.12$ in Overs 1–6 vs Pace, $1.10$ in Overs 7–15 vs Spin, $1.15$ in Overs 16–20.
      - Bowlers: $1.10$ in Overs 1–6 with $\\le 1$ wkt down, $1.20$ in Overs 16–20 of 2nd Innings (slick wet-ball dew factor), $1.15$ in Overs 16–20 of 1st Innings.
    - **Innings Context ($M_{\\text{inn}}$):** $1.15$ when chasing at RRR $\\ge 10.0$, $1.12$ in 1st Innings when $\\ge 3$ wickets down before over 12.
    """)

    st.markdown("#### 3. Composite Standardized Index Equations (BPI & BoPI)")
    st.latex(r"""
    \text{BPI} = 0.25 \cdot Z(SR_{\text{wp}}) + 0.20 \cdot Z(\text{Avg}_{\text{wp}}) + 0.15 \cdot Z(SR_{25-26}) + 0.15 \cdot Z(\text{Bnd}\%_{\text{wp}}) - 0.10 \cdot Z(\text{Dot}\%_{\text{wp}}) + 0.10 \cdot Z(\Delta SR_{\text{lift}}) + 0.05 \cdot Z(I_{\text{pressure}})
    """)
    st.latex(r"""
    \text{BoPI} = -0.25 \cdot Z(\text{Econ}_{\text{wp}}) - 0.20 \cdot Z(SR_{\text{wp}}) - 0.15 \cdot Z(\text{Econ}_{25-26}) + 0.15 \cdot Z(\text{Dot}\%_{\text{wp}}) - 0.10 \cdot Z(\text{Bnd}\%_{\text{wp}}) - 0.10 \cdot Z(\Delta \text{Econ}_{\text{drop}}) + 0.05 \cdot Z(I_{\text{pressure}})
    """)

# Footer Branding
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
    <strong>Rajasthan Royals Sports Data Science Team</strong> &bull; SupeRR Selector Season 2 &bull; 
    Official Submission Dashboard &bull; Engineered in Python, Streamlit, Pandas & Plotly
</div>
""", unsafe_allow_html=True)
