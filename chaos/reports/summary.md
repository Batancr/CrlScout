# Chaos Draft tracker

- Unique battles archived: **3430**
- Tracked top players: **33**
- Draft decisions decoded: **27440**
- strength model fitted on 3430 battles, in-sample accuracy 64.1%.

## Most picked when offered — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Goblin Barrel | 90% | 156 | 67% |
| Fireball | 88% | 185 | 67% |
| Poison | 87% | 158 | 65% |
| Skeleton Army | 86% | 173 | 68% |
| Royal Hogs | 86% | 163 | 65% |
| Skeleton Barrel | 84% | 208 | 73% |
| Goblin Drill | 84% | 170 | 68% |
| Goblin Demolisher | 84% | 162 | 65% |
| Golem | 83% | 183 | 64% |
| Vines | 80% | 148 | 67% |

## Least picked — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Lava Hound | 5% | 184 | 56% |
| Elixir Golem | 7% | 162 | 56% |
| Rage | 10% | 194 | 58% |
| Fisherman | 12% | 164 | 54% |
| Giant Snowball | 12% | 200 | 57% |
| Royal Giant | 17% | 174 | 55% |
| Ice Wizard | 18% | 156 | 63% |
| Elite Barbarians | 23% | 202 | 50% |
| Dark Prince | 23% | 149 | 58% |
| Ram Rider | 23% | 179 | 61% |

## What separates the top players from the field

Pick-rate gap on cards both groups saw enough of. A positive gap means the
tracked top players take it more often than the field does.

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Royal Hogs | 86% | 72% | **+14%** | +0.14 |
| Knight | 69% | 55% | **+14%** | +0.03 |
| Arrows | 76% | 63% | **+13%** | +0.11 |
| Vines | 80% | 69% | **+12%** | +0.25 |
| Poison | 87% | 75% | **+11%** | +0.21 |
| Goblin Drill | 84% | 73% | **+11%** | +0.34 |

Cards the top players avoid *more* than the field:

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Ice Wizard | 18% | 29% | **-11%** | -0.13 |
| Hunter | 32% | 43% | **-11%** | -0.20 |
| Dark Prince | 23% | 34% | **-12%** | -0.15 |
| Lava Hound | 5% | 17% | **-12%** | -0.28 |
| Elite Barbarians | 23% | 36% | **-14%** | -0.24 |
| X-Bow | 26% | 46% | **-20%** | -0.33 |

## Draft-style outliers among the tracked players

How far each player's pick rates sit from the tracked-group consensus.
Higher = more idiosyncratic. Needs 100+ decisions to mean much.

| Player | Decisions | Deviation from consensus | Draft edge | Win rate |
|---|---|---|---|---|
| Arrrr＿ | 124 | 0.218 | +0.109 | 42% |
| Reora. | 180 | 0.216 | +0.156 | 42% |
| 凛冬Rintou✨卤蛋 | 188 | 0.212 | +0.142 | 60% |
| RAIN | 148 | 0.205 | +0.156 | 57% |
| 23BS6N | 124 | 0.203 | +0.131 | 61% |
| Loris | 116 | 0.198 | +0.138 | 52% |
| OcT❤️Lev4ek | 124 | 0.194 | +0.179 | 74% |
| Sam❤️Rehwald | 120 | 0.187 | +0.210 | 67% |
| leon | 140 | 0.185 | +0.134 | 51% |
| MicinoCoccoloso | 192 | 0.180 | +0.129 | 46% |
| Dread Unlock | 136 | 0.180 | +0.142 | 41% |
| Batman | 188 | 0.179 | +0.148 | 53% |
| Aʀоmaτ❤ | 168 | 0.175 | +0.113 | 40% |
| SYX_OGtrooper | 176 | 0.174 | +0.138 | 57% |
| Asaf | 124 | 0.172 | +0.166 | 81% |
| Busfahrer Dirk | 136 | 0.169 | +0.173 | 76% |
| 5>Niko✨Drill | 136 | 0.165 | +0.157 | 47% |
| vicki£22 | 140 | 0.157 | +0.151 | 57% |
| Hazy | 120 | 0.152 | +0.180 | 73% |
| けーたいぷ✨ | 136 | 0.151 | +0.178 | 50% |
| 郁白❤️时光☪ | 136 | 0.148 | +0.180 | 65% |
| Tim f2p | 136 | 0.147 | +0.142 | 47% |
| =★The Star★= | 152 | 0.147 | +0.152 | 47% |
| Eurus | 120 | 0.139 | +0.134 | 87% |
| tiktok@kai_cr12 | 124 | 0.136 | +0.162 | 74% |
| カオス | 164 | 0.133 | +0.166 | 41% |
| ΨΨΨ | 124 | 0.125 | +0.157 | 48% |
| SK xopxsam | 536 | 0.115 | +0.184 | 86% |
| batan | 1052 | 0.091 | +0.158 | 68% |

## Draft skill: capture rate

Share of the strength that was actually on the table which the player took.
'Available' is near-identical for everyone, so this isolates decision quality
from luck of the draw. **Untracked field: 45.9%.**

