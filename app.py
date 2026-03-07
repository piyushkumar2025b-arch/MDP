"""
╔═══════════════════════════════════════════════════════════════╗
║   CHEMOFILTER  ·  CRYSTALLINE NOIR  ·  v7  ·  VIT 2026       ║
║   Radical UI — amber-gold on midnight, frosted glass panels   ║
╚═══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from rdkit import Chem
from rdkit.Chem import (Descriptors, Draw, AllChem, DataStructs, QED,
                        rdMolDescriptors, Crippen)
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests, urllib.parse, io, base64, json, re

# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChemoFilter v7",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  CRYSTALLINE NOIR CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=IBM+Plex+Mono:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&display=swap');

:root {
  --bg:        #080c14;
  --bg2:       #0c1220;
  --bg3:       #101828;
  --glass:     rgba(255,255,255,0.03);
  --amber:     #f5a623;
  --amber2:    #ffc85a;
  --amber3:    #ffe4a0;
  --gold:      #d4a017;
  --ice:       #c8deff;
  --ice2:      #e8f2ff;
  --muted:     rgba(200,222,255,0.35);
  --muted2:    rgba(200,222,255,0.18);
  --border:    rgba(245,166,35,0.14);
  --border2:   rgba(245,166,35,0.07);
  --red:       #ff5c5c;
  --red2:      rgba(255,92,92,0.12);
  --green:     #4ade80;
  --green2:    rgba(74,222,128,0.12);
  --yellow:    #fcd34d;
  --yellow2:   rgba(252,211,77,0.12);
  --radius:    14px;
  --radius-sm: 8px;
}

*, *::before, *::after { box-sizing: border-box; }

/* ── BASE ── */
html, body, [class*="css"] {
  font-family: 'IBM Plex Mono', monospace;
  background: var(--bg) !important;
  color: var(--ice);
}

/* ── BACKGROUND TEXTURE ── */
[data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 120% 60% at 15% 0%,   rgba(245,166,35,0.055) 0%, transparent 55%),
    radial-gradient(ellipse 80%  50% at 85% 100%,  rgba(100,140,255,0.04) 0%, transparent 55%),
    radial-gradient(ellipse 50%  80% at 50% 50%,   rgba(245,166,35,0.015) 0%, transparent 70%),
    repeating-linear-gradient(0deg,   transparent, transparent 79px, rgba(245,166,35,0.025) 80px),
    repeating-linear-gradient(90deg,  transparent, transparent 79px, rgba(245,166,35,0.025) 80px);
  background-attachment: fixed;
}

[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(circle 1px at 20% 30%, rgba(245,166,35,0.5) 0%, transparent 1px),
    radial-gradient(circle 1px at 75% 15%, rgba(245,166,35,0.3) 0%, transparent 1px),
    radial-gradient(circle 1px at 45% 70%, rgba(245,166,35,0.4) 0%, transparent 1px),
    radial-gradient(circle 1px at 88% 55%, rgba(200,222,255,0.3) 0%, transparent 1px),
    radial-gradient(circle 1px at 10% 85%, rgba(200,222,255,0.25) 0%, transparent 1px);
  animation: twinkle 7s ease-in-out infinite alternate;
}
@keyframes twinkle {
  0%,100% { opacity:.5 } 50% { opacity:1 }
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--amber); border-radius: 2px; opacity:.4; }

/* ══════════════════════════════════════════════
   HERO BANNER
══════════════════════════════════════════════ */
.hero {
  position: relative;
  padding: 52px 60px 44px;
  margin-bottom: 32px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: linear-gradient(135deg, #0c1220 0%, #0f1a2e 60%, #0c1220 100%);
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent 0%, var(--amber) 30%, var(--amber2) 55%, var(--amber) 80%, transparent 100%);
  opacity: .7;
}
.hero::after {
  content: '';
  position: absolute; bottom: 0; left: 20%; right: 20%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(245,166,35,0.2), transparent);
}
/* giant decorative hex behind title */
.hero-hex {
  position: absolute;
  right: -20px; top: -30px;
  font-size: 18rem;
  line-height: 1;
  color: rgba(245,166,35,0.025);
  font-family: 'Playfair Display', serif;
  pointer-events: none;
  user-select: none;
  letter-spacing: -10px;
}
.hero-overline {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 5px;
  color: var(--amber);
  text-transform: uppercase;
  margin-bottom: 18px;
  display: flex; align-items: center; gap: 14px;
}
.hero-overline::before {
  content: ''; width: 40px; height: 1px; background: var(--amber); flex-shrink: 0;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 5.8rem;
  font-weight: 900;
  line-height: .92;
  letter-spacing: -2px;
  color: var(--ice2);
  text-shadow: 0 0 80px rgba(245,166,35,0.15);
}
.hero-title span {
  background: linear-gradient(135deg, var(--amber2) 0%, var(--amber) 40%, var(--gold) 70%, var(--amber2) 100%);
  background-size: 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: goldflow 5s linear infinite;
}
@keyframes goldflow { 0% { background-position:0% } 100% { background-position:200% } }
.hero-sub {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.3rem;
  font-weight: 300;
  color: var(--muted);
  letter-spacing: 2px;
  margin-top: 8px;
}
.hero-meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .58rem;
  color: rgba(245,166,35,0.35);
  letter-spacing: 3px;
  margin-top: 18px;
  text-transform: uppercase;
}
.feature-chips {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-top: 22px;
}
.chip {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .52rem; letter-spacing: 1.2px;
  padding: 3px 10px; border-radius: 3px;
  text-transform: uppercase;
}
.chip-base { background: rgba(200,222,255,.05); border: 1px solid rgba(200,222,255,.15); color: var(--muted); }
.chip-gold { background: rgba(245,166,35,.08); border: 1px solid rgba(245,166,35,.3);  color: var(--amber); font-weight: 600; }
.hero-stat-strip {
  position: absolute; right: 52px; top: 52px;
  text-align: right;
}
.hss-num {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem; font-weight: 900; line-height: 1;
  color: rgba(245,166,35,.12);
  letter-spacing: -1px;
}
.hss-lbl {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .5rem; letter-spacing: 3px; color: rgba(245,166,35,.2);
}

/* ══════════════════════════════════════════════
   STATS STRIP
══════════════════════════════════════════════ */
.stats-strip {
  display: grid;
  grid-template-columns: repeat(9,1fr);
  gap: 1px;
  margin: 0 0 28px;
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--border2);
}
.sc {
  background: var(--bg2);
  padding: 18px 6px;
  text-align: center;
  transition: background .2s;
  cursor: default;
}
.sc:hover { background: rgba(245,166,35,.04); }
.sc-val {
  font-family: 'Playfair Display', serif;
  font-size: 2rem; font-weight: 700; line-height: 1;
}
.sc-lbl {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .46rem; letter-spacing: 1.8px;
  color: var(--muted2); margin-top: 5px; text-transform: uppercase;
}

/* ══════════════════════════════════════════════
   SECTION HEADERS
══════════════════════════════════════════════ */
.sec {
  display: flex; align-items: center; gap: 16px;
  margin: 36px 0 20px;
}
.sec-num {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .5rem; color: rgba(245,166,35,.3);
  letter-spacing: 2px;
}
.sec-title {
  font-family: 'Playfair Display', serif;
  font-size: 1rem; font-weight: 700;
  color: var(--ice2); letter-spacing: .5px;
}
.sec-line { flex:1; height:1px; background: linear-gradient(90deg,var(--border),transparent); }
.sec-tag {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .5rem; letter-spacing: 2px;
  color: rgba(245,166,35,.4); text-transform: uppercase;
}

/* ══════════════════════════════════════════════
   GLASS CARDS
══════════════════════════════════════════════ */
.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  position: relative; overflow: hidden;
}
.card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(245,166,35,.35), transparent);
}
.card-inner { padding: 24px; }

/* expanded compound card */
.cpd-shell {
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--bg2);
  margin-bottom: 14px;
  overflow: hidden;
  position: relative;
  transition: border-color .3s, box-shadow .3s;
}
.cpd-shell:hover {
  border-color: rgba(245,166,35,.3);
  box-shadow: 0 8px 60px rgba(245,166,35,.06);
}
.cpd-shell::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--amber), var(--amber2), var(--ice), var(--amber));
  background-size: 200%; opacity: .5;
  animation: borderflow 4s linear infinite;
}
@keyframes borderflow { 0% { background-position:0% } 100% { background-position:200% } }

/* ══════════════════════════════════════════════
   GRADE MEDALLION
══════════════════════════════════════════════ */
.medallion-wrap { text-align: center; margin-bottom: 16px; }
.medallion {
  width: 84px; height: 84px;
  border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 2.4rem; font-weight: 900;
  position: relative;
}
.medallion::after {
  content: '';
  position: absolute; inset: -4px; border-radius: 50%;
  border: 1px solid currentColor; opacity: .25;
}
.medallion::before {
  content: '';
  position: absolute; inset: -8px; border-radius: 50%;
  border: 1px solid currentColor; opacity: .1;
}
.mA { background: rgba(74,222,128,.08);  color: #4ade80;
      box-shadow: 0 0 40px rgba(74,222,128,.2), inset 0 0 20px rgba(74,222,128,.04); }
.mB { background: rgba(245,166,35,.08);  color: var(--amber);
      box-shadow: 0 0 40px rgba(245,166,35,.2), inset 0 0 20px rgba(245,166,35,.04); }
.mC { background: rgba(252,211,77,.08);  color: var(--yellow);
      box-shadow: 0 0 40px rgba(252,211,77,.15), inset 0 0 20px rgba(252,211,77,.03); }
.mF { background: rgba(255,92,92,.08);   color: var(--red);
      box-shadow: 0 0 40px rgba(255,92,92,.2),  inset 0 0 20px rgba(255,92,92,.04); }
.med-id {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .55rem; letter-spacing: 2px;
  color: var(--muted2); margin-top: 7px;
}

/* ══════════════════════════════════════════════
   DESCRIPTOR TABLE
══════════════════════════════════════════════ */
.dtable { width:100%; border-collapse:collapse; }
.dtable tr { border-bottom: 1px solid rgba(200,222,255,.04); }
.dtable tr:last-child { border: none; }
.dtable td { padding: 5.5px 2px; vertical-align: middle; }
.dk {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .6rem; color: var(--muted2); letter-spacing: .5px;
}
.dv {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .7rem; color: var(--ice); text-align: right; font-weight: 500;
}
.ok   { color: var(--green) !important; }
.warn { color: var(--yellow) !important; }
.bad  { color: var(--red) !important; }
.hi   { color: var(--amber) !important; }

/* ══════════════════════════════════════════════
   BAR PROGRESS
══════════════════════════════════════════════ */
.bar-lbl {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .52rem; letter-spacing: 2px;
  color: var(--muted2); text-transform: uppercase; margin: 10px 0 3px;
}
.bar-track {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 2px; height: 7px; overflow: hidden; position: relative;
}
.bar-fill {
  height: 100%; border-radius: 2px;
  position: relative; transition: width .7s cubic-bezier(.34,1.56,.64,1);
}
.bar-fill::after {
  content: '';
  position: absolute; right:0; top:0; bottom:0; width:5px;
  background: rgba(255,255,255,.45); filter: blur(3px);
}
.bar-num {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .5rem; color: var(--muted2);
  text-align: right; margin-top: 2px;
}

/* ══════════════════════════════════════════════
   TOX PILLS
══════════════════════════════════════════════ */
.tpill {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 12px; border-radius: 7px;
  margin: 4px 0; font-family: 'IBM Plex Mono', monospace;
  font-size: .65rem; border-left: 3px solid;
}
.tp-ok   { background: var(--green2); border-color: var(--green); color: #bbf7d0; }
.tp-warn { background: var(--yellow2);border-color: var(--yellow);color: #fef9c3; }
.tp-bad  { background: var(--red2);   border-color: var(--red);   color: #fecaca; }

/* ══════════════════════════════════════════════
   VERDICT BANNER
══════════════════════════════════════════════ */
.verdict {
  border-radius: 10px; padding: 14px 16px;
  margin-top: 14px; position: relative; overflow: hidden;
}
.verdict::before {
  content: ''; position: absolute; top:0; left:0; right:0; height:1px;
  background: currentColor; opacity: .3;
}
.vgo   { background: var(--green2); color: var(--green); }
.vwarn { background: var(--yellow2);color: var(--yellow); }
.vstop { background: var(--red2);   color: var(--red); }
.vt { font-family:'Playfair Display',serif; font-size:.9rem; font-weight:700; }
.vb { font-family:'IBM Plex Mono',monospace; font-size:.62rem; color:var(--muted); margin-top:5px; line-height:1.7; }

/* ══════════════════════════════════════════════
   OPTIMISE BOX
══════════════════════════════════════════════ */
.opt-box {
  background: rgba(245,166,35,.03);
  border: 1px solid rgba(245,166,35,.12);
  border-radius: 10px; padding: 14px; margin-top: 12px;
}
.opt-head {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .55rem; letter-spacing: 2.5px;
  color: var(--amber); text-transform: uppercase; margin-bottom: 10px;
}
.opt-row {
  display: flex; gap: 12px;
  padding: 5px 0; border-bottom: 1px solid rgba(245,166,35,.05);
  font-size: .64rem;
}
.opt-row:last-child { border: none; }
.opt-k { color: var(--amber); font-family:'IBM Plex Mono',monospace; min-width:110px; flex-shrink:0; font-size:.6rem; }
.opt-v { color: var(--muted); line-height: 1.55; }

/* ══════════════════════════════════════════════
   AI PANELS
══════════════════════════════════════════════ */
.ai-panel {
  background: linear-gradient(135deg, rgba(245,166,35,.03), rgba(100,140,255,.02));
  border: 1px solid rgba(245,166,35,.15);
  border-radius: 12px; padding: 18px; margin: 8px 0; position: relative;
}
.ai-panel::before {
  content: '';
  position: absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, var(--amber), var(--ice), var(--amber));
  background-size: 200%; opacity:.3;
  animation: borderflow 5s linear infinite;
}
.ai-head {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .55rem; letter-spacing: 3px;
  color: var(--amber); text-transform: uppercase; margin-bottom: 12px;
  display: flex; align-items: center; gap: 10px;
}
.ai-head::after { content:''; flex:1; height:1px; background:rgba(245,166,35,.12); }
.ai-body {
  font-family: 'IBM Plex Mono', monospace;
  font-size: .7rem; color: var(--muted); line-height: 1.85;
}

/* ══════════════════════════════════════════════
   ANALOGUE CARDS
══════════════════════════════════════════════ */
.ana-card {
  background: rgba(245,166,35,.025);
  border: 1px solid rgba(245,166,35,.12);
  border-radius: 8px; padding: 12px; margin: 6px 0;
}
.ana-n { font-family:'IBM Plex Mono',monospace; font-size:.52rem; letter-spacing:2px; color:var(--muted2); margin-bottom:4px; }
.ana-ch { font-family:'Playfair Display',serif; font-size:.85rem; font-weight:600; color:var(--amber2); margin-bottom:4px; }
.ana-sm { font-family:'IBM Plex Mono',monospace; font-size:.6rem; color:var(--ice); opacity:.65; word-break:break-all; margin:4px 0; }
.ana-ex { font-family:'IBM Plex Mono',monospace; font-size:.6rem; color:var(--muted); line-height:1.5; }

/* ══════════════════════════════════════════════
   CYP ROWS
══════════════════════════════════════════════ */
.cyp-row {
  display:flex; align-items:center; justify-content:space-between;
  padding:7px 12px; border-radius:7px; margin:3px 0;
  font-family:'IBM Plex Mono',monospace; font-size:.65rem;
  border-left:3px solid;
}
.cyp-ok  { background:var(--green2); border-color:rgba(74,222,128,.4); color:#bbf7d0; }
.cyp-bad { background:var(--red2);   border-color:rgba(255,92,92,.4);  color:#fecaca; }

/* ══════════════════════════════════════════════
   REPORT BLOCKS
══════════════════════════════════════════════ */
.rblock {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px; padding: 24px; margin: 14px 0; position:relative; overflow:hidden;
}
.rblock::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, var(--amber), var(--amber2), var(--ice), var(--amber));
  background-size:200%; opacity:.4;
  animation: borderflow 5s linear infinite;
}
.rh {
  font-family:'IBM Plex Mono',monospace;
  font-size:.55rem; letter-spacing:3px; color:var(--amber);
  text-transform:uppercase; margin-bottom:12px; padding-bottom:7px;
  border-bottom:1px solid rgba(245,166,35,.08);
}
.rrow { display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(200,222,255,.03); font-size:.7rem; }
.rrow:last-child { border:none; }
.rk { color:var(--muted2); font-family:'IBM Plex Mono',monospace; }
.rv { color:var(--ice); }

/* ══════════════════════════════════════════════
   REFERENCE BOX
══════════════════════════════════════════════ */
.ref-box {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 18px; padding: 22px 28px; margin-bottom: 28px;
  position:relative; overflow:hidden;
}
.ref-box::before {
  content:'GOLD STANDARD REFERENCE';
  position:absolute; top:12px; right:18px;
  font-family:'IBM Plex Mono',monospace; font-size:.48rem; letter-spacing:2.5px;
  color:rgba(245,166,35,.25); text-transform:uppercase;
}
.ref-name {
  font-family:'Playfair Display',serif;
  font-size:1.2rem; font-weight:700; color:var(--amber2); margin-bottom:4px;
}

/* ══════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: #070b12 !important;
  border-right: 1px solid var(--border2) !important;
}
section[data-testid="stSidebar"] .stTextArea textarea {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--amber2) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: .7rem !important; caret-color: var(--amber);
  border-radius: var(--radius-sm) !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus {
  border-color: rgba(245,166,35,.45) !important;
  box-shadow: 0 0 20px rgba(245,166,35,.06) !important;
}
section[data-testid="stSidebar"] label {
  color: rgba(245,166,35,.55) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: .6rem !important; letter-spacing: 1.8px !important;
}

/* ══════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════ */
.stButton > button, .stDownloadButton > button {
  background: transparent !important;
  border: 1px solid rgba(245,166,35,.3) !important;
  color: var(--amber) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: .6rem !important; letter-spacing: 2px !important;
  text-transform: uppercase !important; border-radius: 6px !important;
  padding: 9px 22px !important; transition: all .25s !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background: rgba(245,166,35,.08) !important;
  border-color: var(--amber) !important;
  box-shadow: 0 0 24px rgba(245,166,35,.18) !important;
}

/* ══════════════════════════════════════════════
   TABS
══════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border2) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted2) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: .6rem !important; letter-spacing: 2px !important;
  text-transform: uppercase !important;
  border-bottom: 2px solid transparent !important;
  padding: 11px 20px !important; transition: all .2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--amber2) !important; }
.stTabs [aria-selected="true"] {
  color: var(--amber) !important;
  border-bottom-color: var(--amber) !important;
  background: rgba(245,166,35,.04) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: transparent !important; padding-top: 26px !important;
}

/* ══════════════════════════════════════════════
   EXPANDERS
══════════════════════════════════════════════ */
.streamlit-expanderHeader {
  background: rgba(245,166,35,.03) !important;
  border: 1px solid var(--border) !important; border-radius: 8px !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: .62rem !important; color: rgba(245,166,35,.55) !important;
  letter-spacing: 1.5px !important;
}
.streamlit-expanderHeader:hover { border-color: rgba(245,166,35,.28) !important; color: var(--amber) !important; }

/* ══════════════════════════════════════════════
   SELECTBOX / SLIDERS
══════════════════════════════════════════════ */
.stSelectbox > div > div {
  background: var(--bg2) !important; border: 1px solid var(--border) !important;
  color: var(--amber2) !important; font-family:'IBM Plex Mono',monospace !important;
  font-size: .72rem !important; border-radius: var(--radius-sm) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
  background: var(--amber) !important;
}

/* ══════════════════════════════════════════════
   DATAFRAME
══════════════════════════════════════════════ */
.stDataFrame iframe { border-radius: 12px !important; }
[data-testid="stDataFrameContainer"] {
  border: 1px solid var(--border) !important; border-radius: 12px !important;
}

/* ══════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════ */
.stSuccess { background:var(--green2) !important; border:1px solid rgba(74,222,128,.25) !important; border-radius:8px !important; color:var(--green) !important; }
.stError   { background:var(--red2)   !important; border:1px solid rgba(255,92,92,.25)  !important; border-radius:8px !important; }
.stInfo    { background:rgba(100,140,255,.06) !important; border:1px solid rgba(100,140,255,.2) !important; border-radius:8px !important; }

/* ══════════════════════════════════════════════
   INFO PILL INLINE
══════════════════════════════════════════════ */
.tag {
  display:inline-block; padding:2px 9px; border-radius:4px;
  font-family:'IBM Plex Mono',monospace; font-size:.58rem; letter-spacing:.5px; margin:2px;
}
.tag-a { background:var(--green2); border:1px solid rgba(74,222,128,.2);  color:#86efac; }
.tag-b { background:var(--yellow2);border:1px solid rgba(252,211,77,.2);  color:#fde68a; }
.tag-c { background:rgba(100,140,255,.1); border:1px solid rgba(100,140,255,.2); color:#a5b4fc; }
.tag-r { background:var(--red2);  border:1px solid rgba(255,92,92,.2);   color:#fca5a5; }

/* ══════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════ */
.footer {
  margin-top: 80px; padding: 30px;
  border-top: 1px solid var(--border2);
  text-align: center;
  font-family: 'IBM Plex Mono', monospace;
  font-size: .48rem; color: rgba(245,166,35,.18);
  letter-spacing: 3px; text-transform: uppercase; line-height: 2.6;
}
.footer hr { border: none; border-top: 1px solid var(--border2); width:50px; margin: 10px auto; }

/* ══════════════════════════════════════════════
   SPINNER
══════════════════════════════════════════════ */
.stSpinner > div { border-color: var(--amber) transparent transparent transparent !important; }

/* ══════════════════════════════════════════════
   TOGGLE
══════════════════════════════════════════════ */
.stToggle label { color:rgba(245,166,35,.55) !important; font-family:'IBM Plex Mono',monospace !important; font-size:.6rem !important; }

/* hide default streamlit branding */
#MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# CACHED RESOURCES
# ──────────────────────────────────────────────────────────────
@st.cache_resource
def build_pains():
    p = FilterCatalogParams()
    p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
    return FilterCatalog(p)
pains_catalog = build_pains()

@st.cache_resource
def load_sascorer():
    try:
        from rdkit.Chem import RDConfig
        import os, importlib.util
        path = os.path.join(RDConfig.RDContribDir, 'SA_Score', 'sascorer.py')
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("sascorer", path)
            m    = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    except: pass
    return None
sascorer = load_sascorer()

GOLD_SMILES = "CN1CCN(CC1)C2=C3C=C(C=CS3)NC4=CC=CC=C24"
gold_mol = Chem.MolFromSmiles(GOLD_SMILES)
gold_fp  = AllChem.GetMorganFingerprintAsBitVect(gold_mol, 2, nBits=2048)
APPROVED  = {"MW":337,"LogP":2.8,"tPSA":81,"HBD":2,"HBA":5,"RotBonds":5,"QED":0.67,"Fsp3":0.35}

CYP_RULES = {
    "CYP1A2":  (["c1ccc2[nH]ccc2c1","c1ccncc1","[NH]c1ccccc1"], "Aromatic amines, planar heterocycles"),
    "CYP2C9":  (["[OH]c1ccccc1","C(=O)[OH]","S(=O)(=O)"],       "Acidic drugs — NSAIDs, warfarin"),
    "CYP2C19": (["n1ccnc1","c1cnc[nH]1","C#N"],                  "Imidazoles, PPIs"),
    "CYP2D6":  (["[NH]CC","CNc1ccccc1","[NH+]"],                  "Basic N + aromatic ring"),
    "CYP3A4":  (["n1cccc1","C1CCNCC1","[nH]1cccc1"],             "Large lipophilic — most drugs"),
}

# ──────────────────────────────────────────────────────────────
# SCIENCE ENGINE
# ──────────────────────────────────────────────────────────────
def sa_score(mol):
    if sascorer:
        try: return round(sascorer.calculateScore(mol), 2)
        except: pass
    try:
        r=rdMolDescriptors.CalcNumRings(mol)
        s=len(Chem.FindMolChiralCenters(mol,includeUnassigned=True))
        h=mol.GetNumHeavyAtoms(); a=Descriptors.NumAromaticRings(mol)
        return min(10.0,max(1.0,round(1+(r*.4+s*.8+h/30+a*.3)*1.2,2)))
    except: return 5.0

def sa_label(v):
    if v<=3: return "Easy",       "ok"
    if v<=5: return "Moderate",   "warn"
    if v<=7: return "Difficult",  "bad"
    return     "Very Hard",       "bad"

def cyp_panel(mol):
    mw=Descriptors.MolWt(mol); lp=Descriptors.MolLogP(mol)
    out={}
    for cyp,(smts,desc) in CYP_RULES.items():
        hit = any(mol.HasSubstructMatch(Chem.MolFromSmarts(s)) for s in smts if Chem.MolFromSmarts(s))
        if cyp=="CYP3A4" and mw>400 and lp>3: hit=True
        out[cyp]={"hit":hit,"desc":desc}
    return out

def complexity_score(mol):
    try:
        r=rdMolDescriptors.CalcNumRings(mol)
        s=len(Chem.FindMolChiralCenters(mol,includeUnassigned=True))
        h=mol.GetNumHeavyAtoms(); br=rdMolDescriptors.CalcNumBridgeheadAtoms(mol)
        sp=rdMolDescriptors.CalcNumSpiroAtoms(mol)
        mac=1 if any(len(x)>=10 for x in mol.GetRingInfo().AtomRings()) else 0
        return round(min(100, r*6+s*10+h*.5+br*8+sp*7+mac*15),1)
    except: return 50.0

def elem_comp(mol):
    d={}
    for a in mol.GetAtoms(): d[a.GetSymbol()]=d.get(a.GetSymbol(),0)+1
    return d

def herg_risk(mol):
    bn=len(mol.GetSubstructMatches(Chem.MolFromSmarts("[NH,NH2,NH3;+0]")))
    ar=Descriptors.NumAromaticRings(mol); mw=Descriptors.MolWt(mol); lp=Descriptors.MolLogP(mol)
    sc=0; fl=[]
    if bn>0: sc+=2; fl.append(f"Basic N×{bn}")
    if ar>=3: sc+=2; fl.append(f"ArRings={ar}")
    if lp>3.5: sc+=1; fl.append(f"LogP={lp:.1f}")
    if mw>400: sc+=1; fl.append(f"MW={mw:.0f}")
    if sc>=4: return "HIGH",fl
    if sc>=2: return "MEDIUM",fl
    return "LOW",fl

def ames_risk(mol):
    alerts={"Ar-amine":"[NH2]c","Nitroso":"[N]=[O]","Nitro":"[$([NX3](=O)=O)]",
            "Alkyl-X":"[CX4][F,Cl,Br,I]","Epoxide":"C1OC1","Acrylate":"C=CC(=O)"}
    found=[n for n,s in alerts.items() if (p:=Chem.MolFromSmarts(s)) and mol.HasSubstructMatch(p)]
    if len(found)>=2: return "Likely Mutagen",found
    if len(found)==1: return "Possible Concern",found
    return "Low Risk",[]

def esol(mol):
    try:
        mw=Descriptors.MolWt(mol); lp=Descriptors.MolLogP(mol)
        rot=Descriptors.NumRotatableBonds(mol); h=mol.GetNumHeavyAtoms()
        na=sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
        return round(.16-.63*lp-.0062*mw+.066*rot-.74*(na/h if h else 0),2)
    except: return None

def sol_label(ls):
    if ls is None: return "Unknown","warn"
    if ls>0:  return "Freely Soluble","ok"
    if ls>-2: return "Soluble","ok"
    if ls>-4: return "Moderately Soluble","warn"
    if ls>-6: return "Slightly Soluble","warn"
    return "Insoluble","bad"

def cns_mpo(mol):
    lp=Descriptors.MolLogP(mol); mw=Descriptors.MolWt(mol)
    tp=Descriptors.TPSA(mol); hb=Descriptors.NumHDonors(mol)
    return sum([lp<=5, lp>=-1, mw<=360, tp<=90, hb<=3, lp<=4])

def score_color(s):
    if s>=75: return "var(--green)"
    if s>=50: return "var(--amber)"
    if s>=25: return "var(--yellow)"
    return "var(--red)"

def score_hex(s):
    if s>=75: return "#4ade80"
    if s>=50: return "#f5a623"
    if s>=25: return "#fcd34d"
    return "#ff5c5c"

def opt_tips(res):
    t=[]
    if res["_mw"]>500:   t.append(("Reduce MW",      f"{res['_mw']:.0f}→<500 Da — remove bulky substituents"))
    if res["_lp"]>5:     t.append(("Lower LogP",      f"{res['_lp']:.2f}→<5 — add OH, COOH or NH₂ groups"))
    if res["_lp"]<-1:    t.append(("Raise LogP",      f"{res['_lp']:.2f}→>−1 — add CH₃ or F substituents"))
    if res["_tp"]>140:   t.append(("Reduce tPSA",     f"{res['_tp']:.0f}→<140 Å² — cyclise polar groups"))
    if res["_hbd"]>4:    t.append(("Reduce HBD",      f"{res['_hbd']}→<5 — N-methylate or replace OH with F"))
    if res["_rot"]>10:   t.append(("Rigidify Chain",  f"{res['_rot']}→≤10 rotatable bonds — form ring"))
    if res["_sa"]>6:     t.append(("Simplify Synth",  f"SA {res['_sa']:.1f}→<5 — reduce ring complexity"))
    if res["_pains"]:    t.append(("PAINS Alert",     "Replace interference substructure"))
    if res["_herg"]=="HIGH": t.append(("Reduce hERG", "Lower basicity or LogP to reduce cardiac risk"))
    cyp_h=[k for k,v in res["_cyp"].items() if v["hit"]]
    if cyp_h: t.append(("CYP Liability", f"Address: {', '.join(cyp_h)}"))
    return t or [("✓ No Action","All key drug-likeness criteria met")]

def calc_lead_score(r):
    s = r["_qed"]*26 + max(0,4-r["_vc"])*5 + (14 if r["_hia"] else 0) + (9 if r["_bbb"] else 0)
    s += r["_sim"]*13 - (10 if r["_pains"] else 0)
    s += 7 if (r["_rot"]<=10 and r["_tp"]<=140) else 0
    s += {"LOW":0,"MEDIUM":-5,"HIGH":-12}.get(r["_herg"],0)
    s -= min(r["_sa"]-1,9)*.8
    s -= sum(1 for v in r["_cyp"].values() if v["hit"])*2
    return max(0,min(100,round(s,1)))

def oral_bio_score(r):
    s = 100 - r["_vc"]*15 - (0 if r["_hia"] else 25) - (15 if r["_pains"] else 0)
    s -= 0 if (r["_rot"]<=10 and r["_tp"]<=140) else 10
    if r["_ls"] and r["_ls"]<-6: s-=15
    elif r["_ls"] and r["_ls"]<-4: s-=5
    return max(0,min(100,s))

def promiscuity(r):
    s = ((30 if r["_pains"] else 0)
       + (20 if r["_herg"]=="HIGH" else 10 if r["_herg"]=="MEDIUM" else 0)
       + sum(1 for v in r["_cyp"].values() if v["hit"])*8
       + (20 if r["_ames"]=="Likely Mutagen" else 10 if r["_ames"]=="Possible Concern" else 0)
       + (10 if r["_lp"]>5 else 0) + (5 if r["_mw"]>500 else 0) + (5 if r["_ar"]>=4 else 0))
    return min(100,s)

def mol_img_b64(mol, sz=(280,210)):
    img=Draw.MolToImage(mol,size=sz)
    buf=io.BytesIO(); img.save(buf,format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

@st.cache_data(show_spinner=False)
def pubchem(smiles):
    try:
        enc=urllib.parse.quote(smiles)
        r=requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{enc}/property/IUPACName,MolecularFormula/JSON",timeout=4)
        if r.status_code==200:
            p=r.json()["PropertyTable"]["Properties"][0]
            return p.get("IUPACName","—"),p.get("MolecularFormula","—")
    except: pass
    return "—","—"

@st.cache_data(show_spinner=False)
def scaffold(smiles):
    try:
        mol=Chem.MolFromSmiles(smiles)
        if mol: return Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol))
    except: pass
    return "—"

@st.cache_data(show_spinner=False)
def ai_explain(data_str):
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":700,
                  "messages":[{"role":"user","content":
                    f"You are an expert medicinal chemist. Write exactly 4 sentences: "
                    f"(1) overall lead assessment, (2) key ADMET strengths, "
                    f"(3) key liabilities, (4) one structural improvement. "
                    f"No markdown, no lists. DATA: {data_str}"}]},timeout=15)
        if r.status_code==200: return r.json()["content"][0]["text"]
    except: pass
    return "AI analysis unavailable."

@st.cache_data(show_spinner=False)
def ai_analogues(smiles, props):
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":900,
                  "messages":[{"role":"user","content":
                    f"Medicinal chemist — suggest 3 structural analogues improving drug-likeness. "
                    f"SMILES: {smiles} PROFILE: {props} "
                    f"Return ONLY a JSON array with 3 objects, keys: smiles, change, expected_improvement. No other text."}]},timeout=18)
        if r.status_code==200: return r.json()["content"][0]["text"]
    except: pass
    return "[]"

@st.cache_data(show_spinner=False)
def ai_repurpose(smiles, props):
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":500,
                  "messages":[{"role":"user","content":
                    f"Pharmacologist — 3 sentences on likely therapeutic indications for this molecule. "
                    f"Cite structural reasons. No markdown. SMILES: {smiles} PROPS: {props}"}]},timeout=12)
        if r.status_code==200: return r.json()["content"][0]["text"]
    except: pass
    return "Repurposing analysis unavailable."

# ──────────────────────────────────────────────────────────────
# CORE ANALYSIS
# ──────────────────────────────────────────────────────────────
def analyze(smiles_list):
    results=[]
    for i,s in enumerate(smiles_list):
        s=s.strip()
        if not s: continue
        mol=Chem.MolFromSmiles(s)
        if not mol: continue
        C=len(mol.GetSubstructMatches(Chem.MolFromSmarts("[#6]"))); is_org=C>4
        mw=Descriptors.MolWt(mol); lp=Descriptors.MolLogP(mol); tp=Descriptors.TPSA(mol)
        hbd=Descriptors.NumHDonors(mol); hba=Descriptors.NumHAcceptors(mol)
        rot=Descriptors.NumRotatableBonds(mol); ar=Descriptors.NumAromaticRings(mol)
        fsp3=Descriptors.FractionCSP3(mol); h=mol.GetNumHeavyAtoms()
        qed=QED.qed(mol) if is_org else 0.0
        fp=AllChem.GetMorganFingerprintAsBitVect(mol,2,nBits=2048)
        sim=DataStructs.TanimotoSimilarity(gold_fp,fp)
        pains=pains_catalog.HasMatch(mol)
        hia=tp<142; bbb=(tp<79 and -2<lp<6)
        ls=esol(mol); sl,sc=sol_label(ls)
        hl,hf=herg_risk(mol); al,af=ames_risk(mol)
        cm=cns_mpo(mol); sa=sa_score(mol); sl_sa,css_sa=sa_label(sa)
        cyp=cyp_panel(mol); cx=complexity_score(mol); elems=elem_comp(mol)
        stereo=len(Chem.FindMolChiralCenters(mol,includeUnassigned=True))
        rings=rdMolDescriptors.CalcNumRings(mol)
        lip=[mw<500,lp<5,hbd<5,hba<10]
        vl=[n for n,ok in zip(["MW","LogP","HBD","HBA"],lip) if not ok]

        if not is_org: grade="F"
        elif len(vl)==0 and sim>0.15 and hia: grade="A"
        elif len(vl)<=1 and hia: grade="B"
        else: grade="C"

        if not is_org: cluster="Non-Organic"
        elif mw>480 or lp>4.5: cluster="Oversized"
        elif sim>0.15: cluster="Target Lead"
        else: cluster="Reference"

        r={
            "ID":f"Cpd-{i+1}","SMILES":s,"Grade":grade,
            "QED":round(qed,3),"Sim":round(sim,3),"Cluster":cluster,
            "MW":round(mw,1),"LogP":round(lp,2),"tPSA":round(tp,1),
            "HBD":hbd,"HBA":hba,"RotBonds":rot,"ArRings":ar,"Fsp3":round(fsp3,2),
            "SA_Score":sa,"SA_Label":sl_sa,"Complexity":cx,
            "CYP_Hits":sum(1 for v in cyp.values() if v["hit"]),
            "logS":round(ls,2) if ls else "N/A","Solubility":sl,
            "CNS_MPO":cm,"hERG":hl,"Ames":al,"HIA":"✅" if hia else "❌",
            "BBB":"✅" if bbb else "❌","Veber":"✅" if (rot<=10 and tp<=140) else "❌",
            "PAINS":"⚠️" if pains else "✅",
            # internals
            "_mol":mol,"_tp":tp,"_lp":lp,"_mw":mw,"_fsp3":fsp3,"_vl":vl,"_vc":len(vl),
            "_org":is_org,"_qed":qed,"_hia":hia,"_bbb":bbb,"_pains":pains,"_rot":rot,
            "_sim":sim,"_h":h,"_hbd":hbd,"_hba":hba,"_ar":ar,"_ls":ls,"_sl":sl,"_sc":sc,
            "_herg":hl,"_hf":hf,"_ames":al,"_af":af,"_cm":cm,"_sa":sa,"_sa_lbl":sl_sa,
            "_cyp":cyp,"_cx":cx,"_elems":elems,"_stereo":stereo,"_fp":fp,"_rings":rings,
        }
        r["LeadScore"]=calc_lead_score(r)
        r["OralBioScore"]=oral_bio_score(r)
        r["PromiscuityRisk"]=promiscuity(r)
        r["_tips"]=opt_tips(r)
        results.append(r)
    return results

# ──────────────────────────────────────────────────────────────
# PLOTLY THEME
# ──────────────────────────────────────────────────────────────
PT = dict(
    paper_bgcolor="#0c1220",
    plot_bgcolor="#080c14",
    font=dict(family="IBM Plex Mono, monospace", color="rgba(200,222,255,0.45)", size=10),
    xaxis=dict(gridcolor="rgba(245,166,35,0.06)", zeroline=False,
               tickfont=dict(size=9, family="IBM Plex Mono")),
    yaxis=dict(gridcolor="rgba(245,166,35,0.06)", zeroline=False,
               tickfont=dict(size=9, family="IBM Plex Mono")),
)

def fig_radar(res):
    cats=["QED","LogP","tPSA","RotBnds","HBD","Fsp3","CNS MPO","SA inv"]
    vals=[
        res["_qed"],
        min(max((res["_lp"]+1)/6,0),1),
        max(0,1-res["_tp"]/142),
        max(0,1-res["_rot"]/12),
        max(0,1-res["_hbd"]/5),
        min(res["_fsp3"],1),
        res["_cm"]/6,
        max(0,1-(res["_sa"]-1)/9),
    ]
    c=score_hex(res["LeadScore"])
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=[.7]*9,theta=cats+[cats[0]],fill='toself',
        line=dict(color='rgba(245,166,35,0.1)',width=1),fillcolor='rgba(245,166,35,0.02)',
        name='Ideal',hoverinfo='skip'))
    fig.add_trace(go.Scatterpolar(
        r=vals+[vals[0]],theta=cats+[cats[0]],fill='toself',name=res["ID"],
        line=dict(color=c,width=2),
        fillcolor=c.replace("#4ade80","rgba(74,222,128,0.1)").replace("#f5a623","rgba(245,166,35,0.1)").replace("#fcd34d","rgba(252,211,77,0.1)").replace("#ff5c5c","rgba(255,92,92,0.1)"),
        marker=dict(size=4,color=c)))
    fig.update_layout(
        polar=dict(bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True,range=[0,1],gridcolor='rgba(245,166,35,0.08)',
                tickfont=dict(size=6,color='rgba(245,166,35,0.3)'),tickvals=[.25,.5,.75]),
            angularaxis=dict(gridcolor='rgba(245,166,35,0.08)',
                tickfont=dict(size=8,color='rgba(200,222,255,0.4)',family='IBM Plex Mono'))),
        paper_bgcolor='rgba(0,0,0,0)',showlegend=False,
        margin=dict(l=24,r=24,t=14,b=14),height=200)
    return fig

def fig_gauge(val, title):
    c=score_hex(val)
    fig=go.Figure(go.Indicator(mode="gauge+number",value=val,
        number=dict(font=dict(size=24,family="Playfair Display",color=c)),
        gauge=dict(
            axis=dict(range=[0,100],tickwidth=1,tickcolor="rgba(245,166,35,0.1)",
                      tickfont=dict(size=6,color='rgba(245,166,35,0.2)')),
            bar=dict(color=c,thickness=0.22),bgcolor="rgba(0,0,0,0)",borderwidth=0,
            steps=[{"range":r[:2],"color":r[2]} for r in [
                (0,25,"rgba(255,92,92,0.05)"),(25,50,"rgba(252,211,77,0.05)"),
                (50,75,"rgba(245,166,35,0.05)"),(75,100,"rgba(74,222,128,0.05)")]],
            threshold=dict(line=dict(color=c,width=2),thickness=.75,value=val)),
        title=dict(text=f"<span style='font-size:.55em;color:rgba(245,166,35,0.4);font-family:IBM Plex Mono;letter-spacing:2px'>{title}</span>",
                   font=dict(size=9))))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=14,r=14,t=28,b=6),height=148)
    return fig

def fig_boiled_egg(data):
    fig=go.Figure()
    # white (HIA) ellipse
    fig.add_shape(type="ellipse",x0=5,y0=-2.5,x1=137,y1=6.5,
        fillcolor="rgba(200,222,255,0.018)",
        line=dict(color="rgba(200,222,255,0.2)",width=1.5,dash="dot"))
    # yolk (BBB) ellipse
    fig.add_shape(type="ellipse",x0=22,y0=-1.8,x1=78,y1=4.3,
        fillcolor="rgba(245,166,35,0.04)",
        line=dict(color="rgba(245,166,35,0.35)",width=1.5))
    fig.add_annotation(x=80,y=5.8,text="HIA zone",showarrow=False,
        font=dict(color="rgba(200,222,255,0.3)",size=9,family="IBM Plex Mono"))
    fig.add_annotation(x=50,y=4.0,text="BBB zone",showarrow=False,
        font=dict(color="rgba(245,166,35,0.45)",size=9,family="IBM Plex Mono"))

    cmap={"Target Lead":"#4ade80","Oversized":"#ff5c5c","Reference":"#f5a623","Non-Organic":"#64748b"}
    for d in data:
        c=cmap.get(d["Cluster"],"#c8deff")
        fig.add_trace(go.Scatter(x=[d["_tp"]],y=[d["_lp"]],mode="markers+text",
            name=d["ID"],text=[f"  {d['ID']}"],
            textfont=dict(size=9,color=c,family="IBM Plex Mono"),textposition="middle right",
            marker=dict(size=13+d["LeadScore"]/18,color=c,symbol="diamond",
                        line=dict(color="#080c14",width=1.5),opacity=.92),
            hovertemplate=(f"<b>{d['ID']}</b><br>tPSA: {d['_tp']:.1f} Å²<br>"
                f"LogP: {d['_lp']:.2f}<br>Grade: {d['Grade']}<br>"
                f"Lead Score: {d['LeadScore']}<br>QED: {d['_qed']:.3f}<br>"
                f"SA: {d['SA_Score']} ({d['SA_Label']})<br>"
                f"hERG: {d['_herg']}<extra></extra>")))
    fig.update_layout(**PT,
        xaxis=dict(title="tPSA (Å²)",range=[-10,220],gridcolor="rgba(245,166,35,0.06)",zeroline=False,
                   titlefont=dict(size=10,color="rgba(245,166,35,0.4)")),
        yaxis=dict(title="LogP (WLOGP)",range=[-4.5,9],gridcolor="rgba(245,166,35,0.06)",zeroline=False,
                   titlefont=dict(size=10,color="rgba(245,166,35,0.4)")),
        height=540,legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10,family="IBM Plex Mono",color="rgba(200,222,255,0.5)")),
        margin=dict(l=60,r=40,t=20,b=60))
    return fig

def fig_similarity(data):
    n=len(data); fps=[d["_fp"] for d in data]
    mat=np.array([[DataStructs.TanimotoSimilarity(fps[i],fps[j]) for j in range(n)] for i in range(n)])
    ids=[d["ID"] for d in data]
    fig=go.Figure(go.Heatmap(z=mat,x=ids,y=ids,
        colorscale=[[0,"#080c14"],[.3,"#111b2e"],[.6,"#7c4a00"],[1,"#f5a623"]],
        text=[[f"{mat[i][j]:.2f}" for j in range(n)] for i in range(n)],
        texttemplate="%{text}",textfont=dict(size=10,family="IBM Plex Mono",color="#080c14"),
        zmin=0,zmax=1,showscale=True,
        colorbar=dict(tickfont=dict(size=8,color="rgba(245,166,35,0.5)"),bgcolor="rgba(0,0,0,0)")))
    fig.update_layout(**PT,
        xaxis=dict(tickfont=dict(size=10,family="IBM Plex Mono",color="rgba(245,166,35,0.55)"),gridcolor="rgba(245,166,35,0.05)"),
        yaxis=dict(tickfont=dict(size=10,family="IBM Plex Mono",color="rgba(245,166,35,0.55)"),gridcolor="rgba(245,166,35,0.05)"),
        margin=dict(l=60,r=20,t=20,b=60),height=max(260,n*70+80))
    return fig

def fig_parallel(data):
    df=pd.DataFrame([{
        "MW":d["_mw"],"LogP":d["_lp"],"tPSA":d["_tp"],
        "QED":d["_qed"],"SA":d["_sa"],"CYP":d["CYP_Hits"],
        "Complexity":d["_cx"],"Lead":d["LeadScore"]} for d in data])
    fig=go.Figure(go.Parcoords(
        line=dict(color=df["Lead"],
                  colorscale=[[0,"#ff5c5c"],[0.5,"#f5a623"],[1,"#4ade80"]],
                  showscale=True,cmin=0,cmax=100,
                  colorbar=dict(tickfont=dict(size=8,color="rgba(245,166,35,0.5)"),
                               title=dict(text="Lead",font=dict(size=9,color="rgba(245,166,35,0.5)")))),
        dimensions=[
            dict(label="MW (Da)",values=df["MW"],range=[0,700]),
            dict(label="LogP",values=df["LogP"],range=[-4,9]),
            dict(label="tPSA",values=df["tPSA"],range=[0,200]),
            dict(label="QED",values=df["QED"],range=[0,1]),
            dict(label="SA Score",values=df["SA"],range=[1,10]),
            dict(label="CYP Hits",values=df["CYP"],range=[0,5]),
            dict(label="Complexity",values=df["Complexity"],range=[0,100]),
            dict(label="Lead Score",values=df["Lead"],range=[0,100]),
        ],
        labelfont=dict(size=9,family="IBM Plex Mono",color="rgba(245,166,35,0.55)"),
        tickfont=dict(size=8,family="IBM Plex Mono",color="rgba(200,222,255,0.3)")))
    fig.update_layout(**PT,margin=dict(l=80,r=80,t=40,b=30),height=360)
    return fig

def fig_pca(data):
    if len(data)<2: return None
    fps=np.array([list(d["_fp"]) for d in data],dtype=float)
    fps_c=fps-fps.mean(0); _,_,Vt=np.linalg.svd(fps_c,full_matrices=False)
    pc=fps_c@Vt[:2].T
    fig=go.Figure()
    for i,d in enumerate(data):
        c=score_hex(d["LeadScore"])
        fig.add_trace(go.Scatter(x=[pc[i,0]],y=[pc[i,1]],mode='markers+text',
            name=d["ID"],text=[f" {d['ID']}"],
            textfont=dict(size=9,color=c,family="IBM Plex Mono"),textposition="middle right",
            marker=dict(size=15,color=d["LeadScore"],
                        colorscale=[[0,"#ff5c5c"],[.5,"#f5a623"],[1,"#4ade80"]],cmin=0,cmax=100,
                        line=dict(color="#080c14",width=1.5),symbol="diamond"),
            hovertemplate=f"<b>{d['ID']}</b><br>Lead: {d['LeadScore']}<extra></extra>",showlegend=False))
    fig.update_layout(**PT,height=400,margin=dict(l=60,r=40,t=20,b=60),
        xaxis=dict(title="PC1",gridcolor="rgba(245,166,35,0.06)",zeroline=False,
                   titlefont=dict(size=10,color="rgba(245,166,35,0.4)")),
        yaxis=dict(title="PC2",gridcolor="rgba(245,166,35,0.06)",zeroline=False,
                   titlefont=dict(size=10,color="rgba(245,166,35,0.4)")))
    return fig

def fig_qed_sa(data):
    fig=go.Figure()
    # QED
    fig.add_trace(go.Bar(x=[d["ID"] for d in data],y=[d["_qed"] for d in data],
        name="QED",marker=dict(color=[score_hex(d["_qed"]*100) for d in data],
            opacity=.8,line=dict(color="#080c14",width=1)),
        text=[f"{d['_qed']:.3f}" for d in data],textposition="outside",
        textfont=dict(size=8,family="IBM Plex Mono",color="rgba(200,222,255,0.5)"),
        hovertemplate="<b>%{x}</b><br>QED: %{y:.3f}<extra></extra>"))
    fig.add_hline(y=0.67,line_dash="dot",line_color="rgba(245,166,35,0.4)",
        annotation_text="FDA median ≈ 0.67",
        annotation_font=dict(size=8,color="rgba(245,166,35,0.5)",family="IBM Plex Mono"))
    fig.update_layout(**PT,height=260,showlegend=False,
        yaxis=dict(range=[0,1.18],gridcolor="rgba(245,166,35,0.05)",title="QED",
                   titlefont=dict(size=9,color="rgba(245,166,35,0.4)")),
        margin=dict(l=40,r=40,t=20,b=40))
    return fig

def fig_sa(data):
    sc=[score_hex(max(0,100-(d["_sa"]-1)/9*100)) for d in data]
    fig=go.Figure(go.Bar(x=[d["ID"] for d in data],y=[d["_sa"] for d in data],
        marker=dict(color=sc,line=dict(color="#080c14",width=1)),
        text=[f"{d['SA_Score']} · {d['SA_Label']}" for d in data],textposition="outside",
        textfont=dict(size=8,family="IBM Plex Mono",color="rgba(200,222,255,0.5)"),
        hovertemplate="<b>%{x}</b><br>SA Score: %{y:.2f}<extra></extra>"))
    fig.add_hline(y=3,line_dash="dot",line_color="rgba(74,222,128,0.4)",
        annotation_text="≤3 Easy",annotation_font=dict(size=8,color="rgba(74,222,128,0.5)",family="IBM Plex Mono"))
    fig.add_hline(y=6,line_dash="dot",line_color="rgba(255,92,92,0.4)",
        annotation_text="≥6 Difficult",annotation_font=dict(size=8,color="rgba(255,92,92,0.5)",family="IBM Plex Mono"))
    fig.update_layout(**PT,height=260,showlegend=False,
        yaxis=dict(range=[0,11.5],gridcolor="rgba(245,166,35,0.05)",title="SA Score",
                   titlefont=dict(size=9,color="rgba(245,166,35,0.4)")),
        margin=dict(l=50,r=40,t=20,b=40))
    return fig

def fig_cyp(data):
    cyps=["CYP1A2","CYP2C9","CYP2C19","CYP2D6","CYP3A4"]
    z=[[1 if d["_cyp"][c]["hit"] else 0 for c in cyps] for d in data]
    fig=go.Figure(go.Heatmap(z=z,x=cyps,y=[d["ID"] for d in data],
        colorscale=[[0,"#0c1220"],[1,"#7c1d1d"]],
        text=[["INHIBITOR" if v else "safe" for v in row] for row in z],
        texttemplate="%{text}",textfont=dict(size=9,family="IBM Plex Mono",color="rgba(255,255,255,0.7)"),
        showscale=False,zmin=0,zmax=1,
        hovertemplate="<b>%{y} — %{x}</b><br>%{text}<extra></extra>"))
    fig.update_layout(**PT,
        xaxis=dict(tickfont=dict(size=9,family="IBM Plex Mono",color="rgba(245,166,35,0.55)"),side="top"),
        yaxis=dict(tickfont=dict(size=9,family="IBM Plex Mono",color="rgba(245,166,35,0.55)")),
        margin=dict(l=70,r=20,t=60,b=10),height=max(180,len(data)*52+80))
    return fig

def fig_elem(elems,cpd_id):
    lb=list(elems.keys()); vl=list(elems.values())
    cols={"C":"#f5a623","H":"#c8deff","O":"#ff5c5c","N":"#a78bfa",
          "S":"#fcd34d","F":"#4ade80","Cl":"#fb923c","Br":"#e879f9","P":"#67e8f9"}
    c=[cols.get(l,"#475569") for l in lb]
    fig=go.Figure(go.Pie(labels=lb,values=vl,hole=.58,
        marker=dict(colors=c,line=dict(color="#080c14",width=2)),
        textfont=dict(size=9,family="IBM Plex Mono"),
        hovertemplate="<b>%{label}</b>: %{value} atoms (%{percent})<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
        legend=dict(font=dict(size=8,family="IBM Plex Mono",color="rgba(245,166,35,0.5)"),bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text=cpd_id,x=.5,y=.5,font_size=9,showarrow=False,
            font=dict(family="IBM Plex Mono",color="rgba(245,166,35,0.4)"))],
        margin=dict(l=8,r=8,t=14,b=8),height=200)
    return fig

def fig_approved(res):
    props=["MW","LogP","tPSA","QED","RotBonds"]
    cv=[res["_mw"],res["_lp"],res["_tp"],res["_qed"],res["_rot"]]
    mv=[APPROVED[p] for p in props]
    fig=go.Figure()
    c=score_hex(res["LeadScore"])
    fig.add_trace(go.Bar(name=res["ID"],x=props,y=cv,
        marker=dict(color=c,opacity=.7,line=dict(color="#080c14",width=1)),
        text=[f"{v:.1f}" for v in cv],textposition="outside",
        textfont=dict(size=9,family="IBM Plex Mono",color="rgba(200,222,255,0.5)")))
    fig.add_trace(go.Bar(name="Approved median",x=props,y=mv,
        marker=dict(color="rgba(200,222,255,0.25)",line=dict(color="rgba(200,222,255,0.4)",width=1)),
        text=[f"{v:.1f}" for v in mv],textposition="outside",
        textfont=dict(size=9,family="IBM Plex Mono",color="rgba(200,222,255,0.5)")))
    fig.update_layout(**PT,barmode="group",height=270,
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10,family="IBM Plex Mono",color="rgba(200,222,255,0.5)")),
        margin=dict(l=40,r=40,t=20,b=40))
    return fig

def html_export(data):
    rows=""
    for d in data:
        hc={"LOW":"#4ade80","MEDIUM":"#fcd34d","HIGH":"#ff5c5c"}.get(d["_herg"],"#aaa")
        ac={"Low Risk":"#4ade80","Possible Concern":"#fcd34d","Likely Mutagen":"#ff5c5c"}.get(d["_ames"],"#aaa")
        sc={"Easy":"#4ade80","Moderate":"#fcd34d","Difficult":"#fb923c","Very Hard":"#ff5c5c"}.get(d["SA_Label"],"#aaa")
        gc={"A":"#4ade80","B":"#f5a623","C":"#fcd34d","F":"#ff5c5c"}.get(d["Grade"],"#aaa")
        lc=score_hex(d["LeadScore"])
        rows+=f"<tr><td>{d['ID']}</td><td style='color:{lc};font-weight:700'>{d['LeadScore']}</td><td style='color:{gc};font-weight:700'>{d['Grade']}</td><td>{d['QED']}</td><td>{d['MW']}</td><td>{d['LogP']}</td><td>{d['tPSA']}</td><td>{d['HIA']}</td><td>{d['BBB']}</td><td>{d.get('logS','N/A')}</td><td style='color:{sc}'>{d['SA_Score']} ({d['SA_Label']})</td><td style='color:{hc}'>{d['_herg']}</td><td style='color:{ac}'>{d['_ames']}</td><td>{d['CYP_Hits']}/5</td><td>{d['CNS_MPO']}/6</td><td>{d['PromiscuityRisk']:.0f}</td><td>{d['PAINS']}</td></tr>"
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>ChemoFilter v7 Report</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@300;400;500&display=swap');
:root{{--bg:#080c14;--bg2:#0c1220;--amber:#f5a623;--ice:#c8deff;--border:rgba(245,166,35,.14);}}
body{{font-family:'IBM Plex Mono',monospace;background:var(--bg);color:var(--ice);padding:48px;
background-image:repeating-linear-gradient(0deg,transparent,transparent 79px,rgba(245,166,35,.02) 80px),
repeating-linear-gradient(90deg,transparent,transparent 79px,rgba(245,166,35,.02) 80px);}}
h1{{font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:900;letter-spacing:-1px;
background:linear-gradient(135deg,#ffc85a,#f5a623,#d4a017);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.sub{{color:rgba(245,166,35,.4);font-size:.62rem;letter-spacing:3px;margin:6px 0 28px;}}
table{{width:100%;border-collapse:collapse;font-size:.65rem;margin-top:12px;}}
th{{background:rgba(245,166,35,.06);color:rgba(245,166,35,.55);padding:10px 8px;text-align:left;
letter-spacing:1px;font-size:.56rem;border-bottom:1px solid rgba(245,166,35,.1);}}
td{{padding:8px;border-bottom:1px solid rgba(200,222,255,.03);color:var(--ice);}}
tr:hover td{{background:rgba(245,166,35,.025);}}
.foot{{margin-top:50px;color:rgba(245,166,35,.15);font-size:.48rem;letter-spacing:3px;
text-align:center;border-top:1px solid rgba(245,166,35,.07);padding-top:22px;}}
</style></head><body>
<h1>ChemoFilter</h1>
<div class="sub">CRYSTALLINE NOIR v7 &nbsp;·&nbsp; VIT CHENNAI MDP 2026 &nbsp;·&nbsp; {len(data)} COMPOUND{'S' if len(data)>1 else ''}</div>
<table><thead><tr>
<th>ID</th><th>LEAD</th><th>GRADE</th><th>QED</th><th>MW</th><th>LOGP</th><th>TPSA</th>
<th>HIA</th><th>BBB</th><th>LOGS</th><th>SA SCORE</th><th>hERG</th><th>AMES</th>
<th>CYP</th><th>CNS MPO</th><th>PROMIC</th><th>PAINS</th>
</tr></thead><tbody>{rows}</tbody></table>
<div class="foot">
BOILED-EGG [DAINA 2016] · LIPINSKI [2001] · ESOL [DELANEY 2004] · QED [BICKERTON 2012]<br>
SA SCORE [ERTL 2009] · CNS MPO [WAGER 2010] · PAINS [BAELL 2010] · RDKIT [LANDRUM]
</div></body></html>""".encode("utf-8")

