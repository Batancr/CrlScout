"""Builds "Monthly Finals Opponents" (monthly_finals_opponents.html) -- the renamed/expanded
successor to event_day_prep.html, per explicit user request (2026-07-19):

"For day 3 monthly finals, my projected opponents are mugi, sandbox and oker, Mohamed Light,
Adriel, but In fact please make a module just like the day 2 one, but for all 15 other
opponents I could face off in during the monthly finals" -- followed by: "no, you don't need
to do deck ratings that's not what i asked, just do the day 2 dashboard, but basically add
the 15 other players in the monthly finals" and "you could just add those players to the
existing module and just rename it monthly finals opponents."

WHAT THIS IS: the SAME 7 Day-2 opponent sections from event_day_prep.html (deck ratings,
set scores, swap suggestions -- unchanged, verbatim), PLUS a new second section covering the
15 possible Day 3 opponents the user named (5 "projected": Mugi, SandBox, 40k Oker, Mohamed
Light, Adriel -- note SandBox is already one of the 7 Day 2 opponents above, so she isn't
duplicated, just cross-referenced; plus 10 more: Pedro, Asaf, Clown/KickAsh, Vitor75, Sub,
SK Morten/Morten, Guriko, Polaris, JorZ, FrancoMedinaSL). Per explicit instruction, the Day 3
section is SCOUTING-STYLE only (their own top win-cons, decks that have empirically beaten
them, and what the wider tracked pool predicts beats their win-con archetype) -- NO deck
verdict badges or set scores, since the user has not prepped/shared specific Day 3 decks yet.
If those decks get shared later, this script's Day-3 section can be upgraded to the same
deck-rating format as Day 2, same pattern as event_day_prep.html.

Deliberately NOT integrated into build_dashboard.py's data/JS pipeline -- zero coupling,
same reasoning as the original event_day_prep.html (own icon-loading logic, own
analyze_target() logic duplicated from add_group_a_matchup_prep.py rather than imported,
since importing that script would side-effect-run its Excel-writing code). Supersedes
event_day_prep.html; crl_opponent_scout.html's header link is updated to point here instead.
"""
import glob
import json
import os
import base64
from collections import Counter

from build_duel_workbook import (
    classify_deck, build_dataset, classify_match_category, parse_time,
)

XLSX_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(XLSX_DIR, "monthly_finals_opponents.html")


def find_master_paths():
    search_globs = [
        "/mnt/user-data/uploads/CRL/master_*.json",
        os.path.join(XLSX_DIR, "master_*.json"),
        "master_*.json",
    ]
    paths, seen = [], set()
    for pattern in search_globs:
        for p in sorted(glob.glob(pattern)):
            if p not in seen:
                seen.add(p)
                paths.append(p)
    return paths


def build_card_icons():
    icons = {}
    for path in find_master_paths():
        try:
            with open(path) as f:
                battles = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for b in battles:
            for side in ("team", "opponent"):
                for p in b.get(side, []):
                    for c in p.get("cards", []) + p.get("supportCards", []):
                        name = c.get("name")
                        if not name:
                            continue
                        url = c.get("iconUrls", {}).get("medium")
                        if url and name not in icons:
                            icons[name] = url
    return icons


def embed_local_icons(icons):
    import re
    local_dir = os.path.join(XLSX_DIR, "card_icons")
    if not os.path.isdir(local_dir):
        return icons
    on_disk = set(os.listdir(local_dir))
    embedded = dict(icons)
    for name in list(icons.keys()):
        base_name = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
        fname = f"{base_name}.png"
        if fname in on_disk:
            fpath = os.path.join(local_dir, fname)
            if os.path.getsize(fpath):
                with open(fpath, "rb") as f:
                    embedded[name] = f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"
    return embedded


# NOTE: unlike event_day_prep.html, this page does NOT embed local icons as base64.
# The Day 3 scouting section alone renders 800+ icon instances (14 opponents x ~59 icons
# each across win-cons/empirical/predictive rows) -- embedding full-resolution local PNGs
# (~180KB each, uncompressed game art) at that volume blew the output past 150MB. Hotlinked
# external iconUrls keep the file small (~text URLs only); the tradeoff is this page needs
# network access to actually show the card images, unlike event_day_prep.html's fully
# offline-capable design. Fine for a working prep page that isn't meant to be permanent.
card_icons = build_card_icons()


def icon_strip(cards):
    imgs = []
    for name in cards:
        url = card_icons.get(name)
        if url:
            imgs.append(f'<div class="ci" title="{name}"><img src="{url}" alt="{name}"></div>')
        else:
            imgs.append(f'<div class="ci ci-fallback" title="{name}">{name[:1]}</div>')
    return '<div class="icon-strip">' + "".join(imgs) + "</div>"


VERDICT_STYLES = {
    "best": ("BEST", "#1B5E20", "#E8F5E9"),
    "strong": ("STRONG", "#1B5E20", "#E8F5E9"),
    "mild": ("MILD POSITIVE", "#0D47A1", "#E3F2FD"),
    "coinflip": ("COINFLIP", "#616161", "#F5F5F5"),
    "weak": ("WEAK SIGNAL", "#E65100", "#FFF3E0"),
    "avoid": ("AVOID", "#B71C1C", "#FCE8E6"),
    "nodata": ("NO DATA", "#9E9E9E", "#FAFAFA"),
}


