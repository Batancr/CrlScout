"""
fetch_practice_pull.py -- SCOPED one-off pull for the top-16 Group A players MINUS Adriel.

WHY THIS EXISTS (2026-07-20): after the Day-2 CRL matches, the projected Monthly Finals
opponents move into free practice. The user wants a pull scoped to just these 16 (Batan +
the 15 projected Day-3 opponents), EXCLUDING Adriel -- Adriel is mid-practice-session, so
pulling him now would capture only a partial session AND risk losing the earlier games of
that session to the API's ~30-battle sliding window before he's done. He'll be pulled
separately once his session finishes, to capture it whole.

WHAT IT DOES: exactly the same non-destructive, accumulating fetch as fetch_cr_battlelogs.py
-- it hits each player's battlelog, writes the latest snapshot to raw_<tag>.json, and merges
new battles into the SAME persistent master_<tag>.json archive (deduped by battleTime, only
ever grows). It just runs over a scoped 15-tag roster instead of the full 84. Anything it
adds integrates seamlessly with the existing archive and the normal rebuild pipeline.

WHAT GETS ADDED: the API returns each player's ~25-30 most recent battles. Since these
players just came out of the CRL matches, the NEW (not-already-archived) battles this pull
adds will be their post-CRL PRACTICE games. Any lingering CRL games the API still returns
are already in the archive and dedupe out as "skipped". The Practice-vs-Official-CRL split
is done later at analysis time (build_duel_workbook.classify_match_category), not here --
this script just captures the battles.

NOTE on the new practice format (2026-07-20): practice duels are now full best-of-THREE even
when someone is already 2-0 -- the third game is still played to explore deck variety. That
matters for how the duel-grouping reads the data later (a practice set can now have all 3
games, unlike a tournament 2-0 that stops at 2), but it needs NO change here -- the fetcher
captures every game the API returns regardless; the grouping caps at 3 games and handles it.

HOW TO RUN (Claude Code, in the CRL folder on the Mac, with CR_API_TOKEN already exported):
    python3 fetch_practice_pull.py

Self-contained on purpose (does not import fetch_cr_battlelogs) so it's a robust standalone
artifact -- but it writes to the identical master_<tag>.json files, so it's fully compatible.
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

# Scoped roster: the full top-16 Group A players (Batan + the 15 projected Monthly Finals
# opponents), PLUS Batan's 2nd account = 17 tags. (Adriel was excluded in an earlier run
# because he was mid-session; he's a full member of this pull now.)
PULL_TAGS = {
    "Batan": "#9RQ8YRYQL",           # you
    "Batan (2nd acct)": "#9RG0VPUVY",  # your second account -- aliased to the main Batan in analysis (build_duel_workbook.ALIAS_TAGS); its practice games roll up under Batan
    "Mugi": "#2CLV2RP0",
    "SandBox": "#Y022GRCJQ",
    "40k Oker": "#YLVV0JPQ",
    "Mohamed Light": "#G9YV9GR8R",
    "Adriel": "#9CPCC890",
    "Pedro": "#RJ88Y8U08",
    "Asaf": "#RUQ0JU2P",
    "KickAsh": "#GPPYR9JYR",          # "Clown" on the standings page
    "Vitor75": "#8LJ92G8UG",
    "Sub": "#U890Q9UQ",
    "Morten": "#R09228V",             # "SK Morten"
    "Guriko": "#2LJ0ULYCC",
    "Polaris": "#U8RYGC8GU",
    "JorZ": "#22LC8JG02",
    "FrancoMedinaSL": "#UJQQCUCQ8",
}
# 17 = the full top-16 Group A roster + Batan's 2nd account (#9RG0VPUVY).
assert len(PULL_TAGS) == 17, f"expected 17 tags, got {len(PULL_TAGS)}"

API_BASE = "https://api.clashroyale.com/v1"
API_PAGE_SIZE_ASSUMED = 25
FETCH_LOG_PATH = "fetch_log.json"

TOKEN = os.environ.get("CR_API_TOKEN")
if not TOKEN:
    sys.exit(
        'No API token found. Set it first, e.g.:\n'
        '  export CR_API_TOKEN="your_token_here"'
    )

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}


def fetch_battlelog(tag: str):
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}/battlelog"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    return resp.json(), None


def check_gap_risk(tag, name, existing_before_merge, new_battles):
    """Same gap-risk detection as the main fetcher: flags when this pull's oldest battle
    doesn't connect back to the newest already-archived battle (i.e. a window of games we
    have zero record of), which for a player mid-practice-session means some of their
    friendlies may have permanently aged out of the API window before we fetched."""
    if not existing_before_merge or not new_battles:
        return None
    try:
        prev_latest = max(b.get("battleTime", "") for b in existing_before_merge)
        this_oldest = min(b.get("battleTime", "") for b in new_battles)
    except ValueError:
        return None
    if this_oldest <= prev_latest:
        return None
    near_full_page = len(new_battles) >= API_PAGE_SIZE_ASSUMED - 3
    return {
        "tag": tag, "name": name,
        "gap_start_battle_time": prev_latest, "gap_end_battle_time": this_oldest,
        "this_fetch_battle_count": len(new_battles),
        "near_full_page": near_full_page, "high_risk": near_full_page,
    }


def merge_into_master(master_path, new_battles, tag, name):
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


def append_fetch_log(fetch_events):
    existing_log = []
    if os.path.exists(FETCH_LOG_PATH):
        try:
            with open(FETCH_LOG_PATH) as f:
                existing_log = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing_log = []
    existing_log.append({
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "pull_type": "scoped_practice_pull_top16_minus_adriel",
        "players": fetch_events,
    })
    with open(FETCH_LOG_PATH, "w") as f:
        json.dump(existing_log, f, indent=2)


def main():
    succeeded, failed, gap_risks, fetch_events = [], [], [], []
    all_types_seen, all_modes_seen = set(), set()

    print(f"Scoped practice pull -- {len(PULL_TAGS)} players (top-16 Group A minus Adriel).\n")
    for name, tag in PULL_TAGS.items():
        print(f"Fetching battle log for {name} ({tag}) ...")
        data, err = fetch_battlelog(tag)
        if data is None:
            print(f"  FAILED: {err}")
            failed.append((name, tag, err))
            time.sleep(0.3)
            continue

        safe = tag.replace("#", "")
        with open(f"raw_{safe}.json", "w") as f:
            json.dump(data, f, indent=2)

        added, skipped, gap_risk = merge_into_master(f"master_{safe}.json", data, tag, name)
        with open(f"master_{safe}.json") as f:
            total = len(json.load(f))
        print(f"  Fetched {len(data)} -- {added} new, {skipped} already archived. "
              f"Archive now {total} total.")
        succeeded.append((name, tag, added, total))
        fetch_events.append({
            "tag": tag, "name": name, "battles_returned": len(data),
            "new": added, "skipped": skipped, "total_in_archive": total,
            "gap_risk": gap_risk,
        })
        if gap_risk:
            gap_risks.append(gap_risk)
        for b in data:
            if b.get("type"):
                all_types_seen.add(b["type"])
            m = b.get("gameMode", {}).get("name")
            if m:
                all_modes_seen.add(m)
        time.sleep(0.3)

    append_fetch_log(fetch_events)

    print("\n--- Summary ---")
    print(f"Succeeded: {len(succeeded)}/{len(PULL_TAGS)}")
    for name, tag, added, total in succeeded:
        print(f"  OK    {name} ({tag}): +{added} new, {total} total")
    if failed:
        print(f"\nFailed: {len(failed)}")
        for name, tag, err in failed:
            print(f"  FAIL  {name} ({tag}): {err}")

    print("\n--- Distinct battle 'type' values this run ---")
    for t in sorted(all_types_seen):
        print(f"  - {t}")
    print("\n--- Distinct 'gameMode.name' values this run ---")
    for m in sorted(all_modes_seen):
        print(f"  - {m}")

    if gap_risks:
        print("\n--- GAP-RISK WARNING (possible missed battles) ---")
        print("These players' oldest returned battle doesn't connect back to the archive AND "
              "the page came back near-full -- some practice games in the gap may be lost. "
              "If any of these were mid-session, pull them again sooner next time.")
        for gr in gap_risks:
            lbl = "HIGH" if gr["high_risk"] else "possible"
            print(f"  [{lbl}] {gr['name']} ({gr['tag']}): gap between "
                  f"{gr['gap_start_battle_time']} and {gr['gap_end_battle_time']} "
                  f"({gr['this_fetch_battle_count']} battles this pull)")
    else:
        print("\nNo gap-risk detected -- every player's new battles connect cleanly with the archive.")

    print("\nDone. Send the master_*.json files back to Claude for the rebuild. "
          "Reminder: Adriel was intentionally skipped -- pull him separately once his "
          "practice session ends so his full session is captured cleanly.")


if __name__ == "__main__":
    main()
