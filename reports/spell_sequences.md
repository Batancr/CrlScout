# Spell sequencing across a duel set

_Generated 2026-08-19 03:39 UTC_

Spells are a ~18-card space and most decks run two, so sequence signal that is invisible at deck level may be readable here.

**Scopes.** The *finals window* (Aug 16+) starts at Day-2 CRL: every game in it is either a real bracket game or top-16 prep for the monthly finals. It is the highest-quality population available, but it is ~646 duels against 4,242 post-patch, so far fewer cells clear significance. Post-patch is kept alongside it for comparison, not because it is more relevant.

> **Method note.** Cards cannot repeat inside a duel set, so game-1 spells are mechanically absent from game 2. Every baseline below is renormalised over only the packages still legal, so the lift column measures preference rather than re-deriving the no-repeat rule.

## Finals window (Aug 16+, Day-2 CRL onward) — CRL + practice

Duels: **686** · distinct game-2 spell packages: **69**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**13 of 28 rows survive FDR correction (q=0.1, threshold p<=0.04491). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Rocket + The Log | **Barbarian Barrel + Lightning** | 45% | 5% | 8.97x | 11 | 0.0001 |
| **✓** | Fireball + Zap | **Barbarian Barrel + Vines** | 25% | 6% | 4.03x | 20 | 0.0065 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 19% | 6% | 3.22x | 27 | 0.0176 |
| **✓** | Barbarian Barrel + Vines | **Lightning + Royal Delivery** | 12% | 4% | 2.87x | 42 | 0.0292 |
| **✓** | Tornado + Zap | **Barbarian Barrel + Fireball** | 31% | 11% | 2.82x | 16 | 0.0257 |
| **✓** | Arrows | **Fireball + Zap** | 12% | 4% | 2.79x | 41 | 0.0325 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 30% | 12% | 2.58x | 27 | 0.0090 |
| **✓** | Barbarian Barrel + Vines | **Lightning + The Log** | 33% | 13% | 2.47x | 42 | 0.0008 |
| **✓** | Lightning + The Log | **Barbarian Barrel + Fireball** | 34% | 14% | 2.46x | 38 | 0.0013 |
| **✓** | Barbarian Barrel + Lightning | **Earthquake + The Log** | 10% | 4% | 2.32x | 71 | 0.0313 |
| **✓** | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 22% | 10% | 2.15x | 46 | 0.0153 |
| **✓** | Barbarian Barrel + Fireball | **Poison + The Log** | 7% | 3% | 2.06x | 138 | 0.0318 |
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 20% | 15% | 1.38x | 138 | 0.0449 |
|  | Lightning + The Log | **Barbarian Barrel + Vines** | 13% | 7% | 1.89x | 38 | 0.1221 |
|  | Barbarian Barrel + Fireball | **Arrows + Giant Snowball** | 4% | 2% | 1.78x | 138 | 0.1510 |
|  | Barbarian Barrel + Lightning | **Fireball + The Log** | 15% | 9% | 1.68x | 71 | 0.0600 |
|  | Arrows | **Barbarian Barrel + Fireball** | 17% | 10% | 1.64x | 41 | 0.1303 |
|  | Barbarian Barrel + Lightning | **Fireball + Zap** | 10% | 6% | 1.60x | 71 | 0.1455 |
|  | Fireball + The Log | **Giant Snowball + Poison** | 26% | 16% | 1.58x | 27 | 0.1410 |
|  | Barbarian Barrel + Lightning + Tornado | **Giant Snowball + Poison** | 24% | 18% | 1.33x | 46 | 0.1898 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**11 of 27 rows survive FDR (q=0.1, p<=0.03986).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 22% | 6% | 3.78x | 23 | 0.0089 |
| **✓** | Royal Giant | Barbarian Barrel + Fireball | **Poison + The Log** | 10% | 3% | 3.16x | 60 | 0.0116 |
| **✓** | Elite Barbarians | Barbarian Barrel + Vines | **Lightning + Royal Delivery** | 12% | 4% | 2.94x | 41 | 0.0266 |
| **✓** | Miner | Tornado + Zap | **Barbarian Barrel + Fireball** | 31% | 11% | 2.82x | 16 | 0.0257 |
| **✓** | Balloon | Tornado + Zap | **Barbarian Barrel + Fireball** | 31% | 11% | 2.82x | 16 | 0.0257 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 30% | 12% | 2.65x | 23 | 0.0123 |
| **✓** | Hog Rider | Lightning + The Log | **Barbarian Barrel + Fireball** | 37% | 14% | 2.64x | 19 | 0.0110 |
| **✓** | Battle Ram | Barbarian Barrel + Vines | **Lightning + The Log** | 35% | 13% | 2.61x | 37 | 0.0007 |
| **✓** | Elite Barbarians | Barbarian Barrel + Vines | **Lightning + The Log** | 34% | 13% | 2.53x | 41 | 0.0006 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Fireball + The Log** | 20% | 9% | 2.21x | 54 | 0.0094 |
| **✓** | Mortar | Barbarian Barrel + Fireball | **Lightning + The Log** | 25% | 15% | 1.67x | 53 | 0.0399 |
|  | Royal Hogs | Lightning + The Log | **Barbarian Barrel + Fireball** | 33% | 14% | 2.39x | 15 | 0.0470 |
|  | Royal Hogs | Barbarian Barrel + Lightning | **Earthquake + The Log** | 9% | 4% | 2.18x | 54 | 0.0792 |
|  | Golem | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 16% | 10% | 1.56x | 38 | 0.1822 |
|  | Royal Hogs | Barbarian Barrel + Lightning | **Fireball + Zap** | 9% | 6% | 1.51x | 54 | 0.2368 |
|  | Royal Giant | Barbarian Barrel + Fireball | **Lightning + The Log** | 22% | 15% | 1.48x | 60 | 0.0931 |
|  | Battle Ram | Arrows | **Barbarian Barrel + Fireball** | 15% | 10% | 1.45x | 33 | 0.2580 |
|  | Elite Barbarians | Barbarian Barrel + Fireball | **Lightning + The Log** | 21% | 15% | 1.42x | 77 | 0.0920 |
|  | Royal Giant | Barbarian Barrel + Fireball | **Giant Snowball + Poison** | 22% | 16% | 1.39x | 60 | 0.1321 |
|  | Elite Barbarians | Barbarian Barrel + Fireball | **Tornado + Zap** | 6% | 5% | 1.37x | 77 | 0.3015 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **490**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**1 of 3 rows survive FDR (q=0.1, p<=0.00169).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Barbarian Barrel + Fireball + Giant Snowball + Poison | **Lightning + The Log** | 39% | 15% | 2.59x | 28 | 0.0017 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows** | 23% | 15% | 1.57x | 35 | 0.1265 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Giant Snowball + Poison** | 26% | 21% | 1.21x | 35 | 0.3200 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Giant Snowball + Poison | 10% |
| Lightning + The Log | 9% |
| Barbarian Barrel + Fireball | 9% |
| Arrows | 8% |
| Fireball + The Log | 6% |
| Barbarian Barrel + Vines | 5% |
| Fireball + Zap | 4% |
| Barbarian Barrel + Lightning | 4% |
| Tornado + Zap | 3% |
| Lightning + Royal Delivery | 3% |

