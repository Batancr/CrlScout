# Chaos Draft tracker

- Unique battles archived: **3797**
- Tracked top players: **39**
- Draft decisions decoded: **30376**
- strength model fitted on 3797 battles, in-sample accuracy 63.5%.

## Most picked when offered — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Fireball | 90% | 238 | 66% |
| Goblin Barrel | 89% | 222 | 64% |
| Poison | 88% | 205 | 63% |
| Goblin Demolisher | 86% | 216 | 64% |
| Goblin Drill | 85% | 230 | 68% |
| Skeleton Army | 85% | 231 | 67% |
| Skeleton Barrel | 85% | 260 | 69% |
| Royal Hogs | 84% | 212 | 64% |
| Golem | 83% | 224 | 61% |
| Vines | 81% | 203 | 63% |

## Least picked — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Lava Hound | 6% | 232 | 57% |
| Elixir Golem | 8% | 219 | 55% |
| Rage | 9% | 254 | 58% |
| Giant Snowball | 11% | 247 | 57% |
| Fisherman | 15% | 217 | 52% |
| Royal Giant | 17% | 228 | 53% |
| Ice Wizard | 20% | 219 | 62% |
| Heal Spirit | 22% | 198 | 62% |
| Rune Giant | 22% | 212 | 56% |
| Dark Prince | 23% | 204 | 54% |

## What separates the top players from the field

Pick-rate gap on cards both groups saw enough of. A positive gap means the
tracked top players take it more often than the field does.

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Arrows | 76% | 64% | **+12%** | +0.13 |
| Poison | 88% | 77% | **+12%** | +0.21 |
| Royal Hogs | 84% | 73% | **+11%** | +0.13 |
| Vines | 81% | 70% | **+11%** | +0.21 |
| Goblin Drill | 85% | 74% | **+11%** | +0.37 |
| Knight | 66% | 55% | **+11%** | +0.06 |

Cards the top players avoid *more* than the field:

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Giant Snowball | 11% | 20% | **-9%** | -0.17 |
| Lava Hound | 6% | 16% | **-10%** | -0.27 |
| Dark Prince | 23% | 33% | **-10%** | -0.19 |
| Hunter | 31% | 41% | **-10%** | -0.20 |
| Elite Barbarians | 24% | 36% | **-12%** | -0.23 |
| X-Bow | 29% | 45% | **-16%** | -0.34 |

## Draft-style outliers among the tracked players

How far each player's pick rates sit from the tracked-group consensus.
Higher = more idiosyncratic. Needs 100+ decisions to mean much.

| Player | Decisions | Deviation from consensus | Draft edge | Win rate |
|---|---|---|---|---|
| Reora. | 180 | 0.220 | +0.154 | 42% |
| 凛冬Rintou✨卤蛋 | 192 | 0.210 | +0.137 | 60% |
| RAIN | 148 | 0.208 | +0.154 | 57% |
| OcT❤️Lev4ek | 124 | 0.198 | +0.180 | 74% |
| Arrrr＿ | 244 | 0.196 | +0.133 | 51% |
| 23BS6N | 124 | 0.196 | +0.130 | 61% |
| Sam❤️Rehwald | 120 | 0.191 | +0.202 | 67% |
| Loris | 140 | 0.189 | +0.137 | 54% |
| Aʀоmaτ❤ | 296 | 0.186 | +0.115 | 49% |
| Dread Unlock | 136 | 0.184 | +0.142 | 41% |
| Golem | 132 | 0.184 | +0.152 | 55% |
| Asaf | 124 | 0.177 | +0.164 | 81% |
| MicinoCoccoloso | 244 | 0.176 | +0.130 | 52% |
| Batman | 192 | 0.171 | +0.142 | 52% |
| 5>Niko✨Drill | 140 | 0.170 | +0.156 | 49% |
| SYX_OGtrooper | 188 | 0.169 | +0.137 | 55% |
| Busfahrer Dirk | 292 | 0.162 | +0.162 | 67% |
| リクルート | 204 | 0.162 | +0.183 | 49% |
| Metalfusion | 128 | 0.161 | +0.136 | 53% |
| vicki£22 | 140 | 0.158 | +0.149 | 57% |
| tarikzius | 132 | 0.157 | +0.180 | 45% |
| けーたいぷ✨ | 136 | 0.154 | +0.175 | 50% |
| leon | 340 | 0.153 | +0.129 | 53% |
| Tim f2p | 184 | 0.151 | +0.122 | 48% |
| Hazy | 120 | 0.150 | +0.179 | 73% |
| 郁白❤️时光☪ | 136 | 0.145 | +0.177 | 65% |
| カオス | 280 | 0.142 | +0.140 | 51% |
| Eurus | 120 | 0.137 | +0.134 | 87% |
| tiktok@kai_cr12 | 124 | 0.136 | +0.164 | 74% |
| ΨΨΨ | 124 | 0.127 | +0.157 | 48% |
| =★The Star★= | 316 | 0.124 | +0.138 | 53% |
| SK xopxsam | 536 | 0.122 | +0.181 | 86% |
| batan | 1052 | 0.094 | +0.154 | 68% |

## Draft skill: capture rate

Share of the strength that was actually on the table which the player took.
'Available' is near-identical for everyone, so this isolates decision quality
from luck of the draw. **Untracked field: 46.8%.**