# ══════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-hex">⬡⬡</div>
  <div class="hero-overline">Computational Drug Screening Platform</div>
  <div class="hero-title">Chemo<span>Filter</span></div>
  <div class="hero-sub">Crystalline Noir Edition &nbsp;·&nbsp; v7</div>
  <div class="hero-meta">ADME · Lipinski · QED · SA Score · CYP Panel · Lead Score™ · AI-Powered · VIT Chennai MDP 2026</div>
  <div class="feature-chips">
    <span class="chip chip-base">BOILED-EGG</span>
    <span class="chip chip-base">LIPINSKI Ro5</span>
    <span class="chip chip-base">VEBER · GHOSE · EGAN</span>
    <span class="chip chip-base">QED Scoring</span>
    <span class="chip chip-base">CNS MPO</span>
    <span class="chip chip-base">ESOL Solubility</span>
    <span class="chip chip-base">PAINS Filter</span>
    <span class="chip chip-base">hERG · Ames</span>
    <span class="chip chip-gold">★ SA Score</span>
    <span class="chip chip-gold">★ CYP Panel ×5</span>
    <span class="chip chip-gold">★ Complexity</span>
    <span class="chip chip-gold">★ Element Donut</span>
    <span class="chip chip-gold">★ Promiscuity Risk</span>
    <span class="chip chip-gold">★ Lead Score™</span>
    <span class="chip chip-gold">★ AI Analogues</span>
    <span class="chip chip-gold">★ Repurposing</span>
    <span class="chip chip-gold">★ Property Editor</span>
    <span class="chip chip-gold">★ PCA Space</span>
    <span class="chip chip-gold">★ Sim Matrix</span>
    <span class="chip chip-gold">★ Parallel Coords</span>
    <span class="chip chip-gold">★ HTML Report</span>
  </div>
  <div class="hero-stat-strip">
    <div class="hss-num">21</div>
    <div class="hss-lbl">Features Active</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  REFERENCE BOX
