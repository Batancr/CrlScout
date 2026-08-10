# Chaos Draft tracker

- Unique battles archived: **3531**
- Tracked top players: **34**
- Draft decisions decoded: **28248**
- strength model fitted on 3531 battles, in-sample accuracy 63.8%.

## Most picked when offered — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Goblin Barrel | 90% | 171 | 65% |
| Fireball | 89% | 194 | 66% |
| Poison | 87% | 173 | 64% |
| Skeleton Army | 87% | 185 | 68% |
| Royal Hogs | 85% | 175 | 64% |
| Goblin Demolisher | 85% | 174 | 63% |
| Skeleton Barrel | 85% | 227 | 72% |
| Goblin Drill | 84% | 192 | 68% |
| Golem | 83% | 195 | 64% |
| Vines | 80% | 164 | 65% |

## Least picked — tracked top players

| Card | Pick rate | Offers | Win rate |
|---|---|---|---|
| Lava Hound | 5% | 191 | 56% |
| Elixir Golem | 7% | 182 | 55% |
| Rage | 10% | 205 | 59% |
| Giant Snowball | 12% | 211 | 57% |
| Fisherman | 13% | 174 | 53% |
| Royal Giant | 16% | 187 | 54% |
| Ice Wizard | 19% | 178 | 63% |
| Dark Prince | 22% | 164 | 55% |
| Elite Barbarians | 23% | 215 | 49% |
| Rune Giant | 24% | 177 | 58% |

## What separates the top players from the field

Pick-rate gap on cards both groups saw enough of. A positive gap means the
tracked top players take it more often than the field does.

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Knight | 68% | 55% | **+13%** | +0.04 |
| Royal Hogs | 85% | 72% | **+13%** | +0.14 |
| Poison | 87% | 76% | **+11%** | +0.20 |
| Arrows | 74% | 63% | **+11%** | +0.12 |
| Vines | 80% | 69% | **+11%** | +0.23 |
| Goblin Drill | 84% | 74% | **+11%** | +0.35 |

Cards the top players avoid *more* than the field:

| Card | Top | Field | Gap | Model strength |
|---|---|---|---|---|
| Flying Machine | 29% | 39% | **-10%** | -0.05 |
| Hunter | 32% | 42% | **-10%** | -0.22 |
| Dark Prince | 22% | 34% | **-12%** | -0.17 |
| Lava Hound | 5% | 17% | **-12%** | -0.27 |
| Elite Barbarians | 23% | 36% | **-13%** | -0.23 |
| X-Bow | 29% | 46% | **-18%** | -0.33 |

## Draft-style outliers among the tracked players

How far each player's pick rates sit from the tracked-group consensus.
Higher = more idiosyncratic. Needs 100+ decisions to mean much.

| Player | Decisions | Deviation from consensus | Draft edge | Win rate |
|---|---|---|---|---|
| Arrrr＿ | 124 | 0.222 | +0.107 | 42% |
| Reora. | 180 | 0.218 | +0.153 | 42% |
| 凛冬Rintou✨卤蛋 | 188 | 0.212 | +0.137 | 60% |
| RAIN | 148 | 0.205 | +0.155 | 57% |
| Loris | 116 | 0.202 | +0.134 | 52% |
| 23BS6N | 124 | 0.201 | +0.126 | 61% |
| OcT❤️Lev4ek | 124 | 0.191 | +0.177 | 74% |
| Sam❤️Rehwald | 120 | 0.190 | +0.207 | 67% |
| Golem | 132 | 0.181 | +0.153 | 55% |
| Aʀоmaτ❤ | 256 | 0.180 | +0.114 | 47% |
| MicinoCoccoloso | 192 | 0.180 | +0.127 | 46% |
| Dread Unlock | 136 | 0.178 | +0.140 | 41% |
| Batman | 192 | 0.176 | +0.144 | 52% |
| leon | 220 | 0.172 | +0.143 | 49% |
| Asaf | 124 | 0.171 | +0.161 | 81% |
| Busfahrer Dirk | 136 | 0.171 | +0.169 | 76% |
| SYX_OGtrooper | 184 | 0.169 | +0.135 | 57% |
| 5>Niko✨Drill | 140 | 0.167 | +0.155 | 49% |
| Metalfusion | 124 | 0.159 | +0.129 | 52% |
| vicki£22 | 140 | 0.156 | +0.149 | 57% |
| けーたいぷ✨ | 136 | 0.151 | +0.175 | 50% |
| Hazy | 120 | 0.150 | +0.177 | 73% |
| 郁白❤️时光☪ | 136 | 0.150 | +0.174 | 65% |
| =★The Star★= | 152 | 0.144 | +0.151 | 47% |
| Tim f2p | 136 | 0.142 | +0.141 | 47% |
| Eurus | 120 | 0.138 | +0.132 | 87% |
| tiktok@kai_cr12 | 124 | 0.134 | +0.160 | 74% |
| カオス | 200 | 0.130 | +0.168 | 46% |
| ΨΨΨ | 124 | 0.122 | +0.157 | 48% |
| SK xopxsam | 536 | 0.117 | +0.179 | 86% |
| batan | 1052 | 0.091 | +0.154 | 68% |

## Draft skill: capture rate

Share of the strength that was actually on the table which the player took.
'Available' is near-identical for everyone, so this isolates decision quality
from luck of the draw. **Untracked field: 46.4%.**

