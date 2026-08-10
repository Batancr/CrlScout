# Chaos Draft tracker

- Unique battles archived: **3617**
- Tracked top players: **34**
- Draft decisions decoded: **28936**
- strength model fitted on 3617 battles, in-sample accuracy 63.7%.

## Most picked when offered — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Fireball | 89% | 205 | 66% |
| Poison | 88% | 184 | 64% |
| Goblin Barrel | 88% | 189 | 65% |
| Goblin Demolisher | 85% | 186 | 63% |
| Skeleton Army | 85% | 201 | 68% |
| Skeleton Barrel | 84% | 236 | 71% |
| Goblin Drill | 84% | 197 | 68% |
| Royal Hogs | 84% | 185 | 65% |
| Golem | 83% | 201 | 63% |
| Vines | 80% | 174 | 63% |

## Least picked — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Lava Hound | 5% | 204 | 56% |
| Elixir Golem | 8% | 192 | 56% |
| Rage | 10% | 216 | 59% |
| Giant Snowball | 12% | 217 | 58% |
| Fisherman | 12% | 184 | 54% |
| Royal Giant | 17% | 196 | 54% |
| Ice Wizard | 20% | 193 | 62% |
| Dark Prince | 22% | 179 | 54% |
| Rune Giant | 22% | 187 | 57% |
| Elite Barbarians | 23% | 230 | 49% |

## What separates the top players from the field

Pick-rate gap on cards both groups saw enough of. A positive gap means the
tracked top players take it more often than the field does.

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Knight | 68% | 55% | **+13%** | +0.04 |
| Poison | 88% | 76% | **+12%** | +0.21 |
| Royal Hogs | 84% | 72% | **+12%** | +0.15 |
| Arrows | 75% | 63% | **+11%** | +0.12 |
| Goblin Drill | 84% | 74% | **+10%** | +0.36 |
| Goblin Hut | 76% | 66% | **+10%** | +0.13 |

Cards the top players avoid *more* than the field:

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Ram Rider | 24% | 33% | **-9%** | -0.16 |
| Hunter | 31% | 41% | **-11%** | -0.20 |
| Dark Prince | 22% | 33% | **-11%** | -0.18 |
| Lava Hound | 5% | 16% | **-11%** | -0.28 |
| Elite Barbarians | 23% | 36% | **-13%** | -0.22 |
| X-Bow | 30% | 46% | **-16%** | -0.32 |

## Draft-style outliers among the tracked players

How far each player's pick rates sit from the tracked-group consensus.
Higher = more idiosyncratic. Needs 100+ decisions to mean much.

| Player | Decisions | Deviation from consensus | Draft edge | Win rate |
|---|---|---|---|---|
| Reora. | 180 | 0.220 | +0.153 | 42% |
| Arrrr＿ | 144 | 0.218 | +0.099 | 44% |
| 凛冬Rintou✨卤蛋 | 188 | 0.210 | +0.138 | 60% |
| RAIN | 148 | 0.207 | +0.155 | 57% |
| 23BS6N | 124 | 0.199 | +0.129 | 61% |
| Loris | 116 | 0.199 | +0.129 | 52% |
| OcT❤️Lev4ek | 124 | 0.193 | +0.175 | 74% |
| Sam❤️Rehwald | 120 | 0.189 | +0.204 | 67% |
| Aʀоmaτ❤ | 296 | 0.183 | +0.115 | 49% |
| MicinoCoccoloso | 196 | 0.182 | +0.129 | 47% |
| Golem | 132 | 0.181 | +0.153 | 55% |
| Dread Unlock | 136 | 0.180 | +0.139 | 41% |
| Batman | 192 | 0.176 | +0.142 | 52% |
| Busfahrer Dirk | 168 | 0.173 | +0.157 | 74% |
| Asaf | 124 | 0.173 | +0.160 | 81% |
| 5>Niko✨Drill | 140 | 0.171 | +0.154 | 49% |
| SYX_OGtrooper | 188 | 0.169 | +0.134 | 55% |
| リクルート | 152 | 0.168 | +0.184 | 45% |
| vicki£22 | 140 | 0.157 | +0.147 | 57% |
| Metalfusion | 124 | 0.155 | +0.128 | 52% |
| けーたいぷ✨ | 136 | 0.153 | +0.174 | 50% |
| leon | 340 | 0.153 | +0.127 | 53% |
| Hazy | 120 | 0.152 | +0.175 | 73% |
| 郁白❤️时光☪ | 136 | 0.150 | +0.175 | 65% |
| Tim f2p | 152 | 0.148 | +0.128 | 45% |
| =★The Star★= | 160 | 0.148 | +0.148 | 50% |
| Eurus | 120 | 0.139 | +0.131 | 87% |
| tiktok@kai_cr12 | 124 | 0.136 | +0.162 | 74% |
| カオス | 200 | 0.130 | +0.167 | 46% |
| ΨΨΨ | 124 | 0.126 | +0.156 | 48% |
| SK xopxsam | 536 | 0.118 | +0.178 | 86% |
| batan | 1052 | 0.091 | +0.152 | 68% |

## Draft skill: capture rate

Share of the strength that was actually on the table which the player took.
'Available' is near-identical for everyone, so this isolates decision quality
from luck of the draw. **Untracked field: 46.8%.**

