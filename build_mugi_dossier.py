"""
Build a dedicated, comprehensive scouting dossier on Mugi (#2CLV2RP0) as a standalone
HTML page (crl_mugi_dossier.html). Zero-coupled to the rest of the pipeline -- reads the
archived master_*.json files directly and renders everything client-independent.

Sections:
  1. Profile + threat summary
  2. Batan head-to-head (the 2-0)
  3. Every set Mugi has LOST (with the winning decks)
  4. Full arsenal, grouped by archetype, with W/L + CRL/Practice split + icon strips
  5. Staple cards (his tells)
  6. Duel-set sequencing (what he leads / follows / closes with)
  7. His own archetype win rates (strong vs shaky decks)
  8. Empirical counters (what has beaten him)
  9. Community counters (what beats his win-con archetypes across the whole pool)
  10. Game plan for Batan + how Mugi likely adjusts
"""
import base64
import glob
import json
import os
from collections import Counter, defaultdict

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_duel_workbook import classify_match_category, parse_time, classify_deck

XLSX_DIR = "/mnt/user-data/uploads/CRL"
MUGI = "2CLV2RP0"
MUGIH = "#2CLV2RP0"
BATAN = "9RQ8YRYQL"
OUT_PATH = "crl_mugi_dossier.html"

# ------------------------------------------------------------------ icons
def find_master_paths():
    # Dedupe by BASENAME, not full path -- the same master_<tag>.json exists in both
    # /home/claude and the uploads dir, and counting both would double every stat.
    paths, seen = [], set()
    for pattern in ["master_*.json", f"{XLSX_DIR}/master_*.json"]:
        for p in sorted(glob.glob(pattern)):
            base = os.path.basename(p)
            if base not in seen:
                seen.add(base); paths.append(p)
    return paths

def build_card_icons():
    icons = {}
    for path in find_master_paths():
        try:
            battles = json.load(open(path))
        except (json.JSONDecodeError, OSError):
            continue
        for b in battles:
            for side in ("team", "opponent"):
                for p in b.get(side, []):
                    for c in p.get("cards", []) + p.get("supportCards", []):
                        name = c.get("name")
                        url = c.get("iconUrls", {}).get("medium")
                        if name and url and name not in icons:
                            icons[name] = url
    return icons

CARD_ICONS = build_card_icons()

def icon_strip(cards, size=34):
    imgs = []
    for name in cards:
        url = CARD_ICONS.get(name)
        if url:
            imgs.append(f'<div class="ci" title="{name}"><img src="{url}" alt="{name}"></div>')
        else:
            imgs.append(f'<div class="ci ci-fallback" title="{name}">{name[:1]}</div>')
    return f'<div class="icon-strip" style="--ci:{size}px">' + "".join(imgs) + "</div>"

def wc_label(deck):
    wc = classify_deck(list(deck))
    return ", ".join(wc) if wc else "no classified win-con"

# ------------------------------------------------------------------ load Mugi
mugi_battles = json.load(open(f"master_{MUGI}.json" if os.path.exists(f"master_{MUGI}.json")
                              else f"{XLSX_DIR}/master_{MUGI}.json"))

def load_master(tag):
    for p in (f"master_{tag}.json", f"{XLSX_DIR}/master_{tag}.json"):
        if os.path.exists(p):
            return json.load(open(p))
    return []

# ------------------------------------------------------------------ compute
# Profile
cat_results = defaultdict(lambda: {"w":0,"l":0})
first_bt = last_bt = None
for b in mugi_battles:
    bt = parse_time(b["battleTime"])
    cat = classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt)
    if cat is None:
        continue
    first_bt = bt if first_bt is None or bt < first_bt else first_bt
    last_bt = bt if last_bt is None or bt > last_bt else last_bt
    team, opp = b["team"][0], b["opponent"][0]
    cf, ca = team.get("crowns") or 0, opp.get("crowns") or 0
    if cf > ca: cat_results[cat]["w"] += 1
    elif cf < ca: cat_results[cat]["l"] += 1