| Player | Games | Win rate | Capture | Available | Won draft | Lost draft |
|---|---|---|---|---|---|---|
| Sam❤️Rehwald | 30 | 67% | **90.3%** | 0.229 | 80% (20) | 40% (10) |
| SK xopxsam | 134 | 86% | **83.7%** | 0.214 | 91% (89) | 76% (45) |
| けーたいぷ✨ | 34 | 50% | **79.8%** | 0.220 | 88% (16) | 17% (18) |
| Busfahrer Dirk | 34 | 76% | **77.3%** | 0.218 | 84% (25) | 56% (9) |
| OcT❤️Lev4ek | 31 | 74% | **76.3%** | 0.232 | 78% (23) | 62% (8) |
| カオス | 50 | 46% | **74.7%** | 0.224 | 52% (31) | 37% (19) |
| 郁白❤️时光☪ | 34 | 65% | **71.6%** | 0.243 | 70% (23) | 55% (11) |
| vicki£22 | 35 | 57% | **71.6%** | 0.208 | 82% (17) | 33% (18) |
| 5>Niko✨Drill | 35 | 49% | **71.5%** | 0.217 | 76% (21) | 7% (14) |
| ΨΨΨ | 31 | 48% | **71.2%** | 0.221 | 59% (17) | 36% (14) |
| Eurus | 30 | 87% | **70.0%** | 0.188 | 95% (20) | 70% (10) |
| Hazy | 30 | 73% | **68.9%** | 0.257 | 77% (22) | 62% (8) |
| =★The Star★= | 38 | 47% | **68.5%** | 0.221 | 56% (18) | 40% (20) |
| Asaf | 31 | 81% | **68.4%** | 0.235 | 83% (18) | 77% (13) |
| batan | 263 | 68% | **67.7%** | 0.227 | 79% (149) | 54% (114) |
| Tim f2p | 34 | 47% | **67.5%** | 0.209 | 56% (16) | 39% (18) |
| Reora. | 45 | 42% | **67.2%** | 0.227 | 64% (22) | 22% (23) |
| Metalfusion | 31 | 52% | **66.1%** | 0.196 | 67% (12) | 42% (19) |
| SYX_OGtrooper | 46 | 57% | **65.7%** | 0.205 | 70% (23) | 43% (23) |
| RAIN | 37 | 57% | **65.3%** | 0.237 | 70% (20) | 41% (17) |
| tiktok@kai_cr12 | 31 | 74% | **64.4%** | 0.248 | 83% (18) | 62% (13) |
| leon | 55 | 49% | **63.8%** | 0.225 | 55% (22) | 45% (33) |
| MicinoCoccoloso | 48 | 46% | **63.7%** | 0.200 | 65% (23) | 28% (25) |
| Batman | 48 | 52% | **62.9%** | 0.228 | 64% (22) | 42% (26) |
| Dread Unlock | 34 | 41% | **62.9%** | 0.223 | 60% (15) | 26% (19) |
| Golem | 33 | 55% | **61.8%** | 0.248 | 63% (19) | 43% (14) |
| 凛冬Rintou✨卤蛋 | 47 | 60% | **61.2%** | 0.224 | 88% (25) | 27% (22) |
| Aʀоmaτ❤ | 64 | 47% | **58.1%** | 0.197 | 53% (17) | 45% (47) |
| Loris | 29 | 52% | **57.8%** | 0.232 | 79% (14) | 27% (15) |
| 23BS6N | 31 | 61% | **55.7%** | 0.226 | 68% (19) | 50% (12) |
| Arrrr＿ | 31 | 42% | **55.2%** | 0.193 | 73% (11) | 25% (20) |

## Tracked players

| Player | Games | Win rate |
|---|---|---|
| batan *(your account)* | 263 | 68% |
| SK xopxsam | 134 | 86% |
| Aʀоmaτ❤ | 64 | 47% |
| leon | 55 | 49% |
| カオス | 50 | 46% |
| Batman | 48 | 52% |
| MicinoCoccoloso | 48 | 46% |
| 凛冬Rintou✨卤蛋 | 47 | 60% |
| SYX_OGtrooper | 46 | 57% |
| Reora. | 45 | 42% |
| =★The Star★= | 38 | 47% |
| RAIN | 37 | 57% |
| vicki£22 | 35 | 57% |
| 5>Niko✨Drill | 35 | 49% |
| Busfahrer Dirk | 34 | 76% |
| けーたいぷ✨ | 34 | 50% |
| 郁白❤️时光☪ | 34 | 65% |
| Tim f2p | 34 | 47% |
| Dread Unlock | 34 | 41% |
| Golem | 33 | 55% |
| tiktok@kai_cr12 | 31 | 74% |
| OcT❤️Lev4ek | 31 | 74% |
| Asaf | 31 | 81% |
| Metalfusion | 31 | 52% |
| Arrrr＿ | 31 | 42% |
| 23BS6N | 31 | 61% |
| ΨΨΨ | 31 | 48% |
| Eurus | 30 | 87% |
| Hazy | 30 | 73% |
| Sam❤️Rehwald | 30 | 67% |
| Loris | 29 | 52% |
| 老板 Ι Batan'宙斯 *(your account)* | 13 | 85% |
| リクルート | 11 | 18% |
| イッシー | 10 | 40% |
