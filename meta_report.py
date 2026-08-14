"""
meta_report.py -- the standing "what's good since the patch" report.

WHY THIS EXISTS
---------------
This analysis kept getting asked for in chat and kept scrolling away. It's the same four
questions every time: what win conditions are winning, which exact decks are winning, which
win-con pairs open a duel best, and what are the good lists for a specific card. So it's a
script now: run it, get the answer, and the file sits in reports/ instead of buried in a
conversation.

It also encodes the reading discipline that made those answers useful, rather than leaving
it to be re-remembered each time:

  * SAMPLE SIZE IS SHOWN NEXT TO EVERY NUMBER, and rows are tagged solid / thin / noise.
    A 70% win rate over 19 games and a 64% over 146 are not the same claim, and the report
    says so rather than ranking them side by side and hoping.
  * ONLY COMPLETE DUEL SETS feed the pair analysis, and only stats-eligible games feed
    anything (see is_stats_eligible / is_real_practice_session in build_duel_workbook.py).
  * THE FIRST-2-GAME FRAMING is used for pairs, not full 3-deck sets. Grouping on two decks
    instead of three roughly doubles the usable sample -- the 3-deck space is so fragmented
    that 71% of combinations appear exactly once.
  * THE MATCH-CATEGORY MIX IS STATED UP FRONT. As of Aug 2026 the archive is ~100% Practice
    post-patch, which is a real limit on what any of this says about bracket play.

USAGE
    python meta_report.py                       # since CRL_PATCH_DATE (default 2026-08-05)
    python meta_report.py --since 2026-07-01
    python meta_report.py --card "Royal Hogs" --card Miner
Writes reports/meta_report.md and reports/meta_report.html.
"""
import argparse
import collections
import os
from datetime import datetime, timezone

import build_duel_workbook as B

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.environ.get("CRL_HOME", HERE), "reports")

# Thresholds. Deliberately different per section: a single deck accumulates games far
# faster than a duel pair accumulates duels, so one global minimum would either drown the
# deck table in noise or empty the pair table.
MIN_DECK_GAMES = 30
MIN_CARD_DECK_GAMES = 15
MIN_PAIR_DUELS = 15
MIN_WINCON_GAMES = 80

# Sample-size bands, used to tag every row. These are judgement calls, but stating them
# once beats re-litigating "is 19 games enough" on every read.
def band(n, solid, thin):
    return "solid" if n >= solid else ("thin" if n >= thin else "noise")


def load(since):
    dl, _, _ = B.build_dataset()
    games = [r for r in dl
             if r["battle_time"] >= since
             and r.get("stats_eligible", True)
             and len(r["deck"]) == 8]
    return dl, games


def wincon_table(games):
    g = collections.Counter(); w = collections.Counter(); n = 0
    for r in games:
        wcs = B.classify_deck(r["deck"]) or []
        if not wcs:
            continue
        n += 1
        for c in wcs:
            g[c] += 1
            if r["crowns_for"] > r["crowns_against"]:
                w[c] += 1
    rows = [(c, g[c], g[c] / n, w[c] / g[c]) for c in g if g[c] >= MIN_WINCON_GAMES]
    return sorted(rows, key=lambda x: -x[3]), n


def deck_table(games, min_games, contains=None):
    g = collections.Counter(); w = collections.Counter()
    who = collections.defaultdict(collections.Counter)
    for r in games:
        k = ", ".join(sorted(r["deck"]))
        g[k] += 1
        who[k][r["player_name"]] += 1
        if r["crowns_for"] > r["crowns_against"]:
            w[k] += 1
    rows = []
    for k, n in g.items():
        if n < min_games:
            continue
        wcs = B.classify_deck(k.split(", ")) or []
        if contains and contains not in wcs:
            continue
        rows.append((k, n, w[k] / n, wcs, [p for p, _ in who[k].most_common(2)]))
    return sorted(rows, key=lambda x: -x[2])