crl_w, crl_l = cat_results["Official CRL"]["w"], cat_results["Official CRL"]["l"]
prac_w, prac_l = cat_results["Practice"]["w"], cat_results["Practice"]["l"]

# Card frequency
card_freq = Counter()
n_tracked = 0
for b in mugi_battles:
    bt = parse_time(b["battleTime"])
    if classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt) is None:
        continue
    n_tracked += 1
    for c in b["team"][0].get("cards", []):
        card_freq[c["name"]] += 1

# Arsenal grouped by archetype
deck_stats = defaultdict(lambda: {"g":0,"w":0,"l":0,"crl":0,"prac":0})
for b in mugi_battles:
    bt = parse_time(b["battleTime"])
    cat = classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt)
    if cat is None:
        continue
    deck = tuple(sorted(c["name"] for c in b["team"][0].get("cards", [])))
    team, opp = b["team"][0], b["opponent"][0]
    cf, ca = team.get("crowns") or 0, opp.get("crowns") or 0
    d = deck_stats[deck]; d["g"] += 1
    d["crl" if cat == "Official CRL" else "prac"] += 1
    if cf > ca: d["w"] += 1
    elif cf < ca: d["l"] += 1

by_arch = defaultdict(list)
for deck, s in deck_stats.items():
    by_arch[wc_label(deck)].append((deck, s))
arch_sorted = sorted(by_arch.items(),
                     key=lambda kv: -sum(s["g"] for _, s in kv[1]))

# Archetype win rates
arch_wr = defaultdict(lambda: [0,0])
for deck, s in deck_stats.items():
    lab = wc_label(deck)
    arch_wr[lab][0] += s["w"]; arch_wr[lab][1] += s["w"] + s["l"]

# Sequencing (CRL sets)
crl_rows = []
for b in mugi_battles:
    bt = parse_time(b["battleTime"])
    if classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt) != "Official CRL":
        continue
    opp = b["opponent"][0]
    crl_rows.append({"bt":bt, "day":bt.date().isoformat(), "opp":opp.get("tag"),
                     "oname":opp.get("name"),
                     "wc":wc_label(tuple(c["name"] for c in b["team"][0].get("cards",[]))),
                     "deck":[c["name"] for c in b["team"][0].get("cards",[])],
                     "odeck":[c["name"] for c in opp.get("cards",[])],
                     "cf":b["team"][0].get("crowns") or 0, "ca":opp.get("crowns") or 0})
sets = defaultdict(list)
for r in crl_rows:
    sets[(r["day"], r["opp"])].append(r)
for k in sets:
    sets[k].sort(key=lambda r: r["bt"])

pos_wc = defaultdict(Counter)
for grp in sets.values():
    for i, r in enumerate(grp, 1):
        pos_wc[min(i,3)][r["wc"]] += 1

# Set records
set_records = []  # (day, oname, otag, w, l, games)
for (day, otag), grp in sets.items():
    w = sum(1 for r in grp if r["cf"] > r["ca"]); l = len(grp) - w
    set_records.append((day, grp[0]["oname"], otag, w, l, grp))
set_records.sort(key=lambda x: (x[0], x[1]))
lost_sets = [s for s in set_records if s[4] > s[3]]

# Empirical counters (what beat Mugi across all tracked players)
beat_wc = Counter()
beat_examples = defaultdict(list)
total_vs = wins_vs = 0
for path in find_master_paths():
    battles = json.load(open(path))
    for b in battles:
        opp = b["opponent"][0]
        if opp.get("tag") != MUGIH:
            continue
        bt = parse_time(b["battleTime"])
        cat = classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt)
        if cat is None:
            continue
        team = b["team"][0]
        cf, ca = team.get("crowns") or 0, opp.get("crowns") or 0
        total_vs += 1
        if cf > ca:
            wins_vs += 1
            deck = [c["name"] for c in team.get("cards", [])]
            lab = wc_label(tuple(deck))
            beat_wc[lab] += 1
            if len(beat_examples[lab]) < 2:
                beat_examples[lab].append((team.get("name"), sorted(deck)))