def deck_block(deck_name, cards, wincons, verdict, detail):
    label, color, bg = VERDICT_STYLES[verdict]
    return f'''<div class="deck-block" style="background:{bg};border-left:4px solid {color};">
      <div class="deck-block-head">
        <span class="deck-name">{deck_name}</span>
        <span class="verdict-badge" style="background:{color};">{label}</span>
      </div>
      {icon_strip(cards)}
      <div class="deck-wincons">Win-con(s): <b>{wincons}</b></div>
      <div class="deck-detail">{detail}</div>
    </div>'''


# ---------------------------------------------------------------------------
# SECTION 1: Day 2 opponents -- UNCHANGED, verbatim from event_day_prep.html.
# Play order: DK -> Lucas jack -> RAD -> Adox -> Lucas.xit -> SandBox -> BenZer.
# ---------------------------------------------------------------------------
OPPONENTS = [
    {
        "name": "DK", "status": "on_deck", "sample_note": "9 tracked games vs him, thin sample",
        "top_wincons": "Royal Giant, Giant, Graveyard",
        "lead": "Lead with D1 (Goblin Drill) -- your only deck with a recorded win against him.",
        "set_score": 4.7,
        "swap_suggestion": "Consider swapping D2 or D4 (both weak, both already-repeated win-cons) for the Balloon/Miner control deck below -- it's DK's own #5 predicted counter (67%) and isn't in any of your other sets.",
        "decks": [
            ("D1 Evo GobDrill Berserker Control", ["Goblin Drill", "Magic Archer", "Giant Snowball", "Knight", "Berserker", "Poison", "Fire Spirit", "Inferno Tower"],
             "Goblin Drill", "best", "1/1 direct win (small sample)"),
            ("D2 Evo WB Bait 2.6 Cycle", ["Wall Breakers", "Dark Prince", "Goblin Barrel", "Dart Goblin", "Skeletons", "Ice Spirit", "Royal Delivery", "Tesla"],
             "Goblin Barrel + Wall Breakers", "weak", "0/1 direct, and the 1 near-identical build (5/8 overlap) played vs him lost"),
            ("D3 Hog GK EvoMK Spirit Empress", ["Mega Knight", "Golden Knight", "Goblin Cage", "Hog Rider", "Spirit Empress", "Vines", "Zappies", "Barbarian Barrel"],
             "Hog Rider", "weak", "0/1 direct (single game, not conclusive)"),
            ("D4 EvoMortar IWiz Cart HeroGobs", ["Skeleton Barrel", "Goblins", "Mortar", "Cannon Cart", "Fireball", "Minions", "Ice Wizard", "The Log"],
             "Mortar + Skeleton Barrel", "weak", "0/1 direct, near-match (5/8) also lost"),
        ],
    },
    {
        "name": "Lucas✨杰克", "status": "on_deck", "sample_note": "28 tracked games vs him, solid sample",
        "top_wincons": "Royal Giant, Wall Breakers, Goblin Drill",
        "lead": "D1 and D2 are your best-proven answers -- lead with either. D3 (Graveyard) is your clearest weak spot against a specific opponent all day.",
        "set_score": 7.8,
        "swap_suggestion": "Consider swapping D3 (Graveyard, your worst-rated deck all day, real losses on record) for the Mortar/Rascals bait toolbox below -- it's literally his #1 AND #5 predicted counters (100%, 80%).",
        "decks": [
            ("D1 Hog EvoLJ Spirit Empress Zappies", ["Lumberjack", "Bowler", "Mega Knight", "Hog Rider", "Spirit Empress", "Zappies", "Arrows", "Electro Spirit"],
             "Hog Rider", "strong", "3/3 (100%) direct win-con matches, near-match also won"),
            ("D2 Berserker Miner Evo Exec Nado", ["Executioner", "Balloon", "Knight", "Miner", "Berserker", "Tornado", "Zap", "Bomb Tower"],
             "Balloon + Miner", "strong", "2/2 (100%) direct, near-match also won"),
            ("D3 GY 3.0 Cycle", ["Archers", "Dark Prince", "Tesla", "Graveyard", "Poison", "Skeletons", "Ice Spirit", "Barbarian Barrel"],
             "Graveyard", "avoid", "1/3 (33%) direct, and both near-identical builds (7/8, 6/8 overlap) actually played vs him LOST"),
            ("D4 EvoMortar Goblinstein Cart EvoGhost", ["Mortar", "Goblinstein", "Royal Ghost", "Cannon Cart", "Lightning", "Goblins", "Minions", "The Log"],
             "Mortar", "coinflip", "1/2 (50%) direct"),
        ],
    },
    {
        "name": "RAD", "status": "confirmed", "sample_note": "20 tracked games vs him overall, only 2 with your specific win-cons",
        "top_wincons": "Wall Breakers, Graveyard, Miner",
        "lead": "No deck here is strongly proven -- direct history is too thin. Treat as a coinflip and pick based on what he brings in Game 1.",
        "set_score": 5.0,
        "swap_suggestion": "Truly no strong signal either way for this whole set -- lowest-confidence matchup of the day. The Archer Queen/Royal Hogs cycle deck below is his #1 predicted counter (100%) and would be worth adding as a 4th option.",
        "decks": [
            ("D1 Hog MM 2.8 Cycle", ["Firecracker", "Mighty Miner", "Tesla", "Hog Rider", "Earthquake", "Skeletons", "Electro Spirit", "The Log"],
             "Hog Rider", "nodata", "No direct data yet; Hog Rider doesn't crack his top community counters"),
            ("D2 EvoRHogs Monk SD", ["Royal Hogs", "Monk", "Archers", "Berserker", "Fireball", "Skeleton Dragons", "Ice Spirit", "Cannon"],
             "Royal Hogs", "mild", "Community-wide, Royal Hogs is a mild (~50%) counter to his win-con pool"),
            ("D3 Evo WB GobDrill 3.0 Cycle", ["Wall Breakers", "Magic Archer", "Giant Snowball", "Goblin Drill", "Knight", "Poison", "Fire Spirit", "Bomb Tower"],
             "Goblin Drill + Wall Breakers", "nodata", "Neither win-con stands out in the community data vs his archetype"),
        ],
    },
    {
        "name": "Adox", "status": "on_deck", "sample_note": "27 tracked games vs him overall, only 1 with your specific win-cons",
        "top_wincons": "Goblin Drill, Mortar, Wall Breakers",
        "lead": "Lead with D1. D2 already has a real loss on record against him -- don't reach for it first.",
        "set_score": 4.7,
        "swap_suggestion": "Consider swapping D2 (Hog Rider, real loss on record) for the Balloon/Miner control deck below -- it's his own #4 predicted counter (75%) and diversifies you off Hog Rider.",
        "decks": [
            ("D1 Evo WB Miner Evo Bats 2.5 Cycle", ["Wall Breakers", "Magic Archer", "Bats", "Miner", "Fire Spirit", "Skeletons", "Royal Delivery", "Bomb Tower"],
             "Miner + Wall Breakers", "best", "No direct games yet, but Wall Breakers is one of his own top-3 win-cons AND a positive community counter (51%)"),
            ("D2 Hog GK EvoMK Spirit Empress", ["Mega Knight", "Golden Knight", "Goblin Cage", "Hog Rider", "Spirit Empress", "Earthquake", "Electro Spirit", "Barbarian Barrel"],
             "Hog Rider", "avoid", "0/1 direct loss, and Hog Rider isn't a strong community counter to his pool"),
            ("D3 EvoMortar Berserker", ["Skeleton Barrel", "Dark Prince", "Mortar", "Berserker", "Fireball", "Dart Goblin", "Minions", "The Log"],
             "Mortar + Skeleton Barrel", "weak", "Mortar sits below breakeven (48%) community-wide vs his archetype"),
        ],
    },
    {
        "name": "Lucas.xit✨之安神", "status": "confirmed", "sample_note": "25 tracked games vs him overall, only 1 with your specific win-cons",
        "top_wincons": "Battle Ram, Prince, Royal Giant",
        "lead": "D1 is your only deck with a real result (a win) -- but his strongest community counters (Lava Hound, Balloon, Miner) aren't in this prep set at all.",
        "set_score": 5.8,
        "swap_suggestion": "Consider swapping D2 or D3 (both unrated, no data either direction) for the Mortar/Rascals bait toolbox below -- it's his #1 predicted counter (100%).",
        "decks": [
            ("D1 Evo WB 2.9 Cycle", ["Wall Breakers", "Magic Archer", "Goblin Barrel", "Ronin", "Fire Spirit", "Ice Spirit", "Royal Delivery", "Tesla"],
             "Goblin Barrel + Wall Breakers", "mild", "1/1 direct win, near-match also won -- tiny sample, and not his strongest community counter"),
            ("D2 Hog MM Evo Bats 2.9 Cycle", ["Firecracker", "Mighty Miner", "Bats", "Hog Rider", "Earthquake", "Skeletons", "The Log", "Bomb Tower"],
             "Hog Rider", "nodata", "No data"),
            ("D3 EGiant Evo ID Nado", ["Inferno Dragon", "Bowler", "Goblin Cage", "Electro Giant", "Lightning", "Guards", "Tornado", "Barbarian Barrel"],
             "Electro Giant", "nodata", "No data"),
        ],
    },
    {
        "name": "SandBox", "status": "confirmed", "sample_note": "81 tracked games vs her -- your deepest data set",
        "top_wincons": "Royal Hogs, Wall Breakers, Miner",
        "lead": "Lead with D3.",
        "set_score": 5.7,
        "swap_suggestion": "Consider swapping D2 (weakest of the three, 3 of 4 near-matches actually lost to her) for the Archer Queen/Royal Hogs cycle deck below -- it's her #1 predicted counter (100%).",
        "decks": [
            ("D3 GK GS GobDrill Bowler", ["Executioner", "Golden Knight", "Giant Snowball", "Goblin Drill", "Giant Skeleton", "Bowler", "Zappies", "Tornado"],
             "Goblin Drill", "best", "70% (7/10) direct win-con match rate; her only real weak point"),
            ("D1 EvoRHogs Berserker", ["Royal Hogs", "Magic Archer", "Tesla", "Ronin", "Berserker", "Fireball", "Electro Spirit", "Barbarian Barrel"],
             "Royal Hogs", "coinflip", "47% (7/15) direct"),
            ("D2 Evo WB Bait 2.4 Cycle", ["Wall Breakers", "Dark Prince", "Goblin Barrel", "Dart Goblin", "Fire Spirit", "Skeletons", "Ice Spirit", "Bomb Tower"],
             "Goblin Barrel + Wall Breakers", "avoid", "42% (5/12) direct; 3 of 4 near-identical builds actually played vs her LOST"),
        ],
    },
    {
        "name": "INA.BenZerRidel", "status": "confirmed", "sample_note": "4 tracked games vs her, thin sample (corrected link)",
        "top_wincons": "Royal Hogs, Goblin Barrel, Wall Breakers",
        "lead": "Lead with D3. D1 already has a real loss on record against her.",
        "set_score": 4.7,
        "swap_suggestion": "Consider swapping D1 (Goblin Drill, real loss on record) for the Archer Queen/Royal Hogs cycle deck below -- it's her #1 predicted counter (100%), and reinforces D3 which uses the same win-con.",
        "decks": [
            ("D3 EvoRHogs AQ EvoCannon 2.9 Cycle", ["Royal Hogs", "Archer Queen", "Cannon", "Earthquake", "Skeletons", "Ice Spirit", "Royal Delivery", "The Log"],
             "Royal Hogs", "best", "50% (1/2) direct -- and Royal Hogs is also her strongest predicted community counter (53%), both signals agree"),
            ("D2 Hog GK EvoMK Spirit Empress", ["Mega Knight", "Golden Knight", "Goblin Cage", "Hog Rider", "Spirit Empress", "Fireball", "Electro Spirit", "Barbarian Barrel"],
             "Hog Rider", "mild", "No direct games yet; community-wide Hog Rider sits at 45% vs her archetype -- roughly neutral"),
            ("D1 GobDrill Berserker EvoGhost Control", ["Royal Ghost", "Magic Archer", "Giant Snowball", "Goblin Drill", "Berserker", "Poison", "Fire Spirit", "Inferno Tower"],
             "Goblin Drill", "weak", "0/1 direct loss; Goblin Drill doesn't crack her top-5 predicted counters either"),
        ],
    },
]

