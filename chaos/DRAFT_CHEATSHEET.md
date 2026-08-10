# Chaos Draft — pick cheat sheet

Built 2026-08-10 from 2,856 battles / 22,848 decoded decisions.
Your capture rate: **66.0%** over 1,052 decisions. Field: 43.9%. SK xopxsam: 81.4%.

Regenerate the underlying numbers any time with `python chaos/analyze_chaos.py`.

---

## 1. Your three habits to break

These are your biggest leaks, measured across every pick you've made.

| Stop taking | How often you took it when the other card was better | Strength given away |
|---|---|---|
| **Ronin** | 16 times | −3.7 |
| **Royal Giant** | 14 times | −3.6 |
| **X-Bow** | 12 times | −3.4 |

All three are bottom-12 cards (Ronin −0.18, Royal Giant −0.39, X-Bow −0.36), and the
top-ladder group has already worked this out — they take X-Bow 28% and Royal Giant 21%.
Ronin is the single most overrated card in the mode: 68% pick rate at the top, 58th of 66
by strength.

**Start taking** the cards you most often pass up when they were the better option:
Witch (14 times), Zappies (17), Skeleton Barrel (13), Rascals (13), Suspicious Bush (7).

---

## 2. Tier list

Only cards offered 200+ times. Percentages are the tracked top players' pick rates.

### Almost always take

| Card | Strength | Top pick rate |
|---|---|---|
| Suspicious Bush | +0.43 | 79% |
| Musketeer | +0.34 | 75% |
| Goblin Demolisher | +0.32 | 84% |
| Skeleton Barrel | +0.29 | 82% |
| Skeleton Army | +0.28 | 84% |
| Goblin Drill | +0.28 | 78% |
| Fireball | +0.28 | 84% |
| Barbarian Barrel | +0.27 | 68% |
| The Log | +0.26 | 73% |
| Goblin Barrel | +0.24 | 91% |
| Electro Wizard | +0.23 | 82% |
| Witch | +0.21 | 63% |

**Underpriced by the field** — Suspicious Bush, Barbarian Barrel, The Log and Witch are all
top-12 by strength but taken well below their value. Bush is the strongest card in the mode.

### Almost always pass

| Card | Strength | Top pick rate |
|---|---|---|
| Royal Giant | −0.39 | 21% |
| Rocket | −0.36 | 39% |
| X-Bow | −0.36 | 28% |
| Inferno Tower | −0.35 | 23% |
| Elixir Golem | −0.34 | 5% |
| Lava Hound | −0.27 | 4% |
| Rage | −0.22 | 12% |
| Goblin Giant | −0.20 | 24% |
| Elite Barbarians | −0.20 | 21% |
| Ronin | −0.18 | 68% |
| Tesla | −0.16 | 51% |
| Giant Snowball | −0.15 | 12% |

**Ronin (68%) and Tesla (51%) are the traps** — the only two weak cards the top group still
takes routinely. Everything else on this list they already avoid.

---

## 3. Specific pairings you keep getting wrong

Faced 3+ times, lost most of them.

| You took | Over | Record |
|---|---|---|
| Royal Giant | Giant Snowball | 3 of 3 wrong |
| Golem | Fireball | 3 of 4 wrong |
| Knight | Electro Spirit | 3 of 3 wrong |
| Executioner | Electro Spirit | 3 of 3 wrong |
| Berserker | Electro Spirit | 3 of 3 wrong |

**Electro Spirit** appears three times. You pass it every time it's up against a mid-cost
troop, and the model rates it positively.

---

## 4. Context — how much this is worth

| | |
|---|---|
| Win rate when you win the draft | **81%** |
| Win rate when you lose the draft | **52%** |
| Draft round where you're weakest | none — rounds 1-4 are all +0.12 to +0.15 |
| Share of outcomes the draft explains | ~1/3 (model accuracy 64.5% vs 50% coin flip) |

Two thirds of the result is still how you play. But a 29-point swing on the half of games
where the draft is decided is not small.

**Your specific weakness is resilience:** 52% when out-drafted, against xopxsam's 73% and
Asaf's 75%. When you win the draft you're normal for the group. When you lose it, you fall
further than your peers do.

---

## Caveats — read before trusting any single line

- **The model can't see synergy.** It rates cards independently, so a pick that's weaker
  alone but fits your other seven perfectly will look wrong here. Trust your read over the
  table when the fit is obvious.
- **It can't see card levels or matchup.** Only which cards were present.
- **Sample sizes vary.** The tier list is solid (200+ offers per card). The specific
  pairings in section 3 are 3-4 observations each — suggestive, not proven.
- **Some circularity.** Your 1,052 decisions helped fit these strengths, so the model
  partly learned from you. Reassuringly you rank 7th of 9 on capture rate, which means it
  isn't simply flattering your habits.