# Community counters vs Mugi-style win-cons
MUGI_WINCONS = {"Graveyard","Goblin Drill","Royal Hogs","Balloon","Miner",
                "Goblin Barrel","Wall Breakers","Royal Giant","Mortar"}
comm = defaultdict(lambda: [0,0])
for path in find_master_paths():
    battles = json.load(open(path))
    for b in battles:
        bt = parse_time(b["battleTime"])
        if classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt) is None:
            continue
        team, opp = b["team"][0], b["opponent"][0]
        opp_wc = set(classify_deck([c["name"] for c in opp.get("cards", [])]))
        if not (opp_wc & MUGI_WINCONS):
            continue
        our = wc_label(tuple(c["name"] for c in team.get("cards", [])))
        if our == "no classified win-con":
            continue
        cf, ca = team.get("crowns") or 0, opp.get("crowns") or 0
        if cf == ca:
            continue
        comm[our][1] += 1
        if cf > ca:
            comm[our][0] += 1
comm_ranked = sorted(((w/g, w, g, lab) for lab,(w,g) in comm.items() if g >= 10),
                     reverse=True)

# Batan H2H detail (the 2-0)
batan_games = []
for b in load_master(BATAN):
    opp = b["opponent"][0]
    if opp.get("tag") != MUGIH:
        continue
    bt = parse_time(b["battleTime"])
    cat = classify_match_category(b.get("type"), b.get("gameMode",{}).get("name"), bt)
    team = b["team"][0]
    cf, ca = team.get("crowns") or 0, opp.get("crowns") or 0
    batan_games.append({"bt":bt, "cat":cat,
                        "res":"W" if cf>ca else ("L" if cf<ca else "T"),
                        "cf":cf, "ca":ca,
                        "mydeck":[c["name"] for c in team.get("cards",[])],
                        "mywc":wc_label(tuple(c["name"] for c in team.get("cards",[]))),
                        "opdeck":[c["name"] for c in opp.get("cards",[])],
                        "opwc":wc_label(tuple(c["name"] for c in opp.get("cards",[]))) })
batan_games.sort(key=lambda x: x["bt"])

print(f"Mugi: CRL {crl_w}-{crl_l}, Practice {prac_w}-{prac_l}, {len(deck_stats)} distinct decks")
print(f"Lost {len(lost_sets)} CRL sets; empirical {wins_vs}/{total_vs} losses; {len(comm_ranked)} community counters")

# ------------------------------------------------------------------ render
def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def h2h_row(g):
    badge = "W" if g["res"]=="W" else ("L" if g["res"]=="L" else "T")
    cls = "win" if g["res"]=="W" else ("loss" if g["res"]=="L" else "tie")
    return f'''<div class="h2h-game">
      <div class="h2h-meta"><span class="rescell {cls}">{badge}</span> {g["bt"].strftime("%b %d %H:%M")} · {g["cf"]}–{g["ca"]} crowns · <span class="tag">{esc(g["cat"])}</span></div>
      <div class="h2h-side"><span class="side-label side-you">Batan</span> <span class="wc">{esc(g["mywc"])}</span>{icon_strip(g["mydeck"],30)}</div>
      <div class="h2h-side"><span class="side-label side-opp">Mugi</span> <span class="wc">{esc(g["opwc"])}</span>{icon_strip(g["opdeck"],30)}</div>
    </div>'''

# 2. Batan head-to-head
h2h_html = "".join(h2h_row(g) for g in batan_games)