PATTERN_ITEMS = [
    {
        "title": "#1 -- Hog Rider (6 of 7 sets)",
        "cards": ["Hog Rider"],
        "detail": "Every opponent except SandBox has a Hog Rider option in your prep (DK, Lucas✨杰克, RAD, Adox, Lucas.xit, BenZer). Your single biggest exposure -- if you play it more than once, especially early, later opponents have every reason to expect it.",
        "counters": [
            ("Goblin Drill cycle", ["Goblin Drill", "Giant Snowball", "Poison", "Fire Spirit"], "65% win rate vs Hog Rider, 251-game sample"),
            ("Golem / Lava Hound beatdown", ["Golem", "Lava Hound", "Tornado", "Lightning"], "also does well vs Hog Rider pools"),
        ],
    },
    {
        "title": "#2 -- Evo Wall Breakers chassis (4 of 7 sets)",
        "cards": ["Wall Breakers", "Magic Archer", "Royal Delivery", "Tesla"],
        "detail": "DK (D2), Adox (D1), Lucas.xit (D1), SandBox (D2). BenZer's corrected set does NOT include this chassis, so it's slightly less universal than first thought.",
        "counters": [
            ("Royal Hogs", ["Royal Hogs"], "60% win rate vs this chassis, 456-game sample"),
            ("Golem/Baby Dragon beatdown + Tornado", ["Golem", "Baby Dragon", "Tornado"], "also scores well"),
        ],
    },
    {
        "title": "#3 -- Goblin Drill (4 of 7 sets)",
        "cards": ["Goblin Drill"],
        "detail": "DK (D1), RAD (D3), SandBox (D3), BenZer (D1) -- more repeated than it first looked once BenZer's real prep was in.",
        "counters": [],
    },
    {
        "title": "#4 -- Mortar (3 of first 4 sets)",
        "cards": ["Mortar"],
        "detail": "DK, Lucas✨杰克, Adox -- all in your first 4 matches.",
        "counters": [
            ("Miner", ["Miner"], "61% win rate vs Mortar pools, 219-game sample"),
            ("Wall Breakers", ["Wall Breakers"], "59% win rate vs Mortar pools -- ironic, since it's also your own repeated deck"),
        ],
    },
]