## Finals window (Aug 16+, Day-2 CRL onward) — Official CRL only

Duels: **304** · distinct game-2 spell packages: **57**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**8 of 11 rows survive FDR correction (q=0.1, threshold p<=0.05827). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 33% | 8% | 4.35x | 15 | 0.0041 |
| **✓** | Barbarian Barrel + Vines | **Lightning + The Log** | 55% | 20% | 2.78x | 20 | 0.0005 |
| **✓** | Arrows | **Barbarian Barrel + Fireball** | 29% | 11% | 2.66x | 17 | 0.0329 |
| **✓** | Barbarian Barrel + Lightning | **Earthquake + The Log** | 14% | 6% | 2.49x | 35 | 0.0483 |
| **✓** | Lightning + The Log | **Barbarian Barrel + Fireball** | 36% | 16% | 2.30x | 25 | 0.0104 |
| **✓** | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 26% | 11% | 2.30x | 19 | 0.0583 |
| **✓** | Barbarian Barrel + Lightning | **Fireball + Zap** | 17% | 7% | 2.29x | 35 | 0.0433 |
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 33% | 22% | 1.52x | 60 | 0.0287 |
|  | Barbarian Barrel + Lightning + Tornado | **Giant Snowball + Poison** | 26% | 15% | 1.80x | 19 | 0.1340 |
|  | Barbarian Barrel + Lightning | **Fireball + The Log** | 17% | 10% | 1.66x | 35 | 0.1479 |
|  | Barbarian Barrel + Fireball | **Giant Snowball + Poison** | 17% | 12% | 1.38x | 60 | 0.1804 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**5 of 10 rows survive FDR (q=0.1, p<=0.03245).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 38% | 8% | 5.02x | 13 | 0.0020 |
| **✓** | Hog Rider | Lightning + The Log | **Barbarian Barrel + Fireball** | 50% | 16% | 3.20x | 12 | 0.0057 |
| **✓** | Elite Barbarians | Barbarian Barrel + Vines | **Lightning + The Log** | 55% | 20% | 2.78x | 20 | 0.0005 |
| **✓** | Battle Ram | Barbarian Barrel + Vines | **Lightning + The Log** | 55% | 20% | 2.78x | 20 | 0.0005 |
| **✓** | Royal Giant | Barbarian Barrel + Fireball | **Lightning + The Log** | 40% | 22% | 1.82x | 25 | 0.0324 |
|  | Royal Hogs | Barbarian Barrel + Lightning | **Fireball + The Log** | 21% | 10% | 2.07x | 28 | 0.0630 |
|  | Golem | Barbarian Barrel + Lightning + Tornado | **Giant Snowball + Poison** | 28% | 15% | 1.90x | 18 | 0.1116 |
|  | Mortar | Barbarian Barrel + Fireball | **Lightning + The Log** | 34% | 22% | 1.57x | 29 | 0.0852 |
|  | Elite Barbarians | Barbarian Barrel + Fireball | **Lightning + The Log** | 32% | 22% | 1.47x | 34 | 0.1082 |
|  | Elite Barbarians | Barbarian Barrel + Fireball | **Giant Snowball + Poison** | 15% | 12% | 1.22x | 34 | 0.3905 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **142**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**2 of 2 rows survive FDR (q=0.1, p<=0.09936).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Giant Snowball + Poison** | 33% | 19% | 1.80x | 18 | 0.0994 |
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows** | 33% | 19% | 1.80x | 18 | 0.0994 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Lightning + The Log | 14% |
| Barbarian Barrel + Fireball | 10% |
| Giant Snowball + Poison | 8% |
| Barbarian Barrel + Vines | 6% |
| Arrows | 6% |
| Fireball + The Log | 6% |
| Fireball + Zap | 4% |
| Earthquake + The Log | 3% |
| Lightning + Royal Delivery | 3% |
| Tornado + Zap | 3% |

