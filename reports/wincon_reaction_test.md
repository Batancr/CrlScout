# Do opponents adapt their game-2 pick?

CRL gives both players a 2-minute break between games to choose their next deck, so a game-2 pick is made knowing what you played and who won. This tests whether that shows up in the data.

Usable duels (decisive game 1): **4771** · directed observations: **9452**

## Test 1 — does the game-1 result change their next pick?

This is the clean test. Your-deck effects are confounded by matchmaking (Elite Barbs players meet Elite Barbs players). The **result** is not: same two players, same two decks, only the winner varies. The permutation shuffles win/loss *within each opening win condition*, so nothing but the result moves.

- 3000 permutations · BH-FDR q=0.1 (threshold p<=0.0000)
- Minimum 25 observations per arm
- Cells scanned: 296 · **survived: 0**

**No cell survived.** Within the resolution of this archive, winning or losing game 1 does not measurably change which win condition an opponent brings next.

That is a genuine finding, not a failed test. The 2-minute window exists and players use it, but at the win-condition level their second pick looks like it was going to happen either way — consistent with players arriving with a planned deck order and adapting only at the card-choice level, which this test cannot see.

### Largest raw result gaps (not significance-tested)

| They opened | They follow with | after LOSS | after WIN | diff | n | p |
|---|---|---|---|---|---|---|
| Ram Rider | Battle Ram | 20.3% | 5.7% | +14.7% | 118/88 | 0.0030 |
| Three Musketeers | Graveyard | 6.7% | 19.4% | -12.7% | 60/62 | 0.0447 |
| Goblin Giant | Elite Barbarians | 13.4% | 2.3% | +11.2% | 67/44 | 0.0257 |
| Ram Rider | Elite Barbarians | 15.3% | 6.8% | +8.4% | 118/88 | 0.0413 |
| Ram Rider | Miner | 3.4% | 10.2% | -6.8% | 118/88 | 0.0350 |
| Three Musketeers | Skeleton Barrel | 6.7% | 12.9% | -6.2% | 60/62 | 0.2309 |
| Ram Rider | Graveyard | 7.6% | 2.3% | +5.4% | 118/88 | 0.0906 |
| Goblin Barrel | Royal Giant | 6.9% | 11.9% | -5.1% | 407/385 | 0.0143 |
| Electro Giant | Goblin Drill | 8.2% | 13.2% | -5.1% | 98/121 | 0.2662 |
| Miner | Royal Hogs | 9.1% | 14.1% | -5.0% | 735/661 | 0.0023 |
| Giant | Skeleton Barrel | 5.6% | 10.4% | -4.9% | 161/134 | 0.1073 |
| Wall Breakers | Royal Giant | 9.1% | 13.9% | -4.8% | 605/495 | 0.0140 |
| Three Musketeers | Wall Breakers | 8.3% | 12.9% | -4.6% | 60/62 | 0.3669 |
| Balloon | Battle Ram | 8.6% | 13.0% | -4.3% | 266/231 | 0.1086 |
| X-Bow | Elite Barbarians | 14.3% | 10.0% | +4.3% | 63/40 | 0.4795 |
