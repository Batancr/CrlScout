# CRL Opponent Scout — project brief

Context file for Claude sessions in this folder. Reconstructed 2026-08-06 from the repo,
git history, and the GitHub Actions workflow. Sections marked **(unverified)** are inferred,
not confirmed — correct them if wrong.

## What this is

A Clash Royale League (CRL) scouting dashboard for Alexander (in-game/GitHub handle: `Batancr`).
Pulls battle logs from the Clash Royale API, aggregates them into a spreadsheet, and renders a
single self-contained HTML dashboard used to scout opponents before matches.

- **Repo:** https://github.com/Batancr/CrlScout (remote `origin`, branch `main`)
- **Local folder:** this directory
- **Live site:** https://crlscout.netlify.app (confirmed by Alexander 2026-08-06; the site ID
  itself lives only in the `NETLIFY_SITE_ID` GitHub secret)

## The dashboard

`crl_opponent_scout.html` (~47 MB, generated, **gitignored** — never committed).

Search a tracked player by name or tag (e.g. `#80ULUJLYY`) and see their most-played decks,
best win-rate decks, top win conditions, and practice history. Two pages: **Scout Tools** and
**Best Picks & Stats**. Filters: All / Practice Only / Official CRL Only, plus a toggle that
weights official CRL games more heavily (activates at 5+ official games for a deck/win-con).
Also has a Group A / Day 2 group-stage panel with snake-seeded brackets, per-player history
modals, and champion/evolution card legends.

Data is a **static snapshot baked into the HTML** — it does not fetch live on load. Refreshing
it means re-running the build pipeline.

Other generated artifacts: `crl_mugi_dossier.html`, `event_day_prep.html`.

## Pipeline (order matters)

```
fetch_cr_battlelogs.py          # CR API -> master_<tag>.json (append-only archive)
                                #   [fetch.yml — runs on its own 30-min cadence]
gap_risk_report.py --window 1   #   -> gap_report.txt; exit 1 = blind window found
build_duel_workbook.py          # -> CRL_Duel_Decks.xlsx
recalc.py CRL_Duel_Decks.xlsx 300
add_ronin_analysis.py
add_group_a_analysis.py
add_batan_matchup_analysis.py
add_group_a_sequencing_analysis.py
add_group_a_matchup_prep.py
recalc.py CRL_Duel_Decks.xlsx 300   # second pass, intentional
build_dashboard.py              # -> crl_opponent_scout.html
compute_run_diff.py             # -> run_summary.txt (diff vs run_state.json)
```

`recalc.py` needs LibreOffice (`libreoffice-calc`) to evaluate xlsx formulas.
Deps: `requests`, `openpyxl` (`requirements.txt`). Python 3.11 in CI.

## Data files

- `master_<tag>.json` — **source of truth.** Append-only per-player battle archive. The CR API
  only returns each player's last ~25–30 battles, so this exists to prevent silent data loss as
  the API window slides. Deduped by `battleTime`.
- `raw_<tag>.json` — latest fetch only, overwritten each run, gitignored (debug).
- `fetch_log.json` — one entry per run; powers the gap-risk warning that flags when a player's
  oldest returned battle doesn't connect to what's archived (= games permanently lost).
- `run_state.json` — persistent snapshot (`total_games`, `players`, `crl_opponents`) that
  `compute_run_diff.py` compares against to build the Discord summary. **Committed, not ignored.**
- `CRL_Duel_Decks.xlsx` — the aggregated workbook the dashboard is built from.
- `card_icons/` — downloaded card images (`download_card_icons.py`).

## Automation — two workflows (split 2026-08-06)

Fetching and rebuilding used to live in one workflow on a 3-hour cron. They were split
because 3 hours is far slower than players burn through the API's ~30-battle window.

### `.github/workflows/fetch.yml` — every 30 min (`*/30 * * * *`)

