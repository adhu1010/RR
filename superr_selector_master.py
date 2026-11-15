#!/usr/bin/env python3
"""
SupeRR Selector Season 2 — Round 1 Master Pipeline (V4 Recency + List B Auction Pool + List A Benchmark)
Author: Adhwaith K P / RR Data Science Team
Usage:
  python superr_selector_master.py
Outputs:
  1. list_b_unstop_top_batters.csv  -> Official Unstop Dropdown Top 10 Batters (Actionable IPL 2027 Auction Pool)
  2. list_b_unstop_top_bowlers.csv  -> Official Unstop Dropdown Top 10 Bowlers (Actionable IPL 2027 Auction Pool)
  3. v4_recency_top_batters.csv     -> Benchmark List A Top Batters (Including Retained Franchise Cores)
  4. v4_recency_top_bowlers.csv     -> Benchmark List A Top Bowlers (Including Retained Franchise Cores)
  5. list_b_bat_chart.png & list_b_bowl_chart.png -> 220 DPI Quadrant Scatter Plots
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 1. LOAD ALL 6 OFFICIAL DATASET FILES
# ==============================================================================
print("[1/5] Loading official SupeRR Selector Season 2 CSV files...")
df = pd.read_csv('ball_by_ball.csv', low_memory=False)
matches = pd.read_csv('matches.csv', low_memory=False)
comps = pd.read_csv('competitions.csv', low_memory=False)
teams = pd.read_csv('teams.csv', low_memory=False)
pe = pd.read_csv('playing_eleven.csv', low_memory=False)
ctpm = pd.read_csv('competition_team_player_mapping.csv', low_memory=False)

df['year'] = pd.to_datetime(df['delivery_ist_time'], errors='coerce').dt.year

# ==============================================================================
# 2. PROGRAMMATIC IPL 2026 ROSTER, ELIGIBILITY & RETENTION MAPPING
# ==============================================================================
IPL_COMP_IDS = {1358, 1715, 2193, 2725, 3298}  # IPL 2022, 2023, 2024, 2025, 2026
PAKISTAN_PLAYER_IDS = set(ctpm[ctpm['team_name'].str.strip().str.lower() == 'pakistan']['player_id'].unique())

RETIRED_NAMES = {
    'Dinesh Karthik', 'Shikhar Dhawan', 'Aaron Finch', 'David Warner', 'Ambati Rayudu',
    'Eoin Morgan', 'Wriddhiman Saha', 'Piyush Chawla', 'Amit Mishra', 'Kedar Jadhav',
    'Saurabh Tiwary', 'Stuart Broad', 'Chris Gayle', 'AB de Villiers', 'Dwayne Bravo',
    'Kieron Pollard', 'Robin Uthappa', 'Parthiv Patel', 'Faf du Plessis', 'Moeen Ali',
    'Ravichandran Ashwin', 'Andre Russell', 'Nicholas Pooran', 'Glenn Maxwell'
}

UNTOUCHABLE_FRANCHISE_CORES = {
    # RR Core (Already owned by Rajasthan Royals)
    'Vaibhav Sooryavanshi', 'Yashasvi Jaiswal', 'Riyan Parag', 'Dhruv Jurel', 'Ravindra Jadeja',
    'Jofra Archer', 'Sam Curran', 'Shimron Hetmyer',
    # MI Core
    'Jasprit Bumrah', 'Suryakumar Yadav', 'Hardik Pandya', 'Rohit Sharma', 'Namboori Tilak Varma',
    'Tilak Varma', 'Naman Dhir',
    # RCB Core
    'Virat Kohli', 'Rajat Patidar', 'Phil Salt', 'Tim David', 'Josh Hazlewood', 'Yash Dayal',
    # CSK Core
    'Ruturaj Gaikwad', 'Mahendra Singh Dhoni', 'Sanju Samson', 'Shivam Dube', 'Noor Ahmad',
    'Khaleel Ahmed', 'Ayush Mhatre',
    # KKR Core
    'Sunil Narine', 'Varun Chakravarthy', 'Rinku Singh', 'Harshit Rana', 'Matheesha Pathirana', 'Cameron Green',
    # SRH Core
    'Heinrich Klaasen', 'Abhishek Sharma', 'Travis Head', 'Pat Cummins', 'Ishan Kishan', 'Nitish Reddy',
    # GT Core
    'Shubman Gill', 'Sai Sudharsan', 'Rashid Khan', 'Jos Buttler', 'Mohammed Siraj', 'Kagiso Rabada', 'Prasidh Krishna',
    # DC Core
    'Axar Patel', 'Kuldeep Yadav', 'Tristan Stubbs', 'Lokesh Rahul', 'Mitchell Starc', 'T Natarajan',
    # PBKS Core
    'Shreyas Iyer', 'Arshdeep Singh', 'Yuzvendra Chahal', 'Shashank Singh', 'Prabhsimran Singh',
    'Priyansh Arya', 'Marco Jansen',
    # LSG Core
    'Rishabh Pant', 'Nicholas Pooran', 'Mayank Yadav', 'Aiden Markram', 'Mitchell Marsh', 'Mohammed Shami',
    # Name-collision disambiguation
    'Haider Ali'
}

ipl_2026_df = ctpm[ctpm['comp_id'] == 3298][['player_id', 'player_name', 'team_id', 'team_name']].drop_duplicates('player_id')
ipl_2026_team_map = dict(zip(ipl_2026_df['player_id'], ipl_2026_df['team_name']))
ipl_2026_player_ids = set(ipl_2026_df['player_id'].unique())

# ==============================================================================
# 3. PRE-DELIVERY SCOREBOARD STATE RECONSTRUCTION
# ==============================================================================
print("[2/5] Reconstructing pre-delivery scoreboard state across 200,999 balls...")
for col in ['is_four', 'is_six', 'is_wicket']:
    df[col] = df[col].astype(str).str.lower() == 'true'

df['is_wide'] = df['extras_type'].astype(str).str.lower() == 'wide'
df['is_noball'] = df['extras_type'].astype(str).str.lower().isin(['overstep', 'noball', 'no ball'])
df['is_legal'] = ~(df['is_wide'] | df['is_noball'])
df['extra_runs'] = np.where(
    df['is_wide'] | df['is_noball'], 1 + df['extras_2_runs'].fillna(0),
    np.where(df['extras_type'].isin(['None', np.nan, None]), 0, 1)
)
df['ball_runs'] = df['runs'].fillna(0) + df['extra_runs']
df = df.sort_values(['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

df['cum_runs'] = df.groupby(['match_id', 'innings'])['ball_runs'].cumsum() - df['ball_runs']
df['cum_wkts'] = df.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - df['is_wicket'].astype(int)
df['balls_bowled'] = df.groupby(['match_id', 'innings'])['is_legal'].cumsum() - df['is_legal'].astype(int)
df['balls_rem'] = np.maximum(120 - df['balls_bowled'], 1)

inn1_totals = df[df['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_total')
df = df.merge(inn1_totals, on='match_id', how='left')
df['target'] = np.where(df['innings'] == 2, df['inn1_total'] + 1, np.nan)
df['runs_needed'] = np.where(df['innings'] == 2, df['target'] - df['cum_runs'], np.nan)
df['rrr'] = np.where(df['innings'] == 2, (df['runs_needed'] / df['balls_rem']) * 6.0, np.nan)

match_meta = matches.merge(comps, on='comp_id', how='left', suffixes=('', '_comp'))
df = df.merge(match_meta, on='match_id', how='left', suffixes=('', '_match'))

# ==============================================================================
# 4. 6-FACTOR CONTEXTUAL, PHYSICS & RECENCY DECAY MULTIPLIERS
# ==============================================================================
print("[3/5] Applying 6-factor contextual, ball-physics, and 2025-26 recency weights...")
df['is_ipl'] = df['comp_id'].isin(IPL_COMP_IDS)
stage_str = df['stage'].astype(str).str.lower()
comp_str = df['comp_name'].astype(str).str.lower()
knockout_flag = (
    df['knock_out'].astype(str).str.lower().isin(['true', '1', 'yes']) |
    stage_str.str.contains(r'final|qualifier|eliminator|playoff|semi', regex=True) |
    comp_str.str.contains(r'world cup|asia cup', regex=True)
)
df['m_level'] = np.where(knockout_flag & df['is_ipl'], 1.30,
                np.where(knockout_flag, 1.22,
                np.where(df['is_ipl'], 1.18, 1.05)))

venue_rpo = (df.groupby('venue_id')['ball_runs'].sum() / df.groupby('venue_id')['is_legal'].sum()) * 6.0
global_rpo = (df['ball_runs'].sum() / df['is_legal'].sum()) * 6.0
df['venue_rpo'] = df['venue_id'].map(venue_rpo).fillna(global_rpo)
df['m_venue_bat'] = np.clip(global_rpo / df['venue_rpo'], 0.90, 1.15)
df['m_venue_bowl'] = np.clip(df['venue_rpo'] / global_rpo, 0.90, 1.15)

df['is_away_bat'] = (df['batting_team_id'] != df['home_team_id']) & (df['bowling_team_id'] == df['home_team_id'])
df['is_away_bowl'] = (df['bowling_team_id'] != df['home_team_id']) & (df['batting_team_id'] == df['home_team_id'])
df['m_away_bat'] = np.where(df['is_away_bat'], 1.12, 1.00)
df['m_away_bowl'] = np.where(df['is_away_bowl'], 1.12, 1.00)

bowl_base = df.groupby('bowler_id').agg(b_balls=('is_legal', 'sum'), b_runs=('ball_runs', 'sum'), b_wkts=('is_wicket', 'sum'))
bowl_base = bowl_base[bowl_base['b_balls'] >= 180]
bowl_base['b_econ'] = (bowl_base['b_runs'] / bowl_base['b_balls']) * 6.0
elite_bowlers = set(bowl_base[(bowl_base['b_econ'] <= bowl_base['b_econ'].quantile(0.30)) | (bowl_base['b_wkts'] >= 30)].index)

bat_base = df[~df['is_wide']].groupby('striker_id').agg(s_balls=('runs', 'count'), s_runs=('runs', 'sum'))
bat_base = bat_base[bat_base['s_balls'] >= 180]
bat_base['s_sr'] = (bat_base['s_runs'] / bat_base['s_balls']) * 100.0
elite_batters = set(bat_base[(bat_base['s_sr'] >= bat_base['s_sr'].quantile(0.70)) | (bat_base['s_runs'] >= 600)].index)

df['m_opp_bat'] = np.where(df['bowler_id'].isin(elite_bowlers), 1.18, 1.00)
df['m_opp_bowl'] = np.where(df['striker_id'].isin(elite_batters), 1.18, 1.00)

is_pace = df['pace_or_spin'].astype(str).str.lower() == 'pace'
is_spin = df['pace_or_spin'].astype(str).str.lower() == 'spin'
df['m_ball_bat'] = np.where((df['overid'] <= 6) & is_pace, 1.12,
                   np.where(df['overid'].between(7, 15) & is_spin, 1.10,
                   np.where(df['overid'] >= 16, 1.15, 1.00)))
df['m_ball_bowl'] = np.where((df['overid'] <= 6) & (df['cum_wkts'] <= 1), 1.10,
                    np.where((df['overid'] >= 16) & (df['innings'] == 2), 1.20,
                    np.where(df['overid'] >= 16, 1.15, 1.00)))
df['m_inn'] = np.where((df['innings'] == 2) & (df['rrr'] >= 10.0), 1.15,
              np.where((df['innings'] == 1) & (df['cum_wkts'] >= 3) & (df['overid'] <= 12), 1.12, 1.00))

recency_map = {2026: 1.50, 2025: 1.25, 2024: 0.90, 2023: 0.65, 2022: 0.45}
df['m_recency'] = df['year'].map(recency_map).fillna(1.00)
df['is_recent'] = df['year'].isin([2025, 2026])

# Base Scoreboard Triggers (Excluding Dead-Rubber Garbage Time)
p_collapse = ((df['overid'] <= 6) & (df['cum_wkts'] >= 2)) | (df['overid'].between(7, 12) & (df['cum_wkts'] >= 3))
p_death_inn1 = (df['innings'] == 1) & (df['overid'] >= 16) & (df['cum_wkts'] <= 7)
p_death_inn2 = (df['innings'] == 2) & (df['overid'] >= 16) & (df['runs_needed'] > 0) & (df['rrr'].between(7.5, 22.0)) & (df['cum_wkts'] <= 8)
p_chase = (df['innings'] == 2) & (df['runs_needed'] > 0) & (df['rrr'].between(9.5, 20.0)) & (df['cum_wkts'] <= 8)

df['p_base'] = (p_collapse | p_death_inn1 | p_death_inn2 | p_chase).astype(float)
df['w_context_bat'] = df['p_base'] * df['m_inn'] * df['m_ball_bat'] * df['m_venue_bat'] * df['m_away_bat'] * df['m_opp_bat'] * df['m_level']
df['w_context_bowl'] = df['p_base'] * df['m_inn'] * df['m_ball_bowl'] * df['m_venue_bowl'] * df['m_away_bowl'] * df['m_opp_bowl'] * df['m_level']
df['w_bat'] = df['w_context_bat'] * df['m_recency']
df['w_bowl'] = df['w_context_bowl'] * df['m_recency']

# ==============================================================================
# 5. AGGREGATE LIST B (AUCTION TARGET POOL) & LIST A (BENCHMARK LEADERBOARD)
# ==============================================================================
print("[4/5] Computing List B (Auction Target Top 10) and List A (Overall Benchmark Top 10)...")

# --- BATTERS ---
bat_df = df[~df['is_wide']].copy()
bat_df['is_out'] = (bat_df['is_wicket'] & (bat_df['dismissed_player_id'] == bat_df['striker_id'])).astype(float)
bat_df['is_bnd'] = (bat_df['is_four'] | bat_df['is_six']).astype(float)
bat_df['is_dot'] = (bat_df['runs'] == 0).astype(float)

bat_p = bat_df[bat_df['p_base'] > 0].copy()
bat_p['w_runs'] = bat_p['runs'] * bat_p['w_bat']
bat_p['w_outs'] = bat_p['is_out'] * bat_p['w_bat']
bat_p['w_bnd'] = bat_p['is_bnd'] * bat_p['w_bat']
bat_p['w_dot'] = bat_p['is_dot'] * bat_p['w_bat']

bat_all = bat_df.groupby(['striker_id', 'striker_name']).agg(
    matches=('match_id', 'nunique'),
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    outs=('is_out', 'sum')
).reset_index()

bat_ipl = bat_df[bat_df['is_ipl']].groupby('striker_id')['match_id'].nunique().rename('ipl_matches').reset_index()
bat_all = bat_all.merge(bat_ipl, on='striker_id', how='left')
bat_all['ipl_matches'] = bat_all['ipl_matches'].fillna(0).astype(int)

bat_press = bat_p.groupby(['striker_id', 'striker_name']).agg(
    p_balls=('runs', 'count'),
    p_runs=('runs', 'sum'),
    w_balls=('w_bat', 'sum'),
    w_runs=('w_runs', 'sum'),
    w_outs=('w_outs', 'sum'),
    w_bnd=('w_bnd', 'sum'),
    w_dot=('w_dot', 'sum'),
    avg_pressure_intensity=('w_context_bat', 'mean')
).reset_index()

bat_rec = bat_p[bat_p['is_recent']].groupby('striker_id').agg(
    rec_p_balls=('runs', 'count'),
    rec_p_runs=('runs', 'sum'),
    rec_p_outs=('is_out', 'sum')
).reset_index()
bat_rec['rec_p_sr'] = (bat_rec['rec_p_runs'] / np.maximum(bat_rec['rec_p_balls'], 1) * 100).round(1)
bat_rec['rec_p_avg'] = (bat_rec['rec_p_runs'] / np.maximum(bat_rec['rec_p_outs'], 1)).round(1)

bat_res = bat_all.merge(bat_press, on=['striker_id', 'striker_name']).merge(bat_rec, on='striker_id', how='left')
bat_res['rec_p_balls'] = bat_res['rec_p_balls'].fillna(0).astype(int)
bat_res['rec_p_sr'] = bat_res['rec_p_sr'].fillna(0)
bat_res['rec_p_avg'] = bat_res['rec_p_avg'].fillna(0)
bat_res['base_sr'] = (bat_res['runs'] / bat_res['balls'] * 100).round(1)
bat_res['base_avg'] = (bat_res['runs'] / np.maximum(bat_res['outs'], 1)).round(1)
bat_res['wp_sr'] = (bat_res['w_runs'] / bat_res['w_balls'] * 100).round(1)
bat_res['wp_avg'] = (bat_res['w_runs'] / np.maximum(bat_res['w_outs'], 1)).round(1)
bat_res['wp_bnd_pct'] = (bat_res['w_bnd'] / bat_res['w_balls'] * 100).round(1)
bat_res['wp_dot_pct'] = (bat_res['w_dot'] / bat_res['w_balls'] * 100).round(1)
bat_res['sr_lift'] = (bat_res['wp_sr'] - bat_res['base_sr']).round(1)
bat_res['recent_form_delta'] = (bat_res['rec_p_sr'] - bat_res['base_sr']).round(1)

bat_res['ipl_2026_team'] = bat_res['striker_id'].map(ipl_2026_team_map).fillna('FREE AGENT (Not in IPL 2026)')
bat_res['in_ipl_2026'] = bat_res['striker_id'].isin(ipl_2026_player_ids)
bat_res['is_pakistani'] = bat_res['striker_id'].isin(PAKISTAN_PLAYER_IDS)
bat_res['is_retired'] = bat_res['striker_name'].isin(RETIRED_NAMES)

# --- LIST B BATTERS (Actionable IPL 2027 Auction Pool - Currently Playing in IPL) ---
bat_b = bat_res[
    (bat_res['in_ipl_2026']) &
    (~bat_res['is_pakistani']) &
    (~bat_res['is_retired']) &
    (~bat_res['striker_name'].isin(UNTOUCHABLE_FRANCHISE_CORES)) &
    (bat_res['p_balls'] >= 80) &
    (bat_res['rec_p_balls'] >= 40)
].copy()

for col in ['wp_sr', 'wp_avg', 'wp_bnd_pct', 'wp_dot_pct', 'sr_lift', 'rec_p_sr', 'avg_pressure_intensity']:
    bat_b[col + '_z'] = (bat_b[col] - bat_b[col].mean()) / bat_b[col].std()

bat_b['bpi_auction'] = (
    0.25 * bat_b['wp_sr_z'] +
    0.20 * bat_b['wp_avg_z'] +
    0.15 * bat_b['rec_p_sr_z'] +
    0.15 * bat_b['wp_bnd_pct_z'] -
    0.10 * bat_b['wp_dot_pct_z'] +
    0.10 * bat_b['sr_lift_z'] +
    0.05 * bat_b['avg_pressure_intensity_z']
).round(3)
bat_b = bat_b.sort_values('bpi_auction', ascending=False).reset_index(drop=True)

# --- LIST A BATTERS (Unrestricted Active IPL 2026 Benchmark) ---
bat_a = bat_res[
    (bat_res['in_ipl_2026']) &
    (bat_res['matches'] >= 25) &
    (bat_res['p_balls'] >= 150) &
    (bat_res['rec_p_balls'] >= 60)
].copy()

for col in ['wp_sr', 'wp_avg', 'wp_bnd_pct', 'wp_dot_pct', 'sr_lift', 'rec_p_sr', 'avg_pressure_intensity']:
    bat_a[col + '_z'] = (bat_a[col] - bat_a[col].mean()) / bat_a[col].std()

bat_a['bpi_v4'] = (
    0.25 * bat_a['wp_sr_z'] +
    0.20 * bat_a['wp_avg_z'] +
    0.15 * bat_a['rec_p_sr_z'] +
    0.15 * bat_a['wp_bnd_pct_z'] -
    0.10 * bat_a['wp_dot_pct_z'] +
    0.10 * bat_a['sr_lift_z'] +
    0.05 * bat_a['avg_pressure_intensity_z']
).round(3)
bat_a = bat_a.sort_values('bpi_v4', ascending=False).reset_index(drop=True)

# --- BOWLERS ---
df['b_wkt'] = (df['is_wicket'] & (~df['dismissal_type'].astype(str).isin(['RunOut', 'Retired Hurt', 'Obstructing the field']))).astype(float)
df['b_runs'] = df['runs'] + np.where(df['is_wide'] | df['is_noball'], 1 + df['extras_2_runs'].fillna(0), 0)
df['b_dot'] = (df['is_legal'] & (df['b_runs'] == 0)).astype(float)
df['b_bnd'] = (df['is_four'] | df['is_six']).astype(float)

bowl_p = df[(df['p_base'] > 0) & df['is_legal']].copy()
bowl_p['w_runs'] = bowl_p['b_runs'] * bowl_p['w_bowl']
bowl_p['w_wkts'] = bowl_p['b_wkt'] * bowl_p['w_bowl']
bowl_p['w_dot'] = bowl_p['b_dot'] * bowl_p['w_bowl']
bowl_p['w_bnd'] = bowl_p['b_bnd'] * bowl_p['w_bowl']

bowl_all = df[df['is_legal']].groupby(['bowler_id', 'bowler_name']).agg(
    matches=('match_id', 'nunique'),
    balls=('is_legal', 'sum'),
    runs=('b_runs', 'sum'),
    wkts=('b_wkt', 'sum')
).reset_index()

bowl_ipl = df[df['is_legal'] & df['is_ipl']].groupby('bowler_id')['match_id'].nunique().rename('ipl_matches').reset_index()
bowl_all = bowl_all.merge(bowl_ipl, on='bowler_id', how='left')
bowl_all['ipl_matches'] = bowl_all['ipl_matches'].fillna(0).astype(int)

bowl_press = bowl_p.groupby(['bowler_id', 'bowler_name']).agg(
    p_balls=('is_legal', 'sum'),
    p_wkts=('b_wkt', 'sum'),
    w_balls=('w_bowl', 'sum'),
    w_runs=('w_runs', 'sum'),
    w_wkts=('w_wkts', 'sum'),
    w_dot=('w_dot', 'sum'),
    w_bnd=('w_bnd', 'sum'),
    avg_pressure_intensity=('w_context_bowl', 'mean')
).reset_index()

bowl_rec = bowl_p[bowl_p['is_recent']].groupby('bowler_id').agg(
    rec_p_balls=('is_legal', 'sum'),
    rec_p_runs=('b_runs', 'sum'),
    rec_p_wkts=('b_wkt', 'sum')
).reset_index()
bowl_rec['rec_p_econ'] = (bowl_rec['rec_p_runs'] / np.maximum(bowl_rec['rec_p_balls'], 1) * 6.0).round(2)
bowl_rec['rec_p_sr'] = (bowl_rec['rec_p_balls'] / np.maximum(bowl_rec['rec_p_wkts'], 1)).round(1)

bowl_res = bowl_all.merge(bowl_press, on=['bowler_id', 'bowler_name']).merge(bowl_rec, on='bowler_id', how='left')
bowl_res['rec_p_balls'] = bowl_res['rec_p_balls'].fillna(0).astype(int)
bowl_res['rec_p_wkts'] = bowl_res['rec_p_wkts'].fillna(0).astype(int)
bowl_res['rec_p_econ'] = bowl_res['rec_p_econ'].fillna(99.0)
bowl_res['rec_p_sr'] = bowl_res['rec_p_sr'].fillna(99.0)

bowl_res['base_econ'] = (bowl_res['runs'] / bowl_res['balls'] * 6.0).round(2)
bowl_res['base_sr'] = (bowl_res['balls'] / np.maximum(bowl_res['wkts'], 1)).round(1)
bowl_res['wp_econ'] = (bowl_res['w_runs'] / bowl_res['w_balls'] * 6.0).round(2)
bowl_res['wp_sr'] = (bowl_res['w_balls'] / np.maximum(bowl_res['w_wkts'], 1)).round(1)
bowl_res['wp_dot_pct'] = (bowl_res['w_dot'] / bowl_res['w_balls'] * 100).round(1)
bowl_res['wp_bnd_pct'] = (bowl_res['w_bnd'] / bowl_res['w_balls'] * 100).round(1)
bowl_res['econ_drop'] = (bowl_res['wp_econ'] - bowl_res['base_econ']).round(2)

bowl_res['ipl_2026_team'] = bowl_res['bowler_id'].map(ipl_2026_team_map).fillna('FREE AGENT (Not in IPL 2026)')
bowl_res['in_ipl_2026'] = bowl_res['bowler_id'].isin(ipl_2026_player_ids)
bowl_res['is_pakistani'] = bowl_res['bowler_id'].isin(PAKISTAN_PLAYER_IDS)
bowl_res['is_retired'] = bowl_res['bowler_name'].isin(RETIRED_NAMES)

# --- LIST B BOWLERS (Actionable IPL 2027 Auction Pool - Currently Playing in IPL) ---
bowl_b = bowl_res[
    (bowl_res['in_ipl_2026']) &
    (~bowl_res['is_pakistani']) &
    (~bowl_res['is_retired']) &
    (~bowl_res['bowler_name'].isin(UNTOUCHABLE_FRANCHISE_CORES)) &
    (bowl_res['p_balls'] >= 80) &
    (bowl_res['rec_p_balls'] >= 40)
].copy()

for col in ['wp_econ', 'wp_sr', 'wp_dot_pct', 'wp_bnd_pct', 'econ_drop', 'rec_p_econ', 'avg_pressure_intensity']:
    bowl_b[col + '_z'] = (bowl_b[col] - bowl_b[col].mean()) / bowl_b[col].std()

bowl_b['bopi_auction'] = (
    -0.25 * bowl_b['wp_econ_z'] -
    0.20 * bowl_b['wp_sr_z'] -
    0.15 * bowl_b['rec_p_econ_z'] +
    0.15 * bowl_b['wp_dot_pct_z'] -
    0.10 * bowl_b['wp_bnd_pct_z'] -
    0.10 * bowl_b['econ_drop_z'] +
    0.05 * bowl_b['avg_pressure_intensity_z']
).round(3)
bowl_b = bowl_b.sort_values('bopi_auction', ascending=False).reset_index(drop=True)

# --- YEARLY PRESSURE AGGREGATIONS FOR REAL-TIME RECENCY INTERPOLATION ---
bat_p['wc_runs'] = bat_p['runs'] * bat_p['w_context_bat']
bat_p['wc_outs'] = bat_p['is_out'] * bat_p['w_context_bat']
bat_p['wc_bnd'] = bat_p['is_bnd'] * bat_p['w_context_bat']
bat_p['wc_dot'] = bat_p['is_dot'] * bat_p['w_context_bat']

bat_yearly = bat_p.groupby(['striker_id', 'striker_name', 'year']).agg(
    p_balls=('runs', 'count'),
    p_runs=('runs', 'sum'),
    p_outs=('is_out', 'sum'),
    p_bnd=('is_bnd', 'sum'),
    p_dot=('is_dot', 'sum'),
    wc_balls=('w_context_bat', 'sum'),
    wc_runs=('wc_runs', 'sum'),
    wc_outs=('wc_outs', 'sum'),
    wc_bnd=('wc_bnd', 'sum'),
    wc_dot=('wc_dot', 'sum')
).reset_index()

bowl_p['wc_runs'] = bowl_p['b_runs'] * bowl_p['w_context_bowl']
bowl_p['wc_wkts'] = bowl_p['b_wkt'] * bowl_p['w_context_bowl']
bowl_p['wc_dot'] = bowl_p['b_dot'] * bowl_p['w_context_bowl']
bowl_p['wc_bnd'] = bowl_p['b_bnd'] * bowl_p['w_context_bowl']

bowl_yearly = bowl_p.groupby(['bowler_id', 'bowler_name', 'year']).agg(
    p_balls=('is_legal', 'sum'),
    p_runs=('b_runs', 'sum'),
    p_wkts=('b_wkt', 'sum'),
    p_dot=('b_dot', 'sum'),
    p_bnd=('b_bnd', 'sum'),
    wc_balls=('w_context_bowl', 'sum'),
    wc_runs=('wc_runs', 'sum'),
    wc_wkts=('wc_wkts', 'sum'),
    wc_dot=('wc_dot', 'sum'),
    wc_bnd=('wc_bnd', 'sum')
).reset_index()

# --- LIST A BOWLERS (Unrestricted Active IPL 2026 Benchmark) ---
bowl_a = bowl_res[
    (bowl_res['in_ipl_2026']) &
    (bowl_res['matches'] >= 25) &
    (bowl_res['p_balls'] >= 150) &
    (bowl_res['rec_p_balls'] >= 60)
].copy()

for col in ['wp_econ', 'wp_sr', 'wp_dot_pct', 'wp_bnd_pct', 'econ_drop', 'rec_p_econ', 'avg_pressure_intensity']:
    bowl_a[col + '_z'] = (bowl_a[col] - bowl_a[col].mean()) / bowl_a[col].std()

bowl_a['bopi_v4'] = (
    -0.25 * bowl_a['wp_econ_z'] -
    0.20 * bowl_a['wp_sr_z'] -
    0.15 * bowl_a['rec_p_econ_z'] +
    0.15 * bowl_a['wp_dot_pct_z'] -
    0.10 * bowl_a['wp_bnd_pct_z'] -
    0.10 * bowl_a['econ_drop_z'] +
    0.05 * bowl_a['avg_pressure_intensity_z']
).round(3)
bowl_a = bowl_a.sort_values('bopi_v4', ascending=False).reset_index(drop=True)

# Save all CSV datasets
bat_b.to_csv('list_b_unstop_top_batters.csv', index=False)
bowl_b.to_csv('list_b_unstop_top_bowlers.csv', index=False)
bat_a.to_csv('v4_recency_top_batters.csv', index=False)
bowl_a.to_csv('v4_recency_top_bowlers.csv', index=False)
bat_yearly.to_csv('bat_yearly_pressure.csv', index=False)
bowl_yearly.to_csv('bowl_yearly_pressure.csv', index=False)

# ==============================================================================
# 6. GENERATE 220 DPI SCATTER QUADRANT CHARTS
# ==============================================================================
print("Generating 220 DPI scatter quadrant plots...")

# Chart 1: List B Batters Quadrant
fig, ax = plt.subplots(figsize=(10, 7), dpi=220)
x = bat_b['base_sr']
y = bat_b['rec_p_sr']
x_mean = x.mean()
y_mean = y.mean()

scatter = ax.scatter(x, y, c=bat_b['bpi_auction'], cmap='plasma', s=bat_b['p_balls']*0.8, alpha=0.85, edgecolors='#254AA5', linewidths=1.2)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('BPI Score (Auction Pool)', fontsize=11, fontweight='bold', color='#1E293B')

ax.axvline(x_mean, color='#EA1A85', linestyle='--', linewidth=1.2, alpha=0.7)
ax.axhline(y_mean, color='#EA1A85', linestyle='--', linewidth=1.2, alpha=0.7)

# Highlight & label top 10 with staggered offsets for pristine readability
bat_offsets = {
    'Karun Nair': (-70, 10),
    'Ryan Rickelton': (8, 6),
    'Quinton de Kock': (10, -12),
    'Ashutosh Sharma': (10, 8),
    'Pathum Nissanka': (-85, -14),
    'Cooper Connolly': (10, -14),
    'Vipraj Nigam': (10, -5),
    'Devdutt Padikkal': (-95, 8),
    'Tom Banton': (8, 8),
    'Finn Allen': (8, -10),
    'Sarfaraz Khan': (-80, 4)
}
top10_bat = bat_b.head(10)
for _, row in top10_bat.iterrows():
    offset = bat_offsets.get(row['striker_name'], (6, 6))
    ax.annotate(
        row['striker_name'],
        (row['base_sr'], row['rec_p_sr']),
        xytext=offset, textcoords='offset points',
        fontsize=8.5, fontweight='bold', color='#1E293B',
        arrowprops=dict(arrowstyle='->', color='#254AA5', lw=0.8, alpha=0.7),
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.9, edgecolor='#254AA5', linewidth=0.7)
    )

ax.text(x.max()*0.92, y.max()*0.98, 'HIGH CLUTCH ELEVATION\n(Top Targets)', fontsize=10, fontweight='bold', color='#254AA5', ha='right', va='top')
ax.set_title('Rajasthan Royals War-Room | List B Batters: Baseline SR vs. 2025-26 Pressure SR', fontsize=12, fontweight='bold', color='#254AA5', pad=12)
ax.set_xlabel('Career Baseline Strike Rate', fontsize=11, fontweight='bold', color='#1E293B')
ax.set_ylabel('2025-2026 Pressure Strike Rate', fontsize=11, fontweight='bold', color='#1E293B')
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('list_b_bat_chart.png', dpi=220)
plt.close()

# Chart 2: List B Bowlers Quadrant
fig, ax = plt.subplots(figsize=(10, 7), dpi=220)
x = bowl_b['base_econ']
y = bowl_b['rec_p_econ']
x_mean = x.mean()
y_mean = y.mean()

scatter = ax.scatter(x, y, c=bowl_b['bopi_auction'], cmap='viridis', s=bowl_b['p_balls']*0.8, alpha=0.85, edgecolors='#EA1A85', linewidths=1.2)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('BoPI Score (Auction Pool)', fontsize=11, fontweight='bold', color='#1E293B')

ax.axvline(x_mean, color='#254AA5', linestyle='--', linewidth=1.2, alpha=0.7)
ax.axhline(y_mean, color='#254AA5', linestyle='--', linewidth=1.2, alpha=0.7)

# Highlight & label top 10 with staggered offsets for pristine readability
bowl_offsets = {
    'Mitchell Santner': (8, -12),
    'Sakib Hussain': (8, 6),
    'Akeal Hosein': (8, 6),
    'Mustafizur Rahman': (8, -14),
    'Corbin Bosch': (8, 8),
    'Jamie Overton': (-85, 12),
    'Mohsin Khan': (-80, -10),
    'Nathan Ellis': (8, -10),
    'Vipraj Nigam': (-80, 8),
    'George Linde': (8, 6),
    'Brydon Carse': (8, 6)
}
top10_bowl = bowl_b.head(10)
for _, row in top10_bowl.iterrows():
    offset = bowl_offsets.get(row['bowler_name'], (6, 6))
    ax.annotate(
        row['bowler_name'],
        (row['base_econ'], row['rec_p_econ']),
        xytext=offset, textcoords='offset points',
        fontsize=8.5, fontweight='bold', color='#1E293B',
        arrowprops=dict(arrowstyle='->', color='#EA1A85', lw=0.8, alpha=0.7),
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.9, edgecolor='#EA1A85', linewidth=0.7)
    )

ax.text(x.min()*1.05, y.min()*1.05, 'ELITE RESTRICTION & CLUTCH\n(Lower Econ = Better)', fontsize=10, fontweight='bold', color='#254AA5', ha='left', va='bottom')
ax.set_title('Rajasthan Royals War-Room | List B Bowlers: Baseline Econ vs. 2025-26 Pressure Econ', fontsize=12, fontweight='bold', color='#254AA5', pad=12)
ax.set_xlabel('Career Baseline Economy (RPO)', fontsize=11, fontweight='bold', color='#1E293B')
ax.set_ylabel('2025-2026 Pressure Economy (RPO)', fontsize=11, fontweight='bold', color='#1E293B')
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('list_b_bowl_chart.png', dpi=220)
plt.close()

print("[5/5] Pipeline complete! Saved CSVs and 220 DPI quadrant charts.")
print("\n=== OFFICIAL UNSTOP DROPDOWN TOP 10 BATTERS (LIST B) ===")
print(bat_b[['striker_name', 'ipl_2026_team', 'p_balls', 'rec_p_balls', 'base_sr', 'wp_sr', 'rec_p_sr', 'wp_avg', 'rec_p_avg', 'bpi_auction']].head(10).to_string(index=False))
print("\n=== OFFICIAL UNSTOP DROPDOWN TOP 10 BOWLERS (LIST B) ===")
print(bowl_b[['bowler_name', 'ipl_2026_team', 'p_balls', 'rec_p_balls', 'rec_p_wkts', 'base_econ', 'wp_econ', 'rec_p_econ', 'wp_sr', 'rec_p_sr', 'bopi_auction']].head(10).to_string(index=False))
