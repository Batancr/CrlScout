# Chaos Draft tracker

- Unique battles archived: **3689**
- Tracked top players: **35**
- Draft decisions decoded: **29512**
- strength model fitted on 3689 battles, in-sample accuracy 63.7%.

## Most picked when offered — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Fireball | 89% | 217 | 66% |
| Poison | 89% | 193 | 64% |
| Goblin Barrel | 88% | 198 | 64% |
| Goblin Demolisher | 86% | 197 | 64% |
| Goblin Drill | 85% | 206 | 68% |
| Skeleton Army | 85% | 212 | 67% |
| Royal Hogs | 84% | 199 | 64% |
| Skeleton Barrel | 84% | 242 | 72% |
| Golem | 82% | 208 | 63% |
| Vines | 81% | 182 | 62% |

## Least picked — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Lava Hound | 6% | 213 | 57% |
| Elixir Golem | 8% | 203 | 56% |
| Rage | 10% | 231 | 58% |
| Giant Snowball | 12% | 228 | 58% |
| Fisherman | 13% | 195 | 53% |
| Royal Giant | 16% | 207 | 53% |
| Ice Wizard | 20% | 198 | 62% |
| Dark Prince | 22% | 187 | 53% |
| Elite Barbarians | 23% | 242 | 49% |
| Heal Spirit | 23% | 179 | 63% |

## What separates the top players from the field

Pick-rate gap on cards both groups saw enough of. A positive gap means the
tracked top players take it more often than the field does.

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Poison | 89% | 76% | **+12%** | +0.22 |
| Royal Hogs | 84% | 73% | **+12%** | +0.14 |
| Knight | 67% | 55% | **+12%** | +0.04 |
| Arrows | 75% | 64% | **+11%** | +0.12 |
| Vines | 81% | 70% | **+11%** | +0.19 |
| Goblin Drill | 85% | 74% | **+11%** | +0.36 |

Cards the top players avoid *more* than the field:

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Ram Rider | 24% | 33% | **-9%** | -0.17 |
| Lava Hound | 6% | 16% | **-10%** | -0.27 |
| Hunter | 31% | 41% | **-11%** | -0.19 |
| Dark Prince | 22% | 33% | **-11%** | -0.19 |
| Elite Barbarians | 23% | 36% | **-13%** | -0.23 |
| X-Bow | 31% | 46% | **-15%** | -0.34 |

## Draft-style outliers among the tracked players

How far each player's pick rates sit from the tracked-group consensus.
Higher = more idiosyncratic. Needs 100+ decisions to mean much.

| Player | Decisions | Deviation from consensus | Draft edge | Win rate |
|---|---|---|---|---|
| Loris | 124 | 0.229 | +0.134 | 55% |
| Reora. | 180 | 0.220 | +0.155 | 42% |
| 凛冬Rintou✨卤蛋 | 188 | 0.209 | +0.139 | 60% |
| RAIN | 148 | 0.206 | +0.154 | 57% |
| Arrrr＿ | 196 | 0.204 | +0.124 | 51% |
| 23BS6N | 124 | 0.198 | +0.128 | 61% |
| OcT❤️Lev4ek | 124 | 0.193 | +0.176 | 74% |
| Sam❤️Rehwald | 120 | 0.190 | +0.204 | 67% |
| Aʀоmaτ❤ | 296 | 0.185 | +0.112 | 49% |
| Golem | 132 | 0.184 | +0.153 | 55% |
| MicinoCoccoloso | 196 | 0.182 | +0.127 | 47% |
| Dread Unlock | 136 | 0.180 | +0.142 | 41% |
| Batman | 192 | 0.175 | +0.142 | 52% |
| Asaf | 124 | 0.175 | +0.161 | 81% |
| 5>Niko✨Drill | 140 | 0.172 | +0.154 | 49% |
| SYX_OGtrooper | 188 | 0.169 | +0.134 | 55% |
| リクルート | 192 | 0.164 | +0.183 | 48% |
| Busfahrer Dirk | 228 | 0.163 | +0.151 | 67% |
| vicki£22 | 140 | 0.158 | +0.147 | 57% |
| Metalfusion | 124 | 0.156 | +0.128 | 52% |
| Tim f2p | 172 | 0.155 | +0.124 | 47% |
| けーたいぷ✨ | 136 | 0.153 | +0.174 | 50% |
| leon | 340 | 0.151 | +0.127 | 53% |
| Hazy | 120 | 0.151 | +0.174 | 73% |
| 郁白❤️时光☪ | 136 | 0.147 | +0.176 | 65% |
| Eurus | 120 | 0.139 | +0.131 | 87% |
| tiktok@kai_cr12 | 124 | 0.133 | +0.163 | 74% |
| カオス | 216 | 0.129 | +0.162 | 50% |
| ΨΨΨ | 124 | 0.128 | +0.156 | 48% |
| SK xopxsam | 536 | 0.120 | +0.178 | 86% |
| =★The Star★= | 260 | 0.116 | +0.134 | 52% |
| batan | 1052 | 0.092 | +0.151 | 68% |

## Draft skill: capture rate

Share of the strength that was actually on the table which the player took.
'Available' is near-identical for everyone, so this isolates decision quality
from luck of the draw. **Untracked field: 46.5%.**