Cheap: ~85 HTTP calls, ~2 min. Fetches via the **RoyaleAPI proxy**
(`https://proxy.royaleapi.dev/v1`) — the CR API token is IP-whitelisted to the proxy IP
`45.79.218.79`, which is why GitHub Actions can call it. Retries the fetch 3× on transient
API errors, runs `gap_risk_report.py`, alerts Discord if any blind window appeared, then
commits. `timeout-minutes: 20`.

### `.github/workflows/update.yml` — every 3 h (`0 */3 * * *`) + `workflow_dispatch`

Expensive: LibreOffice recalcs, dashboard build. **Does not fetch.** Checks archive freshness
first and shouts on Discord if the last fetch is >3 h old (i.e. fetch.yml has silently died).
Rebuilds, deploys to Netlify **only on manual `workflow_dispatch`** (free plan ≈20 build
credits/month — refresh the live site on demand before a match via "Run workflow"), posts the
change summary + a 6-run gap-risk rollup to Discord, commits, uploads the dashboard as a
14-day artifact. `timeout-minutes: 60`.

### `.github/workflows/deploy.yml` — manual only, ~2 min

Fast republish. Runs `build_dashboard.py` alone: no LibreOffice, no workbook recalc, no
`add_*_analysis.py` passes. **Commits nothing** (`permissions: contents: read`).

- Fresh: every game fetched since the last full rebuild — the dashboard reads
  `master_*.json` directly.
- Stale: Deck Stats and Win-Con Sets, which are COUNTIFS output read from the committed
  `CRL_Duel_Decks.xlsx` and only change when `update.yml` recalcs it.

Use before a match to pull in recent practice; use `update.yml` when the workbook-derived
tables need to be current.

### ⚠️ Ownership rule — do not break this

- `fetch.yml` writes **only** `master_*.json` and `fetch_log.json`
- `update.yml` writes **only** derived artifacts (`CRL_Duel_Decks.xlsx`, `run_state.json`, …)
  and enforces it with `git add -A -- . ':!master_*.json' ':!fetch_log.json'`

Disjoint file sets is what lets both push to `main` without `update.yml`'s `-X ours` merge
strategy clobbering battles that `fetch.yml` archived during the multi-minute rebuild.

**Repo secrets required** (Settings → Secrets and variables → Actions):
`CR_API_TOKEN` (used by fetch.yml), `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID`,
`DISCORD_WEBHOOK_URL`. The last three are optional — their steps skip if unset.

## Roster

