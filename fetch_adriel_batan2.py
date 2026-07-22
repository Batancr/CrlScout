"""
fetch_adriel_batan2.py -- SCOPED one-off pull for just two players (2026-07-21):
  1. Adriel (#9CPCC890)          -- was skipped in the last scoped practice pull because he
                                    was mid-session; his session is now done, so capture it.
  2. Batan 2nd account (#9RG0VPUVY) -- the user's SECOND account, just merged into the main
                                    Batan via build_duel_workbook.ALIAS_TAGS. Its OWN battle
                                    log has never been fetched (until now it was only ever
                                    seen from opponents' side). This first direct pull
                                    captures its own games; on rebuild they alias to Batan
                                    (#9RQ8YRYQL) and show up in Batan's own player-side
                                    practice/CRL history.

Same non-destructive, accumulating fetch as fetch_cr_battlelogs.py / fetch_practice_pull.py:
hits each player's battlelog, writes raw_<tag>.json (latest snapshot) and merges new battles
into the persistent master_<tag>.json archive (deduped by battleTime, only ever grows).
Writes to the identical master files, so it integrates with the normal rebuild pipeline.

Practice format reminder (2026-07-20): practice duels are full best-of-THREE even after a
2-0 (3rd game still played for deck variety). Needs no change here -- the fetcher captures
every game the API returns; duel-grouping + the completeness gate handle it downstream.

HOW TO RUN (Claude Code, in the CRL folder on the Mac, with CR_API_TOKEN exported):
    python3 fetch_adriel_batan2.py
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

PULL_TAGS = {
    "Adriel": "#9CPCC890",
    "Batan (2nd acct)": "#9RG0VPUVY",  # aliases to main Batan #9RQ8YRYQL in analysis
}

API_BASE = "https://api.clashroyale.com/v1"
API_PAGE_SIZE_ASSUMED = 25
FETCH_LOG_PATH = "fetch_log.json"

TOKEN = os.environ.get("CR_API_TOKEN")
if not TOKEN:
    sys.exit('No API token found. Set it first, e.g.:\n  export CR_API_TOKEN="your_token_here"')

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}


def fetch_battlelog(tag):
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}/battlelog"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    return resp.json(), None


def check_gap_risk(tag, name, existing_before_merge, new_battles):
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
        "pull_type": "scoped_pull_adriel_and_batan2",
        "players": fetch_events,
    })
    with open(FETCH_LOG_PATH, "w") as f:
        json.dump(existing_log, f, indent=2)


def main():
    succeeded, failed, gap_risks, fetch_events = [], [], [], []
    all_types_seen, all_modes_seen = set(), set()

    print(f"Scoped pull -- {len(PULL_TAGS)} players (Adriel + Batan's 2nd account).\n")
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
        note = " (first-ever fetch of this account)" if total == added else ""
        print(f"  Fetched {len(data)} -- {added} new, {skipped} already archived. "
              f"Archive now {total} total{note}.")
        succeeded.append((name, tag, added, total))
        fetch_events.append({
            "tag": tag, "name": name, "battles_returned": len(data),
            "new": added, "skipped": skipped, "total_in_archive": total, "gap_risk": gap_risk,
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
        for gr in gap_risks:
            lbl = "HIGH" if gr["high_risk"] else "possible"
            print(f"  [{lbl}] {gr['name']} ({gr['tag']}): gap between "
                  f"{gr['gap_start_battle_time']} and {gr['gap_end_battle_time']} "
                  f"({gr['this_fetch_battle_count']} battles this pull)")
    else:
        print("\nNo gap-risk detected -- new battles connect cleanly with the archive.")

    print("\nDone. Send both master_*.json files back to Claude for the rebuild. Batan's 2nd "
          "account (#9RG0VPUVY) will alias into the main Batan automatically on rebuild.")


if __name__ == "__main__":
    main()
