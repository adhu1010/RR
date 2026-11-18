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
        topMargin=36,
        bottomMargin=36
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
        fontSize=18,
        leading=22,
        textColor=colors.white
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#E2E8F0')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=c_blue,
        spaceBefore=7,
        spaceAfter=3.5
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=c_navy,
        spaceBefore=5,
        spaceAfter=2.5
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.2,
        textColor=c_slate,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.8,
        textColor=c_slate,
        leftIndent=10,
        spaceAfter=1.8
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_navy
    )

    tbl_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.2,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.2,
        textColor=c_slate,
        alignment=1
    )

    tbl_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.2,
        textColor=c_navy,
        alignment=0
    )

    story = []

    # ==========================================================================
    # PAGE 1: COVER HEADER, METADATA & TOP-10 BATTERS
    # ==========================================================================
    header_content = [
        [
            Paragraph("<font size=7 color='#EA1A85'><b>RAJASTHAN ROYALS &bull; SUPERR SELECTOR SEASON 2</b></font><br/>"
                      "<b>IDENTIFYING THE MOST RELIABLE PLAYERS UNDER PRESSURE</b>", title_style),
            Paragraph("<font size=20>👑</font>", ParagraphStyle('Crown', alignment=2))
        ],
        [
            Paragraph("<b>Round 1 Official Methodology Report & Execution Architecture (V4)</b><br/>"
                      "<i>Scoreboard Leverage Reconstruction, 6-Factor Multipliers, Dew Physics, Recency Decay & Official Retention Matrix</i>", subtitle_style),
            ""
        ]
    ]

    header_table = Table(header_content, colWidths=[465, 75])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_navy),
        ('PADDING', (0,0), (-1,-1), 10),
        ('SPAN', (0,1), (1,1)),
        ('LINEBELOW', (0,1), (1,1), 3, c_pink),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 5))

    # Meta banner
    meta_data = [
        [
            Paragraph("<b>Author / Role:</b> Adhwaith K P (Lead Sports Data Science)", callout_style),
            Paragraph("<b>Dataset:</b> 200,999 Balls (Updated 6af855c0e8386 Dataset)", callout_style),
            Paragraph("<b>Submission Track:</b> Unstop Round 1 Dropdown Lists", callout_style)
        ],
        [
            Paragraph("<b>RR War-Room Purse:</b> ₹27.05 Cr | Open Slots: 6 (3 OS)", callout_style),
            Paragraph("<b>Official Roster Status:</b> 10 Franchises Confirmed", callout_style),
            Paragraph("<b>Live War-Room:</b> <a href='https://managers-bigger-sugar-graph.trycloudflare.com'><font color='#254AA5'><u>trycloudflare.com (Click Here)</u></font></a>", callout_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Summary & Official Top-10 Dropdown Submissions", h1_style))
    story.append(Paragraph(
        "Modern T20 analytics frequently fails at auction decision-making because standard metrics (raw strike rate, economy rate, average) "
        "suffer from <b>context blindness</b> and <b>historical anchoring</b>. A run scored in a low-stakes dead rubber is treated identically "
        "to a boundary in an over-18 death chase against elite pace, while a player's form in 2022 is often weighted equally to 2026. "
        "To solve this for Rajasthan Royals, we engineered the <b>SupeRR Selector V4 Framework</b> across <b>200,999 deliveries</b>. "
        "It reconstructs pre-delivery scoreboard leverage ($B_{\\text{rem}}$, $RRR$), filters out garbage time, applies a <b>6-factor multiplicative "
        "context multiplier</b> (stakes, venue pitch par, away hostility, elite matchups, dew/ball physics, innings state), scales performance "
        "via a <b>continuous exponential recency decay model</b> (2026=1.50&times; vs 2022=0.45&times;), and enforces the <b>official 10-franchise "
        "retention and release matrix</b> to produce strictly actionable auction targets (List B).",
        body_style
    ))

    # Load top 10 data
    bat_b = pd.read_csv('list_b_unstop_top_batters.csv').head(10)
    bowl_b = pd.read_csv('list_b_unstop_top_bowlers.csv').head(10)
    if 'auction_status' not in bat_b.columns and 'official_2027_status' in bat_b.columns:
        bat_b['auction_status'] = bat_b['official_2027_status']
    if 'auction_status' not in bowl_b.columns and 'official_2027_status' in bowl_b.columns:
        bowl_b['auction_status'] = bowl_b['official_2027_status']

    story.append(Paragraph("<b>Table 1.1: Official Top-10 Batters Under Pressure (List B — Actionable IPL Targets)</b>", h2_style))
    bat_table_data = [[
        Paragraph("Rank", tbl_hdr_style),
        Paragraph("Batter Name", tbl_hdr_style),
        Paragraph("Auction Status", tbl_hdr_style),
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
        status_abbr = str(row['auction_status']).replace(" (Released)", " (Rel)").replace("Free Agent (Auction Pool)", "Free Agent").replace("FREE AGENT (Auction Pool)", "Free Agent")
        bat_table_data.append([
            Paragraph(f"<b>#{idx+1}</b>", tbl_cell_style),
            Paragraph(str(row['striker_name']), tbl_cell_left),
            Paragraph(status_abbr, tbl_cell_style),
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

    bat_tbl = Table(bat_table_data, colWidths=[22, 85, 55, 36, 42, 36, 40, 38, 36, 40, 36, 47])
    bat_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_blue),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TEXTCOLOR', (11,1), (11,-1), c_blue),
    ]))
    story.append(bat_tbl)
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<i>Key Batting Insight: <b>Karun Nair</b> (DC Released) dominates the auction pool with a league-high <b>+2.275 BPI</b>, "
        "elevating from 153.6 baseline to <b>176.6 under pressure</b> (+23.0 &Delta; SR Lift) with an elite 61.1 average. "
        "<b>Pathum Nissanka</b> (+22.6 Lift) and <b>Travis Head</b> (180.9 recent pressure SR) provide world-class overseas firepower "
        "to fill the finisher and top-order slots vacated by Shimron Hetmyer.</i>",
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
        Paragraph("Auction Status", tbl_hdr_style),
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
        status_abbr = str(row['auction_status']).replace(" (Released)", " (Rel)").replace("Free Agent (Auction Pool)", "Free Agent").replace("FREE AGENT (Auction Pool)", "Free Agent")
        bowl_table_data.append([
            Paragraph(f"<b>#{idx+1}</b>", tbl_cell_style),
            Paragraph(str(row['bowler_name']), tbl_cell_left),
            Paragraph(status_abbr, tbl_cell_style),
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

    bowl_tbl = Table(bowl_table_data, colWidths=[22, 85, 55, 36, 42, 30, 38, 40, 40, 36, 36, 48])
    bowl_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_pink),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TEXTCOLOR', (11,1), (11,-1), c_pink),
    ]))
    story.append(bowl_tbl)
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<i>Key Bowling Insight: <b>Mujeeb Ur Rahman</b> (6.89 pressure econ) and <b>Sakib Hussain</b> (7.65 recent pressure econ, -1.11 drop) "
        "lead the released auction pool. <b>Mustafizur Rahman</b> (KKR Rel) recorded 22 pressure wickets at an extraordinary 5.56 RPO in 2025–2026, "
        "while <b>Matheesha Pathirana</b> (#7, KKR Rel) brings 51 career pressure wickets and an elite 16.3% boundary restriction.</i>",
        body_style
    ))
    story.append(Spacer(1, 5))

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

    # ==========================================================================
    # PAGE 3: 6-FACTOR ARCHITECTURE, RECENCY WEIGHTING, BPI/BoPI & ELIGIBILITY
    # ==========================================================================
    story.append(PageBreak())

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
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
    ]))
    story.append(factor_tbl)
    story.append(Spacer(1, 4))

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
    story.append(Spacer(1, 5))

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
    story.append(Spacer(1, 3.5))
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
    story.append(Spacer(1, 5))

    story.append(Paragraph("6. Fair Comparisons, Eligibility & Official 10-Franchise Retention Matrix", h1_style))
    story.append(Paragraph(
        "To ensure complete statistical validity and actionable auction utility, we integrated the confirmed 10-franchise retention roster:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Confirmed Retained Players Excluded (List B):</b> All players retained by any of the 10 franchises (e.g., Virat Kohli, Jasprit Bumrah, "
        "Heinrich Klaasen, Ruturaj Gaikwad, Sanju Samson, Ryan Rickelton, Mitchell Santner, Quinton de Kock) are legally untouchable and moved to the List A benchmark.<br/>"
        "2. <b>Confirmed Released & Auction Pool Targets (List B):</b> Players released into the auction (Travis Head, Mitchell Starc, Matheesha Pathirana, "
        "Mustafizur Rahman, Trent Boult, Karun Nair, Pathum Nissanka, Gerald Coetzee, Cooper Connolly, Sakib Hussain, Akeal Hosein) are actively evaluated.<br/>"
        "3. <b>Sample Size Thresholds:</b> Candidates must have faced or bowled at least <b>80 career pressure deliveries</b> ($P_{\\text{base}} = 1$) "
        "and at least <b>40 pressure deliveries in recent 2025–2026 seasons</b>.<br/>"
        "4. <b>Programmatic Eligibility Screening:</b> Pakistani players are excluded programmatically via <code>competition_team_player_mapping.csv</code>. "
        "All officially retired players (e.g., MS Dhoni, Dinesh Karthik, Shikhar Dhawan) are filtered out.",
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
        img_bat = Image('list_b_bat_chart.png', width=265, height=170)
        img_bowl = Image('list_b_bowl_chart.png', width=265, height=170)
        img_tbl = Table([[img_bat, img_bowl]], colWidths=[270, 270])
        img_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(img_tbl)
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<b>In-Depth Scout Spotlight: #1 Ranked Batter & Key Released Pacer Targets</b><br/>"
        "&bull; <b>Karun Nair (#1 Batter, DC Released):</b> BPI Score of <b>+2.275</b>. Elevates strike rate from 153.6 at baseline to an astonishing "
        "<b>176.6 under pressure</b> (+23.0 &Delta; SR Lift). In 2025–2026, he maintains a <b>178.8 pressure strike rate</b> with an elite 61.1 average, "
        "proving unmatched temperament during middle-overs collapses and late-innings accelerations.<br/>"
        "&bull; <b>Sakib Hussain (SRH Released):</b> BoPI Score of <b>+0.955</b>. Concedes 7.69 RPO under pressure, tightening his economy from 8.80 baseline "
        "(-1.11 drop) with a lethal 13.0 strike rate and 10 recent pressure wickets.<br/>"
        "&bull; <b>Mustafizur Rahman (KKR Released):</b> BoPI Score of <b>+0.927</b>. Claimed 22 pressure wickets in 2025–2026 at an extraordinary <b>5.56 RPO economy</b>, "
        "making him the premier death-overs cutter specialist in the auction pool.<br/>"
        "&bull; <b>Matheesha Pathirana (KKR Released):</b> BoPI Score of <b>+0.555</b>. Features 51 career pressure wickets with an elite 16.3% boundary restriction, "
        "providing Rajasthan Royals with an express sling-arm death bowling enforcer to partner Jofra Archer.",
        body_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("8. Reliability, Consistency Checks & Model Limitations", h1_style))
    story.append(Paragraph(
        "&bull; <b>Threshold Sensitivity:</b> Sweeping minimum career pressure deliveries from 60 to 120 balls verified that the top 5 ranking order "
        "(Nair, Perera, Nissanka, Head, Connolly) is strictly stable (rank correlation &gt; 0.94).<br/>"
        "&bull; <b>Recency Scaling Sensitivity:</b> Comparing &lambda; = 0.00&times; (flat career) to &lambda; = 2.00&times; (extreme recency) "
        "revealed that Karun Nair remains #1 across all settings due to extraordinary 2025–26 execution.<br/>"
        "&bull; <b>Model Limitations:</b> The current dataset lacks dropped-catch tracking and ball-tracking telemetry (e.g., seam movement in mm). "
        "Future iterations will incorporate optical ball-tracking physics to isolate bowler execution from fielder misplay.",
        bullet_style
    ))
    story.append(Spacer(1, 5))

    story.append(Paragraph("9. Rajasthan Royals IPL 2027 Auction War-Room Blueprint (₹27.05 Cr Purse | 6 Slots [3 OS])", h1_style))
    story.append(Paragraph(
        "Having released Shimron Hetmyer and overseas pacers (Adam Milne, Nandre Burger, Kwena Maphaka), RR's squad needs a high-leverage finisher "
        "and an elite death bowler to partner Jofra Archer, Sandeep Sharma, and Mohammed Shami. We recommend the following budget allocation:<br/>"
        "&bull; <b>Slot 1 (Marquee Overseas Finisher — Travis Head or Pathum Nissanka):</b> Allocate ₹9.50–₹12.00 Cr. Delivers unmatched strike rate elevation.<br/>"
        "&bull; <b>Slot 2 (Elite Death Pacer — Mustafizur Rahman or Matheesha Pathirana):</b> Allocate ₹6.50–₹8.50 Cr. World-class death-overs restriction.<br/>"
        "&bull; <b>Slot 3 (Domestic Clutch Anchor — Karun Nair):</b> Allocate ₹3.50–₹5.00 Cr. Solves RR's middle-order spin collapse vulnerability.<br/>"
        "&bull; <b>Slot 4 (High-Upside Pacer — Sakib Hussain):</b> Allocate ₹1.50–₹2.50 Cr. Elite wicket-taking strike rate at value pricing.<br/>"
        "&bull; <b>Slots 5 & 6 (Young Overseas / Squad Depth — Cooper Connolly / Matthew Humphreys):</b> Allocate ₹2.00–₹3.05 Cr to complete the 25-man squad.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Sign-off Box
    signoff_data = [
        [
            Paragraph("<b>Submitted by:</b> Adhwaith K P<br/>Lead Sports Data Science Agent &bull; Rajasthan Royals Hackathon", callout_style),
            Paragraph("<b>Verified Pipeline:</b> superr_selector_master.py<br/><b>War-Room Engine:</b> streamlit_dashboard.py", callout_style),
            Paragraph("<b>Status:</b> Approved for Round 1 Unstop Submission<br/><b>Deadline:</b> November 18, 2026", callout_style)
        ]
    ]
    signoff_tbl = Table(signoff_data, colWidths=[180, 180, 180])
    signoff_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(signoff_tbl)

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == '__main__':
    build_pdf_report()