`PLAYER_TAGS` in `fetch_cr_battlelogs.py` holds both regular practice partners and the full
top-64 CRL field (July 2026 Monthly Finals, Day-1 Swiss standings; rank 17 excluded as DQ'd).
`fetch_top64_day2.py` is superseded — its roster is folded in. To find a missing top-64 tag:
look at the `opponent` side of an already-tracked player's Official-CRL battles, since bracket
play is top-64-vs-top-64 only.

## Duel completeness rule (added 2026-08-06)

Alexander's rule: **Practice duels are supposed to be full 3-game sets.** A short Practice
set means games were lost to the API window, so those games must not feed aggregate stats.
**Official CRL is the opposite** — a 2-0 sweep is genuinely complete and a 1-1 is legitimately
pending, so CRL is never gated by length (`compute_crl_duel_status` remains the authority).

Implemented as `is_stats_eligible()` in `build_duel_workbook.py`, which stamps every
`duel_log` / `duel_summary` row with `stats_eligible`. Gated call sites:
`compute_player_lookup` (workbook), and in `build_dashboard.py`: `compute_best_decks`,
`build_player_briefs`, Deck Explorer `player_decks`.

- **Cutoff: 2026-08-01.** Earlier data was fetched only every 3 h, so most short Practice
  sets back then are cadence artifacts, not signal — gating the full history would drop
  ~51% of all games. Post-cutoff (with the 30-min cadence) a short set is real.
- **Kill switch for CRL event days**, no code edit needed:
  `CRL_ENFORCE_COMPLETENESS=0 python build_duel_workbook.py`
  Move the cutoff with `CRL_COMPLETENESS_FROM=20260901T000000.000Z`.
- **`uncertain_start` is deliberately NOT part of this gate.** It flags the first duel per
  pair (no visibility before the fetch window); it still only gates the sequence-dependent
  analyses (Win-Con Sets, Deck Predictor, Best Picks), as before.
- **The Excel sheets are gated too** (added 2026-08-07). Duel Log carries a **"Stats Eligible"**
  column (col 36 / `AJ`) mirroring the flag, and Deck Stats / Deck Matchups / Card Frequency
  append `COUNTIFS(... ,'Duel Log'!AJ:AJ,"Yes")` to every count. The Player Lookup sheet needed
  no change — it renders `compute_player_lookup`, which is already gated in Python. Workbook
  and dashboard now agree on every deck's game count.
  **If you add a new COUNTIF over Duel Log, add the `ELIGIBLE` criterion pair to it.**

`is_set_complete()` in `build_dashboard.py` fixed a related bug: Best Picks required 3 games
and so discarded every legitimate Official-CRL 2-0 sweep (22 sets on the 07-27 archive).

## Practice-session rule (added 2026-08-07)

Alexander's rule: **a clan/friendly battle is not practice just because it was friendly.**
"Players don't just play 1 set and call it a day." A *session* (consecutive duels vs the same
opponent, `SESSION_GAP_HOURS = 1`) must contain **more than 2 complete duel sets** — i.e.
`MIN_COMPLETE_SETS_PER_PRACTICE_SESSION = 3` — for its games to count as practice at all.

- **Two ways to qualify** (`is_real_practice_session()` in `build_duel_workbook.py`, folded
  into `stats_eligible`): `MIN_COMPLETE_SETS_PER_PRACTICE_SESSION = 3` complete sets **OR**
  `MIN_GAMES_PER_PRACTICE_SESSION = 6` raw games. Env: `CRL_MIN_SETS_PER_SESSION` (0 disables
  the whole rule), `CRL_MIN_GAMES_PER_SESSION`.
- **Why volume is a second path** — a manual QC pass caught the set-count rule dropping
  obviously-real practice. Worst case: Vitor75 vs Clown, **20 games over 134 minutes**, which
  failed because the duel grouper split it into eleven 1–2 game fragments (sizes
  2,2,2,1,2,1,2,3,1,3,1) so only 2 counted as "complete". The set count was measuring the
  health of the duel *grouping*, not whether it was practice. Adding the games test rescued
  all 36 such sessions and changed nothing about the 402 genuine one-offs.
- Net effect: drops 866 games (8.7% of all), 100% Practice.
- **Official CRL is never gated by this.** A one-off bracket meeting is normal, and
  Alexander has personally verified those games.
- **Per session, not per pair** — deliberately. A pair with 14 sets spread over months isn't
  the same as two players actually sitting down to practice.
- The archive backs the threshold up: 444 practice "sessions" hold ZERO complete sets and
  average 1.4 games (one-off clan battles), while real practice clusters at 3–7 sets/session.
  Drops ~13% of all games, all Practice.
- Practice **history** is gated too (`_history_rows`), which was the visible symptom —
  one-off opponents were showing up in Batan's practice log.

## Duel history for all players (added 2026-08-07)

The history modal used to be Group-A-only. It's now built for every tag on the player side of
a logged game (84 players), and a **▤ Duel History** button appears on any searched player's
profile. Export keys are still `group_a_history` / `group_a_practice_history` so nothing
downstream changed; empty arrays are skipped to keep the payload small. The Group-A-only
sections inside the modal (recommendations, matchup prep, sequencing) already guard against
missing tags and render nothing for non-roster players.

## Date filter + icon delivery (added 2026-08-07)

### Date filter

The CR meta resets each monthly balance patch, so all-time deck win rates blend dead metas.
The dashboard now has a **Time period** control (All time / This month / Last 30-60-90 days /
custom date) in the match-category bar.

- `game_log` is exported from `build_dashboard.py` as interned lookup tables plus one 5-int
  row per game: `[playerIdx, deckIdx, isOfficial, isWin, dayOffset]` from a 2020-01-01 epoch.
  Win conditions are resolved **per deck in Python** so `classify_deck()` stays the only
  source of truth. ~10k games ≈ a few hundred KB.
- **Invariant to preserve:** with no cutoff the client uses the Python-built aggregates
  untouched and never runs the JS path (`dateFilterActive()` gates it). So the default view
  can't drift from the workbook, and a JS bug can only affect a filtered view.
- JS mirrors of `compute_player_lookup`, `compute_best_decks`, `build_player_briefs` and the
  Deck Explorer feed live in the `DATE FILTER` block. **`OFFICIAL_GAME_WEIGHT`,
  `MIN_OFFICIAL_GAMES_FOR_WEIGHT` and `MIN_GAMES_FOR_WINRATE_RANKING` are duplicated there
  and must be kept in sync with `build_duel_workbook.py`.**
- `glPct()` implements round-half-to-**even** to match Python's `f"{x:.0%}"`. Plain
  `Math.round` rounds half-up and made a 5/8 win rate show 62% all-time but 63% filtered.
- **Not date-filtered:** win-con sets, duel sets, Deck Predictor (they need duel grouping,
  deliberately not ported to JS), and the Deck Stats / Win-Con Sets tables (Excel COUNTIFS).
  The status line under the control says so.
- Verified by extracting the JS and diffing against Python over 2,500 real games ×
  87 players × both weighting modes — exact match on every field.

### Icon delivery

`CRL_INLINE_ICONS` (default `0`) switches `embed_local_icons()` between:

- **linked** (default): CSS points at `card_icons/<file>.png`; page drops ~47 MB → ~6 MB.
  **`card_icons/` must be served next to the HTML** — `update.yml` copies it into `_site/`.
- **inline** (`CRL_INLINE_ICONS=1`): base64, one portable offline file. The workflow builds
  this second for the downloadable artifact.

## `chaos/` — Chaos Draft tracker (added 2026-08-09) — NOT part of the CRL project

A separate, seasonal, personal-curiosity tracker that shares this repo but no data. It is
deliberately isolated: **nothing in the CRL pipeline reads `chaos/`, and `chaos.yml` writes
nothing outside it.** That's the third leg of the ownership rule.

**Why the mode is interesting:** both players draft from one shared 16-card pool. Each makes
4 choices between 2 cards; the card taken goes to their deck, the loser goes to the opponent.
So every battle records what was *rejected*, not just what was played — a revealed preference,
which beats a usage count.

**The decode** (confirmed by Alexander against his in-game log, and self-consistent on the
4 battles captured from both players' logs): `my[i]` pairs with `opp[9-i]` for all i. Positions
1–4 are that player's picks in draft order; 5–8 are what the opponent passed on, in reverse.

- `chaos/fetch_chaos.py` — chaos-only append-only archive. Roster auto-expands from opponents
  seen, but a candidate needs **2+ sightings AND `CHAOS_MIN_TROPHIES` (2900) trophies**, capped
  at `CHAOS_MAX_ROSTER` (100). The trophy bar exists because matchmaking pairs the top seeds
  against far weaker players — sightings alone would fill the roster with noise. 2900 is ~the
  99th percentile: of 334 opponents in the baseline only 3 clear it, 43 repeat opponents are
  rejected on trophies. Lower to ~2800 if the roster stays too thin.
- `chaos/analyze_chaos.py` — pick rate, win rate, picked-vs-passed, and a ridge logistic
  card-strength model (a card's effect with the other 15 held fixed; ~64% in-sample accuracy).
- `chaos/baseline_backfill.json` — **frozen** slimmed snapshot of the 2,667 chaos battles
  already in the CRL archive. Never re-fetched; gives the tracker history from day one.
- `chaos.yml` — 30-min cron, **auto-stops after `SEASON_END`** (currently 2026-08-18). Bump
  the date to extend; it exists so a seasonal job doesn't outlive its season.

**Findings so far** (2,667 battles, 20,232 decisions): offered pairs are statistically
indistinguishable from random (elixir, rarity and spell-vs-spell rates all match a shuffled
null), so there's no draft-order edge — only per-pair card value. Pick rate and modelled
strength correlate r=0.73; the big disagreements are Ronin (73% picked, 58th strongest) and
Suspicious Bush (62% picked, **strongest card in the mode**).

## Known history / gotchas

- Card icons render via CSS classes, not inline images — an earlier inline approach made the
  history modal slow/broken (commit `a6dd171`).
- The CRL/Practice toggle had a lag bug, fixed in `d091547`.
- Last auto-commit in the local clone: `676e4b0`, 2026-07-27. The local clone is behind the
  remote — `git pull` before doing anything, the workflow has been committing since.
- `*.tar.gz` staging archives in the folder are leftovers and safe to delete.
- **2026-08-06 workflow failure — not our bug.** "The job was not acquired by Runner of type
  hosted even after multiple attempts" + "Internal server error. Correlation ID: ..." is a
  GitHub-side runner-assignment failure. It coincided with a GitHub-wide Actions incident
  (2026-08-06 15:22 UTC → mitigated 2026-08-07 00:06 UTC). Fix is to re-run the workflow.
  If this class of error recurs, always check https://www.githubstatus.com before debugging
  the pipeline.
- `concurrency: group: crl-update, cancel-in-progress: false` means a stuck run **blocks**
  every later run. If runs look "missing", check for one hung at the head of the queue and
  cancel it manually. Both workflows now carry `timeout-minutes`, so this should self-heal.
- **Gap risk was chronic and invisible until 2026-08-06.** An audit of the first 51 logged
  runs found **123 confirmed blind windows** — median ~14 h, worst 126.7 h (Rainbow), across
  ~40 players. `check_gap_risk()` had been detecting them all along but only `print()`ed to
  the Actions log, so silent permanent data loss looked identical to a healthy run. Fixed by
  the 30-min fetch cadence + `gap_risk_report.py` → Discord. **Games lost before that date
  are unrecoverable** — the API cannot return them. Treat pre-08/06 win-rates as slightly
  undercounted, especially for high-volume players (fluffypotato99, INA.BenZerRidel, Hadi,
  くり, LucasXGamer all hit the window ceiling 5+ times).
- **2026-08-06 artifact quota failure.** `Failed to CreateArtifact: Artifact storage quota
  has been hit.` The old step uploaded the ~47 MB dashboard on *every* run with 14-day
  retention — ~5.3 GB live against a 500 MB free quota. Because it was the last step, it
  marked otherwise-successful runs as FAILED (data was already fetched, rebuilt, committed,
  and Discord had already fired — which is why notifications kept arriving on "failed" runs).
  Fixed by purging old artifacts each run, uploading only on `workflow_dispatch`, gzipping,
  `retention-days: 2`, `overwrite: true`, and `continue-on-error: true`. Quota usage is
  recalculated server-side every 6–12 h, so freeing space is not instant.
- Actions bumped to `checkout@v5` / `setup-python@v6` / `upload-artifact@v6` for the Node 20
  deprecation (Node 20 is removed from runners 2026-09-16).
- GitHub does not guarantee cron punctuality — scheduled runs can be delayed or dropped under
  platform load, more so on public repos. The 30-min cadence is a budget, not a promise.

## How to make edits

Dashboard UI/logic lives in `build_dashboard.py` (~214 KB — edit the generator, never the
generated HTML). Workbook/aggregation logic lives in `build_duel_workbook.py` (~108 KB).
After editing, re-run the pipeline locally or push and trigger the workflow manually.