# 3. Lost sets
def lost_set_block(rec):
    day, oname, otag, w, l, grp = rec
    winner_decks = ""
    # pull winning opponent's deck from grp (the opp side beat Mugi in the games Mugi lost)
    for r in grp:
        if r["ca"] > r["cf"]:  # Mugi lost this game -> opponent (odeck) won
            winner_decks += f'''<div class="mini-game">
              <span class="rescell loss">L</span> Mugi's <span class="wc">{esc(r["wc"])}</span> lost to:
              <span class="wc">{esc(wc_label(tuple(r["odeck"])))}</span>{icon_strip(r["odeck"],28)}</div>'''
    return f'''<div class="lostset">
      <div class="lostset-head">{day} · Mugi <b>lost</b> the set to <b>{esc(oname)}</b> ({w}–{l})</div>
      {winner_decks}
    </div>'''
lost_html = "".join(lost_set_block(r) for r in lost_sets)

# 4. Arsenal
def arch_block(lab, decks):
    aw = sum(s["w"] for _, s in decks); al = sum(s["l"] for _, s in decks)
    tot = sum(s["g"] for _, s in decks)
    wr = arch_wr[lab]
    wrpct = f"{wr[0]/wr[1]*100:.0f}%" if wr[1] else "–"
    rows = ""
    for deck, s in sorted(decks, key=lambda x: -x[1]["g"]):
        rows += f'''<div class="deckrow">
          <div class="deckrow-stat"><b>{s["g"]}g</b> <span class="wl">{s["w"]}W-{s["l"]}L</span>
            <span class="split">CRL {s["crl"]} · Prac {s["prac"]}</span></div>
          {icon_strip(list(deck),30)}
        </div>'''
    return f'''<div class="arch">
      <div class="arch-head"><span class="arch-name">{esc(lab)}</span>
        <span class="arch-stat">{tot} games · {aw}W-{al}L · {wrpct} win</span></div>
      {rows}
    </div>'''
arsenal_html = "".join(arch_block(lab, decks) for lab, decks in arch_sorted)

# 5. Card frequency
card_html = ""
for name, ct in card_freq.most_common(24):
    pct = ct / n_tracked * 100
    url = CARD_ICONS.get(name, "")
    img = f'<img src="{url}" alt="{esc(name)}">' if url else f'<span class="ci-fallback">{esc(name[:1])}</span>'
    card_html += f'''<div class="cardfreq">
      <div class="ci">{img}</div>
      <div class="cardfreq-name">{esc(name)}</div>
      <div class="cardfreq-bar"><div class="cardfreq-fill" style="width:{pct:.0f}%"></div></div>
      <div class="cardfreq-pct">{ct} · {pct:.0f}%</div>
    </div>'''

# 6. Sequencing
def seq_col(pos):
    items = "".join(f'<div class="seq-item"><span class="seq-n">{c}×</span> {esc(wc)}</div>'
                    for wc, c in pos_wc[pos].most_common())
    labels = {1:"Game 1 — what he opens with", 2:"Game 2 — the follow-up", 3:"Game 3 — the decider"}
    return f'<div class="seq-col"><div class="seq-head">{labels[pos]}</div>{items}</div>'
seq_html = "".join(seq_col(p) for p in (1,2,3))

# 7. Archetype win rates (strong/shaky)
awr_ranked = sorted(((w/g, w, g, lab) for lab,(w,g) in arch_wr.items() if g >= 3), reverse=True)
awr_html = ""
for wr, w, g, lab in awr_ranked:
    cls = "good" if wr >= 0.7 else ("mid" if wr >= 0.5 else "bad")
    awr_html += f'''<div class="awr-row">
      <div class="awr-bar"><div class="awr-fill {cls}" style="width:{wr*100:.0f}%"></div></div>
      <div class="awr-pct">{wr*100:.0f}%</div>
      <div class="awr-lab">{esc(lab)} <span class="awr-n">({w}/{g})</span></div>
    </div>'''

