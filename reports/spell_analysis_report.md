# Spell sequencing analysis

**Archive:** through 2026-08-18 · **Scripts:** `spell_sequences.py`, `scout_player_spells.py`
**Companion reports:** `spell_sequences.md` (full tables), `spell_scout_asaf.md` (Asaf detail)

---

## The short version

**Spell sequencing works far better than win-condition sequencing.** The earlier win-condition
work produced 7 surviving patterns out of 1,853 scanned (0.4%). Spells produce **36 of 206**
for game 2, **69 of 302** once the win condition is added, and **31 of 93** for game 3 —
between 17% and 33% survival at the same FDR threshold.

Your reasoning for why was correct: spells are an ~18-card space, most decks run exactly two,
and the no-repeat rule bites much harder on a small pool. By game 3 up to four spells are
already spent, which is why that slot is the most readable in the entire dataset.

**Your Royal Hogs hypothesis checks out.** Royal Hogs + Fireball/Barb Barrel in game 1 →
**The Log + Void** in game 2 at 9% against a 2% legal baseline — 4.9x, n=126, p<0.0001.

**Asaf is a spell-identity player.** His spell concentration sits at the 70th–80th percentile
in *all four framings*, unlike his deck pool which swung from 33rd to 90th. His spells are the
stable read; his decks are not.

---

## Method — the trap this avoids

Cards cannot repeat inside a duel set. A game-1 Lightning + Barb Barrel therefore
*mechanically* guarantees game 2 contains neither. Comparing "what follows Lightning + Barb
Barrel" against the overall popularity of spell packages would rediscover that rule and dress
it up as a behavioural insight.

**Every baseline here is constraint-aware:** the game-2 package distribution renormalised over
only those packages still *legal* given what game 1 burned. A 3x lift means they genuinely
prefer that package among what remains available to them.

**Significance.** Hundreds of context/outcome cells are scanned, so an uncorrected p<0.05 would
produce roughly 15 false hits per 300 rows. Each row gets an exact binomial test against its
legal-pool baseline, then Benjamini–Hochberg FDR at q=0.10.

**Spell definition.** The 18 damage/utility spells: Arrows, Barbarian Barrel, Earthquake,
Fireball, Freeze, Giant Snowball, Goblin Curse, Lightning, Poison, Rage, Rocket, Royal
Delivery, The Log, Tornado, Void, Zap, Clone, Mirror. Graveyard and Goblin Barrel are excluded
— they are spells in-game but function as win conditions and are already handled by
`classify_deck()`.

---

## Roster-wide — post-patch (Aug 5+), CRL + practice

**4,242 duels · 122 distinct game-2 spell packages · 36 of 206 rows survive FDR**

### Game 1 spells → game 2 spells

| they opened with | they follow with | rate | legal base | lift | n | p |
|---|---|---|---|---|---|---|
| Fireball + Zap | Goblin Curse + Rage | 4% | 0% | 11.96x | 127 | 0.0001 |
| Arrows + Giant Snowball | Barbarian Barrel + Void | 8% | 1% | 7.55x | 61 | 0.0005 |
| Lightning + Royal Delivery | Barbarian Barrel | 25% | 5% | 5.35x | 24 | 0.0007 |
| Barbarian Barrel + Lightning | Tornado + Void | 2% | 1% | 4.08x | 419 | 0.0002 |
| Lightning + Tornado | Fireball + Zap | 18% | 5% | 3.93x | 28 | 0.0079 |
| Void + Zap | Barbarian Barrel + Lightning | 25% | 7% | 3.62x | 28 | 0.0024 |
| Lightning + Tornado | Barbarian Barrel + Fireball | 32% | 10% | 3.23x | 28 | 0.0011 |
| Barbarian Barrel | Fireball | 4% | 2% | 2.86x | 296 | 0.0008 |
| Barbarian Barrel + Fireball | The Log + Void | 4% | 2% | 2.26x | 546 | 0.0004 |
| Arrows | Barbarian Barrel + Lightning | 15% | 7% | 2.20x | 281 | 0.0000 |

### Their game-1 win condition + spells → their game-2 spells — **your hypothesis**

**69 of 302 rows survive.** Adding the win condition roughly doubles the yield over spells
alone, which is direct evidence that the win condition carries information the spells don't.

