"""
Discover unknown/missing top-64 CRL field members via their opponents.

WHY: the July 2026 Monthly Finals top-64 field is bracket play -- everyone in it only
faces other top-64 members in Official CRL matches. So if a top-64 player we've already
fetched shows an Official-CRL-classified battle against a tag we've never seen before,
that opponent must ALSO be part of the top-64 field (a late replacement, a name/tag we
mis-transcribed off the standings page, someone whose direct fetch failed, etc.) -- and
we get their tag for free from the battle record's `opponent.tag`, no re-research needed.

HOW TO RUN (in the Cowork session, after master_*.json files are on disk):
    python3 find_unknown_crl_opponents.py

WHAT IT DOES:
  1. Loads every master_<tag>.json / raw_<tag>.json / extended_<tag>.json / scout_<tag>.json
     in the data folder (same file set build_duel_workbook.py's load_rows() covers, plus
     extended/scout, so nothing already-tracked gets flagged as "unknown").
  2. Classifies every battle via the same classify_match_category() logic used everywhere
     else in this project (friendly + Friendly gameMode + inside a known live-tournament
     time cluster = Official CRL).
  3. For every Official-CRL-classified battle, checks whether opponent.tag is already a
     known tag (PLAYER_TAGS in fetch_cr_battlelogs.py, OR any archived
     master_/raw_/extended_/scout_ file). If not, it's flagged as an unknown top-64
     candidate.
  4. Prints a report: each unknown tag, the name(s) it showed up under, which already-
     tracked player(s) faced them and when, and how many Official CRL games total.

This does NOT auto-add anyone to PLAYER_TAGS -- it's a discovery report only. Review the
output, confirm the name/tag looks legitimate (not a data glitch), then add it to
fetch_cr_battlelogs.py's PLAYER_TAGS by hand (or ask Claude to do it) before the next fetch.
"""

import glob
import json
import os
import sys
from collections import defaultdict

# Reuse the exact same classification logic as the rest of the project, so "Official CRL"
# means the same thing here as everywhere else.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from build_duel_workbook import classify_match_category, parse_time
except ImportError:
    sys.exit(
        "Couldn't import build_duel_workbook.py -- run this script from the same folder "
        "(needs classify_match_category / parse_time)."
    )

DATA_DIR = "."

# The confirmed top-64 CRL field (July 2026 Monthly Finals, Day-1-Swiss, rank 17 excluded
# as DQ'd) -- see fetch_cr_battlelogs.py for the full name/tag mapping and provenance.
# IMPORTANT: the "any Official CRL opponent must also be top-64" assumption below is only
# valid when the SOURCE player is a confirmed top-64 member -- our other ~185 extended-
# roster/shadow players are NOT guaranteed to only face top-64 opponents (they're a much
# broader practice-partner pool, not bracket-restricted), so this script only scans battles
# logged by these 64 tags, not every archived file.
TOP_64_TAGS = {
    "#9RQ8YRYQL", "#GPPYR9JYR", "#2Q2QCYLPR", "#G9YV9GR8R", "#9CPCC890", "#CPGRQ8VQV",
    "#C88VYCJC", "#2CLV2RP0", "#2YQJJG0VL", "#UJQQCUCQ8", "#2LJ0ULYCC", "#2GCL89QGP",
    "#PCUP9YLVG", "#U890Q9UQ", "#VR90898", "#9GJ0Q0LGG", "#Y022GRCJQ", "#8LJ98G0V",
    "#RUQ0JU2P", "#2YQGC20C", "#R09228V", "#YJPPGL00", "#CGV0V99RQ", "#YLVV0JPQ",
    "#UJRR9RJUL", "#UJYRYCU9", "#GU99JUJ", "#JPPC9URJ", "#GGV9YLQY", "#RRLV0GQCV",
    "#U200V9P", "#2R09LUYPQ", "#20R0VLJL92", "#8LJ92G8UG", "#GR9L9V2LU", "#P8P0Q8CJ",
    "#2829V8V0L", "#U8RYGC8GU", "#CPLGLPU80", "#2J9CR89", "#2VGG29RJ2", "#222LJ8Y8",
    "#J0VU9CGP", "#2LQ2YP98", "#RJ88Y8U08", "#VP9GJYQ2", "#202GUYUP", "#8QRCJQ9Y",
    "#9G28ULYR", "#R2PLLVCY8", "#QG2QPY0", "#Y9R22RQ2", "#2U2RQGQGC", "#LPRR9P",
    "#22LC8JG02", "#LJQVVVQGR", "#9JL2YQ2RV", "#PY9LJCYV", "#22Q8LLU8J", "#U2YVYGGV2",
    "#2VYLGPPUV", "#2LUY2Q98", "#GLJURPRV", "#8G9GJQRVQ",
}
assert len(TOP_64_TAGS) == 64