# 8. Empirical counters
emp_html = ""
for lab, ct in beat_wc.most_common(14):
    exs = beat_examples[lab]
    ex_html = "".join(f'<div class="emp-ex"><span class="emp-who">{esc(who)}</span>{icon_strip(deck,26)}</div>'
                      for who, deck in exs)
    emp_html += f'''<div class="emp-row">
      <div class="emp-lab"><b>{ct}×</b> beaten by <span class="wc">{esc(lab)}</span></div>
      {ex_html}
    </div>'''

# 9. Community counters
comm_html = ""
for wr, w, g, lab in comm_ranked[:16]:
    small = " small-sample" if g < 25 else ""
    cls = "good" if wr >= 0.6 else ("mid" if wr >= 0.5 else "bad")
    comm_html += f'''<div class="comm-row{small}">
      <div class="comm-bar"><div class="comm-fill {cls}" style="width:{wr*100:.0f}%"></div></div>
      <div class="comm-pct">{wr*100:.0f}%</div>
      <div class="comm-lab">{esc(lab)} <span class="comm-n">({w}/{g}{" · low sample" if g<25 else ""})</span></div>
    </div>'''

HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mugi — Scouting Dossier</title>
<style>
  :root {{
    --bg:#0f1420; --plane:#161d2e; --plane2:#1d2740; --line:#2a3550;
    --txt:#e6ebf5; --muted:#93a1c0; --accent:#ffd23f; --you:#5db0ff; --opp:#ff7a7a;
    --good:#37c871; --mid:#5db0ff; --bad:#ff7a7a;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--txt);
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    line-height:1.5; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:22px 18px 80px; }}
  header.top {{ border-bottom:1px solid var(--line); padding-bottom:16px; margin-bottom:8px; }}
  h1 {{ margin:0 0 4px; font-size:30px; letter-spacing:-.02em; }}
  h1 .tag {{ color:var(--muted); font-size:16px; font-weight:500; }}
  .sub {{ color:var(--muted); font-size:14px; }}
  .kpis {{ display:flex; flex-wrap:wrap; gap:10px; margin:16px 0; }}
  .kpi {{ background:var(--plane); border:1px solid var(--line); border-radius:12px;
    padding:12px 16px; min-width:130px; flex:1; }}
  .kpi .n {{ font-size:24px; font-weight:800; }}
  .kpi .k {{ font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
  .kpi.warn .n {{ color:var(--accent); }}
  section {{ background:var(--plane); border:1px solid var(--line); border-radius:14px;
    padding:18px 20px; margin:16px 0; }}
  section h2 {{ margin:0 0 4px; font-size:19px; }}
  section .lead {{ color:var(--muted); font-size:13.5px; margin:0 0 14px; }}
  .icon-strip {{ display:flex; gap:3px; flex-wrap:wrap; margin:4px 0; }}
  .ci {{ width:var(--ci,34px); height:calc(var(--ci,34px)*1.2); flex-shrink:0; }}
  .ci img {{ width:100%; height:100%; object-fit:contain; }}
  .ci-fallback {{ display:flex; align-items:center; justify-content:center; width:var(--ci,34px);
    height:calc(var(--ci,34px)*1.2); background:var(--plane2); border:1px solid var(--line);
    border-radius:4px; font-size:12px; color:var(--muted); }}
  .wc {{ color:var(--accent); font-weight:600; font-size:13px; }}
  .tag {{ color:var(--muted); font-size:11.5px; }}
  /* threat box */
  .threat {{ background:linear-gradient(135deg,#2a1d1d,#1d2740); border:1px solid #4a2d2d; }}
  .threat ul {{ margin:8px 0 0; padding-left:20px; }}
  .threat li {{ margin:6px 0; }}
  /* h2h */
  .h2h-game {{ background:var(--plane2); border:1px solid var(--line); border-radius:10px;
    padding:12px 14px; margin:10px 0; }}
  .h2h-meta {{ font-size:12.5px; color:var(--muted); margin-bottom:8px; }}
  .h2h-side {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin:4px 0; }}
  .side-label {{ font-weight:700; font-size:12px; padding:2px 8px; border-radius:6px; }}
  .side-you {{ background:rgba(93,176,255,.18); color:var(--you); }}
  .side-opp {{ background:rgba(255,122,122,.18); color:var(--opp); }}
  .rescell {{ display:inline-block; width:20px; height:20px; line-height:20px; text-align:center;
    border-radius:5px; font-weight:800; font-size:12px; }}
  .rescell.win {{ background:rgba(55,200,113,.2); color:var(--good); }}
  .rescell.loss {{ background:rgba(255,122,122,.2); color:var(--opp); }}
  .rescell.tie {{ background:var(--plane); color:var(--muted); }}
  /* lost sets */
  .lostset {{ background:var(--plane2); border:1px solid #3a4a2d; border-left:4px solid var(--good);
    border-radius:10px; padding:12px 14px; margin:10px 0; }}
  .lostset-head {{ font-size:14px; margin-bottom:8px; }}
  .mini-game {{ display:flex; align-items:center; gap:6px; flex-wrap:wrap; font-size:12.5px;
    color:var(--muted); margin:5px 0; }}
  /* arsenal */
  .arch {{ border-top:1px solid var(--line); padding:12px 0; }}
  .arch:first-child {{ border-top:none; }}
  .arch-head {{ display:flex; justify-content:space-between; align-items:baseline; gap:10px;
    margin-bottom:6px; flex-wrap:wrap; }}
  .arch-name {{ font-weight:700; font-size:15px; color:var(--accent); }}
  .arch-stat {{ font-size:12.5px; color:var(--muted); }}
  .deckrow {{ display:flex; align-items:center; gap:12px; padding:5px 0; flex-wrap:wrap; }}
  .deckrow-stat {{ min-width:150px; font-size:12.5px; }}
  .deckrow-stat .wl {{ color:var(--muted); }}
  .deckrow-stat .split {{ display:block; font-size:11px; color:var(--muted); }}
  /* card freq */
  .cardgrid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:8px; }}
  .cardfreq {{ display:flex; align-items:center; gap:8px; background:var(--plane2);
    border:1px solid var(--line); border-radius:8px; padding:6px 8px; }}
  .cardfreq .ci {{ width:26px; height:32px; }}
  .cardfreq-name {{ font-size:12px; flex:1; min-width:0; }}
  .cardfreq-bar {{ width:44px; height:6px; background:var(--plane); border-radius:3px; overflow:hidden; }}
  .cardfreq-fill {{ height:100%; background:var(--accent); }}
  .cardfreq-pct {{ font-size:11px; color:var(--muted); white-space:nowrap; }}
  /* sequencing */
  .seq-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
  .seq-col {{ background:var(--plane2); border:1px solid var(--line); border-radius:10px; padding:12px; }}
  .seq-head {{ font-weight:700; font-size:13px; margin-bottom:8px; color:var(--you); }}
  .seq-item {{ font-size:13px; padding:3px 0; }}
  .seq-n {{ color:var(--accent); font-weight:700; }}
  /* bars */
  .awr-row,.comm-row {{ display:flex; align-items:center; gap:10px; padding:4px 0; }}
  .awr-bar,.comm-bar {{ width:120px; height:9px; background:var(--plane2); border-radius:5px; overflow:hidden; flex-shrink:0; }}
  .awr-fill,.comm-fill {{ height:100%; }}
  .awr-fill.good,.comm-fill.good {{ background:var(--good); }}
  .awr-fill.mid,.comm-fill.mid {{ background:var(--mid); }}
  .awr-fill.bad,.comm-fill.bad {{ background:var(--bad); }}
  .awr-pct,.comm-pct {{ width:42px; font-weight:700; font-size:13px; }}
  .awr-lab,.comm-lab {{ font-size:13px; }}
  .awr-n,.comm-n {{ color:var(--muted); font-size:12px; }}
  .comm-row.small-sample {{ opacity:.6; }}
  /* empirical */
  .emp-row {{ border-top:1px solid var(--line); padding:8px 0; }}
  .emp-row:first-child {{ border-top:none; }}
  .emp-lab {{ font-size:13.5px; margin-bottom:4px; }}
  .emp-ex {{ display:flex; align-items:center; gap:8px; margin:3px 0; }}
  .emp-who {{ font-size:11.5px; color:var(--muted); min-width:120px; }}
  /* gameplan */
  .plan {{ background:linear-gradient(135deg,#1d2a20,#1d2740); border:1px solid #2d4a37; }}
  .plan h3 {{ margin:14px 0 6px; font-size:15px; color:var(--good); }}
  .plan p {{ margin:6px 0; font-size:14px; }}
  .plan .adjust h3 {{ color:var(--opp); }}
  .foot {{ color:var(--muted); font-size:12px; margin-top:20px; text-align:center; }}
</style></head><body><div class="wrap">

<header class="top">
  <h1>Mugi <span class="tag">#{MUGI}</span></h1>
  <div class="sub">Scouting dossier · projected Monthly Finals opponent · data through {last_bt.strftime("%b %d %Y")} ({total_vs} tracked games vs our field)</div>
</header>

<div class="kpis">
  <div class="kpi"><div class="n">{crl_w}–{crl_l}</div><div class="k">Official CRL (games)</div></div>
  <div class="kpi"><div class="n">{prac_w}–{prac_l}</div><div class="k">Practice (games)</div></div>
  <div class="kpi warn"><div class="n">{len(deck_stats)}</div><div class="k">distinct decks / {n_tracked}g</div></div>
  <div class="kpi"><div class="n">{len(lost_sets)}</div><div class="k">CRL sets lost (of {len(set_records)})</div></div>
  <div class="kpi"><div class="n">{wins_vs}/{total_vs}</div><div class="k">our field's wins vs him</div></div>
</div>

<section class="threat">
  <h2>⚠️ Threat read</h2>
  <ul>
    <li><b>He is a pure flex player.</b> {len(deck_stats)} different decks in just {n_tracked} tracked games — he plays essentially the entire meta and hard-targets what he expects you to bring. You can't archetype-counter <i>him</i>; you counter the field and punish the specific deck he shows.</li>
    <li><b>He's strong.</b> {crl_w}–{crl_l} in Official CRL ({crl_w/(crl_w+crl_l)*100:.0f}% of games), only <b>{len(lost_sets)} set losses</b> across both tournament days — to Batan (you), Coco, and 40k Oker.</li>
    <li><b>You already have his number once.</b> You beat him <b>2–0</b> with Graveyard + Goblin-Barrel bait. The data below is about not letting him adjust his way out of it.</li>
    <li><b>His shakiest decks:</b> Royal Giant (40% win) and his Royal Hogs / Balloon-Miner lists (57%) — see the archetype win-rate chart. His Mortar and Hog Rider decks are where he's undefeated.</li>
  </ul>
</section>

<section>
  <h2>Your 2–0 over him (Day 1)</h2>
  <p class="lead">The exact games. Note the duel card-lock: he had to bring two entirely different decks, and both lacked a clean answer to what you led with.</p>
  {h2h_html}
</section>

<section>
  <h2>Every set he's actually lost — and to what</h2>
  <p class="lead">Only three players have taken a set off Mugi in tracked CRL play. Here's exactly which decks did it.</p>
  {lost_html}
</section>

<section>
  <h2>His full arsenal ({len(deck_stats)} decks, by archetype)</h2>
  <p class="lead">Every deck he's brought, grouped by win condition, with his record on each and the Official-CRL / Practice split. This is his whole hand — expect any of these.</p>
  {arsenal_html}
</section>

<section>
  <h2>His staple cards (the tells)</h2>
  <p class="lead">Cards Mugi runs most often across all {n_tracked} decks. High-frequency cards are what he's comfortable with — a fast read on which archetype he's on.</p>
  <div class="cardgrid">{card_html}</div>
</section>

<section>
  <h2>How he sequences a duel set</h2>
  <p class="lead">What win-con he tends to open, follow, and close with across his {len(set_records)} tracked CRL sets. Useful for predicting his Game 2/3 once you've seen Game 1.</p>
  <div class="seq-grid">{seq_html}</div>
</section>

<section>
  <h2>His own decks, ranked by win rate</h2>
  <p class="lead">Which of Mugi's archetypes actually perform (min 3 decisive games). Green = his weapons, red = where he's beatable.</p>
  {awr_html}
</section>

<section>
  <h2>What has beaten him (empirical)</h2>
  <p class="lead">Decks from our tracked field that actually took games off Mugi — {wins_vs} wins across {total_vs} games. Small sample, so read as directional.</p>
  {emp_html}
</section>

<section>
  <h2>What beats his win-cons (whole-pool model)</h2>
  <p class="lead">Across every tracked game, when someone faced a Mugi-style win-con (Graveyard / Goblin Drill / Royal Hogs / Balloon-Miner / Goblin Barrel / Wall Breakers / Royal Giant / Mortar), how did each of our win-cons do? Bigger sample than the head-to-head. Faded rows = small sample, don't over-trust.</p>
  {comm_html}
</section>

<section class="plan">
  <h2>🎯 Game plan vs Mugi</h2>
  <h3>Lead with Graveyard again — it's your best and most-proven line.</h3>
  <p>Graveyard is the single deck that's beaten him most across the whole field (see empirical), you main it, and it's a coin-flip-or-better into most of his lists. His Day-1 Royal Hogs deck had no real Graveyard answer — that's the game you already won.</p>
  <h3>Do NOT re-run the same second deck.</h3>
  <p>He's now seen your Goblin-Barrel / Wall-Breakers bait. Expect him to pack concentrated splash (Valkyrie, Log, Bomber/Bats) to blank it. Pivot your second slot to <b>Royal Hogs</b> (your best whole-pool counter at 63% into his archetypes) or your <b>Hog Rider</b> deck — Hog is one of only two things that's beaten him multiple times, and it races his slower Balloon/Mortar/Royal-Giant lines before they set up.</p>
  <h3>Target his shaky decks.</h3>
  <p>If you can bait him onto Royal Giant (40% win) or Royal Hogs / Balloon-Miner (57%), you're in his worst matchups. His Mortar/Skeleton-Barrel and Hog Rider decks are undefeated in the data — don't get into a grind with those; out-tempo instead.</p>
  <div class="adjust">
  <h3>How he likely adjusts to avoid another 2–0</h3>
  <p><b>Anti-Graveyard prep:</b> he'll bring a building + splash core (Bowler/Valkyrie/Bomb Tower + Poison, maybe Freeze) in one deck specifically to survive your GY. His Day-1 loss came from having zero of that.</p>
  <p><b>Anti-bait splash:</b> expect heavy splash in his other deck so your bait stops trading up.</p>
  <p><b>Tempo pivot:</b> being a flex, he may try to out-race rather than out-defend — a fast-cycle Hog/Royal-Hogs to beat Graveyard on the clock, plus an X-Bow or Mortar siege to punish your slower deck. Counter-move: don't bring two slow decks; keep at least one fast win-con so he can't safely commit to a siege.</p>
  </div>
</section>

<div class="foot">Generated from {total_vs} tracked games vs Mugi across the archived master files. Empirical head-to-head samples are small — treat as directional, not definitive. Practice = clanMate/Friendly; Official CRL = live-tournament time-cluster matches.</div>

</div></body></html>'''

open(OUT_PATH, "w").write(HTML)
print(f"wrote {OUT_PATH}: {os.path.getsize(OUT_PATH)} bytes")