| Player | Games | Win rate | Capture | Available | Won draft | Lost draft |
|---|---|---|---|---|---|---|
| Sam❤️Rehwald | 30 | 67% | **89.2%** | 0.227 | 76% (21) | 44% (9) |
| SK xopxsam | 134 | 86% | **84.0%** | 0.216 | 92% (87) | 74% (47) |
| リクルート | 51 | 49% | **81.1%** | 0.226 | 55% (33) | 39% (18) |
| tarikzius | 33 | 45% | **79.5%** | 0.226 | 50% (24) | 33% (9) |
| けーたいぷ✨ | 34 | 50% | **79.0%** | 0.221 | 81% (16) | 22% (18) |
| OcT❤️Lev4ek | 31 | 74% | **76.7%** | 0.234 | 78% (23) | 62% (8) |
| Busfahrer Dirk | 73 | 67% | **74.7%** | 0.217 | 71% (49) | 58% (24) |
| vicki£22 | 35 | 57% | **72.3%** | 0.206 | 78% (18) | 35% (17) |
| 郁白❤️时光☪ | 34 | 65% | **72.2%** | 0.245 | 70% (23) | 55% (11) |
| 5>Niko✨Drill | 35 | 49% | **72.1%** | 0.216 | 79% (19) | 12% (16) |
| ΨΨΨ | 31 | 48% | **71.1%** | 0.221 | 53% (19) | 42% (12) |
| Eurus | 30 | 87% | **70.3%** | 0.191 | 95% (20) | 70% (10) |
| Asaf | 31 | 81% | **69.4%** | 0.237 | 83% (18) | 77% (13) |
| Hazy | 30 | 73% | **68.7%** | 0.260 | 77% (22) | 62% (8) |
| Metalfusion | 32 | 53% | **68.2%** | 0.199 | 64% (14) | 44% (18) |
| batan | 263 | 68% | **68.0%** | 0.227 | 79% (147) | 54% (116) |
| Reora. | 45 | 42% | **67.3%** | 0.228 | 65% (23) | 18% (22) |
| SYX_OGtrooper | 47 | 55% | **67.2%** | 0.204 | 70% (23) | 42% (24) |
| =★The Star★= | 79 | 53% | **67.0%** | 0.206 | 65% (34) | 44% (45) |
| RAIN | 37 | 57% | **65.5%** | 0.235 | 71% (21) | 38% (16) |
| tiktok@kai_cr12 | 31 | 74% | **65.1%** | 0.252 | 75% (20) | 73% (11) |
| カオス | 70 | 51% | **64.7%** | 0.216 | 55% (38) | 47% (32) |
| Dread Unlock | 34 | 41% | **63.8%** | 0.222 | 64% (14) | 25% (20) |
| MicinoCoccoloso | 61 | 52% | **62.7%** | 0.208 | 70% (30) | 35% (31) |
| Batman | 48 | 52% | **62.2%** | 0.228 | 67% (24) | 38% (24) |
| Golem | 33 | 55% | **61.9%** | 0.246 | 61% (18) | 47% (15) |
| 凛冬Rintou✨卤蛋 | 48 | 60% | **61.1%** | 0.224 | 87% (23) | 36% (25) |
| Arrrr＿ | 61 | 51% | **60.6%** | 0.219 | 75% (24) | 35% (37) |
| Loris | 35 | 54% | **59.9%** | 0.228 | 87% (15) | 30% (20) |
| Tim f2p | 46 | 48% | **59.5%** | 0.205 | 62% (21) | 36% (25) |
| Aʀоmaτ❤ | 74 | 49% | **58.2%** | 0.199 | 57% (23) | 45% (51) |
| leon | 85 | 53% | **58.0%** | 0.223 | 67% (39) | 41% (46) |
| 23BS6N | 31 | 61% | **57.3%** | 0.227 | 74% (19) | 42% (12) |

## Tracked players

| Player | Games | Win rate |
|---|---|---|
| batan *(your account)* | 263 | 68% |
| SK xopxsam | 134 | 86% |
| leon | 85 | 53% |
| =★The Star★= | 79 | 53% |
| Aʀоmaτ❤ | 74 | 49% |
| Busfahrer Dirk | 73 | 67% |
| カオス | 70 | 51% |
| MicinoCoccoloso | 61 | 52% |
| Arrrr＿ | 61 | 51% |
| リクルート | 51 | 49% |
| Batman | 48 | 52% |
| 凛冬Rintou✨卤蛋 | 48 | 60% |
| SYX_OGtrooper | 47 | 55% |
| Tim f2p | 46 | 48% |
| Reora. | 45 | 42% |
| RAIN | 37 | 57% |
| Loris | 35 | 54% |
| vicki£22 | 35 | 57% |
| 5>Niko✨Drill | 35 | 49% |
| けーたいぷ✨ | 34 | 50% |
| 郁白❤️时光☪ | 34 | 65% |
| Dread Unlock | 34 | 41% |
| Golem | 33 | 55% |
| tarikzius | 33 | 45% |
| Metalfusion | 32 | 53% |
| tiktok@kai_cr12 | 31 | 74% |
| OcT❤️Lev4ek | 31 | 74% |
| Asaf | 31 | 81% |
| 23BS6N | 31 | 61% |
| ΨΨΨ | 31 | 48% |
| Eurus | 30 | 87% |
| Hazy | 30 | 73% |
| Sam❤️Rehwald | 30 | 67% |
| Sweeping Demon | 16 | 50% |
| 老板 Ι Batan'宙斯 *(your account)* | 13 | 85% |
| かさあま | 12 | 67% |
| イッシー | 10 | 40% |
| GiovanniXD | 9 | 33% |
| Pi✨Maskk | 9 | 56% |