| Player | Games | Win rate | Capture | Available | Won draft | Lost draft |
|---|---|---|---|---|---|---|
| Sam❤️Rehwald | 30 | 67% | **89.9%** | 0.227 | 76% (21) | 44% (9) |
| SK xopxsam | 134 | 86% | **83.6%** | 0.212 | 92% (86) | 75% (48) |
| リクルート | 38 | 45% | **82.7%** | 0.223 | 54% (26) | 25% (12) |
| けーたいぷ✨ | 34 | 50% | **79.3%** | 0.220 | 82% (17) | 18% (17) |
| Busfahrer Dirk | 42 | 74% | **76.0%** | 0.206 | 82% (28) | 57% (14) |
| OcT❤️Lev4ek | 31 | 74% | **75.5%** | 0.232 | 78% (23) | 62% (8) |
| カオス | 50 | 46% | **75.0%** | 0.223 | 50% (32) | 39% (18) |
| 5>Niko✨Drill | 35 | 49% | **71.9%** | 0.214 | 76% (21) | 7% (14) |
| vicki£22 | 35 | 57% | **71.9%** | 0.205 | 83% (18) | 29% (17) |
| 郁白❤️时光☪ | 34 | 65% | **71.4%** | 0.244 | 70% (23) | 55% (11) |
| ΨΨΨ | 31 | 48% | **71.4%** | 0.219 | 59% (17) | 36% (14) |
| Eurus | 30 | 87% | **70.7%** | 0.185 | 94% (17) | 77% (13) |
| Asaf | 31 | 81% | **69.1%** | 0.232 | 83% (18) | 77% (13) |
| Hazy | 30 | 73% | **68.8%** | 0.255 | 77% (22) | 62% (8) |
| =★The Star★= | 40 | 50% | **68.6%** | 0.215 | 58% (19) | 43% (21) |
| Reora. | 45 | 42% | **68.0%** | 0.226 | 67% (21) | 21% (24) |
| batan | 263 | 68% | **67.7%** | 0.225 | 79% (147) | 54% (116) |
| RAIN | 37 | 57% | **66.7%** | 0.233 | 71% (21) | 38% (16) |
| SYX_OGtrooper | 47 | 55% | **66.5%** | 0.201 | 71% (24) | 39% (23) |
| tiktok@kai_cr12 | 31 | 74% | **65.9%** | 0.246 | 76% (21) | 70% (10) |
| Metalfusion | 31 | 52% | **65.5%** | 0.195 | 64% (11) | 45% (20) |
| MicinoCoccoloso | 49 | 47% | **64.5%** | 0.200 | 67% (24) | 28% (25) |
| Dread Unlock | 34 | 41% | **63.3%** | 0.219 | 64% (14) | 25% (20) |
| Golem | 33 | 55% | **62.7%** | 0.244 | 61% (18) | 47% (15) |
| Batman | 48 | 52% | **62.6%** | 0.227 | 67% (24) | 38% (24) |
| 凛冬Rintou✨卤蛋 | 47 | 60% | **62.1%** | 0.223 | 88% (24) | 30% (23) |
| Tim f2p | 38 | 45% | **61.5%** | 0.208 | 53% (17) | 38% (21) |
| Aʀоmaτ❤ | 74 | 49% | **58.8%** | 0.195 | 57% (23) | 45% (51) |
| 23BS6N | 31 | 61% | **57.7%** | 0.223 | 70% (20) | 45% (11) |
| leon | 85 | 53% | **57.3%** | 0.222 | 66% (38) | 43% (47) |
| Loris | 29 | 52% | **56.3%** | 0.230 | 85% (13) | 25% (16) |
| Arrrr＿ | 36 | 44% | **52.0%** | 0.190 | 62% (13) | 35% (23) |

## Tracked players

| Player | Games | Win rate |
|---|---|---|
| batan *(your account)* | 263 | 68% |
| SK xopxsam | 134 | 86% |
| leon | 85 | 53% |
| Aʀоmaτ❤ | 74 | 49% |
| カオス | 50 | 46% |
| MicinoCoccoloso | 49 | 47% |
| Batman | 48 | 52% |
| SYX_OGtrooper | 47 | 55% |
| 凛冬Rintou✨卤蛋 | 47 | 60% |
| Reora. | 45 | 42% |
| Busfahrer Dirk | 42 | 74% |
| =★The Star★= | 40 | 50% |
| リクルート | 38 | 45% |
| Tim f2p | 38 | 45% |
| RAIN | 37 | 57% |
| Arrrr＿ | 36 | 44% |
| vicki£22 | 35 | 57% |
| 5>Niko✨Drill | 35 | 49% |
| けーたいぷ✨ | 34 | 50% |
| 郁白❤️时光☪ | 34 | 65% |
| Dread Unlock | 34 | 41% |
| Golem | 33 | 55% |
| tiktok@kai_cr12 | 31 | 74% |
| OcT❤️Lev4ek | 31 | 74% |
| Asaf | 31 | 81% |
| Metalfusion | 31 | 52% |
| 23BS6N | 31 | 61% |
| ΨΨΨ | 31 | 48% |
| Eurus | 30 | 87% |
| Hazy | 30 | 73% |
| Sam❤️Rehwald | 30 | 67% |
| Loris | 29 | 52% |
| 老板 Ι Batan'宙斯 *(your account)* | 13 | 85% |
| イッシー | 10 | 40% |