def load_known_tags():
    """Every tag we already have SOME data for, from any source -- these never get
    flagged as 'unknown', even if they're not in fetch_cr_battlelogs.py's PLAYER_TAGS."""
    known = set()
    for prefix in ("master_", "raw_", "extended_", "scout_"):
        for path in glob.glob(os.path.join(DATA_DIR, f"{prefix}*.json")):
            base = os.path.basename(path)
            tag = base[len(prefix):-len(".json")]
            if tag and tag not in ("fetch_log", "roster_tags"):  # skip non-tag sidecar files
                known.add(f"#{tag}" if not tag.startswith("#") else tag)

    # Also pull in PLAYER_TAGS directly, in case a tag has been added to the script but no
    # fetch has run for it yet. fetch_cr_battlelogs.py calls sys.exit() at import time if
    # CR_API_TOKEN isn't set, so catch SystemExit too, not just Exception -- we don't need
    # the token here, just the PLAYER_TAGS dict, so a missing token shouldn't break this.
    try:
        import re as _re
        src = open("fetch_cr_battlelogs.py").read()
        start = src.index("PLAYER_TAGS = {")
        end = src.index("\n}", start) + 2
        ns = {}
        exec(src[start:end], ns)
        known |= set(ns["PLAYER_TAGS"].values())
    except (Exception, SystemExit, FileNotFoundError, ValueError):
        pass

    return known


def load_all_battles():
    """(tag, battle) for every archived battle belonging to a CONFIRMED top-64 player --
    NOT every archived file. See the TOP_64_TAGS comment above for why this scope matters:
    the bracket-play assumption only holds for the 64 confirmed field members. Prefers
    master_<tag>.json (the accumulated archive) over raw_<tag>.json (latest snapshot only)
    when both exist for a tag."""
    out = []
    for tag in TOP_64_TAGS:
        safe = tag.replace("#", "")
        master_path = os.path.join(DATA_DIR, f"master_{safe}.json")
        raw_path = os.path.join(DATA_DIR, f"raw_{safe}.json")
        path = master_path if os.path.exists(master_path) else raw_path
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                battles = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for b in battles:
            out.append((tag, b))
    return out


def main():
    known_tags = load_known_tags()
    print(f"Loaded {len(known_tags)} already-known tags across all archived files.\n")

    battles = load_all_battles()
    print(f"Scanning {len(battles)} archived battles for Official CRL matches...\n")

    # tag -> {"names": set(), "faced_by": [(our_tag, our_name, battle_time), ...]}
    unknown = defaultdict(lambda: {"names": set(), "faced_by": []})

    for our_tag, b in battles:
        btype = b.get("type")
        mode_name = b.get("gameMode", {}).get("name")
        try:
            battle_time = parse_time(b["battleTime"])
        except (KeyError, ValueError):
            continue
        team = b.get("team", [{}])[0]
        opp = b.get("opponent", [{}])[0]
        opp_tag = opp.get("tag")
        if not opp_tag:
            continue

        category = classify_match_category(
            btype, mode_name, battle_time,
            opponent_tag=opp_tag, roster_tags=known_tags,
        )
        if category != "Official CRL":
            continue

        if opp_tag not in known_tags:
            unknown[opp_tag]["names"].add(opp.get("name", "?"))
            unknown[opp_tag]["faced_by"].append(
                (our_tag, team.get("name", "?"), b.get("battleTime"))
            )

    if not unknown:
        print("No unknown Official CRL opponents found -- every opponent tag seen in an "
              "Official CRL match is already in the archive. Nothing to add.")
        return

    print(f"--- {len(unknown)} UNKNOWN Official-CRL opponent tag(s) found ---\n")
    print("These are strong top-64 candidates (bracket play means their opponents in "
          "Official CRL are also top-64 members) -- review and add to fetch_cr_battlelogs.py's "
          "PLAYER_TAGS if the name looks legitimate.\n")

    for tag, info in sorted(unknown.items(), key=lambda kv: -len(kv[1]["faced_by"])):
        names = ", ".join(sorted(info["names"]))
        print(f"{tag}  (seen as: {names})  -- {len(info['faced_by'])} Official CRL game(s)")
        for our_tag, our_name, bt in sorted(info["faced_by"], key=lambda x: x[2] or "")[:5]:
            print(f"    faced by {our_name} ({our_tag}) at {bt}")
        if len(info["faced_by"]) > 5:
            print(f"    ... and {len(info['faced_by']) - 5} more")
        print()


if __name__ == "__main__":
    main()