| Player | Games | Win rate | Capture | Available | Won draft | Lost draft |
|---|---|---|---|---|---|---|
| Sam❤️Rehwald | 30 | 67% | **90.2%** | 0.233 | 84% (19) | 36% (11) |
| SK xopxsam | 134 | 86% | **84.0%** | 0.219 | 92% (89) | 73% (45) |
| けーたいぷ✨ | 34 | 50% | **79.3%** | 0.224 | 72% (18) | 25% (16) |
| Busfahrer Dirk | 34 | 76% | **77.1%** | 0.225 | 81% (26) | 62% (8) |
| OcT❤️Lev4ek | 31 | 74% | **74.5%** | 0.241 | 78% (23) | 62% (8) |
| カオス | 41 | 41% | **72.6%** | 0.228 | 40% (25) | 44% (16) |
| 郁白❤️时光☪ | 34 | 65% | **72.1%** | 0.250 | 70% (23) | 55% (11) |
| vicki£22 | 35 | 57% | **71.2%** | 0.211 | 82% (17) | 33% (18) |
| 5>Niko✨Drill | 34 | 47% | **70.9%** | 0.222 | 75% (20) | 7% (14) |
| Eurus | 30 | 87% | **70.5%** | 0.190 | 95% (19) | 73% (11) |
| ΨΨΨ | 31 | 48% | **69.8%** | 0.226 | 56% (18) | 38% (13) |
| batan | 263 | 68% | **68.1%** | 0.232 | 79% (152) | 53% (111) |
| Hazy | 30 | 73% | **68.1%** | 0.264 | 78% (23) | 57% (7) |
| Asaf | 31 | 81% | **68.0%** | 0.245 | 83% (18) | 77% (13) |
| Reora. | 45 | 42% | **67.2%** | 0.232 | 64% (22) | 22% (23) |
| Tim f2p | 34 | 47% | **67.1%** | 0.212 | 56% (16) | 39% (18) |
| =★The Star★= | 38 | 47% | **66.8%** | 0.227 | 58% (19) | 37% (19) |
| SYX_OGtrooper | 44 | 57% | **65.3%** | 0.211 | 71% (24) | 40% (20) |
| RAIN | 37 | 57% | **64.4%** | 0.242 | 71% (21) | 38% (16) |
| tiktok@kai_cr12 | 31 | 74% | **64.2%** | 0.252 | 83% (18) | 62% (13) |
| Batman | 47 | 53% | **63.8%** | 0.232 | 67% (21) | 42% (26) |
| MicinoCoccoloso | 48 | 46% | **63.2%** | 0.205 | 65% (23) | 28% (25) |
| leon | 35 | 51% | **62.4%** | 0.215 | 71% (14) | 38% (21) |
| Dread Unlock | 34 | 41% | **62.3%** | 0.228 | 60% (15) | 26% (19) |
| 凛冬Rintou✨卤蛋 | 47 | 60% | **60.8%** | 0.233 | 88% (25) | 27% (22) |
| Loris | 29 | 52% | **58.8%** | 0.235 | 79% (14) | 27% (15) |
| Aʀоmaτ❤ | 42 | 40% | **57.9%** | 0.195 | 60% (10) | 34% (32) |
| 23BS6N | 31 | 61% | **56.1%** | 0.233 | 70% (20) | 45% (11) |
| Arrrr＿ | 31 | 42% | **54.7%** | 0.199 | 73% (11) | 25% (20) |

## Tracked players

| Player | Games | Win rate |
|---|---|---|
| batan *(your account)* | 263 | 68% |
| SK xopxsam | 134 | 86% |
| MicinoCoccoloso | 48 | 46% |
| Batman | 47 | 53% |
| 凛冬Rintou✨卤蛋 | 47 | 60% |
| Reora. | 45 | 42% |
| SYX_OGtrooper | 44 | 57% |
| Aʀоmaτ❤ | 42 | 40% |
| カオス | 41 | 41% |
| =★The Star★= | 38 | 47% |
| RAIN | 37 | 57% |
| leon | 35 | 51% |
| vicki£22 | 35 | 57% |
| Busfahrer Dirk | 34 | 76% |
| けーたいぷ✨ | 34 | 50% |
| 郁白❤️时光☪ | 34 | 65% |
| Tim f2p | 34 | 47% |
| Dread Unlock | 34 | 41% |
| 5>Niko✨Drill | 34 | 47% |
| tiktok@kai_cr12 | 31 | 74% |
| OcT❤️Lev4ek | 31 | 74% |
| Asaf | 31 | 81% |
| Arrrr＿ | 31 | 42% |
| 23BS6N | 31 | 61% |
| ΨΨΨ | 31 | 48% |
| Eurus | 30 | 87% |
| Hazy | 30 | 73% |
| Sam❤️Rehwald | 30 | 67% |
| Loris | 29 | 52% |
| 老板 Ι Batan'宙斯 *(your account)* | 13 | 85% |
| イッシー | 9 | 44% |
| Golem | 8 | 50% |
| Metalfusion | 8 | 50% |