SUGGESTED_ADDITIONS = [
    {
        "name": "Archer Queen / Royal Hogs cycle",
        "cards": ["Archer Queen", "Cannon", "Earthquake", "Fire Spirit", "Royal Delivery", "Royal Hogs", "Skeletons", "The Log"],
        "why": "Top predicted counter (67-100% win rate) for <b>5 of your 7 opponents</b> -- Adox, RAD, Lucas✨杰克, SandBox, BenZer. You don't currently have an Archer Queen deck at all. Single strongest addition available.",
    },
    {
        "name": "Mortar / Rascals bait toolbox",
        "cards": ["Barbarian Barrel", "Dart Goblin", "Fireball", "Goblins", "Mortar", "Rascals", "Ronin", "Skeleton Barrel"],
        "why": "Top predicted counter (67-100%) for <b>3 of your 7 opponents</b> -- Lucas.xit (both #1 and #2 slots), Lucas✨杰克 (#1 and #5), DK. A stronger refinement of the Mortar concept you already lean on.",
    },
    {
        "name": "Balloon / Miner control",
        "cards": ["Balloon", "Berserker", "Bomb Tower", "Executioner", "Knight", "Miner", "Tornado", "Zap"],
        "why": "Top predicted counter (67-75%) for <b>3 of your 7 opponents</b> -- Adox, DK, BenZer. Also helps diversify you off Hog Rider, your single most over-repeated win-con (see Pattern Warning below).",
    },
]