## Post-patch (Aug 5+) — CRL + practice

Duels: **4408** · distinct game-2 spell packages: **135**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**37 of 216 rows survive FDR correction (q=0.1, threshold p<=0.01603). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Fireball + Zap | **Goblin Curse + Rage** | 4% | 0% | 12.08x | 131 | 0.0001 |
| **✓** | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.69x | 62 | 0.0005 |
| **✓** | Rage + Void + Zap | **Vines** | 19% | 4% | 5.01x | 26 | 0.0028 |
| **✓** | Lightning + Royal Delivery | **Barbarian Barrel + Vines** | 21% | 4% | 4.66x | 24 | 0.0037 |
| **✓** | Barbarian Barrel + Lightning | **Tornado + Void** | 2% | 1% | 4.10x | 433 | 0.0002 |
| **✓** | Lightning + Tornado | **Fireball + Zap** | 18% | 5% | 3.92x | 28 | 0.0080 |
| **✓** | Fireball | **Barbarian Barrel + Vines** | 16% | 4% | 3.78x | 31 | 0.0095 |
| **✓** | Void + Zap | **Barbarian Barrel + Lightning** | 25% | 7% | 3.63x | 28 | 0.0024 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Void** | 3% | 1% | 3.52x | 176 | 0.0077 |
| **✓** | Rage + Void + Zap | **Barbarian Barrel + Lightning** | 23% | 7% | 3.30x | 26 | 0.0079 |
| **✓** | Lightning + Tornado | **Barbarian Barrel + Fireball** | 32% | 10% | 3.22x | 28 | 0.0012 |
| **✓** | Giant Snowball + Poison + Royal Delivery | **Barbarian Barrel + Lightning** | 24% | 8% | 3.17x | 29 | 0.0052 |
| **✓** | (no spells) | **Barbarian Barrel + Fireball** | 22% | 8% | 2.89x | 136 | 0.0000 |
| **✓** | Barbarian Barrel + Vines | **Fireball** | 4% | 2% | 2.55x | 297 | 0.0032 |
| **✓** | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 9% | 4% | 2.46x | 172 | 0.0009 |
| **✓** | Barbarian Barrel + Vines | **Lightning + Royal Delivery** | 3% | 1% | 2.32x | 297 | 0.0126 |
| **✓** | Arrows | **Barbarian Barrel + Lightning** | 15% | 7% | 2.21x | 279 | 0.0000 |
| **✓** | Barbarian Barrel + Fireball | **The Log + Void** | 4% | 2% | 2.20x | 584 | 0.0006 |
| **✓** | Goblin Curse + Zap | **Barbarian Barrel + Vines** | 9% | 4% | 2.17x | 151 | 0.0074 |
| **✓** | Vines | **Barbarian Barrel + Poison** | 8% | 4% | 2.17x | 146 | 0.0101 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**76 of 318 rows survive FDR (q=0.1, p<=0.02218).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Giant | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.95x | 60 | 0.0004 |
| **✓** | Graveyard | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.82x | 61 | 0.0005 |
| **✓** | X-Bow | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 25% | 4% | 6.60x | 32 | 0.0000 |
| **✓** | Mortar | Barbarian Barrel + Lightning | **Tornado + Void** | 3% | 1% | 5.48x | 162 | 0.0024 |
| **✓** | Giant | Rage + Void + Zap | **Vines** | 21% | 4% | 5.43x | 24 | 0.0019 |
| **✓** | Elite Barbarians | Rage + Void + Zap | **Vines** | 19% | 4% | 5.01x | 26 | 0.0028 |
| **✓** | Golem | Lightning + Tornado | **Fireball + Zap** | 23% | 5% | 4.99x | 22 | 0.0027 |
| **✓** | Royal Hogs | Barbarian Barrel + Fireball | **The Log + Void** | 8% | 2% | 4.87x | 132 | 0.0000 |
| **✓** | Royal Hogs | Lightning + Royal Delivery | **Barbarian Barrel + Vines** | 22% | 4% | 4.86x | 23 | 0.0031 |
| **✓** | Elite Barbarians | Poison + The Log | **Barbarian Barrel + Lightning + Tornado** | 16% | 4% | 4.26x | 44 | 0.0012 |
| **✓** | Lava Hound | Goblin Curse + Zap | **Barbarian Barrel + Poison** | 16% | 4% | 4.06x | 37 | 0.0032 |
| **✓** | Skeleton Barrel | Fireball | **Barbarian Barrel + Vines** | 17% | 4% | 4.04x | 29 | 0.0072 |
| **✓** | Graveyard | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 17% | 4% | 3.98x | 29 | 0.0076 |
| **✓** | Mortar | Fireball | **Barbarian Barrel + Vines** | 16% | 4% | 3.78x | 31 | 0.0095 |
| **✓** | Skeleton Barrel | Barbarian Barrel + Fireball | **The Log + Void** | 6% | 2% | 3.72x | 110 | 0.0030 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Tornado + Void** | 2% | 1% | 3.61x | 246 | 0.0134 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Void** | 3% | 1% | 3.51x | 147 | 0.0147 |
| **✓** | Elite Barbarians | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 13% | 4% | 3.49x | 53 | 0.0037 |
| **✓** | Royal Hogs | Barbarian Barrel + Fireball | **Lightning + Tornado** | 6% | 2% | 3.47x | 132 | 0.0024 |
| **✓** | Goblin Barrel | Royal Delivery | **Barbarian Barrel + Vines** | 12% | 4% | 3.32x | 49 | 0.0090 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **3594**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**22 of 78 rows survive FDR (q=0.1, p<=0.02469).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Giant Snowball + Lightning + Poison + The Log | **Barbarian Barrel + Fireball** | 39% | 8% | 4.79x | 18 | 0.0003 |
| **✓** | Arrows + Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 28% | 6% | 4.50x | 29 | 0.0003 |
| **✓** | Arrows + Lightning + The Log | **Barbarian Barrel + Fireball** | 31% | 7% | 4.19x | 36 | 0.0000 |
| **✓** | Arrows + Poison + The Log | **Barbarian Barrel + Lightning** | 29% | 7% | 3.94x | 21 | 0.0030 |
| **✓** | Arrows + Lightning + The Log | **Barbarian Barrel + Poison** | 14% | 4% | 3.73x | 36 | 0.0103 |
| **✓** | Arrows + Barbarian Barrel + Poison | **Fireball + Zap** | 16% | 5% | 3.53x | 44 | 0.0034 |
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows + Rage** | 3% | 1% | 3.40x | 186 | 0.0168 |
| **✓** | Barbarian Barrel + Fireball + Poison + The Log | **Lightning + Tornado** | 10% | 3% | 3.33x | 77 | 0.0028 |
| **✓** | Barbarian Barrel + Fireball | **Goblin Curse + Zap** | 12% | 4% | 3.13x | 49 | 0.0119 |
| **✓** | Barbarian Barrel + Goblin Curse + Lightning + Zap | **Fireball + The Log** | 32% | 11% | 3.07x | 31 | 0.0009 |
| **✓** | Arrows + Vines | **Lightning + The Log** | 26% | 9% | 2.99x | 23 | 0.0122 |
| **✓** | Arrows + Fireball + The Log | **Barbarian Barrel + Lightning** | 19% | 7% | 2.85x | 31 | 0.0167 |
| **✓** | Barbarian Barrel + Giant Snowball + Lightning + Poison | **Fireball + The Log** | 34% | 12% | 2.84x | 50 | 0.0000 |
| **✓** | Barbarian Barrel + Giant Snowball + Lightning + Poison + Tornado | **Fireball + The Log** | 36% | 13% | 2.80x | 39 | 0.0002 |
| **✓** | Barbarian Barrel + Fireball + Giant Snowball + Poison | **Lightning + Tornado** | 7% | 3% | 2.76x | 81 | 0.0219 |
| **✓** | Barbarian Barrel + Giant Snowball + Poison + Vines | **Fireball + The Log** | 26% | 11% | 2.25x | 35 | 0.0145 |
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 20% | 9% | 2.21x | 49 | 0.0130 |
| **✓** | Arrows + Barbarian Barrel + Fireball | **Lightning + The Log** | 26% | 12% | 2.21x | 69 | 0.0009 |
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Giant Snowball + Poison + Royal Delivery** | 5% | 2% | 2.19x | 186 | 0.0236 |
| **✓** | Barbarian Barrel + Lightning + Poison + The Log + Tornado | **Arrows** | 40% | 19% | 2.11x | 20 | 0.0237 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Arrows | 9% |
| Barbarian Barrel + Fireball | 8% |
| Giant Snowball + Poison | 7% |
| Lightning + The Log | 7% |
| Fireball + The Log | 6% |
| Barbarian Barrel + Lightning | 6% |
| Fireball + Zap | 3% |
| Barbarian Barrel + Poison | 3% |
| Barbarian Barrel + Vines | 3% |
| Goblin Curse + Zap | 3% |