| g1 win con | g1 spells | g2 spells | rate | legal base | lift | n | p |
|---|---|---|---|---|---|---|---|
| Giant | Arrows + Giant Snowball | Barbarian Barrel + Void | 8% | 1% | 7.80x | 59 | 0.0005 |
| Graveyard | Arrows + Giant Snowball | Barbarian Barrel + Void | 8% | 1% | 7.67x | 60 | 0.0005 |
| X-Bow | Fireball + The Log | Barb Barrel + Lightning + Tornado | 25% | 4% | 6.77x | 32 | 0.0000 |
| Mortar | Barbarian Barrel + Lightning | Tornado + Void | 3% | 1% | 5.38x | 159 | 0.0026 |
| Golem | Lightning + Tornado | Fireball + Zap | 23% | 5% | 5.00x | 22 | 0.0027 |
| **Royal Hogs** | **Barbarian Barrel + Fireball** | **The Log + Void** | **9%** | **2%** | **4.90x** | **126** | **0.0000** |
| **Royal Hogs** | **Lightning + Royal Delivery** | **Barbarian Barrel** | **22%** | **5%** | **4.65x** | **23** | **0.0037** |
| Lava Hound | Goblin Curse + Zap | Barbarian Barrel + Poison | 16% | 4% | 4.01x | 37 | 0.0034 |
| Elite Barbarians | Fireball + The Log | Barb Barrel + Lightning + Tornado | 13% | 4% | 3.64x | 52 | 0.0029 |
| **Royal Hogs** | **Barbarian Barrel + Fireball** | **Lightning + Tornado** | **6%** | **2%** | **3.26x** | **126** | **0.0061** |
| Elite Barbarians | Barbarian Barrel | Fireball | 5% | 2% | 3.24x | 262 | 0.0002 |

**On your Royal Hogs question specifically.** You asked whether, with Royal Hogs spent, players
lean toward Poison/Log or instead toward Lightning/Log since the biggest spell-bait threat is
gone. The data says **both, and Log is the constant.** After Royal Hogs + Barb Barrel/Fireball
they go **The Log + Void** (4.9x) or **Lightning + Tornado** (3.3x). The Log appears in the
strongest branch, so your first instinct was closer — but note this is a correlation. It does
not prove they are reasoning about your spell-bait lean; it only shows the tendency is real.

### Games 1+2 spells → game 3 — **the most readable slot in the dataset**

**31 of 93 rows survive.** 3,435 duels reach game 3.

| spells already spent | game 3 spells | rate | legal base | lift | n | p |
|---|---|---|---|---|---|---|
| Poison + The Log | Barbarian Barrel + Lightning | 35% | 5% | 6.57x | 17 | 0.0002 |
| Snowball + Lightning + Poison + Log | Barbarian Barrel + Fireball | 39% | 8% | 4.65x | 18 | 0.0004 |
| Arrows + Lightning + The Log | Barbarian Barrel + Fireball | 31% | 8% | 4.06x | 36 | 0.0000 |
| Barb Barrel + Fireball + Snowball | Lightning + The Log | 43% | 12% | 3.68x | 14 | 0.0033 |
| Arrows + Poison + The Log | Barbarian Barrel + Lightning | 25% | 7% | 3.49x | 20 | 0.0117 |
| Barb Barrel + Goblin Curse + Lightning + Zap | Fireball + The Log | 32% | 10% | 3.10x | 31 | 0.0008 |
| Barb Barrel + Snowball + Lightning + Poison | Fireball + The Log | 35% | 12% | 2.93x | 49 | 0.0000 |

The pattern across these rows is consistent: **once the cheap small spells are spent, the
remaining pick collapses toward Barb Barrel + Fireball or Lightning + Log.** Those two packages
absorb most of the surviving game-3 probability mass.

---

## Roster-wide — post-patch, Official CRL only

**994 duels · 12 of 45 game-2 rows survive · only 1 of 4 game-3 rows survives**

| they opened with | they follow with | rate | legal base | lift | n |
|---|---|---|---|---|---|
| Fireball + Zap | Barbarian Barrel | 26% | 8% | 3.45x | 23 |
| Tornado + Zap | Barbarian Barrel + Fireball | 31% | 10% | 2.99x | 32 |
| Arrows | Barbarian Barrel + Fireball | 25% | 10% | 2.52x | 63 |
| Giant Snowball + Poison | Barbarian Barrel + Fireball | 25% | 11% | 2.31x | 52 |
| Lightning + The Log | Barbarian Barrel + Fireball | 29% | 14% | 2.07x | 68 |
| Barbarian Barrel + Fireball | Lightning + The Log | 34% | 20% | 1.73x | 176 |

