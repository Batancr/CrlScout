"""
Fetch + permanently archive the "Extended Roster" -- opponents encountered in Official
CRL games who are NOT part of the original 48-player roster, but who the user wants
tracked on an ongoing basis going forward (added 2026-07-19, per explicit user request:
"I want to expand beyond just 50 players being tracked officially").

Deliberately DIFFERENT from both the main roster fetch and the one-off scout fetch:
  - Like the main roster (fetch_cr_battlelogs.py): accumulates an ARCHIVE over time
    (extended_<tag>.json), deduped by battleTime, merged fresh on every run -- never
    loses history the way a one-off scout snapshot does.
  - UNLIKE the main roster: these players are NOT added to PLAYER_TAGS and their
    extended_<tag>.json files are intentionally a different filename prefix than
    master_<tag>.json. build_duel_workbook.py's Official CRL roster+cluster signal
    only treats master_*.json (and raw_*.json) filenames as "roster" -- keeping these
    players out of that set is REQUIRED, not incidental: if they were counted as
    roster, games between them and the original 48 would stop being classified as
    Official CRL. build_dashboard.py reads extended_*.json separately and classifies
    their battles with the same Practice/Official-CRL rules as the main roster, deduped
    against battles already known from the original 48's own archives.

HOW TO RUN (same API token as the regular fetch):
  1. Make sure CR_API_TOKEN is set: export CR_API_TOKEN="paste_your_token_here"
  2. python3 fetch_extended_roster.py
     (fetches every tag currently in extended_roster_tags.json; safe to re-run any time
     -- only ever adds newly-seen battles, never removes anything)

TO ADD NEW PLAYERS (added 2026-07-19, flexible by design): pass their tag(s) as
command-line arguments and they're permanently added to extended_roster_tags.json before
the fetch runs -- no need to hand-edit the JSON file yourself:
  python3 fetch_extended_roster.py "#20R0VLJL92"                (name auto-looked-up)
  python3 fetch_extended_roster.py "#20R0VLJL92:Adox"           (name given explicitly)
  python3 fetch_extended_roster.py "#TAG1" "#TAG2:Name2" ...    (any number at once)
Once added this way, that player is fetched on every future run automatically, same as
everyone else -- you only need to name them the first time.

Starting list (184 tags): every distinct opponent found in an Official CRL duel across
all fetches so far (through the 8th fetch / round 5). Narrower than "every practice
opponent too" per explicit user decision (2026-07-19) -- Official CRL opponents only,
since that's a much more relevant, "respectable" set than every casual practice partner.
To add someone later, just add a "TAG": "Name" entry below and re-run.
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

FETCH_LOG_PATH = "extended_fetch_log.json"
TAGS_PATH = "extended_roster_tags.json"

if not os.path.exists(TAGS_PATH):
    sys.exit(
        f"Missing {TAGS_PATH} -- this should be the tag/name map generated alongside "
        "this script (a JSON object of {\"TAG\": \"Name\", ...}). Copy it into this "
        "folder before running."
    )
with open(TAGS_PATH) as f:
    EXTENDED_ROSTER_TAGS = json.load(f)


def fetch_battlelog(tag: str):
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}/battlelog"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    return resp.json(), None


def merge_into_extended(extended_path: str, new_battles: list) -> tuple[int, int]:
    existing = []
    if os.path.exists(extended_path):
        with open(extended_path) as f:
            existing = json.load(f)
    seen_times = {b.get("battleTime") for b in existing}
    added = 0
    for b in new_battles:
        if b.get("battleTime") not in seen_times:
            existing.append(b)
            seen_times.add(b.get("battleTime"))
            added += 1
    skipped = len(new_battles) - added
    existing.sort(key=lambda b: b.get("battleTime", ""))
    with open(extended_path, "w") as f:
        json.dump(existing, f, indent=2)
    return added, skipped


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
        "players": fetch_events,
    })
    with open(FETCH_LOG_PATH, "w") as f:
        json.dump(existing_log, f, indent=2)


def fetch_player_info(tag: str):
    tag_clean = tag if tag.startswith("#") else f"#{tag}"
    url = f"{API_BASE}/players/{quote(tag_clean)}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return None
    return resp.json()


def main():
    # ADDED 2026-07-19, per user request ("make it flexible so I can add players"):
    # any command-line args are treated as new tags to add to the permanently-tracked
    # list, on top of everyone already in extended_roster_tags.json. Two forms accepted
    # per arg: "TAG" (name auto-looked-up via the API) or "TAG:Name" (name given
    # explicitly, no lookup needed -- useful if the API lookup fails or you already know
    # the name). New tags are merged into extended_roster_tags.json and saved back, so
    # they're part of the permanent list from now on -- no need to pass them again next
    # time. Example:
    #   python3 fetch_extended_roster.py "#20R0VLJL92" "#ABC123XYZ:SomeName"
    new_tags_added = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if ":" in arg:
                tag_part, name_part = arg.split(":", 1)
            else:
                tag_part, name_part = arg, None
            tag_clean = tag_part if tag_part.startswith("#") else f"#{tag_part}"
            if tag_clean in EXTENDED_ROSTER_TAGS:
                print(f"  (already tracked: {tag_clean} -- {EXTENDED_ROSTER_TAGS[tag_clean]})")
                continue
            if not name_part:
                profile = fetch_player_info(tag_clean)
                name_part = profile.get("name") if profile else tag_clean
            EXTENDED_ROSTER_TAGS[tag_clean] = name_part
            new_tags_added.append((tag_clean, name_part))
        if new_tags_added:
            with open(TAGS_PATH, "w") as f:
                json.dump(EXTENDED_ROSTER_TAGS, f, ensure_ascii=False, indent=2)
            print(f"Added {len(new_tags_added)} new tag(s) to {TAGS_PATH}:")
            for t, n in new_tags_added:
                print(f"  {t} -- {n}")

    tags = list(EXTENDED_ROSTER_TAGS.items())
    print(f"Fetching {len(tags)} extended-roster players...")
    succeeded, failed = [], []
    fetch_events = []

    for i, (tag, name) in enumerate(tags, 1):
        tag_clean = tag if tag.startswith("#") else f"#{tag}"
        safe_name = tag_clean.replace("#", "")
        battles, err = fetch_battlelog(tag_clean)
        if battles is None:
            print(f"  [{i}/{len(tags)}] FAILED {tag_clean} ({name}): {err}")
            failed.append({"tag": tag_clean, "name": name, "error": err})
            fetch_events.append({"tag": tag_clean, "name": name, "status": "failed", "error": err})
            time.sleep(0.1)
            continue

        extended_path = f"extended_{safe_name}.json"
        added, skipped = merge_into_extended(extended_path, battles)
        succeeded.append(tag_clean)
        fetch_events.append({
            "tag": tag_clean, "name": name, "status": "ok",
            "fetched_count": len(battles), "added": added, "skipped_dupe": skipped,
        })
        print(f"  [{i}/{len(tags)}] OK {tag_clean} ({name}): +{added} new, {skipped} already known")
        time.sleep(0.1)  # light throttle -- 184 sequential calls

    append_fetch_log(fetch_events)

    print(f"\nDone. {len(succeeded)}/{len(tags)} succeeded, {len(failed)} failed.")
    if failed:
        print("Failed tags (may have changed tag, be inactive, or a transient API error):")
        for f_ in failed:
            print(f"  {f_['tag']} ({f_['name']}): {f_['error']}")
        print("Re-run the script any time to retry -- it's safe, only adds new battles.")


if __name__ == "__main__":
    main()