# ---------------------------------------------------------------------------
# SECTION 2 (NEW): Day 3 / Monthly Finals possible opponents -- scouting only,
# no deck ratings (user has no Day 3 decks prepped yet). Data computed live below
# via analyze_target(), duplicated from add_group_a_matchup_prep.py's logic
# (not imported, to avoid side-effect-running that script's Excel write).
#
# 5 "projected" (most likely, per user): Mugi, SandBox*, 40k Oker, Mohamed Light, Adriel.
# *SandBox is already one of the 7 Day 2 opponents above -- cross-referenced, not duplicated.
# 10 more possible: Pedro, Asaf, Clown (=KickAsh), Vitor75, Sub, SK Morten (=Morten),
# Guriko, Polaris, JorZ, FrancoMedinaSL.
# ---------------------------------------------------------------------------
DAY3_OPPONENTS = [
    ("Mugi", "#2CLV2RP0", True),
    ("40k Oker", "#YLVV0JPQ", True),
    ("Mohamed Light", "#G9YV9GR8R", True),
    ("Adriel", "#9CPCC890", True),
    ("Pedro", "#RJ88Y8U08", False),
    ("Asaf", "#RUQ0JU2P", False),
    ("Clown (KickAsh)", "#GPPYR9JYR", False),
    ("Vitor75", "#8LJ92G8UG", False),
    ("Sub", "#U890Q9UQ", False),
    ("SK Morten", "#R09228V", False),
    ("Guriko", "#2LJ0ULYCC", False),
    ("Polaris", "#U8RYGC8GU", False),
    ("JorZ", "#22LC8JG02", False),
    ("FrancoMedinaSL", "#UJQQCUCQ8", False),
]
# True = one of the user's 5 "projected" (most likely) Day 3 opponents.

MIN_GAMES_DECK = 3
MIN_GAMES_WINCON = 5

_ROSTER_TAGS_ONLY = {
    f"#{os.path.basename(p)[len('master_'):-len('.json')]}" for p in find_master_paths()
}

full_duel_log, _duel_summary, _session_stats = build_dataset()


def load_extended_rows_for_tag(tag):
    tag_digits = tag.lstrip('#')
    for candidate in (
        f'/mnt/user-data/uploads/CRL/extended_{tag_digits}.json',
        os.path.join(XLSX_DIR, f'extended_{tag_digits}.json'),
        f'extended_{tag_digits}.json',
    ):
        if os.path.exists(candidate):
            path = candidate
            break
    else:
        return []
    with open(path) as f:
        battles = json.load(f)
    rows = []
    for b in battles:
        team = b.get('team', [{}])[0]
        opp = b.get('opponent', [{}])[0]
        deck = [c['name'] for c in team.get('cards', [])]
        opp_deck = [c['name'] for c in opp.get('cards', [])]
        if not deck:
            continue
        battle_time = parse_time(b['battleTime'])
        category = classify_match_category(
            b.get('type'), b.get('gameMode', {}).get('name'), battle_time,
            opponent_tag=opp.get('tag'), roster_tags=_ROSTER_TAGS_ONLY,
        )
        if category is None:
            continue
        rows.append({
            'player_tag': team.get('tag'),
            'opponent_tag': opp.get('tag'),
            'battle_time': battle_time,
            'deck': deck,
            'opponent_deck': opp_deck,
            'crowns_for': team.get('crowns', 0),
            'crowns_against': opp.get('crowns', 0),
        })
    return rows


def analyze_target(tag):
    target_games = [r for r in full_duel_log if r['player_tag'] == tag and r['deck'] and len(r['deck']) == 8]
    used_extended_fallback = False
    if not target_games:
        extended = load_extended_rows_for_tag(tag)
        target_games = [r for r in extended if r['deck'] and len(r['deck']) == 8]
        used_extended_fallback = bool(target_games)

    wincon_games = Counter()
    wincon_wins = Counter()
    for r in target_games:
        won = r['crowns_for'] > r['crowns_against']
        for wc in (classify_deck(r['deck']) or []):
            wincon_games[wc] += 1
            if won:
                wincon_wins[wc] += 1
    top_wincons = [wc for wc, _g in wincon_games.most_common(3)]

    opp_deck_games_vs_target = Counter()
    opp_deck_wins_vs_target = Counter()
    for r in target_games:
        if not r.get('opponent_deck') or len(r['opponent_deck']) != 8:
            continue
        dk = ', '.join(sorted(r['opponent_deck']))
        opp_deck_games_vs_target[dk] += 1
        if r['crowns_for'] < r['crowns_against']:
            opp_deck_wins_vs_target[dk] += 1

    target_set = set(top_wincons)
    predicted = {'sample_size': 0, 'top_decks': []}
    if target_set:
        filtered = [
            r for r in full_duel_log
            if r.get('deck') and set(classify_deck(r['deck']) or []) & target_set
        ]
        opp_deck_games = Counter()
        opp_deck_wins = Counter()
        for r in filtered:
            if not r.get('opponent_deck') or len(r['opponent_deck']) != 8:
                continue
            dk = ', '.join(sorted(r['opponent_deck']))
            opp_deck_games[dk] += 1
            if r['crowns_for'] < r['crowns_against']:
                opp_deck_wins[dk] += 1
        top_decks = sorted(
            [{'deck': dk, 'games': g, 'wins': opp_deck_wins[dk], 'win_rate': opp_deck_wins[dk] / g}
             for dk, g in opp_deck_games.items() if g >= MIN_GAMES_DECK],
            key=lambda x: (-x['win_rate'], -x['games']),
        )[:4]
        predicted = {'sample_size': len(filtered), 'top_decks': top_decks}

    personal_threat_decks = {
        dk for dk, g in opp_deck_games_vs_target.items()
        if g >= 2 and opp_deck_wins_vs_target[dk] / g >= 0.5
    }
    predicted_deck_keys = {row['deck'] for row in predicted['top_decks']}
    double_confirmed = sorted(personal_threat_decks & predicted_deck_keys)

    ranked_empirical = sorted(
        [(dk, g, opp_deck_wins_vs_target[dk]) for dk, g in opp_deck_games_vs_target.items()
         if g >= MIN_GAMES_DECK],
        key=lambda x: (-(x[2] / x[1]), -x[1]),
    )[:3]

    return {
        'total_games': len(target_games),
        'used_extended_fallback': used_extended_fallback,
        'top_wincons': top_wincons,
        'wincon_games': wincon_games, 'wincon_wins': wincon_wins,
        'ranked_empirical': ranked_empirical,
        'predicted': predicted,
        'double_confirmed': double_confirmed,
    }


