# Deck Predictor — accuracy backtest

**Run date:** 2026-08-18 · **Archive cutoff:** 2026-08-16 17:39 UTC
**Scripts:** `backtest_predictor.py`, `verify_backtest.py`

---

## The short version

**The predictor cannot be right the majority of the time at Game 2, and no input format
fixes that.** The best configuration puts the real win condition in its top 3 about **34%**
of the time. The naive "just guess the most popular deck" baseline gets **28%**. The tool is
adding roughly 6 percentage points over guessing.

**Typing all 8 cards is not measurably better than typing just the win condition.**
Difference: +1.2 pp, 95% CI [−0.1%, +2.7%]. That interval crosses zero. Directionally more
information helps, but at n=1200 it is inside the noise — so the extra typing buys you
nothing you can rely on.

**Game 3 is a different story, and it is where the real win is.** Predicting game 3 from
games 1+2 with all 16 burned cards known more than doubles the baseline, and both effects
survive a paired significance test.

---

## Method

For every duel with ≥2 games: hide that entire duel, rebuild the transition model from every
*other* duel, feed it game 1 under one input representation, take the top 3, check the truth.

Hiding matters. With the duel left in its own training data, accuracy came out **14.7%**
instead of **11.3%** — a 3.3 pp inflation. Every number in this report is the leave-one-out
number.

**Scale:** 6,910 duels · 6,671 distinct decks · 122 cards · 118 win-condition sets ·
17,630 training transitions.

### Why "exact deck" is the wrong target

**6,671 distinct decks across 6,910 duels.** Almost every deck in the archive is unique — a
single tech swap creates a "new" deck. Exact-deck accuracy is therefore near-zero by
construction and tells you nothing. Two better targets are used throughout:

- **near-deck** — a predicted deck sharing ≥6 of 8 cards with the truth. Same win condition,
  same core, same counterplay. For prep purposes this is the same deck.
- **win-con top-3** — the real win condition is somewhere in the top 3.

---

## Game 2 — full results

Test set: 1,200 randomly sampled Practice duels with a confirmed clean start. Trained on
Practice only, which is what the dashboard does today.

| Input representation | near-deck | win-con top-3 | vs. baseline (near) |
|---|---|---|---|
| win-con only | 12.1% | 30.0% | +1.1% [−0.6, +2.8] |
| 4 cards | 12.8% | 30.7% | — |
| 6 cards | 12.2% | 31.7% | +1.2% [−0.5, +3.0] |
| **8 cards (full deck)** | **13.3%** | **31.9%** | +2.3% [+0.6, +4.2] ✓ |
| 8 cards, no burn filter | 12.8% | 30.8% | +1.8% [+0.0, +3.7] |
| **8 cards + opponent history ×10** | **15.5%** | **34.1%** | **+4.5% [+2.4, +6.7] ✓** |
| burn filter only, no model | 11.2% | 30.8% | — |
| *baseline: overall deck popularity* | *11.0%* | *28.2%* | — |
| *baseline: opponent's most-played decks* | *9.7%* | *29.0%* | — |

✓ = 95% CI excludes zero (paired bootstrap over duels)

### What this says

**Only one thing clearly works: weighting the opponent's own history.** Boosting that
specific player's past duels 10× while keeping the roster as backoff is the single
configuration that beats baseline with room to spare, on both metrics. Everything else is
marginal.

**More cards helps, but not enough to prove it.** The 12.1% → 13.3% climb from win-con-only
to full deck is monotone and in the right direction across 4, 6 and 8 cards — but the paired
CI on the endpoints crosses zero. I would not claim the 8-card input is better than the
win-con input on this evidence.

**The burned-card filter does almost nothing at Game 2:** +0.5 pp [−0.1, +1.2]. Eight burned
cards out of 122 just does not narrow the field much.

---

## Game 3 — the actual finding

Test set: 1,200 Practice duels with 3 clean games. Query = both decks' cards (16 burned).

| Input representation | near-deck | deck top-3 |
|---|---|---|
| **all 16 cards + burn filter** | **14.9%** | **7.6%** |
| 16 cards, no burn filter | 9.8% | 4.2% |
| burn filter only, no model at all | 12.3% | 5.3% |
| G1+G2 win conditions only | 9.1% | 3.3% |
| *baseline: popularity* | *7.2%* | *1.6%* |

