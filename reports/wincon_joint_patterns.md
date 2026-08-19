# Does your game-1 win condition predict their game-2 deck?

Physical duels analysed: **4772** (9454 directed observations, each duel counted from both sides).

## How this was tested

The null hypothesis is deliberately harsh: **their own game 1 already tells you everything, and your deck adds nothing.** The permutation shuffles YOUR game-1 win conditions across duels while leaving each opponent's own game1->game2 pairing untouched. A pattern only counts if it beats that.

- 3000 permutations
- Benjamini-Hochberg FDR at q=0.1 (threshold p <= 0.0003)
- Minimum 15 observations per context, minimum 5 per cell
- Candidate cells scanned: 1853

## Result: **7 of 1853** patterns survived

| You open | They open | They follow with | rate | base rate | lift | n | p |
|---|---|---|---|---|---|---|---|
| Golem | Goblin Drill | **Hog Rider** | 25% | 6% | 3.88x | 36 | 0.0003 |
| Royal Giant | Graveyard | **Goblin Drill** | 11% | 3% | 3.71x | 74 | 0.0003 |
| Royal Giant | Ram Rider | **Battle Ram** | 42% | 14% | 2.99x | 19 | 0.0003 |
| Elite Barbarians | Royal Giant | **Elite Barbarians** | 10% | 4% | 2.30x | 143 | 0.0003 |
| Elite Barbarians | Wall Breakers | **Elite Barbarians** | 16% | 7% | 2.25x | 103 | 0.0003 |
| Elite Barbarians | Graveyard | **Elite Barbarians** | 16% | 8% | 2.05x | 108 | 0.0003 |
| Royal Giant | Royal Hogs | **Wall Breakers** | 16% | 8% | 2.03x | 189 | 0.0003 |

## Strongest raw associations (NOT significance-tested)

Shown only so you can see what the scan was looking at. These have not survived the permutation test and should not be acted on.

| You open | They open | They follow with | rate | base | lift | n | p |
|---|---|---|---|---|---|---|---|
| Miner | Ram Rider | Wall Breakers | 17% | 3% | 4.90x | 30 | 0.0020 |
| Balloon | Goblin Drill | Golem | 16% | 3% | 4.69x | 32 | 0.0033 |
| Rune Giant | Graveyard | Rune Giant | 12% | 3% | 4.01x | 58 | 0.0013 |
| Golem | Goblin Drill | Hog Rider | 25% | 6% | 3.88x | 36 | 0.0003 |
| Mortar | Electro Giant | Royal Giant | 35% | 9% | 3.81x | 23 | 0.0013 |
| Royal Giant | Graveyard | Goblin Drill | 11% | 3% | 3.71x | 74 | 0.0003 |
| Ram Rider | Graveyard | Battle Ram | 32% | 9% | 3.60x | 22 | 0.0020 |
| Electro Giant | Graveyard | Battle Ram | 31% | 9% | 3.53x | 16 | 0.0023 |
| Hog Rider | Rune Giant | Goblin Barrel | 13% | 4% | 3.50x | 39 | 0.0043 |
| Wall Breakers | Balloon | Lava Hound | 9% | 3% | 3.35x | 57 | 0.0143 |
| Skeleton Barrel | Balloon | Mortar | 21% | 6% | 3.33x | 28 | 0.0013 |
| Lava Hound | Graveyard | Goblin Drill | 10% | 3% | 3.30x | 52 | 0.0103 |
| Giant | Golem | Wall Breakers | 26% | 8% | 3.28x | 19 | 0.0033 |
| Giant | Graveyard | Mortar | 22% | 7% | 3.07x | 23 | 0.0073 |
| Balloon | Lava Hound | Royal Hogs | 29% | 9% | 3.06x | 21 | 0.0060 |

## For comparison: what their own game 1 says

| They open | They follow with | rate | n |
|---|---|---|---|
| Rune Giant | Elite Barbarians | 17% | 574 |
| X-Bow | Battle Ram | 15% | 103 |
| Rune Giant | Battle Ram | 14% | 574 |
| Ram Rider | Battle Ram | 14% | 206 |
| Wall Breakers | Royal Hogs | 14% | 1100 |
| Goblin Giant | Royal Hogs | 14% | 111 |
| Elite Barbarians | Royal Hogs | 13% | 1598 |
| Three Musketeers | Graveyard | 13% | 122 |
| Battle Ram | Royal Hogs | 13% | 1371 |
| Goblin Barrel | Royal Hogs | 13% | 792 |
| X-Bow | Elite Barbarians | 13% | 103 |
| Skeleton Barrel | Royal Hogs | 12% | 823 |
| Royal Giant | Miner | 12% | 1244 |
| Giant | Royal Hogs | 12% | 295 |
| Ram Rider | Elite Barbarians | 12% | 206 |
| Graveyard | Miner | 11% | 1131 |
| Miner | Royal Hogs | 11% | 1396 |
| Wall Breakers | Royal Giant | 11% | 1100 |
| Royal Giant | Wall Breakers | 11% | 1244 |
| Electro Giant | Goblin Drill | 11% | 219 |