def scout_block(name, tag, is_projected, data):
    projected_tag = ' <span class="status-tag projected">projected</span>' if is_projected else ''
    fallback_note = (
        ' (from Extended Roster snapshot, not full match history)'
        if data['used_extended_fallback'] else ''
    )
    if data['total_games'] == 0:
        return f'''
        <div class="scout-card">
          <div class="scout-head"><span class="scout-name">{name}{projected_tag}</span><span class="scout-tag">{tag}</span></div>
          <div class="scout-empty">No games recorded for this player yet.</div>
        </div>'''

    wincon_rows = "".join(
        f'<div class="wc-row">{icon_strip([wc])}<span class="wc-label">{wc}</span>'
        f'<span class="wc-stat">{data["wincon_wins"][wc]}/{data["wincon_games"][wc]} '
        f'({100*data["wincon_wins"][wc]/data["wincon_games"][wc]:.0f}%)</span></div>'
        for wc in data['top_wincons']
    ) or '<div class="scout-empty">No clear win-con pattern yet.</div>'

    empirical_rows = "".join(
        f'<div class="counter-row">{icon_strip(dk.split(", "))}'
        f'<div class="counter-text"><span class="counter-stat" style="color:{"#B71C1C" if w/g>=0.6 else "#444"};">'
        f'{w}/{g} ({100*w/g:.0f}%)</span>{" ⚠ double-confirmed" if dk in data["double_confirmed"] else ""}</div></div>'
        for dk, g, w in data['ranked_empirical']
    ) or '<div class="scout-empty">No opponent deck has faced them 3+ times yet.</div>'

    predicted = data['predicted']
    predictive_rows = "".join(
        f'<div class="counter-row">{icon_strip(row["deck"].split(", "))}'
        f'<div class="counter-text"><span class="counter-stat">{row["wins"]}/{row["games"]} '
        f'({100*row["win_rate"]:.0f}%)</span>{" ⚠ also beat them personally" if row["deck"] in data["double_confirmed"] else ""}</div></div>'
        for row in predicted['top_decks']
    ) or '<div class="scout-empty">No deck reaches the sample minimum against this win-con pool yet.</div>'

    return f'''
    <div class="scout-card">
      <div class="scout-head"><span class="scout-name">{name}{projected_tag}</span><span class="scout-tag">{tag}</span></div>
      <div class="scout-meta">{data["total_games"]} tracked games{fallback_note}</div>
      <div class="scout-section-label">Their top win-cons</div>
      {wincon_rows}
      <div class="scout-section-label">What has empirically beaten them (3+ games)</div>
      {empirical_rows}
      <div class="scout-section-label">Predicted community counters ({predicted["sample_size"]}-game pool)</div>
      {predictive_rows}
    </div>'''


opponent_sections = []
for i, opp in enumerate(OPPONENTS, start=1):
    status_tag = ' <span class="status-tag on-deck">on deck</span>' if opp["status"] == "on_deck" else ""
    decks_html = "".join(
        deck_block(dn, cards, wc, verdict, detail) for dn, cards, wc, verdict, detail in opp["decks"]
    )
    score = opp["set_score"]
    score_color = "#1B5E20" if score >= 7 else ("#0D47A1" if score >= 6 else ("#616161" if score >= 5 else ("#E65100" if score >= 4.5 else "#B71C1C")))
    opponent_sections.append(f'''
    <section class="opp-section" id="opp-{i}">
      <div class="opp-head">
        <span class="opp-num">{i}</span>
        <h2>{opp["name"]}{status_tag}</h2>
        <span class="set-score" style="background:{score_color};">{score}/10</span>
      </div>
      <div class="opp-meta">{opp["sample_note"]} &middot; their top win-cons: <b>{opp["top_wincons"]}</b></div>
      <div class="deck-grid">{decks_html}</div>
      <div class="opp-lead">👉 {opp["lead"]}</div>
      <div class="opp-swap">🔁 {opp["swap_suggestion"]}</div>
    </section>''')

additions_html = "".join(f'''
    <div class="addition-item">
      <div class="addition-name">{a["name"]}</div>
      {icon_strip(a["cards"])}
      <div class="addition-why">{a["why"]}</div>
    </div>''' for a in SUGGESTED_ADDITIONS)

