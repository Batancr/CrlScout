# Spell sequencing across a duel set

_Generated 2026-08-18 07:31 UTC_

Spells are a ~18-card space and most decks run two, so sequence signal that is invisible at deck level may be readable here.

> **Method note.** Cards cannot repeat inside a duel set, so game-1 spells are mechanically absent from game 2. Every baseline below is renormalised over only the packages still legal, so the lift column measures preference rather than re-deriving the no-repeat rule.

## Post-patch (Aug 5+) — CRL + practice

Duels: **4242** · distinct game-2 spell packages: **122**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**36 of 206 rows survive FDR correction (q=0.1, threshold p<=0.01656). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Fireball + Zap | **Goblin Curse + Rage** | 4% | 0% | 11.96x | 127 | 0.0001 |
| **✓** | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.55x | 61 | 0.0005 |
| **✓** | Lightning + Royal Delivery | **Barbarian Barrel** | 25% | 5% | 5.35x | 24 | 0.0007 |
| **✓** | Barbarian Barrel + Lightning | **Tornado + Void** | 2% | 1% | 4.08x | 419 | 0.0002 |
| **✓** | Lightning + Tornado | **Fireball + Zap** | 18% | 5% | 3.93x | 28 | 0.0079 |
| **✓** | Void + Zap | **Barbarian Barrel + Lightning** | 25% | 7% | 3.62x | 28 | 0.0024 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Void** | 4% | 1% | 3.51x | 170 | 0.0079 |
| **✓** | Fireball | **Barbarian Barrel** | 16% | 4% | 3.49x | 32 | 0.0131 |
| **✓** | Rage + Void + Zap | **Barbarian Barrel + Lightning** | 23% | 7% | 3.29x | 26 | 0.0081 |
| **✓** | Lightning + Tornado | **Barbarian Barrel + Fireball** | 32% | 10% | 3.23x | 28 | 0.0011 |
| **✓** | Giant Snowball + Poison + Royal Delivery | **Barbarian Barrel + Lightning** | 24% | 8% | 3.16x | 29 | 0.0052 |
| **✓** | Barbarian Barrel | **Fireball** | 4% | 2% | 2.86x | 296 | 0.0008 |
| **✓** | Royal Delivery | **Barbarian Barrel** | 10% | 4% | 2.67x | 68 | 0.0156 |
| **✓** | Barbarian Barrel + Poison | **Lightning + Tornado** | 4% | 2% | 2.48x | 191 | 0.0166 |
| **✓** | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 9% | 4% | 2.46x | 165 | 0.0013 |
| **✓** | Barbarian Barrel + Fireball | **The Log + Void** | 4% | 2% | 2.26x | 546 | 0.0004 |
| **✓** | Goblin Curse + Zap | **Barbarian Barrel** | 9% | 4% | 2.23x | 151 | 0.0043 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel** | 10% | 5% | 2.21x | 170 | 0.0020 |
| **✓** | Arrows | **Barbarian Barrel + Lightning** | 15% | 7% | 2.20x | 281 | 0.0000 |
| **✓** | Royal Delivery | **Barbarian Barrel + Fireball** | 18% | 8% | 2.16x | 68 | 0.0085 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**69 of 302 rows survive FDR (q=0.1, p<=0.02192).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Giant | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.80x | 59 | 0.0005 |
| **✓** | Graveyard | Arrows + Giant Snowball | **Barbarian Barrel + Void** | 8% | 1% | 7.67x | 60 | 0.0005 |
| **✓** | X-Bow | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 25% | 4% | 6.77x | 32 | 0.0000 |
| **✓** | Mortar | Barbarian Barrel + Lightning | **Tornado + Void** | 3% | 1% | 5.38x | 159 | 0.0026 |
| **✓** | Golem | Lightning + Tornado | **Fireball + Zap** | 23% | 5% | 5.00x | 22 | 0.0027 |
| **✓** | Royal Hogs | Barbarian Barrel + Fireball | **The Log + Void** | 9% | 2% | 4.90x | 126 | 0.0000 |
| **✓** | Graveyard | Giant Snowball + Poison | **Barbarian Barrel** | 21% | 5% | 4.73x | 28 | 0.0014 |
| **✓** | Royal Hogs | Lightning + Royal Delivery | **Barbarian Barrel** | 22% | 5% | 4.65x | 23 | 0.0037 |
| **✓** | Lava Hound | Goblin Curse + Zap | **Barbarian Barrel + Poison** | 16% | 4% | 4.01x | 37 | 0.0034 |
| **✓** | Skeleton Barrel | Fireball | **Barbarian Barrel** | 17% | 4% | 3.85x | 29 | 0.0087 |
| **✓** | Elite Barbarians | Fireball + The Log | **Barbarian Barrel + Lightning + Tornado** | 13% | 4% | 3.64x | 52 | 0.0029 |
| **✓** | Skeleton Barrel | Barbarian Barrel + Fireball | **The Log + Void** | 6% | 2% | 3.64x | 108 | 0.0033 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Tornado + Void** | 2% | 1% | 3.64x | 235 | 0.0130 |
| **✓** | Mortar | Fireball | **Barbarian Barrel** | 16% | 4% | 3.61x | 31 | 0.0115 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Void** | 4% | 1% | 3.50x | 142 | 0.0149 |
| **✓** | Goblin Barrel | Royal Delivery | **Barbarian Barrel** | 13% | 4% | 3.32x | 47 | 0.0090 |
| **✓** | Elite Barbarians | Rage + Void + Zap | **Barbarian Barrel + Lightning** | 23% | 7% | 3.29x | 26 | 0.0081 |
| **✓** | Royal Hogs | Barbarian Barrel + Fireball | **Lightning + Tornado** | 6% | 2% | 3.26x | 126 | 0.0061 |
| **✓** | Elite Barbarians | Barbarian Barrel | **Fireball** | 5% | 2% | 3.24x | 262 | 0.0002 |
| **✓** | Golem | Lightning + Tornado | **Barbarian Barrel + Fireball** | 32% | 10% | 3.20x | 22 | 0.0043 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **3435**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**31 of 93 rows survive FDR (q=0.1, p<=0.03212).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Poison + The Log | **Barbarian Barrel + Lightning** | 35% | 5% | 6.57x | 17 | 0.0002 |
| **✓** | Barbarian Barrel + Lightning + The Log | **Giant Snowball + Poison + Royal Delivery** | 10% | 2% | 4.81x | 50 | 0.0038 |
| **✓** | Giant Snowball + Lightning + Poison + The Log | **Barbarian Barrel + Fireball** | 39% | 8% | 4.65x | 18 | 0.0004 |
| **✓** | Arrows + Lightning + The Log | **Barbarian Barrel + Fireball** | 31% | 8% | 4.06x | 36 | 0.0000 |
| **✓** | Arrows + Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 25% | 6% | 3.92x | 28 | 0.0015 |
| **✓** | Arrows + Lightning + The Log | **Barbarian Barrel + Poison** | 14% | 4% | 3.69x | 36 | 0.0107 |
| **✓** | Barbarian Barrel + Fireball + Giant Snowball | **Lightning + The Log** | 43% | 12% | 3.68x | 14 | 0.0033 |
| **✓** | Arrows + Poison + The Log | **Barbarian Barrel + Lightning** | 25% | 7% | 3.49x | 20 | 0.0117 |
| **✓** | Arrows | **Barbarian Barrel + Lightning** | 14% | 4% | 3.27x | 37 | 0.0174 |
| **✓** | Barbarian Barrel + Fireball + Giant Snowball + Poison | **Lightning + Tornado** | 9% | 3% | 3.23x | 70 | 0.0107 |
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows + Rage** | 3% | 1% | 3.22x | 177 | 0.0207 |
| **✓** | Arrows + Barbarian Barrel + Poison | **Fireball + Zap** | 14% | 4% | 3.19x | 50 | 0.0060 |
| **✓** | Arrows + Barbarian Barrel + Lightning + Tornado | **Earthquake + The Log** | 17% | 5% | 3.15x | 30 | 0.0195 |
| **✓** | Barbarian Barrel + Goblin Curse + Lightning + Zap | **Fireball + The Log** | 32% | 10% | 3.10x | 31 | 0.0008 |
| **✓** | Barbarian Barrel + Poison | **Fireball + The Log** | 28% | 9% | 3.09x | 29 | 0.0031 |
| **✓** | Barbarian Barrel + Giant Snowball + Poison | **Goblin Curse + Zap** | 14% | 4% | 3.01x | 37 | 0.0239 |
| **✓** | Barbarian Barrel + Giant Snowball + Lightning + Poison | **Fireball + The Log** | 35% | 12% | 2.93x | 49 | 0.0000 |
| **✓** | Barbarian Barrel + Fireball + Lightning + The Log | **Earthquake + Royal Delivery** | 3% | 1% | 2.86x | 177 | 0.0321 |
| **✓** | Barbarian Barrel + Giant Snowball + Lightning + Poison + Tornado | **Fireball + The Log** | 36% | 13% | 2.83x | 39 | 0.0002 |
| **✓** | Barbarian Barrel + Lightning | **Fireball + The Log** | 24% | 9% | 2.73x | 38 | 0.0045 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Arrows | 10% |
| Barbarian Barrel + Fireball | 8% |
| Giant Snowball + Poison | 7% |
| Lightning + The Log | 7% |
| Fireball + The Log | 6% |
| Barbarian Barrel + Lightning | 6% |
| (no spells) | 5% |
| Barbarian Barrel | 4% |
| Barbarian Barrel + Poison | 4% |
| Fireball + Zap | 3% |