## Post-patch (Aug 5+) — Official CRL only

Duels: **994** · distinct game-2 spell packages: **90**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**9 of 43 rows survive FDR correction (q=0.1, threshold p<=0.01505). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Fireball + Zap | **Barbarian Barrel + Vines** | 26% | 8% | 3.45x | 23 | 0.0061 |
| **✓** | Tornado + Zap | **Barbarian Barrel + Fireball** | 31% | 10% | 2.99x | 32 | 0.0011 |
| **✓** | Arrows | **Barbarian Barrel + Fireball** | 28% | 10% | 2.79x | 57 | 0.0001 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Lightning** | 15% | 6% | 2.46x | 52 | 0.0150 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 25% | 11% | 2.31x | 52 | 0.0030 |
| **✓** | Lightning + The Log | **Barbarian Barrel + Fireball** | 29% | 14% | 2.07x | 68 | 0.0010 |
| **✓** | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 25% | 13% | 1.97x | 51 | 0.0115 |
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 34% | 20% | 1.73x | 176 | 0.0000 |
| **✓** | Barbarian Barrel + Lightning | **Fireball + The Log** | 19% | 12% | 1.62x | 119 | 0.0134 |
|  | Barbarian Barrel + Vines | **Fireball** | 5% | 2% | 2.83x | 102 | 0.0325 |
|  | Barbarian Barrel + Lightning | **Arrows + Vines** | 5% | 2% | 2.69x | 119 | 0.0253 |
|  | Earthquake + The Log | **Barbarian Barrel + Vines** | 20% | 8% | 2.62x | 25 | 0.0381 |
|  | Lightning + Tornado | **Barbarian Barrel + Fireball** | 31% | 12% | 2.55x | 16 | 0.0379 |
|  | Arrows | **Fireball + Zap** | 9% | 4% | 2.13x | 57 | 0.0852 |
|  | Arrows | **Barbarian Barrel + Lightning** | 12% | 6% | 2.10x | 57 | 0.0473 |
|  | Giant Snowball + Poison | **Barbarian Barrel + Vines** | 12% | 7% | 1.74x | 52 | 0.1288 |
|  | Barbarian Barrel + Lightning | **Vines** | 5% | 3% | 1.74x | 119 | 0.1332 |
|  | Barbarian Barrel + Fireball | **Poison + The Log** | 3% | 2% | 1.59x | 176 | 0.1798 |
|  | Giant Snowball + Poison | **Fireball + The Log** | 13% | 9% | 1.57x | 52 | 0.1564 |
|  | Barbarian Barrel + Fireball | **Lightning + Tornado** | 3% | 2% | 1.56x | 176 | 0.2181 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**23 of 52 rows survive FDR (q=0.1, p<=0.04402).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Arrows + Vines** | 8% | 2% | 4.15x | 77 | 0.0033 |
| **✓** | Miner | Tornado + Zap | **Barbarian Barrel + Fireball** | 32% | 10% | 3.09x | 31 | 0.0009 |
| **✓** | Balloon | Tornado + Zap | **Barbarian Barrel + Fireball** | 32% | 10% | 3.09x | 31 | 0.0009 |
| **✓** | Elite Barbarians | Barbarian Barrel + Vines | **Fireball** | 5% | 2% | 3.01x | 96 | 0.0259 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Lightning** | 19% | 6% | 2.97x | 43 | 0.0048 |
| **✓** | Battle Ram | Barbarian Barrel + Vines | **Fireball** | 5% | 2% | 2.86x | 101 | 0.0313 |
| **✓** | Elite Barbarians | Arrows | **Barbarian Barrel + Lightning** | 17% | 6% | 2.86x | 30 | 0.0284 |
| **✓** | Golem | Lightning + Tornado | **Barbarian Barrel + Fireball** | 33% | 12% | 2.72x | 15 | 0.0289 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Vines** | 8% | 3% | 2.69x | 77 | 0.0246 |
| **✓** | Battle Ram | Arrows | **Barbarian Barrel + Lightning** | 16% | 6% | 2.67x | 45 | 0.0148 |
| **✓** | Battle Ram | Arrows | **Barbarian Barrel + Fireball** | 27% | 10% | 2.65x | 45 | 0.0013 |
| **✓** | Hog Rider | Earthquake + The Log | **Barbarian Barrel + Vines** | 20% | 8% | 2.62x | 25 | 0.0381 |
| **✓** | Mortar | Barbarian Barrel + Lightning | **Fireball + Zap** | 16% | 6% | 2.54x | 32 | 0.0440 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 26% | 11% | 2.37x | 43 | 0.0050 |
| **✓** | Hog Rider | Lightning + The Log | **Barbarian Barrel + Fireball** | 33% | 14% | 2.34x | 24 | 0.0148 |
| **✓** | Royal Hogs | Lightning + The Log | **Barbarian Barrel + Fireball** | 33% | 14% | 2.34x | 33 | 0.0045 |
| **✓** | Golem | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 26% | 13% | 2.04x | 34 | 0.0259 |
| **✓** | Elite Barbarians | Barbarian Barrel + Fireball | **Lightning + The Log** | 40% | 20% | 2.02x | 88 | 0.0000 |
| **✓** | Mortar | Barbarian Barrel + Fireball | **Lightning + The Log** | 39% | 20% | 1.98x | 77 | 0.0001 |
| **✓** | Royal Giant | Barbarian Barrel + Fireball | **Lightning + The Log** | 36% | 20% | 1.81x | 76 | 0.0009 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **429**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**0 of 3 rows survive FDR (q=0.1, p<=0.00000).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Giant Snowball + Poison** | 27% | 17% | 1.57x | 45 | 0.0697 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Vines** | 13% | 9% | 1.45x | 45 | 0.2279 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows** | 16% | 15% | 1.02x | 45 | 0.5430 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Lightning + The Log | 12% |
| Barbarian Barrel + Fireball | 9% |
| Giant Snowball + Poison | 8% |
| Arrows | 7% |
| Fireball + The Log | 7% |
| Barbarian Barrel + Vines | 5% |
| Barbarian Barrel + Lightning | 5% |
| Fireball + Zap | 4% |
| Earthquake + The Log | 3% |
| (no spells) | 3% |
