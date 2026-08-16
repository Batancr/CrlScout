"""
Clash Royale battle log fetcher -- now with a persistent, accumulating archive.

WHY THIS CHANGED: the Clash Royale API's battlelog endpoint only returns each
player's most recent ~25-30 battles, not their full history. Every previous
version of this script overwrote raw_<tag>.json on each run, which meant
re-running it later could silently lose older practice duels that had aged
out of the API's returned window. This version fixes that: it still writes
the latest snapshot to raw_<tag>.json (handy for debugging), but ALSO merges
every fetch into a persistent master_<tag>.json per player that only ever
grows -- new battles get appended, already-seen battles are skipped, nothing
already captured is ever lost, even as the live API window slides forward.

ROSTER UPDATE 2026-07-19: PLAYER_TAGS now also includes the full top-64 CRL field (July 2026
Monthly Finals, Day-1-Swiss standings, rank 17 excluded as DQ'd) -- not just your regular
practice partners. This is now the single script to run; the standalone fetch_top64_day2.py
is no longer needed going forward (its roster is folded in here). If a future top-64 field
member is missing a tag (a late replacement, a fetch failure that never got a tag confirmed,
etc.), the fastest way to find their tag without re-researching is to look at the `opponent`
side of an already-tracked top-64 player's own Official-CRL-classified battles -- since
bracket play is top-64-vs-top-64 only, any opponent tag that shows up there is by definition
also part of the top-64 field, tag included in the battle record for free.

HOW TO RUN:
  1. Python 3 + `pip install requests`.
  2. Set your API token: export CR_API_TOKEN="paste_your_token_here"
     (don't hardcode it in this file, especially if it's ever committed to git)
  3. Edit PLAYER_TAGS below if you want to add/remove players.
  4. Run from the network your API key is whitelisted for:
         python3 fetch_cr_battlelogs.py

OUTPUT (per player):
  - raw_<tag>.json    -- latest fetch only, overwritten each run (debugging)
  - master_<tag>.json -- accumulated history, only ever grows, deduped by
                         battleTime (unique per player's own battle log)

Also writes/appends to:
  - fetch_log.json -- one entry per run, with a timestamp and per-player
                       battle counts/gap-risk flags. This is what makes the
                       gap-risk warning below possible at all: it's how we'd
                       notice if a player played more friendlies than the API
                       returns (~25-30) in between two fetches, which would
                       mean some of the games in the middle permanently aged
                       out of the API window and were never captured by any
                       fetch -- undetectable after the fact without this log.

The script prints how many NEW battles were added vs already-seen (skipped)
for each player, so you can see at a glance whether anything's actually new
since the last run -- and, added 2026-07-18, a GAP-RISK WARNING section
flagging any player where this fetch's oldest battle doesn't connect back to
what was already archived, which is the concrete symptom of the API-window
data-loss risk described above.
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

# Confirmed player roster (name -> tag). Edit freely to add/remove players.
PLAYER_TAGS = {
    # Monthly Finals qualifiers added to tracking 2026-08-16
    "Soudy": "#290UQY8C",
    "Ardentoas": "#RP0L2Y8C9",
    # Day-2 CRL group opponents (added 2026-08-16)
    "SK xopxsam2": "#Y99Y90VQV",   # the '2' account Batan faces Day 2 (distinct from tracked SK xopxsam #2LQ2YP98)
    "RemiEli": "#2JRLG8PUQ",
    "Adriel": "#9CPCC890",
    "Asaf": "#RUQ0JU2P",
    "Betfas": "#V0L800PUJ",
    "EGW": "#C88VYCJC",
    "ElMollejas": "#80ULUJLYY",
    "ErBacce": "#J89JRRU",
    "FurkanArabaci": "#989P0PCCR",
    "Kimchi": "#PCUP9YLVG",  # corrected 2026-07-17: #RU9VQV9C is his main, not his practice account
    "Kitassyan": "#P8RLY0V9",
    "LucasXGamer": "#9G28ULYR",
    "Mateja": "#LJQVVVQGR",
    "Morten": "#R09228V",
    "Mugi": "#2CLV2RP0",
    "Ruben": "#LPRR9P",
    "Ryley": "#C0V0UQ9UY",
    "Samuel Bassotto": "#PCJ29YJJ",
    "Taa": "#LP8PLVJCU",
    "Viiper": "#U200V9P",
    "Vitor75": "#8LJ92G8UG",
    "Wallace": "#YJPPGL00",
    "Xopxsam": "#2LQ2YP98",
    "Yoru": "#2Q2QCYLPR",
    "Batan": "#9RQ8YRYQL",
    "Batan (2nd acct)": "#9RG0VPUVY",  # user's SECOND account -- aliased to #9RQ8YRYQL in build_duel_workbook.ALIAS_TAGS so its games roll up under the main Batan

    "Dess": "#UJRR9RJUL",
    "Droy": "#UG0J8RGU9",
    "Guriko": "#2LJ0ULYCC",
    "Ian77": "#Y9R22RQ2",
    "JorZ": "#22LC8JG02",
    "Mohamed Light": "#G9YV9GR8R",
    "Nicoco": "#G0CYJ00J",
    "Niuzi": "#UJYRYCU9",
    "Nooby": "#UQ9Y0VP0J",
    "Pedro": "#RJ88Y8U08",
    "Rainbow": "#VR90898",
    "Rakan": "#JQ2V2JJ8G",
    "Rin": "#V8CPG02JU",
    "SandBox": "#Y022GRCJQ",
    "Sinistro": "#20Y0GGGUP2",
    "Steeef": "#9LVP2RCLL",
    "Sub": "#U890Q9UQ",
    "Tanjiro": "#208R8PQJP9",
    "Tourist": "#C89L0002L",
    "Turan": "#P8P0Q8CJ",
    "Tyton": "#PPCJJV88Q",
    "Woo": "#U2YVYGGV2",
    "coco": "#2VGG29RJ2",
    "KickAsh": "#GPPYR9JYR",
    "Evolve": "#898Y8PGJ9",
    "Adox": "#20R0VLJL92",
    "RAD": "#8QRCJQ9Y",
    "DK": "#8G9GJQRVQ",
    "LF丨张✨Ink❤️llb": "#U90LPY0QV",  # DQ'd from July 2026 Monthly Finals -- kept for historical data, no longer an active tournament threat
    "Lucas.xit✨之安神": "#2R09LUYPQ",
    # --- Top-64 CRL field additions (2026-07-19), merged in from the July 2026 Monthly
    # Finals Day-1-Swiss standings (statsroyale.com/leagues/crl/july-2026-monthly-finals/
    # day-1-swiss), ranks 1-65 minus rank 17 (LF丨张✨Ink❤️llb above, disqualified). Only the
    # ~31 names below were NOT already covered by an existing tag above (some top-64 players
    # share a tag with someone already tracked under a different in-game display name, e.g.
    # GPPYR9JYR = KickAsh here / shows as "Clown" on the standings page -- tag is what
    # matters, not the label). This merge folds the standalone fetch_top64_day2.py roster
    # into this single script going forward -- no need to run both separately anymore.
    "!¡osama™️!¡": "#CPGRQ8VQV",
    "GençAslan:)": "#2YQJJG0VL",
    "FrancoMedinaSL": "#UJQQCUCQ8",
    "John77": "#2GCL89QGP",
    "INA.BenZerRidel": "#9GJ0Q0LGG",
    "사과도둑": "#8LJ98G0V",
    "TTK:MrAwesomeCR": "#2YQGC20C",  # was scout-only before this merge (scout_2YQGC20C.json); now gets full master-file tracking
    "FelipePT": "#CGV0V99RQ",
    "40k Oker": "#YLVV0JPQ",
    "神│Venpers™☆": "#GU99JUJ",
    "てち": "#JPPC9URJ",
    "HaRu": "#GGV9YLQY",
    "ZQuentino": "#RRLV0GQCV",
    "CAPGUN": "#GR9L9V2LU",
    "Reminor": "#2829V8V0L",
    "Polaris": "#U8RYGC8GU",
    "Sosaa1of1": "#CPLGLPU80",
    "Klaus": "#2J9CR89",
    "⇀スキル丨Hadi": "#222LJ8Y8",
    "SK Dominik": "#J0VU9CGP",
    "OS xAlee": "#VP9GJYQ2",
    "Wyze❤️Ultimo": "#202GUYUP",
    "WL ツ Dam's ✨": "#R2PLLVCY8",
    "ꨄ Max ✨": "#QG2QPY0",
    "Viktor": "#2U2RQGQGC",
    "dark✨安花": "#9JL2YQ2RV",
    "DaniGamer": "#PY9LJCYV",
    "kodigogg": "#22Q8LLU8J",  # previously only known as an anomaly-row opponent name; now fully tracked
    "Nadir": "#2VYLGPPUV",
    "くり": "#2LUY2Q98",
    "fluffypotato99": "#GLJURPRV",
}

# Sanity check: the July 2026 Monthly Finals top-64 field (minus 1 DQ) should all be present.
_TOP_64_TAGS = {
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
_missing = _TOP_64_TAGS - set(PLAYER_TAGS.values())
if _missing:
    print(f"WARNING: {len(_missing)} top-64 tag(s) not found in PLAYER_TAGS: {_missing}")

# API base. Defaults to the official endpoint (works locally from your whitelisted IP).
# In GitHub Actions (no fixed IP), set env CR_API_BASE=https://proxy.royaleapi.dev/v1 and
# whitelist RoyaleAPI's fixed IP (45.79.218.79) on your API token -- the proxy forwards to
# Supercell from that one IP so a runner with a changing IP still works. See docs.royaleapi.com/proxy.html
API_BASE = os.environ.get("CR_API_BASE", "https://api.clashroyale.com/v1")

TOKEN = (os.environ.get("CR_API_TOKEN") or "").strip()  # .strip() guards against a stray newline/space in the GitHub secret breaking the auth header
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


# The battlelog endpoint returns each player's most recent battles only -- historically
# up to 25-30 depending on account/season. Used as a heuristic for "this fetch may have
# maxed out the window", NOT a hard guarantee -- see check_gap_risk() below.
API_PAGE_SIZE_ASSUMED = 25
FETCH_LOG_PATH = "fetch_log.json"


def check_gap_risk(tag: str, name: str, existing_before_merge: list, new_battles: list):
    """Detect (not just guess at) a specific, real risk: friendly battles that happened
    in between two fetches but that neither the old master nor this new fetch has any
    record of. If this fetch's oldest returned battle doesn't reach back far enough to
    connect with the newest battle already in the archive, there's a time gap with zero
    visibility -- and if this fetch also came back with a near-full page (suggesting the
    API had at least this many to give and may have cut off earlier ones), any friendly
    battles the player played during that gap are very likely gone for good, with no way
    to recover them retroactively. Returns a dict describing the risk, or None."""
    if not existing_before_merge or not new_battles:
        return None
    try:
        prev_latest = max(b.get("battleTime", "") for b in existing_before_merge)
        this_oldest = min(b.get("battleTime", "") for b in new_battles)
    except ValueError:
        return None
    if this_oldest <= prev_latest:
        return None  # this fetch's window overlaps/connects with what we already had -- no gap

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


def merge_into_master(master_path: str, new_battles: list, tag: str, name: str) -> tuple[int, int, dict]:
    """Load existing master (if any), merge in new battles deduped by
    battleTime, save back. Returns (added_count, skipped_count, gap_risk_or_None)."""
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
    """Append this run's per-player fetch metadata (timestamp, counts, gap-risk flags) to
    a persistent fetch_log.json so future runs -- and any later audit -- can see exactly
    when each player was fetched and whether a gap-risk was flagged, instead of having to
    infer it after the fact from battle timestamps alone."""
    existing_log = []
    if os.path.exists(FETCH_LOG_PATH):
        try:
            with open(FETCH_LOG_PATH) as f:
                existing_log = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing_log = []
    existing_log.append({
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
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
            "during the uncovered gap below may be permanently lost (the API had more to give "
            "than we could see, and by the time we fetch again those may have aged out "
            "further). Nothing can recover them retroactively -- fetching MORE OFTEN going "
            "forward is the only way to avoid this happening again."
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
        "\nDone. Send the master_*.json files back to Claude (not just "
        "raw_*.json) -- master files are the accumulated, deduped archive "
        "that the Excel workbook gets rebuilt from."
    )


if __name__ == "__main__":
    main()
