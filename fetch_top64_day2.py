"""
Clash Royale battle log fetcher -- TOP 64 CRL FIELD (July 2026 Monthly Finals).

WHAT THIS IS: a separate fetch script from fetch_cr_battlelogs.py. That script tracks your
practice partners (53 players). THIS script tracks the full Day-1-Swiss-ranked top 64 field
for the July 2026 Monthly Finals -- i.e. everyone you (or anyone in the bracket) could face
in Day 2 group play, not just your usual practice partners. Source: the Day 1 Swiss standings
page (statsroyale.com/leagues/crl/july-2026-monthly-finals/day-1-swiss), ranks 1-65 minus
rank 17 (LF丨张✨Ink❤️llb, disqualified -- excluded per your instruction), giving exactly 64
players. Several names below already overlap your practice roster (same tag) -- that's fine,
see "MASTER FILE SHARING" below.

WHY A SEPARATE SCRIPT: keeps the two rosters/purposes clearly separated (practice-partner
tracking vs. tournament-field scouting) without one script's edits accidentally touching the
other's PLAYER_TAGS list. Both scripts write to the SAME kind of file
(master_<tag>.json / raw_<tag>.json) in the SAME folder, so Claude's dashboard/workbook
rebuild picks up data from both automatically (build_dataset() globs ALL master_*.json files
in the folder regardless of which script fetched them).

MASTER FILE SHARING: for players already in your practice roster (e.g. SandBox, Adox, RAD,
DK, Lucas.xit, Lucas✨杰克, Yoru, Mugi/むぎったん, Kimchi, EGW, coco/Coco, etc.) this script
merges into the SAME master_<tag>.json file that fetch_cr_battlelogs.py already uses --
same dedup-by-battleTime logic, so running both scripts is 100% safe and nothing gets
double-counted or overwritten. For the ~30 players who are ONLY in the top-64 field (not your
regular practice partners), this creates brand-new master_<tag>.json archives.

A FEW NAMES CHANGED SINCE YOUR LAST FETCH (same tag, different in-game display name right
now) -- noted here so it's not mistaken for a new/different player:
  - GPPYR9JYR: tracked as "KickAsh" in your practice roster, shows as "Clown" on this
    standings page.
  - LPRR9P: tracked as "Ruben"/"Rubén", shows as "RUBIZALEZ" here.
  - U2YVYGGV2: tracked as "Woo", shows as "우티비구독좋아요" here.
  - 9G28ULYR: tracked as "LucasXGamer", shows as "Lucas✨杰克" here.
This script uses the display names AS SHOWN ON THE STANDINGS PAGE below (doesn't matter for
data integrity -- the tag, not the name, determines the file path).

HOW TO RUN:
  1. Python 3 + `pip install requests`.
  2. Set your API token: export CR_API_TOKEN="paste_your_token_here"
  3. Run from the network your API key is whitelisted for:
         python3 fetch_top64_day2.py

OUTPUT (per player, in the current folder):
  - raw_<tag>.json    -- latest fetch only, overwritten each run (debugging)
  - master_<tag>.json -- accumulated history, only ever grows, deduped by battleTime

Also writes/appends to fetch_log.json (same shared log fetch_cr_battlelogs.py uses).

NOTE ON "LAST 7 DUEL SETS" / "DAY 2 ONLY": this script just fetches and archives raw battle
logs -- exactly like fetch_cr_battlelogs.py. It does NOT try to filter to Day 2 or limit to
7 duel sets itself; that filtering (identifying which archived battles fall inside the Day 2
live-tournament window, grouping them into real B03 duel sets via group_into_duels(), and
truncating to the most recent 7 per player) happens back in the Cowork session once you send
the master_*.json files back, using the same classify_match_category() / group_into_duels()
logic already built for Round 1. Reason: the Day 2 live time-window isn't knowable in advance
(same as Round 1's window, which had to be identified AFTER the fact from real battle
timestamps) -- so send the data back once Day 2 is actually done/in-progress and Claude will
identify the window and produce the last-7-duel-sets breakdown from there. A set that ended
2-0 will naturally show up as a 2-game duel, not artificially padded to 3.

HOW OFTEN TO RUN: the CR API only returns each player's most recent ~25-30 battles, so if you
want to catch every Day 2 duel for all 64 players (not just whatever's left in the API window
by the time you get around to fetching), run this MORE THAN ONCE during Day 2 -- e.g. once
partway through and once after it wraps -- same gap-risk protection as the practice-partner
script (a GAP-RISK WARNING will print if a re-fetch can't connect back to what's already
archived AND came back with a near-full page, meaning some games in between may be
unrecoverable).
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from urllib.parse import quote

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run: pip install requests")

# Top 64 CRL field, July 2026 Monthly Finals -- Day 1 Swiss standings, ranks 1-65 minus
# rank 17 (LF丨张✨Ink❤️llb, disqualified -- excluded per user instruction). 64 players.
PLAYER_TAGS = {
    "老板 Ι Batan'宙斯": "#9RQ8YRYQL",       # 1
    "Clown": "#GPPYR9JYR",                    # 2  (aka KickAsh in practice roster)
    "Yoru": "#2Q2QCYLPR",                     # 3
    "Mohamed Light": "#G9YV9GR8R",            # 4
    "adriel": "#9CPCC890",                    # 5
    "!¡osama™️!¡": "#CPGRQ8VQV",              # 6
    "EGW": "#C88VYCJC",                       # 7
    "むぎったん": "#2CLV2RP0",                 # 8  (aka Mugi)
    "GençAslan:)": "#2YQJJG0VL",              # 9
    "FrancoMedinaSL": "#UJQQCUCQ8",           # 10
    "ぐりてゃん": "#2LJ0ULYCC",                 # 11 (aka Guriko)
    "John77": "#2GCL89QGP",                   # 12
    "Kimchi77✨小小罗": "#PCUP9YLVG",          # 13 (aka Kimchi)
    "CAL Sub ™✨杰克": "#U890Q9UQ",            # 14 (aka Sub)
    "Rainbow": "#VR90898",                    # 15
    "INA.BenZerRidel": "#9GJ0Q0LGG",          # 16
    # rank 17, LF丨张✨Ink❤️llb #U90LPY0QV -- DISQUALIFIED, excluded
    "SandBox": "#Y022GRCJQ",                  # 18
    "사과도둑": "#8LJ98G0V",                    # 19
    "Asaf": "#RUQ0JU2P",                      # 20
    "TTK:MrAwesomeCR": "#2YQGC20C",           # 21
    "SK Morten": "#R09228V",                  # 22 (aka Morten)
    "Wallace": "#YJPPGL00",                   # 23
    "FelipePT": "#CGV0V99RQ",                 # 24
    "40k Oker": "#YLVV0JPQ",                  # 25
    "Dess": "#UJRR9RJUL",                     # 26
    "鬼舞辻無惨": "#UJYRYCU9",                  # 27 (aka Niuzi)
    "神│Venpers™☆": "#GU99JUJ",               # 28
    "てち": "#JPPC9URJ",                        # 29
    "HaRu": "#GGV9YLQY",                      # 30
    "ZQuentino": "#RRLV0GQCV",                # 31
    "JL Viiper": "#U200V9P",                  # 32
    "Lucas.xit✨之安神": "#2R09LUYPQ",         # 33
    "Adox": "#20R0VLJL92",                    # 34
    "Vitor75": "#8LJ92G8UG",                  # 35
    "CAPGUN": "#GR9L9V2LU",                   # 36
    "Turan✨": "#P8P0Q8CJ",                    # 37 (aka Turan)
    "Reminor": "#2829V8V0L",                  # 38
    "Polaris": "#U8RYGC8GU",                  # 39
    "Sosaa1of1": "#CPLGLPU80",                # 40
    "Klaus": "#2J9CR89",                      # 41
    "Coco": "#2VGG29RJ2",                     # 42 (aka coco)
    "⇀スキル丨Hadi": "#222LJ8Y8",              # 43
    "SK Dominik": "#J0VU9CGP",                # 44
    "SK xopxsam": "#2LQ2YP98",                # 45 (aka Xopxsam)
    "Pedro™️": "#RJ88Y8U08",                  # 46 (aka Pedro)
    "OS xAlee": "#VP9GJYQ2",                  # 47
    "Wyze❤️Ultimo": "#202GUYUP",              # 48
    "RAD": "#8QRCJQ9Y",                       # 49
    "Lucas✨杰克": "#9G28ULYR",                # 50 (aka LucasXGamer)
    "WL ツ Dam's ✨": "#R2PLLVCY8",            # 51
    "ꨄ Max ✨": "#QG2QPY0",                    # 52
    "Ian77": "#Y9R22RQ2",                     # 53
    "Viktor": "#2U2RQGQGC",                   # 54
    "RUBIZALEZ": "#LPRR9P",                   # 55 (aka Ruben/Rubén)
    "JorZ": "#22LC8JG02",                     # 56
    "TMX I Mateja": "#LJQVVVQGR",             # 57 (aka Mateja)
    "dark✨安花": "#9JL2YQ2RV",                # 58
    "DaniGamer": "#PY9LJCYV",                 # 59
    "kodigogg": "#22Q8LLU8J",                 # 60
    "우티비구독좋아요": "#U2YVYGGV2",           # 61 (aka Woo)
    "Nadir": "#2VYLGPPUV",                    # 62
    "くり": "#2LUY2Q98",                        # 63
    "fluffypotato99": "#GLJURPRV",            # 64
    "DK": "#8G9GJQRVQ",                       # 65 -- yes, only 64 slots used (rank 17 excluded)
}

assert len(PLAYER_TAGS) == 64, f"expected 64 players, got {len(PLAYER_TAGS)}"

API_BASE = "https://api.clashroyale.com/v1"

TOKEN = os.environ.get("CR_API_TOKEN")
if not TOKEN:
    sys.exit(
        "No API token found. Set it first, e.g.:\n"
        '  export CR_API_TOKEN="your_token_here"'
    )

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
}


def fetch_battlelog(tag: str):
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}/battlelog"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    return resp.json(), None


API_PAGE_SIZE_ASSUMED = 25
FETCH_LOG_PATH = "fetch_log.json"


def check_gap_risk(tag: str, name: str, existing_before_merge: list, new_battles: list):
    if not existing_before_merge or not new_battles:
        return None
    try:
        prev_latest = max(b.get("battleTime", "") for b in existing_before_merge)
        this_oldest = min(b.get("battleTime", "") for b in new_battles)
    except ValueError:
        return None
    if this_oldest <= prev_latest:
        return None

    gap_str_start, gap_str_end = prev_latest, this_oldest
    near_full_page = len(new_battles) >= API_PAGE_SIZE_ASSUMED - 3
    return {
        "tag": tag,
        "name": name,
        "gap_start_battle_time": gap_str_start,
        "gap_end_battle_time": gap_str_end,
        "this_fetch_battle_count": len(new_battles),
        "near_full_page": near_full_page,
        "high_risk": near_full_page,
    }


def merge_into_master(master_path: str, new_battles: list, tag: str, name: str):
    existing = []
    if os.path.exists(master_path):
        with open(master_path) as f:
            existing = json.load(f)

    gap_risk = check_gap_risk(tag, name, existing, new_battles)

    seen_times = {b.get("battleTime") for b in existing}
    added = 0
    for b in new_battles:
        if b.get("battleTime") not in seen_times:
            existing.append(b)
            seen_times.add(b.get("battleTime"))
            added += 1
    skipped = len(new_battles) - added

    existing.sort(key=lambda b: b.get("battleTime", ""))
    with open(master_path, "w") as f:
        json.dump(existing, f, indent=2)

    return added, skipped, gap_risk


def append_fetch_log(fetch_events: list):
    existing_log = []
    if os.path.exists(FETCH_LOG_PATH):
        try:
            with open(FETCH_LOG_PATH) as f:
                existing_log = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing_log = []
    existing_log.append({
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "fetch_top64_day2.py",
        "players": fetch_events,
    })
    with open(FETCH_LOG_PATH, "w") as f:
        json.dump(existing_log, f, indent=2)


def main():
    succeeded = []
    failed = []
    all_types_seen = set()
    all_modes_seen = set()
    gap_risks = []
    fetch_events = []

    for name, tag in PLAYER_TAGS.items():
        print(f"Fetching battle log for {name} ({tag}) ...")
        data, err = fetch_battlelog(tag)
        if data is None:
            print(f"  FAILED: {err}")
            failed.append((name, tag, err))
            time.sleep(0.3)
            continue

        safe_name = tag.replace("#", "")
        raw_path = f"raw_{safe_name}.json"
        master_path = f"master_{safe_name}.json"

        with open(raw_path, "w") as f:
            json.dump(data, f, indent=2)

        added, skipped, gap_risk = merge_into_master(master_path, data, tag, name)
        with open(master_path) as f:
            total_in_master = len(json.load(f))

        print(f"  Fetched {len(data)} battles from API -- "
              f"{added} new, {skipped} already in archive. "
              f"Archive now has {total_in_master} total battles.")
        succeeded.append((name, tag, added, total_in_master))
        fetch_events.append({
            "tag": tag, "name": name,
            "battles_returned": len(data), "new": added, "skipped": skipped,
            "total_in_archive": total_in_master,
            "gap_risk": gap_risk,
        })
        if gap_risk:
            gap_risks.append(gap_risk)

        for battle in data:
            btype = battle.get("type")
            if btype:
                all_types_seen.add(btype)
            mode = battle.get("gameMode", {}).get("name")
            if mode:
                all_modes_seen.add(mode)

        time.sleep(0.3)  # be polite to the API

    append_fetch_log(fetch_events)

    print("\n--- Summary ---")
    print(f"Succeeded: {len(succeeded)}/{len(PLAYER_TAGS)}")
    for name, tag, added, total in succeeded:
        print(f"  OK    {name} ({tag}): +{added} new, {total} total in archive")
    if failed:
        print(f"\nFailed: {len(failed)}")
        for name, tag, err in failed:
            print(f"  FAIL  {name} ({tag}): {err}")

    print("\n--- Distinct battle 'type' values seen this run ---")
    for t in sorted(all_types_seen):
        print(f"  - {t}")

    print("\n--- Distinct 'gameMode.name' values seen this run ---")
    for m in sorted(all_modes_seen):
        print(f"  - {m}")

    if gap_risks:
        print("\n--- GAP-RISK WARNING (possible missed battles) ---")
        print(
            "For these players, this fetch's oldest returned battle doesn't reach back far "
            "enough to connect with the newest battle already in the archive, AND this fetch "
            "came back with a near-full page -- meaning any friendly battles they played "
            "during the uncovered gap below may be permanently lost. Fetching MORE OFTEN "
            "during Day 2 is the only way to avoid this."
        )
        for gr in gap_risks:
            risk_label = "HIGH" if gr["high_risk"] else "possible"
            print(f"  [{risk_label}] {gr['name']} ({gr['tag']}): uncovered gap between "
                  f"{gr['gap_start_battle_time']} and {gr['gap_end_battle_time']} "
                  f"(this fetch returned {gr['this_fetch_battle_count']} battles)")
    else:
        print("\nNo gap-risk detected this run -- every player's new battles connect "
              "cleanly with what was already archived.")

    print(
        "\nDone. Send the master_*.json files back to Claude (not just raw_*.json) -- "
        "master files are the accumulated, deduped archive Claude will use to identify "
        "Day 2's live-tournament window and pull the last 7 duel sets per player."
    )


if __name__ == "__main__":
    main()
