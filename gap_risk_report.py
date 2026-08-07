"""
gap_risk_report.py -- turn fetch_log.json's gap-risk flags into a visible alert.

WHY THIS EXISTS
---------------
fetch_cr_battlelogs.py has always DETECTED gap risk (a window of time where a player
played battles that neither the archive nor the new fetch can see, because the Clash
Royale API only hands back their last ~25-30 games). But it only ever PRINTED that
warning to stdout. In GitHub Actions that means it scrolls past in a log nobody reads,
so silent, permanent data loss looked exactly like a healthy run.

An audit of fetch_log.json on 2026-08-06 found 123 confirmed blind windows across the
first 51 logged runs -- median ~14h, worst ~127h. This script makes that loud:
it writes a short report meant to be appended to the Discord message, and sets an
exit code the workflow can act on.

USAGE
-----
    python gap_risk_report.py [--window N] [--out gap_report.txt]

    --window N   only consider the most recent N logged runs (default 1 = this run)
    --out PATH   write the report here (default gap_report.txt); nothing is written
                 when there is nothing to report

EXIT CODES
----------
    0  no gap risk in the examined window (or no log yet)
    1  gap risk found -- report written

Exit 1 is deliberately NOT an error the pipeline should die on: a gap is a fact about
the past that failing the build cannot undo. The workflow uses it to decide whether to
shout, not whether to stop.
"""
import argparse
import json
import os
import sys
from datetime import datetime

LOG_PATH = os.path.join(os.environ.get("CRL_HOME", "."), "fetch_log.json")


def parse_battle_time(s: str):
    """Clash Royale battleTime format: 20260806T151233.000Z"""
    try:
        return datetime.strptime(s, "%Y%m%dT%H%M%S.%fZ")
    except (ValueError, TypeError):
        return None


def gap_hours(gr: dict):
    a = parse_battle_time(gr.get("gap_start_battle_time"))
    b = parse_battle_time(gr.get("gap_end_battle_time"))
    if not a or not b:
        return None
    return (b - a).total_seconds() / 3600.0


def collect(entries):
    """Flatten gap-risk dicts out of the given fetch_log entries."""
    out = []
    for e in entries:
        for p in e.get("players", []):
            gr = p.get("gap_risk")
            if gr:
                out.append((e.get("fetched_at_utc", "?"), gr))
    return out


def build_report(found, window, total_runs):
    high = [(t, g) for t, g in found if g.get("high_risk")]
    lines = []
    scope = "this run" if window == 1 else f"the last {window} runs"
    lines.append(
        f"⚠️ **Gap risk: {len(found)} blind window(s)** in {scope} "
        f"({len(high)} high-risk)."
    )
    lines.append(
        "_Battles played inside these windows were never returned by the API and "
        "cannot be recovered. Fetching more often is the only prevention._"
    )

    # Longest first -- the long ones are where real games went missing.
    ranked = sorted(found, key=lambda tg: gap_hours(tg[1]) or 0, reverse=True)
    for _, g in ranked[:8]:
        h = gap_hours(g)
        dur = f"{h:.1f}h" if h is not None else "unknown"
        flag = "HIGH" if g.get("high_risk") else "possible"
        lines.append(
            f"  • [{flag}] {g.get('name', '?')} ({g.get('tag', '?')}): "
            f"{dur} blind, {g.get('gap_start_battle_time', '?')} → "
            f"{g.get('gap_end_battle_time', '?')}"
        )
    if len(ranked) > 8:
        lines.append(f"  …and {len(ranked) - 8} more (see fetch_log.json).")

    lines.append(f"_Examined {window} of {total_runs} logged runs._")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=1,
                    help="how many of the most recent runs to examine (default 1)")
    ap.add_argument("--out", default="gap_report.txt")
    args = ap.parse_args()

    if not os.path.exists(LOG_PATH):
        print("No fetch_log.json yet; nothing to check.")
        return 0

    try:
        with open(LOG_PATH) as f:
            log = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # A corrupt log is itself worth knowing about, but it is not a gap.
        print(f"Could not read {LOG_PATH}: {e}")
        return 0

    if not log:
        print("fetch_log.json is empty; nothing to check.")
        return 0

    window = max(1, min(args.window, len(log)))
    found = collect(log[-window:])

    if not found:
        print(f"No gap risk in the last {window} run(s). Archive is continuous.")
        # Leave no stale report behind from a previous run.
        if os.path.exists(args.out):
            os.remove(args.out)
        return 0

    report = build_report(found, window, len(log))
    with open(args.out, "w") as f:
        f.write(report)
    print(report)
    return 1


if __name__ == "__main__":
    sys.exit(main())
