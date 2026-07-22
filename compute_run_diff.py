"""
compute_run_diff.py -- "what changed since last run" summary for the CRL tracker.

Runs at the end of each automated pipeline. It reloads the same per-game data the dashboard
uses (build_duel_workbook.load_rows), computes a compact STATE for the 16 tracked Group A
players + the Official-CRL opponent pool, diffs it against the previous run's state
(run_state.json, committed to the repo), writes:

  * run_summary.txt  -- a short human-readable summary (the Discord message body)
  * run_state.json   -- the new state, to diff against next run

The diff highlights, since the previous run:
  * how many new games/duels were added
  * any Group A player who DEBUTED a new win-condition archetype (new to them)
  * notable overall win-rate shifts for Group A players (>= 4 pts, >= 10 games)
  * new opponents appearing in Official CRL

First run (no prior state) just captures a baseline and says so.

Self-contained beyond importing build_duel_workbook, so it inherits DATA_DIR / CRL_HOME
path handling and the exact classification the rest of the pipeline uses.
"""
import os
import json

from build_duel_workbook import load_rows, classify_deck, DATA_DIR, canon_tag

STATE_PATH = os.path.join(DATA_DIR, "run_state.json")
SUMMARY_PATH = os.path.join(DATA_DIR, "run_summary.txt")

# The 16 tracked Group A players (tag -> display name). Tags are canonical (Batan's alt is
# aliased to his main upstream in load_rows, so it never appears separately here).
GROUP_A = {
    "#9RQ8YRYQL": "Batan (you)",
    "#2CLV2RP0": "Mugi",
    "#Y022GRCJQ": "SandBox",
    "#YLVV0JPQ": "40k Oker",
    "#G9YV9GR8R": "Mohamed Light",
    "#9CPCC890": "Adriel",
    "#RJ88Y8U08": "Pedro",
    "#RUQ0JU2P": "Asaf",
    "#GPPYR9JYR": "Clown (KickAsh)",
    "#8LJ92G8UG": "Vitor75",
    "#U890Q9UQ": "Sub",
    "#R09228V": "SK Morten",
    "#2LJ0ULYCC": "Guriko",
    "#U8RYGC8GU": "Polaris",
    "#22LC8JG02": "JorZ",
    "#UJQQCUCQ8": "FrancoMedinaSL",
}

WINRATE_SHIFT_PTS = 4.0      # report a win-rate move of at least this many points
WINRATE_MIN_GAMES = 10       # ...only once a player has at least this many games


def wincon_sig(deck):
    """A deck's win-condition archetype signature (order-independent). Empty if the deck has
    no recognised win condition -- those are skipped for 'new deck' reporting to cut noise."""
    wcs = classify_deck(deck) or []
    return " + ".join(sorted(wcs)) if wcs else ""


def build_state(rows):
    """Compact, JSON-serialisable snapshot of the things we diff on."""
    per_player = {}          # tag -> {"name","games","wins","wincons":set}
    crl_opponents = set()    # opponent tags seen in Official CRL
    for r in rows:
        tag = r["player_tag"]
        if tag in GROUP_A:
            p = per_player.setdefault(tag, {"name": GROUP_A[tag], "games": 0, "wins": 0, "wincons": set()})
            p["games"] += 1
            if (r["crowns_for"] or 0) > (r["crowns_against"] or 0):
                p["wins"] += 1
            if len(r["deck"]) == 8:
                sig = wincon_sig(r["deck"])
                if sig:
                    p["wincons"].add(sig)
        if r.get("match_category") == "Official CRL":
            ot = r.get("opponent_tag")
            if ot:
                crl_opponents.add(canon_tag(ot))
    # serialise (sets -> sorted lists)
    return {
        "total_games": len(rows),
        "players": {
            tag: {
                "name": p["name"], "games": p["games"], "wins": p["wins"],
                "wincons": sorted(p["wincons"]),
            } for tag, p in per_player.items()
        },
        "crl_opponents": sorted(crl_opponents),
    }


def pct(w, g):
    return (100.0 * w / g) if g else 0.0


def diff_summary(old, new):
    lines = []
    new_games = new["total_games"] - old["total_games"]
    if new_games > 0:
        lines.append(f"**+{new_games} new games** since last run (now {new['total_games']} total).")
    else:
        lines.append(f"No new games since last run ({new['total_games']} total).")

    # New win-con archetypes debuted by a Group A player
    debut_lines = []
    for tag, np in new["players"].items():
        op = old["players"].get(tag)
        old_wcs = set(op["wincons"]) if op else set()
        fresh = [w for w in np["wincons"] if w not in old_wcs]
        # only surface debuts when we already had a baseline for this player (avoid first-sighting spam)
        if op and fresh:
            for w in fresh:
                debut_lines.append(f"  • {np['name']} debuted a new deck: **{w}**")
    if debut_lines:
        lines.append("\n\U0001F195 New decks debuted:")
        lines.extend(debut_lines)

    # Win-rate shifts
    shift_lines = []
    for tag, np in new["players"].items():
        op = old["players"].get(tag)
        if not op:
            continue
        if np["games"] < WINRATE_MIN_GAMES:
            continue
        old_wr, new_wr = pct(op["wins"], op["games"]), pct(np["wins"], np["games"])
        delta = new_wr - old_wr
        if abs(delta) >= WINRATE_SHIFT_PTS:
            arrow = "↑" if delta > 0 else "↓"
            shift_lines.append(
                f"  • {np['name']}: {old_wr:.0f}% → {new_wr:.0f}% ({arrow}{abs(delta):.0f} pts, {np['games']}g)"
            )
    if shift_lines:
        lines.append("\n\U0001F4C8 Win-rate shifts:")
        lines.extend(shift_lines)

    # New Official-CRL opponents
    new_opps = [t for t in new["crl_opponents"] if t not in set(old["crl_opponents"])]
    if new_opps:
        shown = ", ".join(new_opps[:15])
        more = f" (+{len(new_opps) - 15} more)" if len(new_opps) > 15 else ""
        lines.append(f"\n\U0001F464 {len(new_opps)} new CRL opponent(s) in the pool: {shown}{more}")

    if len(lines) == 1 and new_games <= 0:
        lines.append("Nothing notable changed.")
    return "\n".join(lines)


def main():
    rows = load_rows()
    new_state = build_state(rows)

    old_state = None
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH) as f:
                old_state = json.load(f)
        except (json.JSONDecodeError, OSError):
            old_state = None

    header = "\U0001F3AF **CRL tracker updated**"
    if old_state is None:
        body = (f"{header}\n\nBaseline captured: {new_state['total_games']} games across "
                f"{len(new_state['players'])} tracked players. Change tracking starts next run.")
    else:
        body = f"{header}\n\n" + diff_summary(old_state, new_state)

    # Discord hard-caps a message at 2000 chars; keep a safety margin.
    if len(body) > 1900:
        body = body[:1880].rstrip() + "\n…(truncated)"

    with open(SUMMARY_PATH, "w") as f:
        f.write(body)
    with open(STATE_PATH, "w") as f:
        json.dump(new_state, f, indent=2, ensure_ascii=False)

    print("Wrote run_summary.txt and run_state.json")
    print("---- summary ----")
    print(body)


if __name__ == "__main__":
    main()
