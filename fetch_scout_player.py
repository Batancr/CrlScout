"""
One-off "scout" fetch for a SINGLE player who is NOT part of the tracked 48-player roster
(e.g. an upcoming opponent you want to look up ahead of a match).

This is deliberately kept SEPARATE from fetch_cr_battlelogs.py / PLAYER_TAGS / master_<tag>.json:
- Does NOT touch fetch_cr_battlelogs.py or the roster's PLAYER_TAGS dict.
- Does NOT write into fetch_log.json or any master_<tag>.json archive.
- The player will NOT be counted as "roster" for the Official CRL opponent-detection signal
  (build_duel_workbook.py treats anyone without a master_<tag>.json as a non-roster opponent) --
  exactly right for a scouting target, not a teammate.
- Writes a standalone scout_<tag>.json snapshot instead, which the analysis step reads directly
  (not merged into anything).

HOW TO RUN (same API token as the regular fetch):
  1. Make sure CR_API_TOKEN is set: export CR_API_TOKEN="paste_your_token_here"
  2. python3 fetch_scout_player.py QY2L98GQ8
     (tag with or without the leading # both work; pass a different tag to scout someone else)

Safe to re-run any time -- it just overwrites scout_<tag>.json with the latest snapshot (the
API only ever returns each player's most recent ~25-30 battles anyway, so there's no
accumulating-archive benefit for a one-off scouting look the way there is for the tracked
roster).
"""

import os
import sys
import json
from urllib.parse import quote

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run: pip install requests")

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


def fetch_player_info(tag: str):
    """Bonus: also grab the player's basic profile (current name, trophies, clan) --
    doesn't affect duel analysis but useful context when scouting someone unfamiliar."""
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None
    return resp.json()


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 fetch_scout_player.py <tag>  (e.g. QY2L98GQ8 or #QY2L98GQ8)")
    tag = sys.argv[1]
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    safe_name = tag_clean.replace("#", "")

    print(f"Fetching battle log for scout target {tag_clean} ...")
    data, err = fetch_battlelog(tag_clean)
    if data is None:
        sys.exit(f"FAILED: {err}")

    out_path = f"scout_{safe_name}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    profile = fetch_player_info(tag_clean)
    profile_name = profile.get("name") if profile else None
    profile_trophies = profile.get("trophies") if profile else None
    profile_clan = (profile.get("clan") or {}).get("name") if profile else None

    print(f"Wrote {len(data)} battles to {out_path}")
    if profile:
        print(f"Player: {profile_name}  |  Trophies: {profile_trophies}  |  Clan: {profile_clan}")
    else:
        print("(Could not fetch player profile info -- battle log alone was still saved.)")

    types_seen = sorted({b.get("type") for b in data if b.get("type")})
    modes_seen = sorted({b.get("gameMode", {}).get("name") for b in data if b.get("gameMode")})
    print(f"Distinct battle 'type' values seen: {types_seen}")
    print(f"Distinct 'gameMode.name' values seen: {modes_seen}")


if __name__ == "__main__":
    main()
