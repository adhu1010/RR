#!/usr/bin/env python3
"""
SupeRR Selector Season 2 — Round 1 V5 Official Master Pipeline
Author: Adhwaith K P
Integrates:
  - Updated ball-by-ball dataset (6af855c0e8386_ball_by_ball.csv / ball_by_ball.csv)
  - Official 10-Team Confirmed Retained, Traded-In & Released Lists for IPL 2027 (184 locked players)
  - 6-Factor Context & Physics Engine + Exponential Recency Decay (M_recency)
Outputs:
  - v5_official_released_ipl_batters.csv & v5_official_released_ipl_bowlers.csv (Option A: IPL-Proven Released Pool)
  - v5_all_available_auction_batters.csv & v5_all_available_auction_bowlers.csv (Option B: Global + Released Pool)
  - v5_released_bat_chart.png & v5_released_bowl_chart.png (220 DPI Quadrant Visuals)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 1. LOAD UPDATED DATASET & SUPPORTING FILES
# ==============================================================================
bbb_file = '6af855c0e8386_ball_by_ball.csv' if os.path.exists('6af855c0e8386_ball_by_ball.csv') else 'ball_by_ball.csv'
print(f"[1/5] Loading {bbb_file} and supporting CSVs...")
df = pd.read_csv(bbb_file, low_memory=False)
matches = pd.read_csv('matches.csv', low_memory=False)
comps = pd.read_csv('competitions.csv', low_memory=False)
teams = pd.read_csv('teams.csv', low_memory=False)
pe = pd.read_csv('playing_eleven.csv', low_memory=False)
ctpm = pd.read_csv('competition_team_player_mapping.csv', low_memory=False)

df['year'] = pd.to_datetime(df['delivery_ist_time'], errors='coerce').dt.year

# ==============================================================================
# 2. OFFICIAL 10-TEAM IPL 2027 RETENTION, TRADE & RELEASE MAPPING
# ==============================================================================
IPL_COMP_IDS = {1358, 1715, 2193, 2725, 3298}  # IPL 2022–2026
PAKISTAN_PLAYER_IDS = set(ctpm[ctpm['team_name'].str.strip().str.lower() == 'pakistan']['player_id'].unique())

RETIRED_NAMES = {
    'Dinesh Karthik', 'Shikhar Dhawan', 'Aaron Finch', 'David Warner', 'Ambati Rayudu',
    'Eoin Morgan', 'Wriddhiman Saha', 'Piyush Chawla', 'Amit Mishra', 'Kedar Jadhav',
    'Saurabh Tiwary', 'Stuart Broad', 'Chris Gayle', 'AB de Villiers', 'Dwayne Bravo',
    'Kieron Pollard', 'Robin Uthappa', 'Parthiv Patel', 'Faf du Plessis', 'Moeen Ali',
    'Ravichandran Ashwin', 'Andre Russell', 'Glenn Maxwell', 'Mahendra Singh Dhoni', 'MS Dhoni'
}

# All 184 Confirmed Retained & Traded-In Players Across All 10 IPL Franchises for 2027
CONFIRMED_RETAINED_2027 = {
    # 1. RCB (20 Retained)
    'Virat Kohli', 'Rajat Patidar', 'Phil Salt', 'Jitesh Sharma', 'Devdutt Padikkal',
    'Venkatesh Iyer', 'Krunal Pandya', 'Tim David', 'Romario Shepherd', 'Swapnil Singh', 'Kanishk Chouhan',
    'Josh Hazlewood', 'Bhuvneshwar Kumar', 'Yash Dayal', 'Rasikh Salam', 'Lungi Ngidi',
    'Suyash Sharma', 'Nuwan Thushara', 'Jacob Duffy', 'Abhinandan Singh',
    # 2. CSK (19 Retained)
    'Ruturaj Gaikwad', 'Sanju Samson', 'Noor Ahmad', 'Shivam Dube', 'Anshul Kamboj',
    'Liam Livingstone', 'Jack Edwards', 'Devon Conway', 'Kartik Sharma', 'Ayush Mhatre',
    'Dewald Brevis', 'Jamie Overton', 'Gurjapneet Singh', 'Mukesh Choudhary', 'Ramakrishna Ghosh',
    'Urvil Patel', 'Vansh Bedi', 'Shaik Rasheed', 'Andre Siddarth',
    # 3. MI (16 Retained)
    'Rohit Sharma', 'Suryakumar Yadav', 'Surya Kumar Yadav', 'Jasprit Bumrah', 'Namboori Tilak Varma', 'Tilak Varma',
    'Arshdeep Singh', 'Quinton de Kock', 'Ryan Rickelton', 'Mitchell Santner', 'Will Jacks', 'William Jacks',
    'Sherfane Rutherford', 'Corbin Bosch', 'Naman Dhir', 'Shardul Thakur', 'Ashwani Kumar', 'Robin Minz',
    'Raj Bawa', 'Raghu Sharma', 'Ruchit Ahir', 'Krish Bhagat',
    # 4. KKR (17 Retained)
    'Cameron Green', 'Sunil Narine', 'Rinku Singh', 'Varun Chakravarthy', 'Harshit Rana',
    'Angkrish Raghuvanshi', 'Ramandeep Singh', 'Finn Allen', 'Manish Pandey', 'Tim Seifert',
    'Rovman Powell', 'Anukul Roy', 'Sarthak Ranjan', 'Kartik Tyagi', 'Vaibhav Arora', 'Prashant Solanki', 'Saurabh Dubey',
    # 5. SRH (18 Retained)
    'Pat Cummins', 'Patrick Cummins', 'Abhishek Sharma', 'Heinrich Klaasen', 'Ishan Kishan',
    'Nitish Kumar Reddy', 'Nitish Reddy', 'Eshan Malinga', 'Khaleel Ahmed', 'Nathan Ellis',
    'T Natarajan', 'T. Natarajan', 'Wiaan Mulder', 'Brydon Carse', 'Rahul Chahar',
    'Abhinav Manohar', 'Simarjeet Singh', 'Atharva Taide', 'Atharwa Taide', 'Aniket Verma',
    'Harsh Dubey', 'Smaran Ravichandran', 'Ravichandran Smaran',
    # 6. DC (16 Retained)
    'Rishabh Pant', 'Axar Patel', 'Lokesh Rahul', 'KL Rahul', 'Tristan Stubbs',
    'Jake Fraser-McGurk', 'Mukesh Kumar', 'Zeeshan Ansari', 'Ashutosh Sharma', 'Sameer Rizvi',
    'Vipraj Nigam', 'Dushmantha Chameera', 'Auqib Nabi', 'Ajay Mandal', 'Tripurana Vijay', 'Sahil Parakh', 'Madhav Tiwari',
    # 7. RR (19 Retained)
    'Riyan Parag', 'Yashasvi Jaiswal', 'Dhruv Jurel', 'Vaibhav Sooryavanshi', 'Vaibhav Suryavanshi',
    'Jofra Archer', 'Sandeep Sharma', 'Mohammed Shami', 'M Siddharth', 'M. Siddharth', 'Manimaran Siddharth',
    'Ravindra Jadeja', 'Dasun Shanaka', 'Donovan Ferreira', 'Lhuan Pretorius', 'Lhuan-dre Pretorius',
    'Shubham Dubey', 'Sushant Mishra', 'Yash Punja', 'Yash Raj Punja', 'Emanjot Singh Chahal', 'Aman Rao Perala', 'Brijesh Sharma',
    # 8. PBKS (19 Retained)
    'Shreyas Iyer', 'Hardik Pandya', 'Prabhsimran Singh', 'Priyansh Arya', 'Shashank Singh',
    'Marcus Stoinis', 'Marco Jansen', 'Yuzvendra Chahal', 'Harpreet Brar', 'Josh Inglis',
    'Ben Dwarshuis', 'Vishnu Vinod', 'Vyshak Kumar', 'Vyshak Vijaykumar', 'Xavier Bartlett',
    'Yash Thakur', 'Azmatullah Omarzai', 'Suryansh Shedge', 'Cooper Connolly', 'Harnoor Pannu', 'Harnoor Singh', 'Musheer Khan',
    # 9. LSG (18 Retained)
    'Nicholas Pooran', 'Kuldeep Yadav', 'Mitchell Marsh', 'Aiden Markram', 'Sam Curran',
    'Mayank Yadav', 'Mohsin Khan', 'Ravi Bishnoi', 'Ayush Badoni', 'Abdul Samad',
    'Shahbaz Ahmed', 'Prince Yadav', 'Digvesh Singh Rathi', 'Digvesh Rathi', 'Digvesh Singh',
    'Arjun Tendulkar', 'Akash Singh', 'Himmat Singh', 'Akshat Raghuwanshi', 'Mukul Choudhary',
    # 10. GT (22 Retained)
    'Shubman Gill', 'Sai Sudharsan', 'Rashid Khan', 'Jos Buttler', 'Mohammed Siraj',
    'Kagiso Rabada', 'Prasidh Krishna', 'Rahul Tewatia', 'Harshal Patel', 'Washington Sundar',
    'Sai Kishore', 'R Sai Kishore', 'Glenn Phillips', 'Jason Holder', 'Tom Banton',
    'Anuj Rawat', 'Kumar Kushagra', 'Manav Suthar', 'Arshad Khan', 'Nishant Sindhu', 'Nishant Kumar Sindhu',
    'Gurnoor Brar', 'Gurnoor Singh Brar', 'Ashok Sharma', 'Jayant Yadav',
    'Haider Ali'
}

ipl_2026_df = ctpm[ctpm['comp_id'] == 3298][['player_id', 'player_name', 'team_id', 'team_name']].drop_duplicates('player_id')
ipl_2026_team_map = dict(zip(ipl_2026_df['player_id'], ipl_2026_df['team_name']))
ever_ipl_ids = set(ctpm[ctpm['comp_id'].isin(IPL_COMP_IDS)]['player_id'].unique())

def get_official_2027_status(player_id, player_name):
    if player_name in CONFIRMED_RETAINED_2027:
        return 'Retained / Traded In (Locked)'
    if player_id in ipl_2026_team_map:
        return f"Released ({ipl_2026_team_map[player_id]})"
    if player_id in ever_ipl_ids:
        return 'Free Agent (Unattached IPL)'
    return 'Free Agent (T20I / Global)'

# ==============================================================================
# 3. PRE-DELIVERY SCOREBOARD RECONSTRUCTION
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
# 5. AGGREGATE V5 AVAILABLE AUCTION POOLS (OPTION A: IPL-PROVEN & OPTION B: ALL)
# ==============================================================================
print("[4/5] Computing V5 Official Available Auction Pools...")
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
    ipl_matches=('is_ipl', lambda s: bat_df.loc[s.index, 'match_id'][s].nunique()),
    balls=('runs', 'count'),
    runs=('runs', 'sum'),
    outs=('is_out', 'sum')
).reset_index()

bat_press = bat_p.groupby(['striker_id', 'striker_name']).agg(
    p_balls=('runs', 'count'), p_runs=('runs', 'sum'), w_balls=('w_bat', 'sum'),
    w_runs=('w_runs', 'sum'), w_outs=('w_outs', 'sum'), w_bnd=('w_bnd', 'sum'),
    w_dot=('w_dot', 'sum'), avg_pressure_intensity=('w_context_bat', 'mean')
).reset_index()

bat_rec = bat_p[bat_p['is_recent']].groupby('striker_id').agg(
    rec_p_balls=('runs', 'count'), rec_p_runs=('runs', 'sum'), rec_p_outs=('is_out', 'sum')
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

bat_res['official_2027_status'] = [get_official_2027_status(pid, pname) for pid, pname in zip(bat_res['striker_id'], bat_res['striker_name'])]
bat_res['is_pakistani'] = bat_res['striker_id'].isin(PAKISTAN_PLAYER_IDS)
bat_res['is_retired'] = bat_res['striker_name'].isin(RETIRED_NAMES)

# Option A: IPL-Proven Officially Released & Unattached Batters
bat_v5_ipl = bat_res[
    (~bat_res['is_pakistani']) & (~bat_res['is_retired']) &
    (~bat_res['striker_name'].isin(CONFIRMED_RETAINED_2027)) &
    (bat_res['ipl_matches'] >= 1) & (bat_res['p_balls'] >= 70) & (bat_res['rec_p_balls'] >= 30)
].copy()

for col in ['wp_sr', 'wp_avg', 'wp_bnd_pct', 'wp_dot_pct', 'sr_lift', 'rec_p_sr', 'avg_pressure_intensity']:
    bat_v5_ipl[col + '_z'] = (bat_v5_ipl[col] - bat_v5_ipl[col].mean()) / bat_v5_ipl[col].std()

bat_v5_ipl['bpi_v5'] = (
    0.25 * bat_v5_ipl['wp_sr_z'] + 0.20 * bat_v5_ipl['wp_avg_z'] + 0.15 * bat_v5_ipl['rec_p_sr_z'] +
    0.15 * bat_v5_ipl['wp_bnd_pct_z'] - 0.10 * bat_v5_ipl['wp_dot_pct_z'] + 0.10 * bat_v5_ipl['sr_lift_z'] +
    0.05 * bat_v5_ipl['avg_pressure_intensity_z']
).round(3)
bat_v5_ipl = bat_v5_ipl.sort_values('bpi_v5', ascending=False).reset_index(drop=True)

# Bowlers
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
    ipl_matches=('is_ipl', lambda s: df.loc[s.index, 'match_id'][s].nunique()),
    balls=('is_legal', 'sum'),
    runs=('b_runs', 'sum'),
    wkts=('b_wkt', 'sum')
).reset_index()

bowl_press = bowl_p.groupby(['bowler_id', 'bowler_name']).agg(
    p_balls=('is_legal', 'sum'), p_wkts=('b_wkt', 'sum'), w_balls=('w_bowl', 'sum'),
    w_runs=('w_runs', 'sum'), w_wkts=('w_wkts', 'sum'), w_dot=('w_dot', 'sum'),
    w_bnd=('w_bnd', 'sum'), avg_pressure_intensity=('w_context_bowl', 'mean')
).reset_index()

bowl_rec = bowl_p[bowl_p['is_recent']].groupby('bowler_id').agg(
    rec_p_balls=('is_legal', 'sum'), rec_p_runs=('b_runs', 'sum'), rec_p_wkts=('b_wkt', 'sum')
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

bowl_res['official_2027_status'] = [get_official_2027_status(pid, pname) for pid, pname in zip(bowl_res['bowler_id'], bowl_res['bowler_name'])]
bowl_res['is_pakistani'] = bowl_res['bowler_id'].isin(PAKISTAN_PLAYER_IDS)
bowl_res['is_retired'] = bowl_res['bowler_name'].isin(RETIRED_NAMES)

# Option A: IPL-Proven Officially Released & Unattached Bowlers
bowl_v5_ipl = bowl_res[
    (~bowl_res['is_pakistani']) & (~bowl_res['is_retired']) &
    (~bowl_res['bowler_name'].isin(CONFIRMED_RETAINED_2027)) &
    (bowl_res['ipl_matches'] >= 1) & (bowl_res['p_balls'] >= 70) & (bowl_res['rec_p_balls'] >= 30)
].copy()

for col in ['wp_econ', 'wp_sr', 'wp_dot_pct', 'wp_bnd_pct', 'econ_drop', 'rec_p_econ', 'avg_pressure_intensity']:
    bowl_v5_ipl[col + '_z'] = (bowl_v5_ipl[col] - bowl_v5_ipl[col].mean()) / bowl_v5_ipl[col].std()

bowl_v5_ipl['bopi_v5'] = (
    -0.25 * bowl_v5_ipl['wp_econ_z'] - 0.20 * bowl_v5_ipl['wp_sr_z'] - 0.15 * bowl_v5_ipl['rec_p_econ_z'] +
    0.15 * bowl_v5_ipl['wp_dot_pct_z'] - 0.10 * bowl_v5_ipl['wp_bnd_pct_z'] - 0.10 * bowl_v5_ipl['econ_drop_z'] +
    0.05 * bowl_v5_ipl['avg_pressure_intensity_z']
).round(3)
bowl_v5_ipl = bowl_v5_ipl.sort_values('bopi_v5', ascending=False).reset_index(drop=True)

bat_v5_ipl.to_csv('v5_official_released_ipl_batters.csv', index=False)
bowl_v5_ipl.to_csv('v5_official_released_ipl_bowlers.csv', index=False)
print("[5/5] Saved v5_official_released_ipl_batters.csv and v5_official_released_ipl_bowlers.csv!")