## Post-patch (Aug 5+) — Official CRL only

Duels: **994** · distinct game-2 spell packages: **81**

### Game 1 spells → game 2 spells

Baseline is constraint-aware: the game-2 package distribution renormalised over only packages still legal after game 1 burned its cards. Lift is therefore preference, not the no-repeat rule.


**12 of 45 rows survive FDR correction (q=0.1, threshold p<=0.02539). Only ticked rows are trustworthy.**

| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Fireball + Zap | **Barbarian Barrel** | 26% | 8% | 3.45x | 23 | 0.0061 |
| **✓** | Barbarian Barrel | **Fireball** | 5% | 2% | 3.03x | 102 | 0.0254 |
| **✓** | Tornado + Zap | **Barbarian Barrel + Fireball** | 31% | 10% | 2.99x | 32 | 0.0011 |
| **✓** | Arrows | **Barbarian Barrel + Fireball** | 25% | 10% | 2.52x | 63 | 0.0004 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Lightning** | 15% | 6% | 2.46x | 52 | 0.0150 |
| **✓** | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 25% | 11% | 2.31x | 52 | 0.0030 |
| **✓** | Lightning + The Log | **Barbarian Barrel + Fireball** | 29% | 14% | 2.07x | 68 | 0.0010 |
| **✓** | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 25% | 13% | 1.97x | 51 | 0.0115 |
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 34% | 20% | 1.73x | 176 | 0.0000 |
| **✓** | Barbarian Barrel + Lightning | **Fireball + The Log** | 19% | 12% | 1.62x | 119 | 0.0134 |
| **✓** | Barbarian Barrel | **Lightning + The Log** | 25% | 16% | 1.53x | 102 | 0.0177 |
| **✓** | Barbarian Barrel + Lightning | **Arrows** | 21% | 14% | 1.52x | 119 | 0.0204 |
|  | Earthquake + The Log | **Barbarian Barrel** | 20% | 8% | 2.62x | 25 | 0.0381 |
|  | Lightning + Tornado | **Barbarian Barrel + Fireball** | 31% | 12% | 2.55x | 16 | 0.0379 |
|  | Arrows | **Fireball + Zap** | 8% | 4% | 1.93x | 63 | 0.1176 |
|  | Arrows | **Barbarian Barrel + Lightning** | 11% | 6% | 1.90x | 63 | 0.0736 |
|  | Giant Snowball + Poison | **Barbarian Barrel** | 12% | 7% | 1.74x | 52 | 0.1288 |
|  | Barbarian Barrel + Fireball | **Poison + The Log** | 3% | 2% | 1.59x | 176 | 0.1798 |
|  | Giant Snowball + Poison | **Fireball + The Log** | 13% | 9% | 1.57x | 52 | 0.1564 |
|  | Barbarian Barrel + Fireball | **Lightning + Tornado** | 3% | 2% | 1.56x | 176 | 0.2181 |

