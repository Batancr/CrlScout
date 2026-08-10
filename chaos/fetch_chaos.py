"""
fetch_chaos.py -- Chaos 1v1 Draft tracker. COMPLETELY SEPARATE FROM THE CRL PROJECT.

WHAT THIS IS
------------
A narrow, personal-curiosity tracker for the Chaos 1v1 Draft ladder. It shares the CRL
project's methodology (append-only per-player archives, gap-risk awareness, a scheduled
fetch that outruns the API window) but NONE of its data, and nothing here is read by the
CRL workbook or dashboard.

  * Everything it writes lives under chaos/.
  * It stores ONLY Chaos_1v1_Draft battles. Ladder, friendlies, CRL etc. are discarded.
  * chaos.yml is the only workflow that touches this folder; the CRL workflows never do.

WHY CHAOS DRAFT IS WORTH TRACKING SEPARATELY
--------------------------------------------
Both players draft from one shared 16-card pool, alternating picks, and the loser of each
pick goes to the opponent. That means every battle records not just what each player used
but what they were OFFERED and turned down -- a revealed preference, which is far more
informative than a usage count. The array order encodes it (see decode_draft below).

ROSTER GROWTH AND WHY IT'S CAPPED
---------------------------------
Seeded with a hand-picked set of top ladder players. After each run it can promote
opponents it saw into the tracked roster, so coverage compounds the way the CRL extended
roster did. That has to be bounded or it grows without limit: every added player is another
API call every cycle, forever. MAX_ROSTER caps the total, and candidates are ranked by how
often we've seen them (a player met repeatedly is genuinely active in this mode) with
trophies as the tiebreak.

THIS IS A SEASONAL TRACKER. Set CHAOS_SEASON_END and the workflow stops on its own rather
than quietly running for months after the ladder season it was built for has ended.

USAGE
    CR_API_TOKEN=... python fetch_chaos.py
Env:
    CHAOS_MAX_ROSTER      total tracked players allowed  (default 100)
    CHAOS_SEED_ONLY=1     do not auto-promote opponents; track only the seed roster
    CR_API_BASE           default https://proxy.royaleapi.dev/v1 (IP-whitelisted proxy)
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.parse import quote

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
BATTLE_DIR = os.path.join(HERE, "battles")
ROSTER_PATH = os.path.join(HERE, "roster.json")
FETCH_LOG_PATH = os.path.join(HERE, "fetch_log.json")

API_BASE = os.environ.get("CR_API_BASE", "https://proxy.royaleapi.dev/v1")
TOKEN = os.environ.get("CR_API_TOKEN", "")
GAME_MODE = "Chaos_1v1_Draft"

MAX_ROSTER = int(os.environ.get("CHAOS_MAX_ROSTER", "100"))
SEED_ONLY = os.environ.get("CHAOS_SEED_ONLY", "0").strip().lower() in ("1", "true", "yes")

# A promoted opponent must have been seen in at least this many Chaos Draft battles.
# 2 is deliberate: one meeting is a coincidence, two means they're playing this mode
# regularly enough to be worth a slot.
MIN_SIGHTINGS_TO_PROMOTE = 2

# ...AND must have hit this trophy count in a Chaos Draft battle we saw.
#
# WHY: matchmaking routinely pairs the top-8 seeds against far weaker players, so sightings
# alone would fill the roster with whoever happened to queue at the right moment. The point
# of this tracker is top-ladder behaviour, and one bad-but-frequent opponent costs a slot
# and an API call every cycle for the rest of the season.
#
# CALIBRATION (2026-08-09, over 2,282 players in the baseline): 2900 is about the 99th
# percentile of Chaos Draft trophies -- only 28 players clear it, 25 of them seen 2+ times.
# Deliberately strict. Lower it to ~2800 (106 players) if the roster stays too small to be
# useful. Note trophies drift during a season, so this is judged on the HIGHEST value we've
# observed for that player, not their current one.
#
# Seeds and Batan bypass this entirely -- they're hand-picked.
MIN_TROPHIES_TO_PROMOTE = int(os.environ.get("CHAOS_MIN_TROPHIES", "2900"))

# Seed roster: top Chaos Draft ladder players (supplied 2026-08-09), including Batan's two
# accounts -- he is a top player in this mode and is analysed as one of the tracked group,
# not held out. All seeds bypass the trophy bar below; they're hand-picked, not discovered.
SEED = {
    "#220PRU8YYY": "Eurus",
    "#2LQ2YP98":   "SK xopxsam",
    "#VJ2J0P2R2":  "Sam❤️Rehwald",
    "#V9QYURLVC":  "凛冬Rintou✨卤蛋",
    "#YJP2RPUJJ":  "OcT❤️Lev4ek",
    "#PYYLQQ80R":  "Busfahrer Dirk",
    "#208YUJVPQU": "tiktok@kai_cr12",
    "#VCQRP0VVJ":  "Asaf",
}
BATAN = {"#9RQ8YRYQL": "老板 Ι Batan'宙斯", "#9RG0VPUVY": "batan"}


def canon(tag):
    t = (tag or "").strip().upper()
    return t if t.startswith("#") else f"#{t}"


def safe_name(tag):
    return canon(tag).lstrip("#")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def load_roster():
    """roster.json: {tag: {name, source, added_utc, sightings}}. Seeds are merged in on
    every run so adding a seed by hand takes effect without touching the stored file."""
    roster = load_json(ROSTER_PATH, {})
    for tag, name in {**SEED, **BATAN}.items():
        entry = roster.setdefault(canon(tag), {})
        entry.setdefault("name", name)
        entry.setdefault("source", "seed")
        entry.setdefault("added_utc", datetime.now(timezone.utc).isoformat())
        entry.setdefault("sightings", 0)
    return roster


def fetch_battlelog(tag):
    url = f"{API_BASE}/players/{quote(canon(tag))}/battlelog"
    r = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}",
                                   "Accept": "application/json"}, timeout=20)
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:200]}"
    return r.json(), None


def merge_battles(tag, battles):
    """Append-only per-player archive of Chaos Draft battles, deduped by battleTime.
    Returns (added, skipped, gap_risk_or_None) -- same contract as the CRL fetcher."""
    os.makedirs(BATTLE_DIR, exist_ok=True)
    path = os.path.join(BATTLE_DIR, f"{safe_name(tag)}.json")
    existing = load_json(path, [])
    chaos = [b for b in battles if (b.get("gameMode") or {}).get("name") == GAME_MODE]

    gap = None
    if existing and chaos:
        prev_latest = max(b.get("battleTime", "") for b in existing)
        this_oldest = min(b.get("battleTime", "") for b in chaos)
        # The API returns the last ~25-30 battles of ALL modes, so for a player who mixes
        # modes the chaos-only slice can legitimately start after our newest stored chaos
        # battle without anything being lost. Only flag when the RAW window itself doesn't
        # reach back far enough -- that's the real "games aged out" signal.
        raw_oldest = min(b.get("battleTime", "") for b in battles) if battles else ""
        if raw_oldest > prev_latest and len(battles) >= 22:
            gap = {"tag": canon(tag), "gap_start": prev_latest, "gap_end": raw_oldest,
                   "returned": len(battles)}

    seen = {b.get("battleTime") for b in existing}
    added = 0
    for b in chaos:
        if b.get("battleTime") not in seen:
            existing.append(b)
            seen.add(b.get("battleTime"))
            added += 1
    existing.sort(key=lambda b: b.get("battleTime", ""))
    with open(path, "w") as f:
        json.dump(existing, f, indent=1)
    return added, len(chaos) - added, gap


def opponents_in(battles, me_tag):
    out = []
    for b in battles:
        if (b.get("gameMode") or {}).get("name") != GAME_MODE:
            continue
        for side in ("team", "opponent"):
            for p in (b.get(side) or []):
                if p.get("tag") and canon(p["tag"]) != canon(me_tag):
                    out.append((canon(p["tag"]), p.get("name"), p.get("startingTrophies") or 0))
    return out


def main():
    if not TOKEN:
        print("ERROR: CR_API_TOKEN is not set.")
        return 1

    roster = load_roster()
    tags = list(roster)
    print(f"Chaos Draft fetch -- {len(tags)} tracked players (cap {MAX_ROSTER})")

    events, gaps, candidates = [], [], {}
    ok = fail = total_new = 0
    for tag in tags:
        data, err = fetch_battlelog(tag)
        if err:
            fail += 1
            print(f"  FAIL  {roster[tag].get('name') or tag}: {err}")
            events.append({"tag": tag, "error": err})
            time.sleep(0.3)
            continue
        added, skipped, gap = merge_battles(tag, data)
        ok += 1
        total_new += added
        if gap:
            gaps.append(gap)
        chaos_n = sum(1 for b in data if (b.get("gameMode") or {}).get("name") == GAME_MODE)
        events.append({"tag": tag, "name": roster[tag].get("name"),
                       "returned": len(data), "chaos_in_window": chaos_n,
                       "new": added, "skipped": skipped, "gap_risk": gap})
        print(f"  OK    {(roster[tag].get('name') or tag)[:24]:24s} "
              f"+{added:3d} new ({chaos_n}/{len(data)} in window were chaos)")
        for otag, oname, otr in opponents_in(data, tag):
            if otag in roster:
                roster[otag]["sightings"] = roster[otag].get("sightings", 0) + 1
                continue
            c = candidates.setdefault(otag, {"name": oname, "seen": 0, "trophies": 0})
            c["seen"] += 1
            c["trophies"] = max(c["trophies"], otr)
            if oname:
                c["name"] = oname
        time.sleep(0.3)

    # --- roster expansion, strictly bounded ---
    if SEED_ONLY:
        print("\nCHAOS_SEED_ONLY set -- not promoting any opponents.")
    else:
        room = MAX_ROSTER - len(roster)
        if room <= 0:
            print(f"\nRoster is at the cap ({len(roster)}/{MAX_ROSTER}) -- not adding anyone.")
        else:
            eligible = [(t, c) for t, c in candidates.items()
                        if c["seen"] >= MIN_SIGHTINGS_TO_PROMOTE
                        and c["trophies"] >= MIN_TROPHIES_TO_PROMOTE]
            # Rank by trophies first: with a hard cap, a slot should go to the strongest
            # qualifying player, not merely the most frequently encountered one.
            ranked = sorted(eligible, key=lambda kv: (-kv[1]["trophies"], -kv[1]["seen"]))[:room]
            for t, c in ranked:
                roster[t] = {"name": c["name"], "source": "discovered",
                             "added_utc": datetime.now(timezone.utc).isoformat(),
                             "sightings": c["seen"], "trophies_when_added": c["trophies"]}
            print(f"\nPromoted {len(ranked)} opponent(s); roster now {len(roster)}/{MAX_ROSTER}.")
            for t, c in ranked:
                print(f"   + {(c['name'] or t)[:26]:26s} {t:13s} "
                      f"{c['trophies']} trophies, seen {c['seen']}x")
            low_tr = sum(1 for t, c in candidates.items()
                         if c["seen"] >= MIN_SIGHTINGS_TO_PROMOTE
                         and c["trophies"] < MIN_TROPHIES_TO_PROMOTE)
            thin = sum(1 for t, c in candidates.items() if c["seen"] < MIN_SIGHTINGS_TO_PROMOTE)
            print(f"   skipped: {low_tr} below {MIN_TROPHIES_TO_PROMOTE} trophies, "
                  f"{thin} seen only once, {max(0, len(eligible) - len(ranked))} no room")

    with open(ROSTER_PATH, "w") as f:
        json.dump(roster, f, indent=1, ensure_ascii=False)

    log = load_json(FETCH_LOG_PATH, [])
    log.append({"fetched_at_utc": datetime.now(timezone.utc).isoformat(),
                "roster_size": len(roster), "new_battles": total_new,
                "ok": ok, "failed": fail, "players": events})
    with open(FETCH_LOG_PATH, "w") as f:
        json.dump(log, f, indent=1, ensure_ascii=False)

    stored = 0
    if os.path.isdir(BATTLE_DIR):
        for fn in os.listdir(BATTLE_DIR):
            stored += len(load_json(os.path.join(BATTLE_DIR, fn), []))
    print(f"\n{ok} ok / {fail} failed. +{total_new} new chaos battles this run; "
          f"{stored} stored across {len(roster)} players.")
    if gaps:
        print(f"\nGAP RISK on {len(gaps)} player(s) -- their API window didn't reach back to "
              f"what we already had, so battles in between are unrecoverable:")
        for g in gaps:
            print(f"   {g['tag']}: {g['gap_start']} -> {g['gap_end']} ({g['returned']} returned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