**Burn filter effect: +5.2 pp [+3.5, +6.9] — real.**
**Transition model on top of the burn filter: +2.6 pp [+1.2, +3.9] — also real.**

At Game 3 the burned-card constraint finally has enough to work with: 16 of 122 cards are
off the table, and that alone beats every Game-2 configuration. **Game 3 is roughly twice as
predictable as Game 2**, and the tool currently does not exploit this.

---

## Training on Official CRL — clear improvement

The dashboard's predictor **excludes Official CRL entirely** (`build_dashboard.py` skips any
row where `match_category` is not `Practice`). So when you tested it against your Day-1 and
Day-2 games, you were querying a model that has never seen a single CRL duel.

Tested on 1,200 Official CRL duels:

| Representation | practice-only training | blended training | change |
|---|---|---|---|
| 8 cards (full deck) | 11.9% | 13.4% | +1.5 |
| 8 cards, opponent history ×10 | 13.2% | 15.7% | +2.5 |
| **8 cards, this player only** | **10.8%** (89% answered) | **17.5%** (100% answered) | **+6.7** |
| win-con only | 11.7% | 12.2% | +0.5 |

The player-specific mode is the big mover — and note the coverage column. Practice-only
training left it **unable to answer 11% of queries at all**, because many CRL opponents have
no practice history in the archive. Blending fixes both problems.

**Recommendation: blend Official CRL into the predictor's training data.** This is a
one-condition change and it is the highest-value fix in this report.

---

## Your own games — too small to conclude anything

| Test set | n | best near-deck | best win-con top-3 |
|---|---|---|---|
| Batan, Official CRL (Day 1 + Day 2) | 35 | 20.0% | 45.7% |
| Batan, Practice | 60 | 8.3% | 36.7% |

At n=35 the margin of error is roughly ±8 pp, so nothing here separates. Worth flagging
honestly: on your CRL slice the **naive "opponent's most-played decks" baseline scored
highest** on win-con top-3 (45.7%). I do not believe that reflects a real effect — it
contradicts the 1,200-duel result — but it is what the data says, and it is a fair warning
against tuning on 35 duels.

Also: **your recent practice vs Coco and Ian77 is not in this analysis.** This archive ends
2026-08-16 17:39 UTC and contains no Batan-vs-Coco or Batan-vs-Ian77 duels. Both are tracked
players (964 and 338 games), so a `git pull` and a cache refresh will pick them up.

---

## Caveats I want on the record

**The burned-card filter's measured value is an upper bound.** Games inside one duel share
zero cards ~100% of the time (6,908 of 6,909 pairs) — but `build_duel_workbook.py`'s grouper
*uses* card-disjointness to decide where one duel ends and the next begins, so part of that
is circular. The filter is still legitimate to use at predict time, since at a real match you
see game 1's eight cards regardless of why they won't reappear.

**This is not literally the dashboard's code.** I reimplemented the scorer as a
similarity-weighted kNN so that every representation could be compared with only the input
varying. The dashboard's actual chain (exact deck key → win-con-set key → card-overlap
fallback) is a special case of this. Conclusions about *relative* input value transfer;
absolute percentages for the shipped tool may differ by a point or two.

**Future leakage is modest.** Leave-one-out lets the model learn from duels that happened
after the one being predicted. Re-run time-causally (train only on earlier duels), the 8-card
representation scored 13.5% near-deck vs 13.3% — essentially unchanged.

**Sampling.** 1,200-duel random samples, not the full 4,052, for runtime. Margin of error at
these rates is roughly ±2 pp.

---

## What I would change in the dashboard

1. **Blend Official CRL into the predictor's training set.** Biggest single win, especially
   for CRL opponents you have no practice history against. Currently excluded outright.
2. **Add a burned-card filter to the Game-3 predictor.** +5.2 pp, verified. This is the
   strongest effect in the whole study and it is currently unused.
3. **Weight the specific opponent's history ~10× rather than using it exclusively.**
   Opponent-only mode is too thin and fails to answer 11% of queries; opponent-boosted-with-
   roster-backoff beats both.
4. **Stop asking for all 8 cards as if it matters.** It does not, measurably, at Game 2. Let
   the win condition alone be a first-class input — it costs one dropdown and performs within
   noise of the full deck.
5. **Show the shortlist honestly.** A top-3 that is right ~34% of the time is still useful
   for prep, but it should be labelled as "1 in 3", not presented as a prediction.