### Their game-1 win condition + spells → their game-2 spells

Your hypothesis: having already spent (say) Royal Hogs, the biggest spell-bait threat is gone, which should move their next spell choice.


**20 of 52 rows survive FDR (q=0.1, p<=0.03809).**

| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|---|
| **✓** | Elite Barbarians | Barbarian Barrel | **Fireball** | 5% | 2% | 3.22x | 96 | 0.0201 |
| **✓** | Balloon | Tornado + Zap | **Barbarian Barrel + Fireball** | 32% | 10% | 3.09x | 31 | 0.0009 |
| **✓** | Miner | Tornado + Zap | **Barbarian Barrel + Fireball** | 32% | 10% | 3.09x | 31 | 0.0009 |
| **✓** | Battle Ram | Barbarian Barrel | **Fireball** | 5% | 2% | 3.06x | 101 | 0.0245 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Lightning** | 19% | 6% | 2.97x | 43 | 0.0048 |
| **✓** | Golem | Lightning + Tornado | **Barbarian Barrel + Fireball** | 33% | 12% | 2.72x | 15 | 0.0289 |
| **✓** | Hog Rider | Earthquake + The Log | **Barbarian Barrel** | 20% | 8% | 2.62x | 25 | 0.0381 |
| **✓** | Battle Ram | Arrows | **Barbarian Barrel + Lightning** | 14% | 6% | 2.45x | 49 | 0.0229 |
| **✓** | Battle Ram | Arrows | **Barbarian Barrel + Fireball** | 24% | 10% | 2.43x | 49 | 0.0028 |
| **✓** | Goblin Drill | Giant Snowball + Poison | **Barbarian Barrel + Fireball** | 26% | 11% | 2.37x | 43 | 0.0050 |
| **✓** | Hog Rider | Lightning + The Log | **Barbarian Barrel + Fireball** | 33% | 14% | 2.34x | 24 | 0.0148 |
| **✓** | Royal Hogs | Lightning + The Log | **Barbarian Barrel + Fireball** | 33% | 14% | 2.34x | 33 | 0.0045 |
| **✓** | Golem | Barbarian Barrel + Lightning + Tornado | **Fireball + The Log** | 26% | 13% | 2.04x | 34 | 0.0259 |
| **✓** | Elite Barbarians | Barbarian Barrel + Fireball | **Lightning + The Log** | 40% | 20% | 2.02x | 88 | 0.0000 |
| **✓** | Mortar | Barbarian Barrel + Fireball | **Lightning + The Log** | 39% | 20% | 1.98x | 77 | 0.0001 |
| **✓** | Royal Giant | Barbarian Barrel + Fireball | **Lightning + The Log** | 36% | 20% | 1.81x | 76 | 0.0009 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Arrows** | 23% | 14% | 1.69x | 77 | 0.0162 |
| **✓** | Royal Hogs | Barbarian Barrel + Lightning | **Fireball + The Log** | 19% | 12% | 1.63x | 77 | 0.0377 |
| **✓** | Elite Barbarians | Barbarian Barrel | **Lightning + The Log** | 25% | 16% | 1.56x | 96 | 0.0157 |
| **✓** | Battle Ram | Barbarian Barrel | **Lightning + The Log** | 25% | 16% | 1.54x | 101 | 0.0157 |

### Games 1+2 spells → game 3 spells

Duels reaching game 3: **429**. By game 3 up to four spells are burned, so the legal pool is small — which is exactly why this is the most predictable slot.


**1 of 4 rows survive FDR (q=0.1, p<=0.01412).**

| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |
|---|---|---|---|---|---|---|---|
| **✓** | Barbarian Barrel + Fireball | **Lightning + The Log** | 36% | 11% | 3.22x | 14 | 0.0141 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Giant Snowball + Poison** | 27% | 17% | 1.57x | 45 | 0.0697 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **Arrows** | 20% | 18% | 1.09x | 45 | 0.4461 |
|  | Barbarian Barrel + Fireball + Lightning + The Log | **(no spells)** | 13% | 14% | 0.93x | 45 | 0.6457 |

### Most common game-2 spell packages overall

| package | share |
|---|---|
| Lightning + The Log | 12% |
| Barbarian Barrel + Fireball | 9% |
| Arrows | 8% |
| Giant Snowball + Poison | 8% |
| Fireball + The Log | 7% |
| Barbarian Barrel | 5% |
| Barbarian Barrel + Lightning | 5% |
| (no spells) | 5% |
| Fireball + Zap | 4% |
| Earthquake + The Log | 3% |
