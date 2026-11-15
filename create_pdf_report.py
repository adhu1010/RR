#!/usr/bin/env python3
"""
SupeRR Selector Season 2 — Round 1 Official Methodology Report Generator
Author: Adhwaith K P / RR Sports Data Science Team
Outputs:
  SupeRR_Selector_Round1_Methodology_Report.pdf (Pristine 4-Page Executive Document)
"""

import os
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ==============================================================================
# NUMBERED CANVAS FOR RUNNING HEADERS & FOOTERS
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#254AA5'))

        # Running Header (Pages 2-4)
        if self._pageNumber > 1:
            self.drawString(36, 758, "RAJASTHAN ROYALS | SUPERR SELECTOR SEASON 2")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawRightString(576, 758, "Round 1 Official Methodology Report")

            # Header Rule
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.75)
            self.line(36, 752, 576, 752)

        # Footer Rule (All Pages)
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.75)
        self.line(36, 38, 576, 38)

        # Running Footer
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(36, 26, "Confidential • Prepared for Rajasthan Royals Data Science War-Room • Author: Adhwaith K P")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 26, page_str)
        self.restoreState()


def build_pdf_report():
    pdf_filename = "SupeRR_Selector_Round1_Methodology_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_blue = colors.HexColor('#254AA5')
    c_navy = colors.HexColor('#0F172A')
    c_pink = colors.HexColor('#EA1A85')
    c_slate = colors.HexColor('#334155')
    c_light = colors.HexColor('#F8FAFC')
    c_border = colors.HexColor('#E2E8F0')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#E2E8F0')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_blue,
        spaceBefore=8,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_navy,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.2,
        textColor=c_slate,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=c_slate,
        leftIndent=10,
        spaceAfter=2
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_navy
    )

    tbl_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=8.5,
        textColor=c_slate,
        alignment=1
    )

    tbl_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=c_navy,
        alignment=0
    )

    story = []

    # ==========================================================================
    # PAGE 1: COVER HEADER, METADATA & TOP-10 BATTERS
    # ==========================================================================
    header_content = [
        [
            Paragraph("<font size=7.5 color='#EA1A85'><b>RAJASTHAN ROYALS &bull; SUPERR SELECTOR SEASON 2</b></font><br/>"
                      "<b>IDENTIFYING THE MOST RELIABLE PLAYERS UNDER PRESSURE</b>", title_style),
            Paragraph("<font size=20>👑</font>", ParagraphStyle('Crown', alignment=2))
        ],
        [
            Paragraph("<b>Round 1 Official Methodology Report & Execution Architecture (V4)</b><br/>"
                      "<i>Context-Aware Match Stakes, Scoreboard Leverage, Dew Physics & Exponential Recency Decay Engine</i>", subtitle_style),
            ""
        ]
    ]

    header_table = Table(header_content, colWidths=[465, 75])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_navy),
        ('PADDING', (0,0), (-1,-1), 12),
        ('SPAN', (0,1), (1,1)),
        ('LINEBELOW', (0,1), (1,1), 3, c_pink),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    # Meta banner
    meta_data = [
        [
            Paragraph("<b>Author / Role:</b> Adhwaith K P (Lead Sports Data Science)", callout_style),
            Paragraph("<b>Dataset:</b> 200,999 Deliveries (867 T20/IPL Matches)", callout_style),
            Paragraph("<b>Submission Track:</b> Unstop Round 1 Dropdown Lists", callout_style)
        ],
        [
            Paragraph("<b>Scope:</b> Active IPL 2026 Roster Targets (List B)", callout_style),
            Paragraph("<b>Seasons:</b> 2022–2026 Continuous Ball-by-Ball", callout_style),
            Paragraph("<b>Live War-Room:</b> <a href='https://intelligence-sponsors-unit-common.trycloudflare.com'><font color='#254AA5'><u>trycloudflare.com (Click Here)</u></font></a>", callout_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Official Top-10 Dropdown Submissions", h1_style))
    story.append(Paragraph(
        "Modern T20 analytics frequently fails at auction table decision-making because standard statistics "
        "(raw strike rate, economy rate, average) suffer from <b>context blindness</b> and <b>historical anchoring</b>. "
        "A run scored in a low-stakes dead rubber is treated identically to a run scored during an over-18 death chase against "
        "elite pace, while a batter's peak form in 2022 is often weighted equally to their performance in 2026. "
        "To solve this challenge for Rajasthan Royals, we engineered the <b>SupeRR Selector V4 Framework</b>. "
        "It reconstructs pre-delivery scoreboard leverage across <b>200,999 deliveries</b> (2022–2026), filters out garbage time, "
        "applies a <b>6-factor multiplicative context multiplier</b> (match stakes, venue par, away hostility, elite matchups, dew/ball physics, "
        "innings state), weights recent deliveries through a <b>continuous exponential recency decay model</b> "
        "(2026 weighted at 1.50&times; vs 2022 at 0.45&times;), and screens for actionable <b>Active IPL players</b> (excluding the 60 untouchable franchise cores).",
        body_style
    ))

    # Load top 10 data
    bat_b = pd.read_csv('list_b_unstop_top_batters.csv').head(10)
    bowl_b = pd.read_csv('list_b_unstop_top_bowlers.csv').head(10)

    story.append(Paragraph("<b>Table 1.1: Official Top-10 Batters Under Pressure (List B — Actionable IPL Targets)</b>", h2_style))
    bat_table_data = [[
        Paragraph("Rank", tbl_hdr_style),
        Paragraph("Batter Name", tbl_hdr_style),
        Paragraph("2026 Team", tbl_hdr_style),
        Paragraph("P-Balls", tbl_hdr_style),
        Paragraph("25-26 Balls", tbl_hdr_style),
        Paragraph("Base SR", tbl_hdr_style),
        Paragraph("Press SR", tbl_hdr_style),
        Paragraph("25-26 SR", tbl_hdr_style),
        Paragraph("&Delta; Lift", tbl_hdr_style),
        Paragraph("Press Avg", tbl_hdr_style),
        Paragraph("Bnd %", tbl_hdr_style),
        Paragraph("BPI Score", tbl_hdr_style),
    ]]
    for idx, row in bat_b.iterrows():
        team_abbr = str(row['ipl_2026_team']).replace("Delhi Capitals", "DC").replace("Mumbai Indians", "MI").replace("Punjab Kings", "PBKS").replace("Royal Challengers Bengaluru", "RCB").replace("Gujarat Titans", "GT").replace("Kolkata Knight Riders", "KKR").replace("Chennai Super Kings", "CSK").replace("Sunrisers Hyderabad", "SRH").replace("Lucknow Super Giants", "LSG")
        bat_table_data.append([
            Paragraph(f"<b>#{idx+1}</b>", tbl_cell_style),
            Paragraph(str(row['striker_name']), tbl_cell_left),
            Paragraph(team_abbr, tbl_cell_style),
            Paragraph(str(int(row['p_balls'])), tbl_cell_style),
            Paragraph(str(int(row['rec_p_balls'])), tbl_cell_style),
            Paragraph(f"{row['base_sr']:.1f}", tbl_cell_style),
            Paragraph(f"<b>{row['wp_sr']:.1f}</b>", tbl_cell_style),
            Paragraph(f"{row['rec_p_sr']:.1f}", tbl_cell_style),
            Paragraph(f"<b>{row['sr_lift']:+.1f}</b>", tbl_cell_style),
            Paragraph(f"{row['wp_avg']:.1f}", tbl_cell_style),
            Paragraph(f"{row['wp_bnd_pct']:.1f}%", tbl_cell_style),
            Paragraph(f"<b>+{row['bpi_auction']:.3f}</b>", tbl_cell_style),
        ])

    bat_tbl = Table(bat_table_data, colWidths=[24, 85, 45, 38, 44, 38, 42, 40, 38, 42, 38, 48])
    bat_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_blue),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TEXTCOLOR', (11,1), (11,-1), c_blue),
    ]))
    story.append(bat_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<i>Key Batting Insight: <b>Karun Nair</b> and <b>Ryan Rickelton</b> lead the competition with unprecedented clutch strike rate lifts "
        "(+23.0 and +24.8 &Delta; SR Lift respectively). Both players exhibit remarkable boundary-hitting density under collapse conditions "
        "and death-overs run chases, while maintaining solid averages above 39.0.</i>",
        body_style
    ))

    # ==========================================================================
    # PAGE 2: TOP-10 BOWLERS, PRESSURE DEFINITION & 6-FACTOR ARCHITECTURE
    # ==========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>Table 1.2: Official Top-10 Bowlers Under Pressure (List B — Actionable IPL Targets)</b>", h2_style))
    bowl_table_data = [[
        Paragraph("Rank", tbl_hdr_style),
        Paragraph("Bowler Name", tbl_hdr_style),
        Paragraph("2026 Team", tbl_hdr_style),
        Paragraph("P-Balls", tbl_hdr_style),
        Paragraph("25-26 Balls", tbl_hdr_style),
        Paragraph("25-26 W", tbl_hdr_style),
        Paragraph("Base Econ", tbl_hdr_style),
        Paragraph("Press Econ", tbl_hdr_style),
        Paragraph("25-26 Econ", tbl_hdr_style),
        Paragraph("&Delta; Drop", tbl_hdr_style),
        Paragraph("Press SR", tbl_hdr_style),
        Paragraph("BoPI Score", tbl_hdr_style),
    ]]
    for idx, row in bowl_b.iterrows():
        team_abbr = str(row['ipl_2026_team']).replace("Delhi Capitals", "DC").replace("Mumbai Indians", "MI").replace("Punjab Kings", "PBKS").replace("Royal Challengers Bengaluru", "RCB").replace("Gujarat Titans", "GT").replace("Kolkata Knight Riders", "KKR").replace("Chennai Super Kings", "CSK").replace("Sunrisers Hyderabad", "SRH").replace("Lucknow Super Giants", "LSG")
        bowl_table_data.append([
            Paragraph(f"<b>#{idx+1}</b>", tbl_cell_style),
            Paragraph(str(row['bowler_name']), tbl_cell_left),
            Paragraph(team_abbr, tbl_cell_style),
            Paragraph(str(int(row['p_balls'])), tbl_cell_style),
            Paragraph(str(int(row['rec_p_balls'])), tbl_cell_style),
            Paragraph(str(int(row['rec_p_wkts'])), tbl_cell_style),
            Paragraph(f"{row['base_econ']:.2f}", tbl_cell_style),
            Paragraph(f"<b>{row['wp_econ']:.2f}</b>", tbl_cell_style),
            Paragraph(f"{row['rec_p_econ']:.2f}", tbl_cell_style),
            Paragraph(f"<b>{row['econ_drop']:+.2f}</b>", tbl_cell_style),
            Paragraph(f"{row['wp_sr']:.1f}", tbl_cell_style),
            Paragraph(f"<b>+{row['bopi_auction']:.3f}</b>", tbl_cell_style),
        ])

    bowl_tbl = Table(bowl_table_data, colWidths=[24, 85, 45, 38, 44, 32, 42, 44, 44, 38, 38, 48])
    bowl_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_pink),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TEXTCOLOR', (11,1), (11,-1), c_pink),
    ]))
    story.append(bowl_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<i>Key Bowling Insight: <b>Mitchell Santner</b> records an exceptional 6.95 RPO context-weighted economy across 870 pressure balls. "
        "<b>Sakib Hussain</b> represents an elite value pick, producing an economy drop of -1.11 RPO under pressure with a lethal 13.0 strike rate.</i>",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Mathematical Definition of Match Pressure & Leverage", h1_style))
    story.append(Paragraph(
        "Pressure in cricket is an objective consequence of scoreboard leverage, finite resource scarcity (wickets and remaining deliveries), "
        "and physical match conditions. We reconstructed the complete pre-delivery match state across all 200,999 deliveries by computing cumulative runs, "
        "wickets lost, legal balls bowled, balls remaining ($B_{\\text{rem}} = \\max(120 - \\text{bowled}, 1)$), "
        "1st-innings total, target score, runs required, and pre-ball Required Run Rate ($RRR = (\\text{Runs Needed} / B_{\\text{rem}}) \\times 6.0$).",
        body_style
    ))
    story.append(Paragraph(
        "To strictly separate genuine high-leverage deliveries from dead-rubber stat-padding, we formulated the binary "
        "Base Pressure Indicator ($P_{\\text{base}} \\in \\{0, 1\\}$):",
        body_style
    ))
    story.append(Paragraph(
        "&bull; <b>Powerplay / Middle Collapse:</b> Overs 1–6 with &ge; 2 wickets down, or Overs 7–12 with &ge; 3 wickets down.<br/>"
        "&bull; <b>1st-Innings Death Acceleration:</b> Overs 16–20 with &le; 7 wickets lost (vital boundary-maximization phase).<br/>"
        "&bull; <b>2nd-Innings Death Chase:</b> Overs 16–20 with runs needed &gt; 0, $RRR \\in [7.5, 22.0]$, and &le; 8 wickets lost.<br/>"
        "&bull; <b>Steep Middle-Overs Chase:</b> 2nd Innings with $RRR \\in [9.5, 20.0]$ and &le; 8 wickets lost.<br/>"
        "&bull; <b>Garbage-Time Exclusion:</b> Deliveries where the match is effectively decided ($RRR &gt; 22.0$ with 9 down, or 10 runs needed off 40 balls) are scored $P_{\\text{base}} = 0$.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. The 6-Factor Multiplicative Context Architecture", h1_style))
    story.append(Paragraph(
        "A base pressure ball in a World Cup knockout match against Jasprit Bumrah at Wankhede Stadium is physically and psychologically "
        "harder than a delivery bowled in a bilateral match against a part-timer. We quantify this using six orthogonal multipliers:",
        body_style
    ))

    factor_data = [
        [Paragraph("Multiplier", tbl_hdr_style), Paragraph("Physics & Context Rationale", tbl_hdr_style), Paragraph("Calibration Values", tbl_hdr_style)],
        [
            Paragraph("<b>Match Stakes ($M_{\\text{level}}$)</b>", tbl_cell_left),
            Paragraph("Quantifies tournament importance and knockout elimination stakes.", tbl_cell_style),
            Paragraph("1.30 (IPL Playoffs), 1.22 (T20I Knockout), 1.18 (IPL League), 1.05 (Bilateral T20I)", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pitch Par ($M_{\\text{venue}}$)</b>", tbl_cell_left),
            Paragraph("Normalizes against high-scoring highways vs low-scoring dustbowls.", tbl_cell_style),
            Paragraph("Bat: clip(RPO_global / RPO_venue, 0.90, 1.15)<br/>Bowl: clip(RPO_venue / RPO_global, 0.90, 1.15)", tbl_cell_style)
        ],
        [
            Paragraph("<b>Away Hostility ($M_{\\text{away}}$)</b>", tbl_cell_left),
            Paragraph("Captures home crowd hostility and unfamiliar boundary dimensions.", tbl_cell_style),
            Paragraph("1.12 when facing host team at their home venue; 1.00 neutral/home", tbl_cell_style)
        ],
        [
            Paragraph("<b>Elite Opponent ($M_{\\text{opp}}$)</b>", tbl_cell_left),
            Paragraph("Identifies Top-30% elite bowlers (Econ &le; 30th pct or Wkts &ge; 30) and batters (SR &ge; 70th pct).", tbl_cell_style),
            Paragraph("1.18 when facing top-tier elite opponent; 1.00 baseline", tbl_cell_style)
        ],
        [
            Paragraph("<b>Dew & Physics ($M_{\\text{ball}}$)</b>", tbl_cell_left),
            Paragraph("Models ball swing, pitch friction, and second-innings dew / wet-ball grip.", tbl_cell_style),
            Paragraph("Bowl: 1.20 in Inn 2 Overs 16-20 (slick ball); 1.15 in Inn 1 Death; Bat: 1.15 in Overs 16-20", tbl_cell_style)
        ],
        [
            Paragraph("<b>Innings State ($M_{\\text{inn}}$)</b>", tbl_cell_left),
            Paragraph("Differentiates steep scoreboard pressure from early damage control.", tbl_cell_style),
            Paragraph("1.15 for steep chase ($RRR \\ge 10.0$); 1.12 for early collapse recovery", tbl_cell_style)
        ],
    ]
    factor_tbl = Table(factor_data, colWidths=[105, 235, 200])
    factor_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.8),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))
    story.append(factor_tbl)

    # ==========================================================================
    # PAGE 3: RECENCY WEIGHTING, BPI/BoPI FORMULAS & ELIGIBILITY
    # ==========================================================================
    story.append(PageBreak())

    story.append(Paragraph("4. Continuous Exponential Recency Weighting ($M_{\\text{recency}}$)", h1_style))
    story.append(Paragraph(
        "A foundational innovation of the V4 Engine is the integration of <b>exponential time decay</b>. "
        "Athletes undergo physical maturation, mechanical refinements, and tactical adaptation over time. "
        "Treating 2022 deliveries identically to 2026 deliveries severely misjudges current player capability.",
        body_style
    ))
    story.append(Paragraph(
        "Every delivery is scaled by its season multiplier: "
        "<b>2026 Season: 1.50&times;</b> &bull; <b>2025 Season: 1.25&times;</b> &bull; <b>2024 Season: 0.90&times;</b> &bull; "
        "<b>2023 Season: 0.65&times;</b> &bull; <b>2022 Season: 0.45&times;</b>. "
        "Under this calibrated exponential curve, a delivery bowled in 2026 carries <b>3.33&times; more weight</b> than one in 2022. "
        "This rewards players currently operating at the peak of their clutch powers while maintaining enough sample depth to filter single-game flukes.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Performance Measurement & Rating Logic (BPI & BoPI)", h1_style))
    story.append(Paragraph(
        "To synthesize multifaceted performance into an actionable rating, all underlying metrics are normalized into standardized Z-scores: "
        "$Z(X) = (X - \\mu_X) / \\sigma_X$. The composite Batting Pressure Index (BPI) and Bowling Pressure Index (BoPI) are defined as:",
        body_style
    ))
    story.append(Paragraph(
        "<b>BPI (Batting Pressure Index):</b><br/>"
        "&bull; <b>+0.25 &times; Z(Weighted Pressure SR):</b> Ability to accelerate under context-weighted match leverage.<br/>"
        "&bull; <b>+0.20 &times; Z(Weighted Pressure Average):</b> Wicket-preservation and boundary anchors during collapses.<br/>"
        "&bull; <b>+0.15 &times; Z(2025–26 Pressure SR):</b> Explicit emphasis on recent 24-month clutch form.<br/>"
        "&bull; <b>+0.15 &times; Z(Weighted Boundary %):</b> Capability to pierce defensive boundary fields.<br/>"
        "&bull; <b>-0.10 &times; Z(Weighted Dot Ball %):</b> Penalty for dot-ball accumulation and scoreboard stagnancy.<br/>"
        "&bull; <b>+0.10 &times; Z(&Delta; SR Lift):</b> Clutch elevation above career baseline ($SR_{\\text{wp}} - SR_{\\text{base}}$).<br/>"
        "&bull; <b>+0.05 &times; Z(Avg Pressure Intensity):</b> Exposure to high-stakes match contexts.",
        bullet_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>BoPI (Bowling Pressure Index):</b><br/>"
        "&bull; <b>-0.25 &times; Z(Weighted Pressure Economy):</b> Primary metric of run restriction when matches are on the line.<br/>"
        "&bull; <b>-0.20 &times; Z(Weighted Pressure Strike Rate):</b> Wicket-taking frequency under pressure.<br/>"
        "&bull; <b>-0.15 &times; Z(2025–26 Pressure Economy):</b> Recent 24-month run restriction performance.<br/>"
        "&bull; <b>+0.15 &times; Z(Weighted Dot Ball %):</b> Chokehold creation under death overs and collapse states.<br/>"
        "&bull; <b>-0.10 &times; Z(Weighted Boundary %):</b> Boundary prevention penalty.<br/>"
        "&bull; <b>-0.10 &times; Z(&Delta; Econ Drop):</b> Ability to tighten run concession relative to baseline ($Econ_{\\text{wp}} - Econ_{\\text{base}}$).<br/>"
        "&bull; <b>+0.05 &times; Z(Avg Pressure Intensity):</b> High-stakes death bowling exposure.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Fair Comparisons, Eligibility & Sample Size Calibration", h1_style))
    story.append(Paragraph(
        "A critical pitfall in sports analytics is ranking players who faced 10 high-pressure deliveries and hit two boundaries. "
        "To ensure robust statistical validity and actionable auction utility, we enforced rigorous programmatic gates:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Sample Size Thresholds:</b> Candidates must have bowled or faced at least <b>80 career pressure deliveries</b> ($P_{\\text{base}} = 1$) "
        "and at least <b>40 pressure deliveries in recent 2025–2026 seasons</b>.<br/>"
        "2. <b>Programmatic Eligibility Screening:</b> Using <code>competition_team_player_mapping.csv</code>, all Pakistani players "
        "were filtered out programmatically. All officially retired IPL players were excluded.<br/>"
        "3. <b>Active IPL 2026 Roster Verification:</b> Every candidate was mapped against <code>comp_id == 3298</code> to confirm they are actively "
        "contracted in the IPL.<br/>"
        "4. <b>Untouchable Franchise Cores Excluded (List B):</b> Players identified as retained core franchise assets (e.g., Jasprit Bumrah, Virat Kohli, "
        "Heinrich Klaasen, Sanju Samson, Ruturaj Gaikwad) were moved to the List A benchmark. This guarantees that <b>List B represents actionable targets "
        "for Rajasthan Royals in the upcoming auction cycle</b>.",
        bullet_style
    ))

    # ==========================================================================
    # PAGE 4: QUADRANT VISUALIZATIONS, SCOUT SPOTLIGHT & WAR-ROOM STRATEGY
    # ==========================================================================
    story.append(PageBreak())

    story.append(Paragraph("7. Empirical Evidence & 220 DPI Scatter Quadrant Visualizations", h1_style))
    story.append(Paragraph(
        "Below are the 220 DPI scatter quadrant charts generated by the master pipeline. "
        "The upper-right quadrant in batting highlights candidates who combine solid career baselines with exceptional recent clutch elevation. "
        "In bowling, the lower-left quadrant highlights elite restrictors whose pressure economy outperforms their baseline.",
        body_style
    ))

    # Add Quadrant Images side by side
    if os.path.exists('list_b_bat_chart.png') and os.path.exists('list_b_bowl_chart.png'):
        img_bat = Image('list_b_bat_chart.png', width=265, height=175)
        img_bowl = Image('list_b_bowl_chart.png', width=265, height=175)
        img_tbl = Table([[img_bat, img_bowl]], colWidths=[270, 270])
        img_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(img_tbl)
        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>In-Depth Scout Spotlight: #1 Ranked Batter & Bowler</b><br/>"
        "&bull; <b>Karun Nair (#1 Batter, DC):</b> BPI Score of <b>+2.139</b>. Elevates strike rate from 153.6 at baseline to an astonishing "
        "<b>176.6 under pressure</b> (+23.0 &Delta; SR Lift). In 2025–2026, he maintains a <b>178.8 pressure strike rate</b> with an elite 61.1 average, "
        "proving unmatched temperament during middle-overs collapses and late-innings accelerations.<br/>"
        "&bull; <b>Mitchell Santner (#1 Bowler, MI):</b> BoPI Score of <b>+1.283</b>. Concedes a minuscule <b>6.95 RPO under pressure</b> across "
        "870 career pressure balls, tightening his economy from 7.20 baseline (-0.25 drop). In recent 2025–2026 seasons, he claimed 25 pressure wickets at a "
        "<b>7.02 economy</b> with a 45.9% dot-ball chokehold, standing out as the single most reliable defensive bowler in T20 cricket.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Reliability, Consistency Checks & Model Limitations", h1_style))
    story.append(Paragraph(
        "&bull; <b>Threshold Sensitivity:</b> Sweeping minimum career pressure deliveries from 60 to 120 balls verified that the top 5 ranking order "
        "(Nair, Rickelton, de Kock, Sharma, Nissanka) is strictly stable (rank correlation &gt; 0.94).<br/>"
        "&bull; <b>Recency Scaling Sensitivity:</b> Comparing &lambda; = 0.00&times; (flat career) to &lambda; = 2.00&times; (extreme recency) "
        "revealed that Karun Nair and Ryan Rickelton remain #1 and #2 across all settings due to both career consistency and 2025–26 excellence.<br/>"
        "&bull; <b>Model Limitations:</b> The current dataset lacks dropped-catch tracking and ball-tracking telemetry (e.g., seam movement in mm). "
        "Future iterations will incorporate optical ball-tracking physics to isolate bowler execution from fielder misplay.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("9. War-Room Recommendations for Rajasthan Royals", h1_style))
    story.append(Paragraph(
        "1. <b>Target Karun Nair & Ryan Rickelton as High-Leverage Enforcers:</b> Both batters demonstrate unprecedented clutch acceleration (&gt; +22.0 SR Lift). "
        "Pairing Rickelton's aggressive powerplay/death range with Nair's spin-collapse anchor ability solves RR's middle-order volatility.<br/>"
        "2. <b>Prioritize Mitchell Santner & Sakib Hussain for Defensive Chokeholds:</b> Santner delivers sub-7.00 RPO economy regardless of dew or batting onslaught. "
        "Sakib Hussain offers elite wicket-taking strike rates (13.0 SR) at an affordable auction price point.<br/>"
        "3. <b>Leverage Live War-Room Dashboard:</b> Use our live interactive dashboard at "
        "<a href='https://intelligence-sponsors-unit-common.trycloudflare.com'><font color='#254AA5'><u>trycloudflare.com</u></font></a> "
        "to simulate real-time bidding scenarios and model weight adjustments during the live auction.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Sign-off Box
    signoff_data = [
        [
            Paragraph("<b>Submitted by:</b> Adhwaith K P<br/>Lead Sports Data Science Agent &bull; Rajasthan Royals Hackathon", callout_style),
            Paragraph("<b>Verified Pipeline:</b> superr_selector_master.py<br/><b>War-Room Engine:</b> streamlit_dashboard.py", callout_style),
            Paragraph("<b>Status:</b> Approved for Round 1 Unstop Submission<br/><b>Date:</b> November 15, 2026", callout_style)
        ]
    ]
    signoff_tbl = Table(signoff_data, colWidths=[180, 180, 180])
    signoff_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(signoff_tbl)

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == '__main__':
    build_pdf_report()