# ══════════════════════════════════════════════════════════════
with st.container():
    st.markdown('<div class="ref-box">', unsafe_allow_html=True)
    r1, r2, r3 = st.columns([1, 3, 2])
    with r1:
        st.markdown(
            f'<img src="data:image/png;base64,{mol_img_b64(gold_mol,(160,128))}" '
            f'style="width:100%;border-radius:8px;border:1px solid rgba(245,166,35,.2)">', 
            unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="ref-name">🏆 Olanzapine — CNS Gold Standard</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.63rem;color:rgba(200,222,255,.4);line-height:2.1">
        DrugBank DB00334 &nbsp;·&nbsp; FDA 1996 &nbsp;·&nbsp; Antipsychotic<br>
        MW 312.4 Da &nbsp;·&nbsp; LogP 2.87 &nbsp;·&nbsp; tPSA 30.9 Å²<br>
        <span style="color:#f5a623">All Lipinski pass &nbsp;·&nbsp; BBB penetrant &nbsp;·&nbsp; CNS MPO 5/6</span><br>
        <span style="color:#4ade80">SA Score ~2.8 (Easy) &nbsp;·&nbsp; QED 0.44 &nbsp;·&nbsp; CYP2D6 substrate</span>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:rgba(200,222,255,.3);line-height:2.5">
        ⬡ &nbsp;<span style="color:rgba(200,222,255,.55)">White ellipse</span> → HIA (tPSA &lt; 142 Å²)<br>
        ⬡ &nbsp;<span style="color:#f5a623">Yolk region</span> → BBB (tPSA &lt; 79 Å²)<br>
        📐 Daina &amp; Zoete, ChemMedChem 2016<br>
        ⚗️ <span style="color:#c8deff">SA Score · Ertl, J Cheminf 2009</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
color:var(--amber);margin-bottom:2px">⬡ Discovery Lab</div>
<div style="font-family:'IBM Plex Mono',monospace;font-size:.5rem;
color:rgba(245,166,35,.25);letter-spacing:3px;margin-bottom:20px">CRYSTALLINE NOIR v7 · 21 FEATURES</div>
""", unsafe_allow_html=True)

DEFAULTS = ("CN1CCN(CC1)C2=C3C=C(C=CS3)NC4=CC=CC=C24, "
            "S(C1=CC=C(N)C=C1)(=O)(=O)N, "
            "CN1C=NC2=C1C(=O)N(C(=O)N2C)C, "
            "[Na+].[Cl-], CC(=O)Oc1ccccc1C(=O)O")

input_text = st.sidebar.text_area("SMILES INPUT", DEFAULTS, height=145,
    help="Comma-separated SMILES strings. Use Quick Library below for examples.")

csv_up = st.sidebar.file_uploader("BATCH CSV (smiles column)", type=["csv"])
if csv_up:
    try:
        df_up = pd.read_csv(csv_up)
        col   = next((c for c in df_up.columns if c.lower()=="smiles"), None)
        if col:
            input_text = ", ".join(df_up[col].dropna().astype(str).tolist())
            st.sidebar.success(f"✅ {len(df_up)} compounds loaded")
        else: st.sidebar.error("No 'smiles' column found")
    except Exception as e: st.sidebar.error(str(e))

enable_ai = st.sidebar.toggle("✦ Enable AI Features (Claude)", value=True)

with st.sidebar.expander("QUICK LIBRARY"):
    libs = {"Aspirin":"CC(=O)Oc1ccccc1C(=O)O","Ibuprofen":"CC(C)Cc1ccc(cc1)C(C)C(=O)O",
        "Caffeine":"CN1C=NC2=C1C(=O)N(C(=O)N2C)C","Paracetamol":"CC(=O)Nc1ccc(O)cc1",
        "Olanzapine":"CN1CCN(CC1)C2=C3C=C(C=CS3)NC4=CC=CC=C24",
        "Dopamine":"NCCc1ccc(O)c(O)c1","Metformin":"CN(C)C(=N)NC(=N)N"}
    for name, smi in libs.items():
        if st.button(f"+ {name}", key=f"lib_{name}"):
            input_text = smi

with st.sidebar.expander("SCIENTIFIC REFERENCES"):
    st.markdown("""<div style="font-size:.58rem;color:rgba(245,166,35,.3);font-family:'IBM Plex Mono',monospace;line-height:2.2">
[1] Daina, ChemMedChem 2016<br>[2] Lipinski, ADDR 2001<br>
[3] Delaney, JCICS 2004<br>[4] Bickerton, Nat Chem 2012<br>
[5] Wager, ACS Chem Neurosci 2010<br>[6] Baell, JMC 2010<br>
[7] Ertl &amp; Schuffenhauer, J Cheminf 2009<br>
[8] Rogers &amp; Hahn, JCIM 2010<br>[9] RDKit — rdkit.org</div>""",
    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ANALYSIS
# ══════════════════════════════════════════════════════════════
if input_text.strip():
    with st.spinner("⬡  Running ADMET · CYP · SA · AI analysis..."):
        data = analyze(input_text.split(","))

    if not data:
        st.error("No valid SMILES found. Please check input.")
        st.stop()

    total  = len(data)
    ga     = sum(1 for d in data if d["Grade"]=="A")
    hia_ok = sum(1 for d in data if d["_hia"])
    bbb_ok = sum(1 for d in data if d["_bbb"])
    pf     = sum(1 for d in data if d["_pains"])
    hh     = sum(1 for d in data if d["_herg"]=="HIGH")
    aqed   = sum(d["_qed"] for d in data)/total
    als    = sum(d["LeadScore"] for d in data)/total
    asa    = sum(d["_sa"] for d in data)/total

    # ── STATS STRIP
    def sv(v,c): return f'<div class="sc-val" style="color:{c}">{v}</div>'
    st.markdown(f"""
<div class="stats-strip">
  <div class="sc">{sv(total,"var(--ice2)")}<div class="sc-lbl">Compounds</div></div>
  <div class="sc">{sv(ga,score_hex(ga/total*100 if total else 0))}<div class="sc-lbl">Grade A</div></div>
  <div class="sc">{sv(hia_ok,"#4ade80")}<div class="sc-lbl">Good HIA</div></div>
  <div class="sc">{sv(bbb_ok,"var(--amber)")}<div class="sc-lbl">BBB Cross</div></div>
  <div class="sc">{sv(f"{aqed:.2f}",score_hex(aqed*100))}<div class="sc-lbl">Avg QED</div></div>
  <div class="sc">{sv(f"{als:.0f}",score_hex(als))}<div class="sc-lbl">Avg Lead</div></div>
  <div class="sc">{sv(f"{asa:.1f}","#a78bfa")}<div class="sc-lbl">Avg SA</div></div>
  <div class="sc">{sv(hh,"#ff5c5c")}<div class="sc-lbl">hERG High</div></div>
  <div class="sc">{sv(pf,"#fb923c")}<div class="sc-lbl">PAINS Flags</div></div>
</div>""", unsafe_allow_html=True)

    # ── LEADERBOARD
    st.markdown("""<div class="sec">
      <span class="sec-num">01</span>
      <span class="sec-title">Compound Leaderboard</span>
      <div class="sec-line"></div>
      <span class="sec-tag">Ranked by Lead Score™</span>
    </div>""", unsafe_allow_html=True)

    cols_show=["ID","LeadScore","OralBioScore","PromiscuityRisk","Grade","QED",
               "SA_Score","Complexity","CYP_Hits","Sim","MW","LogP","tPSA",
               "logS","Solubility","HIA","BBB","CNS_MPO","hERG","Ames","Veber","PAINS"]
    df_show=pd.DataFrame(data)[cols_show]
    st.dataframe(df_show.style
        .background_gradient(cmap="YlOrRd", subset=["LeadScore","OralBioScore"])
        .background_gradient(cmap="Reds",   subset=["PromiscuityRisk","SA_Score","CYP_Hits"])
        .background_gradient(cmap="Blues",  subset=["Sim"])
        .background_gradient(cmap="Greens", subset=["QED"]),
        use_container_width=True, height=min(80+34*total,320))

    dl1,dl2 = st.columns(2)
    with dl1:
        st.download_button("📥 Export CSV",
            data=df_show.assign(SMILES=[d["SMILES"] for d in data]).to_csv(index=False).encode(),
            file_name="chemofilter_v7.csv", mime="text/csv")
    with dl2:
        st.download_button("🌐 Export HTML Report",
            data=html_export(data), file_name="chemofilter_v7_report.html", mime="text/html")

    # ══════════════════════════════════════════════════════════
    #  TABS
    # ══════════════════════════════════════════════════════════
    TABS = st.tabs([
        "🔬 Diagnostics",
        "🍳 BOILED-EGG",
        "📊 Analysis Suite",
        "⚗️ SA + CYP",
        "🧠 AI Features",
        "📋 Full Report"
    ])

    MEDAL = {"A":"mA","B":"mB","C":"mC","F":"mF"}
    PALETTE = ["#f5a623","#4ade80","#c8deff","#a78bfa","#fb923c","#e879f9","#67e8f9","#fbbf24"]

    # ══════ TAB 1 — DIAGNOSTICS ══════
    with TABS[0]:
        for i, res in enumerate(data):
            pc = PALETTE[i%len(PALETTE)]
            mc = MEDAL.get(res["Grade"],"mF")
            with st.expander(
                f"⬡  {res['ID']}  ·  Grade {res['Grade']}  ·  "
                f"Lead Score {res['LeadScore']}/100  ·  SA {res['SA_Score']} ({res['SA_Label']})  ·  {res['Cluster']}",
                expanded=(i==0)):
                st.markdown('<div style="padding:4px">', unsafe_allow_html=True)
                c1,c2,c3 = st.columns([1.2,1.5,1.3])

                # ─ COL 1: Structure + Gauges + Donut
                with c1:
                    st.markdown(
                        f'<div class="medallion-wrap">'
                        f'<div class="medallion {mc}">{res["Grade"]}</div>'
                        f'<div class="med-id">{res["ID"]}</div></div>',
                        unsafe_allow_html=True)
                    st.markdown(
                        f'<img src="data:image/png;base64,{mol_img_b64(res["_mol"],(270,200))}" '
                        f'style="width:100%;border-radius:8px;border:1px solid var(--border)">',
                        unsafe_allow_html=True)

                    iupac, formula = pubchem(res["SMILES"])
                    if iupac!="—":
                        st.markdown(
                            f'<div style="text-align:center;margin:8px 0">'
                            f'<span class="tag tag-c">🔍 {iupac[:28]}{"…" if len(iupac)>28 else ""}</span>'
                            f'<span class="tag tag-b">{formula}</span></div>',
                            unsafe_allow_html=True)
                    sc = scaffold(res["SMILES"])
                    if sc!="—":
                        st.markdown(
                            f'<div style="text-align:center;margin-bottom:6px">'
                            f'<span class="tag tag-a">⬡ {sc[:36]}{"…" if len(sc)>36 else ""}</span></div>',
                            unsafe_allow_html=True)

                    g1,g2 = st.columns(2)
                    with g1: st.plotly_chart(fig_gauge(res["LeadScore"],"LEAD SCORE"), use_container_width=True, key=f"glead_{i}")
                    with g2: st.plotly_chart(fig_gauge(res["OralBioScore"],"ORAL BIO"), use_container_width=True, key=f"goral_{i}")
                    st.plotly_chart(fig_elem(res["_elems"], res["ID"]), use_container_width=True, key=f"elem_{i}")

                # ─ COL 2: Descriptor Table + Bars
                with c2:
                    def drow(k,v,css=""):
                        return f'<tr><td class="dk">{k}</td><td class="dv {css}">{v}</td></tr>'
                    hc = {"LOW":"ok","MEDIUM":"warn","HIGH":"bad"}.get(res["_herg"],"")
                    ac = {"Low Risk":"ok","Possible Concern":"warn","Likely Mutagen":"bad"}.get(res["_ames"],"")
                    sc2 = {"Easy":"ok","Moderate":"warn","Difficult":"bad","Very Hard":"bad"}.get(res["SA_Label"],"")

                    st.markdown(f"""<table class="dtable">
{drow("MW",f"{res['MW']} Da","ok" if res['_mw']<500 else "bad")}
{drow("LogP",res['LogP'],"ok" if -1<res['_lp']<5 else "bad")}
{drow("tPSA",f"{res['tPSA']} Å²","ok" if res['_tp']<142 else "bad")}
{drow("HBD / HBA",f"{res['HBD']} / {res['HBA']}")}
{drow("RotBonds",res['RotBonds'],"ok" if res['_rot']<=10 else "warn")}
{drow("ArRings",res['ArRings'])}
{drow("StereoCenters",res['StereoCenters'],"warn" if res['_stereo']>2 else "ok")}
{drow("Fsp3",res['Fsp3'],"ok" if res['_fsp3']>0.25 else "warn")}
{drow("QED",res['QED'],"ok" if res['_qed']>0.5 else "warn")}
{drow("Tanimoto",res['Sim'],"ok" if res['_sim']>0.15 else "warn")}
{drow("HIA","✅" if res['_hia'] else "❌","ok" if res['_hia'] else "bad")}
{drow("BBB","✅" if res['_bbb'] else "❌","ok" if res['_bbb'] else "warn")}
{drow("CNS MPO",f"{res['CNS_MPO']}/6","ok" if res['_cm']>=4 else "warn")}
{drow("logS (ESOL)",res['logS'],res['_sc'])}
{drow("Solubility",res['Solubility'],res['_sc'])}
{drow("hERG",res['_herg'],hc)}
{drow("Ames",res['_ames'],ac)}
{drow("CYP Hits",f"{res['CYP_Hits']}/5","bad" if res['CYP_Hits']>=3 else "warn" if res['CYP_Hits']>0 else "ok")}
</table>""", unsafe_allow_html=True)

                    # Progress bars
                    def bar(label, val, maxv, color):
                        pct=min(100,val/maxv*100)
                        return f"""<div class="bar-lbl">{label}</div>
<div class="bar-track"><div class="bar-fill" style="width:{pct:.0f}%;background:{color}"></div></div>
<div class="bar-num">{val:.1f} / {maxv:.0f}</div>"""

                    st.markdown(
                        bar("SA Score", res["_sa"], 10, score_hex(100-res["_sa"]/10*100)) +
                        bar("Complexity Score", res["_cx"], 100, score_hex(100-res["_cx"])) +
                        bar("Promiscuity Risk", res["PromiscuityRisk"], 100, score_hex(res["PromiscuityRisk"])),
                        unsafe_allow_html=True)

                    with st.expander("Rule-Set Panel"):
                        checks=[
                            ("Lipinski Ro5","✅" if res["_vc"]==0 else "⚠️" if res["_vc"]==1 else "❌",
                             f"{4-res['_vc']}/4 rules pass"),
                            ("Veber Rule","✅" if (res["_rot"]<=10 and res["_tp"]<=140) else "❌",
                             f"RotBonds {res['_rot']}, tPSA {res['_tp']:.0f}"),
                            ("Ghose Filter","✅" if (160<=res["_mw"]<=480 and -0.4<=res["_lp"]<=5.6) else "❌",
                             f"MW {res['_mw']:.0f}, LogP {res['_lp']:.2f}"),
                            ("Egan Rule","✅" if (res["_lp"]<=5.88 and res["_tp"]<=131.6) else "❌",
                             f"LogP {res['_lp']:.2f}, tPSA {res['_tp']:.0f}"),
                            ("PAINS","⚠️ Flagged" if res["_pains"] else "✅ Clear","Pan-assay interference"),
                        ]
                        for name,icon,detail in checks:
                            ca,cb = st.columns([4,1])
                            ca.markdown(
                                f"<span style='font-family:IBM Plex Mono,monospace;font-size:.65rem;color:rgba(200,222,255,.55)'>{name}</span>"
                                f"<br><span style='font-family:IBM Plex Mono,monospace;font-size:.56rem;color:rgba(200,222,255,.3)'>{detail}</span>",
                                unsafe_allow_html=True)
                            cb.markdown(
                                f"<div style='text-align:right;font-size:.95rem;margin-top:4px'>{icon}</div>",
                                unsafe_allow_html=True)

                # ─ COL 3: Radar + Tox + Optimise + Verdict
                with c3:
                    st.markdown(
                        "<div style='font-family:IBM Plex Mono,monospace;font-size:.5rem;"
                        "color:rgba(245,166,35,.3);text-align:center;letter-spacing:2px;"
                        "margin-bottom:4px;text-transform:uppercase'>Drug-Likeness Radar</div>",
                        unsafe_allow_html=True)
                    st.plotly_chart(fig_radar(res), use_container_width=True, key=f"rad_{i}")

                    # Tox pills
                    def tpill(cls,icon,label,detail):
                        return f'<div class="tpill {cls}"><span style="font-size:.9rem">{icon}</span><span><b>{label}</b>{f" · {detail}" if detail else ""}</span></div>'
                    hi={"LOW":"tp-ok","MEDIUM":"tp-warn","HIGH":"tp-bad"}.get(res["_herg"],"tp-ok")
                    hi_ic={"LOW":"✅","MEDIUM":"⚠️","HIGH":"🚨"}.get(res["_herg"],"❓")
                    ai2={"Low Risk":"tp-ok","Possible Concern":"tp-warn","Likely Mutagen":"tp-bad"}.get(res["_ames"],"tp-ok")
                    ai_ic={"Low Risk":"✅","Possible Concern":"⚠️","Likely Mutagen":"🧬"}.get(res["_ames"],"❓")
                    st.markdown(
                        tpill(hi,hi_ic,f"hERG: {res['_herg']}", "; ".join(res["_hf"][:2])) +
                        tpill(ai2,ai_ic,f"Ames: {res['_ames']}", "; ".join(res["_af"])) +
                        tpill("tp-bad" if res["_pains"] else "tp-ok",
                              "⚠️" if res["_pains"] else "✅",
                              f"PAINS: {'Flagged' if res['_pains'] else 'Clear'}", ""),
                        unsafe_allow_html=True)

                    # CYP quick summary
                    cyp_bad=[k for k,v in res["_cyp"].items() if v["hit"]]
                    if cyp_bad:
                        st.markdown(
                            f'<div class="tpill tp-warn"><span style="font-size:.9rem">⚡</span>'
                            f'<span>CYP inhibition likely: <b>{", ".join(cyp_bad)}</b></span></div>',
                            unsafe_allow_html=True)

                    # Optimise box
                    st.markdown('<div class="opt-box"><div class="opt-head">⚡ Optimisation Guide</div>', unsafe_allow_html=True)
                    for tip_k, tip_v in res["_tips"][:5]:
                        st.markdown(
                            f'<div class="opt-row"><span class="opt-k">{tip_k}</span>'
                            f'<span class="opt-v">{tip_v[:80]}{"…" if len(tip_v)>80 else ""}</span></div>',
                            unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Verdict banner
                    if not res["_org"]:
                        st.markdown('<div class="verdict vstop"><div class="vt">❌ Non-Organic Entity</div><div class="vb">Not applicable for standard pharmacokinetic profiling.</div></div>', unsafe_allow_html=True)
                    elif res["Grade"]=="A":
                        st.markdown(f'<div class="verdict vgo"><div class="vt">🟢 Primary Lead — Bio-Ready</div><div class="vb">All Lipinski pass · HIA predicted · CNS similarity confirmed · Lead {res["LeadScore"]}/100</div></div>', unsafe_allow_html=True)
                    elif res["_vc"]==0:
                        st.markdown(f'<div class="verdict vgo"><div class="vt">🟢 Bio-Ready Scaffold</div><div class="vb">Stable drug-like properties · Lead {res["LeadScore"]}/100</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="verdict vwarn"><div class="vt">🟡 Optimise: {", ".join(res["_vl"])}</div><div class="vb">Lead {res["LeadScore"]}/100 · See optimisation guide above</div></div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

    # ══════ TAB 2 — BOILED-EGG ══════
    with TABS[1]:
        st.markdown("""<div class="sec">
          <span class="sec-num">02</span>
          <span class="sec-title">BOILED-EGG ADME Map</span>
          <div class="sec-line"></div>
          <span class="sec-tag">Daina & Zoete, ChemMedChem 2016 · Bubble size ∝ Lead Score</span>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_boiled_egg(data), use_container_width=True)

        q1,q2 = st.columns(2)
        with q1:
            st.markdown('<div class="sec" style="margin-top:8px"><span class="sec-num">02b</span><span class="sec-title">QED Distribution</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
            st.plotly_chart(fig_qed_sa(data), use_container_width=True)
        with q2:
            st.markdown('<div class="sec" style="margin-top:8px"><span class="sec-num">02c</span><span class="sec-title">SA Score</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
            st.plotly_chart(fig_sa(data), use_container_width=True)

    # ══════ TAB 3 — ANALYSIS SUITE ══════
    with TABS[2]:
        if len(data)>1:
            at1,at2,at3,at4 = st.tabs(["Similarity Matrix","Parallel Coordinates","PCA Space","vs Approved Drugs"])
            with at1:
                st.caption("Tanimoto pairwise similarity of Morgan fingerprints (ECFP4)")
                st.plotly_chart(fig_similarity(data), use_container_width=True)
            with at2:
                st.caption("Drag axes to filter · Colour = Lead Score (red → amber → green)")
                st.plotly_chart(fig_parallel(data), use_container_width=True)
            with at3:
                st.caption("PCA of 2048-bit Morgan fingerprints — closer = more similar")
                p=fig_pca(data)
                if p: st.plotly_chart(p, use_container_width=True)
            with at4:
                sel=st.selectbox("Select compound",[d["ID"] for d in data])
                sr=next(d for d in data if d["ID"]==sel)
                st.plotly_chart(fig_approved(sr), use_container_width=True)
        else:
            st.info("Add 2 or more compounds to unlock comparison charts.")

    # ══════ TAB 4 — SA + CYP ══════
    with TABS[3]:
        st.markdown("""<div class="sec">
          <span class="sec-num">04</span>
          <span class="sec-title">Synthetic Accessibility</span>
          <div class="sec-line"></div>
          <span class="sec-tag">Ertl & Schuffenhauer, J Cheminformatics 2009</span>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_sa(data), use_container_width=True)

        st.markdown("""<div class="sec">
          <span class="sec-num">04b</span>
          <span class="sec-title">CYP Inhibition Panel — 5 Isoforms</span>
          <div class="sec-line"></div>
          <span class="sec-tag">Rule-based structural alerts</span>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_cyp(data), use_container_width=True)

        with st.expander("CYP Isoform Reference"):
            for cyp,(smts,desc) in CYP_RULES.items():
                st.markdown(
                    f"<span style='color:var(--amber);font-family:IBM Plex Mono,monospace;font-size:.7rem'><b>{cyp}</b></span>"
                    f" <span style='color:rgba(200,222,255,.4);font-family:IBM Plex Mono,monospace;font-size:.65rem'>— {desc}</span>",
                    unsafe_allow_html=True)

        st.markdown("""<div class="sec" style="margin-top:28px">
          <span class="sec-num">04c</span>
          <span class="sec-title">Interactive Property Editor</span>
          <div class="sec-line"></div>
          <span class="sec-tag">Live what-if analysis</span>
        </div>""", unsafe_allow_html=True)

        sel2 = st.selectbox("Compound to edit", [d["ID"] for d in data], key="pe2")
        sd   = next(d for d in data if d["ID"]==sel2)
        ec1,ec2 = st.columns(2)
        with ec1:
            nmw  = st.slider("MW (Da)",  100.0, 700.0, float(sd["_mw"]),  5.0)
            nlp  = st.slider("LogP",     -3.0,  9.0,   float(sd["_lp"]),  0.1)
            ntp  = st.slider("tPSA (Å²)",0.0,  200.0, float(sd["_tp"]),  1.0)
        with ec2:
            nhbd = st.slider("HBD",   0, 10, int(sd["_hbd"]))
            nhba = st.slider("HBA",   0, 15, int(sd["_hba"]))
            nrot = st.slider("RotBonds",0,20, int(sd["_rot"]))
        nviol=[n for n,ok in zip(["MW","LogP","HBD","HBA"],[nmw<500,nlp<5,nhbd<5,nhba<10]) if not ok]
        nhia=ntp<142; nbbb=(ntp<79 and -2<nlp<6)
        if not sd["_org"]: ng="F"
        elif len(nviol)==0 and sd["_sim"]>0.15 and nhia: ng="A"
        elif len(nviol)<=1 and nhia: ng="B"
        else: ng="C"
        nls=max(0,min(100,sd["LeadScore"]-(len(nviol)-sd["_vc"])*15-(0 if nhia else 10)))
        gcol={"A":"#4ade80","B":"#f5a623","C":"#fcd34d","F":"#ff5c5c"}
        st.markdown(f"""
<div style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;
padding:24px;margin:16px 0;display:flex;gap:52px;align-items:center;flex-wrap:wrap">
  <div style="text-align:center">
    <div style="font-family:IBM Plex Mono,monospace;font-size:.5rem;color:rgba(245,166,35,.3);letter-spacing:2px;margin-bottom:7px">ORIGINAL</div>
    <div style="font-family:'Playfair Display',serif;font-size:3rem;font-weight:900;color:{gcol.get(sd['Grade'],'#aaa')};letter-spacing:3px">{sd['Grade']}</div>
    <div style="font-family:IBM Plex Mono,monospace;font-size:.55rem;color:rgba(200,222,255,.3)">Lead: {sd['LeadScore']}/100</div>
  </div>
  <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:rgba(245,166,35,.2)">→</div>
  <div style="text-align:center">
    <div style="font-family:IBM Plex Mono,monospace;font-size:.5rem;color:rgba(245,166,35,.3);letter-spacing:2px;margin-bottom:7px">EDITED</div>
    <div style="font-family:'Playfair Display',serif;font-size:3rem;font-weight:900;color:{gcol.get(ng,'#aaa')};letter-spacing:3px">{ng}</div>
    <div style="font-family:IBM Plex Mono,monospace;font-size:.55rem;color:rgba(200,222,255,.3)">Lead: ~{nls:.0f}/100</div>
  </div>
  <div style="font-family:IBM Plex Mono,monospace;font-size:.63rem;color:rgba(200,222,255,.4);line-height:2.2">
    HIA: {"✅" if nhia else "❌"} &nbsp;&nbsp; BBB: {"✅" if nbbb else "❌"}<br>
    Violations: {len(nviol)} {("("+", ".join(nviol)+")") if nviol else ""}<br>
    Veber: {"✅" if (nrot<=10 and ntp<=140) else "❌"}
  </div>
</div>""", unsafe_allow_html=True)

    # ══════ TAB 5 — AI ══════
    with TABS[4]:
        if not enable_ai:
            st.info("Enable AI Features using the sidebar toggle.")
        else:
            for i, res in enumerate(data):
                st.markdown(f"""<div class="sec">
                  <span class="sec-num">✦</span>
                  <span class="sec-title">{res['ID']} — AI Analysis</span>
                  <div class="sec-line"></div>
                  <span class="sec-tag">Claude Sonnet</span>
                </div>""", unsafe_allow_html=True)
                props=(f"Grade:{res['Grade']} Lead:{res['LeadScore']} QED:{res['_qed']:.3f} "
                    f"MW:{res['_mw']:.1f} LogP:{res['_lp']:.2f} tPSA:{res['_tp']:.1f} "
                    f"HIA:{'Y' if res['_hia'] else 'N'} BBB:{'Y' if res['_bbb'] else 'N'} "
                    f"CNS_MPO:{res['_cm']}/6 SA:{res['_sa']}({res['SA_Label']}) "
                    f"hERG:{res['_herg']} Ames:{res['_ames']} PAINS:{'Y' if res['_pains'] else 'N'} "
                    f"CYP:{res['CYP_Hits']}/5 Violations:{res['_vc']}")
                ai1,ai2,ai3 = st.columns(3)
                with ai1:
                    st.markdown('<div class="ai-panel"><div class="ai-head">📊 Pharmacokinetic Assessment</div>', unsafe_allow_html=True)
                    with st.spinner("Analysing..."):
                        st.markdown(f'<div class="ai-body">{ai_explain(props)}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with ai2:
                    st.markdown('<div class="ai-panel"><div class="ai-head">🔄 Drug Repurposing Hint</div>', unsafe_allow_html=True)
                    with st.spinner("Analysing..."):
                        st.markdown(f'<div class="ai-body">{ai_repurpose(res["SMILES"], props)}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with ai3:
                    st.markdown('<div class="ai-panel"><div class="ai-head">⚗️ Structural Analogues</div>', unsafe_allow_html=True)
                    with st.spinner("Generating..."):
                        aj = ai_analogues(res["SMILES"], props)
                    try:
                        analogs = json.loads(re.sub(r'```json|```','',aj).strip())
                        for j,a in enumerate(analogs[:3]):
                            st.markdown(f"""<div class="ana-card">
<div class="ana-n">ANALOGUE {j+1}</div>
<div class="ana-ch">{a.get('change','Modification')}</div>
<div class="ana-sm">{a.get('smiles','—')}</div>
<div class="ana-ex">Expected: {a.get('expected_improvement','—')}</div>
</div>""", unsafe_allow_html=True)
                    except:
                        st.markdown('<div class="ai-body">Analogue generation unavailable.</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                if i<len(data)-1:
                    st.markdown('<hr style="border:none;border-top:1px solid rgba(245,166,35,.07);margin:28px 0">', unsafe_allow_html=True)

    # ══════ TAB 6 — FULL REPORT ══════
    with TABS[5]:
        st.markdown("""<div class="sec">
          <span class="sec-num">06</span>
          <span class="sec-title">Full Compound Report</span>
          <div class="sec-line"></div>
          <span class="sec-tag">Use Ctrl+P or Export HTML for print-ready PDF</span>
        </div>""", unsafe_allow_html=True)

        for res in data:
            gc2={"A":"#4ade80","B":"#f5a623","C":"#fcd34d","F":"#ff5c5c"}.get(res["Grade"],"#aaa")
            st.markdown(f"""
<div class="rblock">
  <div style="display:flex;align-items:baseline;gap:16px;margin-bottom:18px">
    <span style="font-family:'Playfair Display',serif;font-size:1.35rem;font-weight:900;color:{gc2}">{res['ID']}</span>
    <span style="font-family:IBM Plex Mono,monospace;font-size:.58rem;color:rgba(245,166,35,.4);letter-spacing:2px">
      GRADE {res['Grade']} &nbsp;·&nbsp; LEAD {res['LeadScore']}/100 &nbsp;·&nbsp; {res['Cluster']}
    </span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px">
    <div>
      <div class="rh">Physicochemical</div>
      <div class="rrow"><span class="rk">MW</span><span class="rv">{res['MW']} Da</span></div>
      <div class="rrow"><span class="rk">LogP</span><span class="rv">{res['LogP']}</span></div>
      <div class="rrow"><span class="rk">tPSA</span><span class="rv">{res['tPSA']} Å²</span></div>
      <div class="rrow"><span class="rk">HBD / HBA</span><span class="rv">{res['HBD']} / {res['HBA']}</span></div>
      <div class="rrow"><span class="rk">RotBonds</span><span class="rv">{res['RotBonds']}</span></div>
      <div class="rrow"><span class="rk">Fsp3</span><span class="rv">{res['Fsp3']}</span></div>
      <div class="rrow"><span class="rk">StereoCenters</span><span class="rv">{res['StereoCenters']}</span></div>
      <div class="rrow"><span class="rk">Rings</span><span class="rv">{res['Rings']}</span></div>
      <div class="rrow"><span class="rk">SA Score</span><span class="rv">{res['SA_Score']} ({res['SA_Label']})</span></div>
      <div class="rrow"><span class="rk">Complexity</span><span class="rv">{res['Complexity']:.0f} / 100</span></div>
    </div>
    <div>
      <div class="rh">ADME Profile</div>
      <div class="rrow"><span class="rk">HIA</span><span class="rv">{res['HIA']}</span></div>
      <div class="rrow"><span class="rk">BBB</span><span class="rv">{res['BBB']}</span></div>
      <div class="rrow"><span class="rk">QED</span><span class="rv">{res['QED']}</span></div>
      <div class="rrow"><span class="rk">logS (ESOL)</span><span class="rv">{res['logS']}</span></div>
      <div class="rrow"><span class="rk">Solubility</span><span class="rv">{res['Solubility']}</span></div>
      <div class="rrow"><span class="rk">CNS MPO</span><span class="rv">{res['CNS_MPO']} / 6</span></div>
      <div class="rrow"><span class="rk">Tanimoto</span><span class="rv">{res['Sim']}</span></div>
      <div class="rrow"><span class="rk">Veber Rule</span><span class="rv">{res['Veber']}</span></div>
      <div class="rrow"><span class="rk">Lip. Violations</span><span class="rv">{res['_vc']} / 4</span></div>
      <div class="rrow"><span class="rk">Oral Bio Score</span><span class="rv">{res['OralBioScore']} / 100</span></div>
    </div>
    <div>
      <div class="rh">Safety Profile</div>
      <div class="rrow"><span class="rk">hERG Risk</span><span class="rv">{res['_herg']}</span></div>
      <div class="rrow"><span class="rk">Ames Risk</span><span class="rv">{res['_ames']}</span></div>
      <div class="rrow"><span class="rk">PAINS</span><span class="rv">{res['PAINS']}</span></div>
      <div class="rrow"><span class="rk">CYP Hits</span><span class="rv">{res['CYP_Hits']} / 5</span></div>
      <div class="rrow"><span class="rk">Promiscuity</span><span class="rv">{res['PromiscuityRisk']:.0f} / 100</span></div>
      <div class="rrow"><span class="rk">Lead Score™</span><span class="rv">{res['LeadScore']} / 100</span></div>
      <div class="rrow"><span class="rk">Cluster</span><span class="rv">{res['Cluster']}</span></div>
      <div class="rrow"><span class="rk">Grade</span><span class="rv"><b style="color:{gc2}">{res['Grade']}</b></span></div>
    </div>
  </div>
  <div style="margin-top:12px;font-family:IBM Plex Mono,monospace;font-size:.55rem;
  color:rgba(200,222,255,.2);word-break:break-all">SMILES: {res['SMILES']}</div>
</div>""", unsafe_allow_html=True)

        with st.expander("Scientific References"):
            st.markdown("""
| # | Reference | Year |
|---|---|---|
| [1] | Daina A, Zoete V. BOILED-Egg. *ChemMedChem* 11:1117 | 2016 |
| [2] | Lipinski CA et al. Rule of Five. *ADDR* 46:3 | 2001 |
| [3] | Delaney JS. ESOL. *JCICS* 44:1000 | 2004 |
| [4] | Bickerton GR et al. QED. *Nat Chem* 4:90 | 2012 |
| [5] | Wager TT et al. CNS MPO. *ACS Chem Neurosci* 1:435 | 2010 |
| [6] | Baell JB, Holloway GA. PAINS. *JMC* 53:2719 | 2010 |
| [7] | Ertl P, Schuffenhauer A. SA Score. *J Cheminf* 1:8 | 2009 |
| [8] | Rogers D, Hahn M. ECFP. *JCIM* 50:742 | 2010 |
| [9] | Landrum G. RDKit | 2006+ |
""")

else:
    # EMPTY STATE
    st.markdown("""
<div style="text-align:center;padding:110px 40px;
border:1px solid var(--border2);border-radius:24px;margin-top:16px;
position:relative;overflow:hidden;background:var(--bg2)">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,rgba(245,166,35,0.03),transparent 65%)"></div>
  <div style="font-family:'Playfair Display',serif;font-size:7rem;font-weight:900;
  color:rgba(245,166,35,0.05);line-height:1;position:relative;letter-spacing:-3px">⬡</div>
  <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;
  color:rgba(245,166,35,0.15);letter-spacing:4px;position:relative;margin-top:-10px">
  Awaiting Input</div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:.63rem;
  color:rgba(200,222,255,.2);margin-top:16px;line-height:2.4;position:relative">
    Enter SMILES strings in the sidebar &nbsp;·&nbsp; comma-separated &nbsp;·&nbsp; or upload CSV<br>
    Example: &nbsp;<span style="color:rgba(245,166,35,.4)">CC(=O)Oc1ccccc1C(=O)O</span> (Aspirin)
  </div>
</div>""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
  ChemoFilter &nbsp;·&nbsp; Crystalline Noir Edition v7 &nbsp;·&nbsp; VIT Chennai MDP 2026
  <hr>
  Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; RDKit &nbsp;·&nbsp; Plotly &nbsp;·&nbsp; Claude AI &nbsp;·&nbsp; 21 Active Features
  <hr>
  BOILED-EGG [Daina 2016] &nbsp;·&nbsp; Lipinski [2001] &nbsp;·&nbsp; ESOL [Delaney 2004] &nbsp;·&nbsp; QED [Bickerton 2012]<br>
  SA Score [Ertl 2009] &nbsp;·&nbsp; CNS MPO [Wager 2010] &nbsp;·&nbsp; PAINS [Baell 2010] &nbsp;·&nbsp; RDKit [Landrum]
</div>
""", unsafe_allow_html=True)