**Lifts are much smaller here — 1.5–3.5x versus up to 12x pooled.** Two things to note. Tournament
players converge on a narrower spell meta, so the *legal baseline itself is higher* and there is
less room for lift. And 994 duels simply cannot support the game-3 analysis: one surviving row.
**For game-3 spell reading you need the practice data pooled in.**

---

## Asaf — spell profile across the four framings

| framing | duels | games | packages | top-3 concentration | vs roster |
|---|---|---|---|---|---|
| Post-patch, CRL + practice | 35 | 94 | 27 | 36% | 80th pctile |
| Post-patch, Official CRL only | 16 | 38 | 14 | **50%** | 78th pctile |
| All time, CRL + practice | 74 | 199 | 43 | 34% | 70th pctile |
| All time, Official CRL only | 38 | 93 | 24 | 44% | 75th pctile |

> **No p-values on his transitions, deliberately.** Split four ways his transition cells land at
> n = 1–4. No honest test survives that, and printing one would invite reading noise as a tell.
> Concentration percentile is the statistically usable number.

### The finding: his spells are stabler than his decks

His **deck** concentration swung wildly across framings — 33rd percentile all-time, 90th
post-patch in CRL. His **spell** concentration sits at 70–80th percentile in *every* framing,
including all-time. He has been a narrow-spell player the whole time; only his win conditions
have churned.

**Practical read: prep against his spell package, not his deck list.** In post-patch CRL, half
his games come from just three spell packages.

### What he brings

**Post-patch, Official CRL only** (16 duels — indicative only):

| package | games | share |
|---|---|---|
| Giant Snowball + Poison | 7 | 18% |
| Barbarian Barrel + Fireball | 7 | 18% |
| Barbarian Barrel | 5 | 13% |
| (no spells) | 3 | 8% |

**Post-patch, CRL + practice** — individual spell usage:

| spell | decks | share of his decks |
|---|---|---|
| Barbarian Barrel | 26 | 28% |
| Fireball | 19 | 20% |
| Giant Snowball | 18 | 19% |
| Poison | 16 | 17% |
| The Log | 14 | 15% |
| Zap | 12 | 13% |
| Lightning | 10 | 11% |

**Barbarian Barrel is in 28% of his post-patch decks** and it is his single most-used spell in
every framing (24% all-time). If you are choosing what to bait, assume Barb Barrel is present.

### His sequencing

**Post-patch, CRL + practice** — only **4 of 29** game-1→game-2 spell transitions occurred more
than once:

| he opened | he followed with | times |
|---|---|---|
| Barbarian Barrel + Fireball | Giant Snowball + Poison | 4 |
| Barbarian Barrel + Fireball | Lightning + The Log | 2 |
| Barbarian Barrel + Fireball | Giant Snowball | 2 |
| Barbarian Barrel | Giant Snowball + Poison | 2 |

**All time** — 12 of 55 repeated:

| he opened | he followed with | times |
|---|---|---|
| Barbarian Barrel + Fireball | Giant Snowball + Poison | 5 |
| Lightning + The Log | Giant Snowball + Poison | 4 |
| Royal Delivery | Lightning + The Log | 3 |
| Royal Delivery | Giant Snowball + Poison | 3 |

**The one tendency worth carrying into finals: Barb Barrel + Fireball → Snowball + Poison.**
It is his most repeated transition in both post-patch (4 times) and all-time (5 times), and it
sits inside his two most-used packages. That is as close to a read as 35 duels supports.

Note that **Royal Delivery has largely dropped out post-patch** — 11% of his all-time games, and
it does not appear in his post-patch top 8. Don't prep for it.

His game-3 spell transitions are all n=1. There is nothing there.

---

## Caveats

**These are roster-wide tendencies, not opponent-specific reads.** A 4.9x lift describes how the
tracked population behaves, not how one named player will behave.

**Sample sizes vary enormously** — surviving rows run from n=14 to n=546. Prefer high-n rows. A
2.3x lift at n=546 is worth more than a 6.6x at n=17.

**The Official-CRL-only game-3 analysis is not usable.** One surviving row out of four.

**Asaf's transition tables carry no significance claim** and should not be treated as
predictions. The concentration percentiles are the trustworthy part of that section.

**Correlation, not mechanism.** A surviving pattern shows the tendency is real. It does not
establish that players are reasoning the way the hypothesis supposes — only that the behaviour
occurs more than the legal pool predicts.

**Related null result.** Whether an opponent won or lost game 1 does *not* measurably change
which win condition they bring next — 296 cells scanned, zero survived FDR. See
`wincon_reaction_test.md`.