| Player | Games | Win rate | Capture | Available | Won draft | Lost draft |
|---|---|---|---|---|---|---|
| Sam❤️Rehwald | 30 | 67% | **89.9%** | 0.227 | 76% (21) | 44% (9) |
| SK xopxsam | 134 | 86% | **83.3%** | 0.213 | 92% (88) | 74% (46) |
| リクルート | 48 | 48% | **80.9%** | 0.226 | 57% (30) | 33% (18) |
| けーたいぷ✨ | 34 | 50% | **79.3%** | 0.219 | 78% (18) | 19% (16) |
| OcT❤️Lev4ek | 31 | 74% | **75.3%** | 0.233 | 78% (23) | 62% (8) |
| カオス | 54 | 50% | **74.1%** | 0.218 | 52% (33) | 48% (21) |
| Busfahrer Dirk | 57 | 67% | **73.9%** | 0.205 | 75% (36) | 52% (21) |
| 5>Niko✨Drill | 35 | 49% | **71.9%** | 0.214 | 79% (19) | 12% (16) |
| 郁白❤️时光☪ | 34 | 65% | **71.8%** | 0.244 | 70% (23) | 55% (11) |
| vicki£22 | 35 | 57% | **71.7%** | 0.205 | 79% (19) | 31% (16) |
| ΨΨΨ | 31 | 48% | **71.5%** | 0.219 | 56% (18) | 38% (13) |
| Eurus | 30 | 87% | **70.0%** | 0.187 | 94% (18) | 75% (12) |
| Asaf | 31 | 81% | **69.3%** | 0.232 | 83% (18) | 77% (13) |
| Reora. | 45 | 42% | **68.6%** | 0.226 | 67% (21) | 21% (24) |
| Hazy | 30 | 73% | **68.3%** | 0.255 | 77% (22) | 62% (8) |
| batan | 263 | 68% | **67.3%** | 0.225 | 79% (148) | 54% (115) |
| SYX_OGtrooper | 47 | 55% | **66.4%** | 0.201 | 74% (23) | 38% (24) |
| RAIN | 37 | 57% | **66.1%** | 0.232 | 73% (22) | 33% (15) |
| tiktok@kai_cr12 | 31 | 74% | **65.8%** | 0.247 | 75% (20) | 73% (11) |
| Metalfusion | 31 | 52% | **65.4%** | 0.195 | 70% (10) | 43% (21) |
| =★The Star★= | 65 | 52% | **64.7%** | 0.206 | 61% (31) | 44% (34) |
| Dread Unlock | 34 | 41% | **64.5%** | 0.220 | 64% (14) | 25% (20) |
| MicinoCoccoloso | 49 | 47% | **63.3%** | 0.201 | 67% (24) | 28% (25) |
| Batman | 48 | 52% | **62.9%** | 0.226 | 65% (23) | 40% (25) |
| Golem | 33 | 55% | **62.4%** | 0.244 | 63% (19) | 43% (14) |
| 凛冬Rintou✨卤蛋 | 47 | 60% | **61.8%** | 0.224 | 88% (26) | 24% (21) |
| Tim f2p | 43 | 47% | **60.4%** | 0.205 | 58% (19) | 38% (24) |
| Arrrr＿ | 49 | 51% | **59.8%** | 0.207 | 72% (18) | 39% (31) |
| Loris | 31 | 55% | **58.6%** | 0.229 | 86% (14) | 29% (17) |
| leon | 85 | 53% | **57.2%** | 0.222 | 67% (39) | 41% (46) |
| Aʀоmaτ❤ | 74 | 49% | **57.1%** | 0.195 | 57% (23) | 45% (51) |
| 23BS6N | 31 | 61% | **56.9%** | 0.225 | 74% (19) | 42% (12) |

## Tracked players

| Player | Games | Win rate |
|---|---|---|
| batan *(your account)* | 263 | 68% |
| SK xopxsam | 134 | 86% |
| leon | 85 | 53% |
| Aʀоmaτ❤ | 74 | 49% |
| =★The Star★= | 65 | 52% |
| Busfahrer Dirk | 57 | 67% |
| カオス | 54 | 50% |
| MicinoCoccoloso | 49 | 47% |
| Arrrr＿ | 49 | 51% |
| Batman | 48 | 52% |
| リクルート | 48 | 48% |
| SYX_OGtrooper | 47 | 55% |
| 凛冬Rintou✨卤蛋 | 47 | 60% |
| Reora. | 45 | 42% |
| Tim f2p | 43 | 47% |
| RAIN | 37 | 57% |
| vicki£22 | 35 | 57% |
| 5>Niko✨Drill | 35 | 49% |
| けーたいぷ✨ | 34 | 50% |
| 郁白❤️时光☪ | 34 | 65% |
| Dread Unlock | 34 | 41% |
| Golem | 33 | 55% |
| Loris | 31 | 55% |
| tiktok@kai_cr12 | 31 | 74% |
| OcT❤️Lev4ek | 31 | 74% |
| Asaf | 31 | 81% |
| Metalfusion | 31 | 52% |
| 23BS6N | 31 | 61% |
| ΨΨΨ | 31 | 48% |
| Eurus | 30 | 87% |
| Hazy | 30 | 73% |
| Sam❤️Rehwald | 30 | 67% |
| 老板 Ι Batan'宙斯 *(your account)* | 13 | 85% |
| イッシー | 10 | 40% |
| tarikzius | 4 | 50% |