def pair_table(dl, since):
    """Win-con signature of the FIRST TWO games of each complete duel.

    Two decks instead of three is the whole point: it collapses the combinatorial blow-up
    that makes 3-deck sets unmeasurable, while still capturing the part of a duel that
    decides it -- win the first two and the third never matters."""
    by = collections.defaultdict(list)
    for r in dl:
        by[r["duel_id"]].append(r)
    out = collections.defaultdict(lambda: {"d": 0, "g": 0, "w": 0, "two": 0,
                                           "full": collections.Counter(),
                                           "decks": collections.Counter()})
    for _did, gs in by.items():
        gs.sort(key=lambda r: r["battle_time"])
        if gs[0]["battle_time"] < since or gs[0].get("uncertain_start"):
            continue
        if not gs[0].get("stats_eligible", True):
            continue
        nr = [x for x in gs if not x["is_rematch"]][:3]
        if len(nr) < 2:
            continue
        wc = set()
        for x in nr[:2]:
            wc.update(B.classify_deck(x["deck"]) or [])
        if not wc:
            continue
        d = out[" + ".join(sorted(wc))]
        d["d"] += 1
        won = 0
        for x in nr[:2]:
            d["g"] += 1
            if x["crowns_for"] > x["crowns_against"]:
                d["w"] += 1
                won += 1
            d["decks"][", ".join(sorted(x["deck"]))] += 1
        if won == 2:
            d["two"] += 1
        if len(nr) >= 3:
            f = set()
            for x in nr:
                f.update(B.classify_deck(x["deck"]) or [])
            d["full"][" + ".join(sorted(f))] += 1
    return sorted([(k, v) for k, v in out.items() if v["d"] >= MIN_PAIR_DUELS],
                  key=lambda kv: -(kv[1]["w"] / kv[1]["g"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=os.environ.get("CRL_PATCH_DATE", "2026-08-05"))
    ap.add_argument("--card", action="append", default=None,
                    help="repeatable; adds a per-card deck section")
    args = ap.parse_args()
    since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    cards = args.card or ["Royal Hogs", "Miner", "Goblin Drill", "Rune Giant"]

    dl, games = load(since)
    if not games:
        print(f"No eligible games since {args.since}."); return 0
    latest = max(r["battle_time"] for r in games)
    cats = collections.Counter(r["match_category"] for r in games)
    L = [f"# CRL meta report — since {since:%b %-d, %Y}", "",
         f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · "
         f"latest battle {latest:%Y-%m-%d %H:%M} UTC", "",
         f"**{len(games):,} eligible games** · " +
         " · ".join(f"{k} {v:,}" for k, v in cats.most_common()), ""]
    if cats.get("Official CRL", 0) == 0:
        L += ["> ⚠️ **No Official CRL games in this window** — everything below is practice "
              "data. Practice and bracket metas diverge, especially on blind Game-1 picks.", ""]

    wc, n = wincon_table(games)
    L += ["## Top win conditions", "",
          f"Share is of the {n:,} games with a classified win condition.", "",
          "| Win con | Games | Share | Win rate |", "|---|---|---|---|"]
    for c, g, sh, wr in wc[:12]:
        L.append(f"| {c} | {g:,} | {sh:.1%} | **{wr:.0%}** |")

    dk = deck_table(games, MIN_DECK_GAMES)
    L += ["", f"## Best decks ({MIN_DECK_GAMES}+ games)", "",
          f"{len(dk)} decks qualify. **Confidence** flags sample size — treat *noise* rows "
          "as unproven no matter how high the win rate looks.", "",
          "| Win rate | Games | Confidence | Deck |", "|---|---|---|---|"]
    for k, g, wr, _wcs, _p in dk[:12]:
        L.append(f"| **{wr:.0%}** | {g} | {band(g, 100, 50)} | {k} |")

    pr = pair_table(dl, since)
    L += ["", "## First-2-game win-con pairs", "",
          "Grouped on the win conditions of the duel's **first two** games. Winning those "
          "two ends the set, so this measures the opener rather than the whole trio — and "
          "pairing on two decks instead of three roughly doubles the usable sample.", "",
          f"{len(pr)} pairs have {MIN_PAIR_DUELS}+ duels.", "",
          "| First-2 win | 2-0 rate | Duels | Confidence | Pair |", "|---|---|---|---|---|"]
    for k, v in pr[:10]:
        L.append(f"| **{v['w']/v['g']:.0%}** | {v['two']/v['d']:.0%} | {v['d']} | "
                 f"{band(v['d'], 40, 20)} | {k} |")
    if pr:
        L += ["", "### Most-used decks in the top pairs", ""]
        for k, v in pr[:3]:
            L.append(f"**{k}** — {v['d']} duels, {v['w']/v['g']:.0%} first-2")
            if v["full"]:
                f, fn = v["full"].most_common(1)[0]
                L.append(f"- usual full set ({fn}×): {f}")
            for d, dn in v["decks"].most_common(2):
                L.append(f"- {dn}× `{d}`")
            L.append("")

    for card in cards:
        rows = deck_table(games, MIN_CARD_DECK_GAMES, contains=card)
        L += [f"## {card} decks ({MIN_CARD_DECK_GAMES}+ games)", ""]
        if not rows:
            L += [f"*No {card} deck reaches {MIN_CARD_DECK_GAMES} games in this window.*", ""]
            continue
        tot = sum(r[1] for r in rows)
        avg = sum(r[1] * r[2] for r in rows) / tot
        L += [f"{len(rows)} lists, {tot} games, {avg:.0%} combined.", "",
              "| Win | Games | Confidence | Other win cons | Deck | Played by |",
              "|---|---|---|---|---|---|"]
        for k, g, wr, wcs, ps in rows[:6]:
            others = ", ".join(c for c in wcs if c != card) or "—"
            L.append(f"| **{wr:.0%}** | {g} | {band(g, 60, 25)} | {others} | {k} | "
                     f"{', '.join(ps)} |")
        L.append("")

    L += ["---", "",
          "### How to read this", "",
          "- **solid** = enough games to act on. **thin** = directional. "
          "**noise** = do not act on it, however good the number looks.",
          "- Only *stats-eligible* games count: incomplete practice duel sets and one-off "
          "clan battles are excluded (see `is_stats_eligible` / `is_real_practice_session`).",
          "- Pairs use only **complete** duels with a certain start.",
          "- Win conditions come from `classify_deck()`, which is community knowledge rather "
          "than an API field — a deck with no recognised win condition is skipped.", ""]

    os.makedirs(OUT_DIR, exist_ok=True)
    md = "\n".join(L)
    with open(os.path.join(OUT_DIR, "meta_report.md"), "w", encoding="utf-8") as f:
        f.write(md)
    _write_html(os.path.join(OUT_DIR, "meta_report.html"), md)
    print(f"{len(games):,} games since {args.since} -> reports/meta_report.md + .html")
    return 0


def _write_html(path, md):
    """Minimal markdown -> HTML. No CDN, no library: the report has to open offline."""
    import html as _h
    out, in_tbl = [], False
    for line in md.split("\n"):
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            tag = "th" if not in_tbl else "td"
            if not in_tbl:
                out.append("<table>")
                in_tbl = True
            row = "".join(f"<{tag}>{_fmt(c)}</{tag}>" for c in cells)
            out.append(f"<tr>{row}</tr>")
            continue
        if in_tbl:
            out.append("</table>")
            in_tbl = False
        if line.startswith("### "): out.append(f"<h3>{_fmt(line[4:])}</h3>")
        elif line.startswith("## "): out.append(f"<h2>{_fmt(line[3:])}</h2>")
        elif line.startswith("# "):  out.append(f"<h1>{_fmt(line[2:])}</h1>")
        elif line.startswith("> "):  out.append(f'<div class="warn">{_fmt(line[2:])}</div>')
        elif line.startswith("- "):  out.append(f"<li>{_fmt(line[2:])}</li>")
        elif line.strip() == "---":  out.append("<hr>")
        elif line.strip():           out.append(f"<p>{_fmt(line)}</p>")
    if in_tbl:
        out.append("</table>")
    css = """<style>
:root{--bg:#12131a;--card:#1b1d27;--line:#2b2e3d;--tx:#e7e9f0;--dim:#9aa0b4;--acc:#60a5fa}
body{margin:0;padding:24px;max-width:1100px;background:var(--bg);color:var(--tx);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:26px 0 8px;color:var(--acc)}
h3{font-size:15px;margin:18px 0 6px;color:var(--dim)}
table{width:100%;border-collapse:collapse;margin:8px 0 4px;font-size:14px}
td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--dim);font-size:12px;text-transform:uppercase;font-weight:600}
code{background:var(--card);padding:1px 5px;border-radius:4px;font-size:13px}
.warn{background:var(--card);border-left:3px solid #fab219;padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0}
p{margin:6px 0}li{margin:3px 0}hr{border:none;border-top:1px solid var(--line);margin:22px 0}
@media(prefers-color-scheme:light){:root{--bg:#f6f7f9;--card:#fff;--line:#e3e5ea;
--tx:#14161c;--dim:#666e80;--acc:#1d4ed8}}
</style>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset="utf-8"><title>CRL meta report</title>'
                + css + "\n".join(out))


def _fmt(t):
    import re, html as _h
    t = _h.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t


if __name__ == "__main__":
    raise SystemExit(main())