pattern_sections = []
for item in PATTERN_ITEMS:
    counters_html = "".join(
        f'<div class="counter-row">{icon_strip(cards)}<div class="counter-text"><b>{name}</b><br><span class="counter-detail">{detail}</span></div></div>'
        for name, cards, detail in item["counters"]
    )
    pattern_sections.append(f'''
    <div class="pattern-item">
      <div class="pattern-title">{item["title"]}</div>
      {icon_strip(item["cards"])}
      <div class="pattern-detail">{item["detail"]}</div>
      {"<div class='counters-label'>What the data says beats it:</div>" + counters_html if counters_html else ""}
    </div>''')

day3_cards = []
for name, tag, is_projected in DAY3_OPPONENTS:
    data = analyze_target(tag)
    day3_cards.append(scout_block(name, tag, is_projected, data))
day3_html = "".join(day3_cards)

nav_html = (
    "".join(f'<a href="#opp-{i}">{i}. {opp["name"]}</a>' for i, opp in enumerate(OPPONENTS, start=1))
    + '<a href="#day3" style="background:#E3F2FD;color:#0D47A1;border-color:#90CAF9;">Day 3 Opponents</a>'
    + '<a href="#additions" style="background:#E8F5E9;color:#1B5E20;border-color:#A5D6A7;">+ Deck Additions</a>'
    + '<a href="#pattern-warning" class="nav-warn">⚠ Pattern Warning</a>'
)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Monthly Finals Opponents -- Duel Cheat Sheet</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    background: #F4F6F8; color: #1a1a1a; margin: 0; padding: 0;
  }}
  .delete-banner {{
    background: #FFF3E0; color: #7A4A00; text-align: center; padding: 8px 16px;
    font-size: 12.5px; font-weight: 600; border-bottom: 1px solid #FFE0B2;
  }}
  .wrap {{ max-width: 980px; margin: 0 auto; padding: 20px 20px 60px; }}
  header.top {{ text-align: center; margin-bottom: 18px; }}
  header.top h1 {{ margin: 0 0 4px; font-size: 26px; }}
  header.top .subtitle {{ color: #555; font-size: 13.5px; }}
  .play-order {{
    background: #1F4E78; color: #fff; border-radius: 10px; padding: 12px 16px;
    text-align: center; font-size: 14px; font-weight: 600; margin-bottom: 16px;
  }}
  nav.jump {{
    display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-bottom: 24px;
  }}
  nav.jump a {{
    background: #fff; border: 1px solid #DADFE3; border-radius: 20px; padding: 6px 12px;
    font-size: 12.5px; text-decoration: none; color: #1F4E78; font-weight: 600;
  }}
  nav.jump a.nav-warn {{ background: #FCE8E6; color: #B71C1C; border-color: #F3C6C2; }}
  section.opp-section {{
    background: #fff; border-radius: 12px; padding: 18px 20px; margin-bottom: 16px;
    border: 1px solid #E3E7EA;
  }}
  .opp-head {{ display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }}
  .opp-num {{
    background: #1F4E78; color: #fff; width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px;
    flex-shrink: 0;
  }}
  .opp-head h2 {{ margin: 0; font-size: 19px; }}
  .set-score {{
    margin-left: auto; color: #fff; font-size: 14px; font-weight: 800; border-radius: 8px;
    padding: 4px 10px; flex-shrink: 0;
  }}
  .status-tag {{ font-size: 10.5px; font-weight: 700; border-radius: 10px; padding: 2px 8px; vertical-align: middle; }}
  .status-tag.on-deck {{ background: #FFF2CC; color: #7A4A00; }}
  .status-tag.projected {{ background: #E3F2FD; color: #0D47A1; }}
  .opp-meta {{ font-size: 12.5px; color: #666; margin: 4px 0 14px; }}
  .deck-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; }}
  .deck-block {{ border-radius: 8px; padding: 10px 12px; }}
  .deck-block-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; gap: 6px; }}
  .deck-name {{ font-size: 12.5px; font-weight: 700; }}
  .verdict-badge {{ color: #fff; font-size: 10px; font-weight: 700; border-radius: 8px; padding: 2px 8px; white-space: nowrap; }}
  .icon-strip {{ display: flex; flex-wrap: wrap; gap: 3px; margin-bottom: 6px; }}
  .ci {{ width: 30px; height: 37px; border-radius: 4px; overflow: hidden; background: #eee; flex-shrink: 0; }}
  .ci img {{ width: 100%; height: 100%; object-fit: cover; }}
  .ci-fallback {{ display: flex; align-items: center; justify-content: center; font-size: 12px; color: #999; }}
  .deck-wincons {{ font-size: 11.5px; margin-bottom: 4px; }}
  .deck-detail {{ font-size: 11.5px; color: #444; }}
  .opp-lead {{ margin-top: 14px; font-size: 13px; font-weight: 600; background: #F0F7FF; border-radius: 8px; padding: 10px 12px; }}
  .opp-swap {{ margin-top: 8px; font-size: 12.5px; background: #F3EEFF; border-radius: 8px; padding: 9px 12px; color: #4527A0; }}
  #day3 {{
    background: #F0F7FF; border: 2px solid #90CAF9; border-radius: 12px; padding: 20px; margin-bottom: 16px;
  }}
  #day3 h2 {{ color: #0D47A1; margin-top: 0; }}
  .day3-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }}
  .scout-card {{ background: #fff; border-radius: 10px; padding: 14px 16px; border: 1px solid #CFE3FB; }}
  .scout-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }}
  .scout-name {{ font-weight: 700; font-size: 14.5px; }}
  .scout-tag {{ font-size: 11px; color: #999; font-family: monospace; }}
  .scout-meta {{ font-size: 11.5px; color: #666; margin-bottom: 10px; }}
  .scout-section-label {{ font-size: 10.5px; font-weight: 700; color: #666; text-transform: uppercase; margin: 10px 0 4px; }}
  .scout-empty {{ font-size: 12px; color: #999; font-style: italic; padding: 4px 0; }}
  .wc-row {{ display: flex; align-items: center; gap: 8px; padding: 3px 0; }}
  .wc-row .icon-strip {{ margin-bottom: 0; }}
  .wc-label {{ font-size: 12px; flex: 1; }}
  .wc-stat {{ font-size: 11.5px; color: #666; font-weight: 600; }}
  #additions {{
    background: #E8F5E9; border: 2px solid #A5D6A7; border-radius: 12px; padding: 20px; margin-bottom: 16px;
  }}
  #additions h2 {{ color: #1B5E20; margin-top: 0; }}
  .addition-item {{ background: #fff; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; border: 1px solid #C8E6C9; }}
  .addition-name {{ font-weight: 700; font-size: 14px; margin-bottom: 6px; }}
  .addition-why {{ font-size: 12.5px; color: #444; margin-top: 6px; }}
  #pattern-warning {{
    background: #FFF8F7; border: 2px solid #F3C6C2; border-radius: 12px; padding: 20px;
  }}
  #pattern-warning h2 {{ color: #B71C1C; margin-top: 0; }}
  .pattern-item {{ background: #fff; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px; border: 1px solid #F3C6C2; }}
  .pattern-title {{ font-weight: 700; font-size: 14px; margin-bottom: 6px; }}
  .pattern-detail {{ font-size: 12.5px; color: #444; margin: 6px 0 10px; }}
  .counters-label {{ font-size: 11px; font-weight: 700; color: #666; text-transform: uppercase; margin-bottom: 4px; }}
  .counter-row {{ display: flex; align-items: center; gap: 10px; padding: 6px 0; border-top: 1px solid #f0f0f0; }}
  .counter-text {{ font-size: 12px; }}
  .counter-detail {{ color: #666; }}
  .counter-stat {{ font-weight: 700; }}
  .takeaway {{ background: #fff; border-radius: 10px; padding: 14px 16px; font-size: 13px; font-weight: 600; margin-top: 8px; }}
</style>
</head>
<body>
<div class="delete-banner">🗑 Working prep page for the CRL Monthly Finals -- safe to delete after the event, not linked into any other tracker data.</div>
<div class="wrap">
  <header class="top">
    <h1>Monthly Finals Opponents</h1>
    <p class="subtitle">Day 2 (below): your 7 prepped decks rated against real tracked data. Day 3 (further down): scouting data -- top win-cons and proven/predicted counters -- for all 15 possible opponents, since decks aren't prepped for that round yet.</p>
  </header>
  <div class="play-order">Day 2 play order: DK &rarr; Lucas✨杰克 &rarr; RAD &rarr; Adox &rarr; Lucas.xit✨之安神 &rarr; SandBox &rarr; INA.BenZerRidel</div>
  <nav class="jump">{nav_html}</nav>

  {"".join(opponent_sections)}

  <section id="day3">
    <h2>🗓 Day 3 / Monthly Finals -- 15 Possible Opponents</h2>
    <p style="font-size:13px;">Scouting data only -- no deck ratings yet since Day 3 decks aren't prepped. "Projected" tags mark your 5 most-likely opponents (Mugi, 40k Oker, Mohamed Light, Adriel -- SandBox is also projected but already covered in the Day 2 section above, not repeated here). The other 10 are additional possible opponents in the bracket.</p>
    <div class="day3-grid">{day3_html}</div>
  </section>

  <section id="additions">
    <h2>💡 Suggested Deck Additions (Day 2 pool)</h2>
    <p style="font-size:13px;">Data-driven picks that would help against multiple Day 2 opponents and aren't already in your current 7 sets.</p>
    {additions_html}
  </section>

  <section id="pattern-warning">
    <h2>⚠ Pattern-Detection Warning (Day 2 pool)</h2>
    <p style="font-size:13px;">All 7 Day 2 opponents are in your own round-robin group -- anyone who's compared notes with an earlier opponent could be scouting a pattern by the back half of your day.</p>
    {"".join(pattern_sections)}
    <div class="takeaway">Practical takeaway: Hog Rider is your real exposure this time. If two decks are similarly rated for an opponent, favor holding Hog Rider back rather than opening with it, especially from opponent 3 (RAD) onward. Your Royal Hogs and Graveyard/Mortar decks are comparatively under-used and give you a way to break the pattern.</div>
  </section>
</div>
</body>
</html>'''

with open(OUT_PATH, "w") as f:
    f.write(html)
print(f"wrote {OUT_PATH} ({len(html)} bytes)")
for name, tag, is_projected in DAY3_OPPONENTS:
    d = analyze_target(tag)
    print(f"  {name} ({tag}): {d['total_games']} games"
          f"{' [extended fallback]' if d['used_extended_fallback'] else ''}, "
          f"top wincons={d['top_wincons']}, predicted sample={d['predicted']['sample_size']}")
