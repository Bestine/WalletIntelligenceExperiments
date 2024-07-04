## Summary of Analysis

| Attribute | Value |
|-----------|-------|
| Total Wallets Submitted | 1000 |
| Unique Wallets Analyzed | 1000 (Duplicates Removed: 0) |
| Normal Wallets (IsBot | False, Outbound Activity: True): 959 (95.90%) |
| Fresh Wallets (IsBot | False, Outbound Activity: False): 17 (1.70%) |
| Bot Wallets (IsBot | True): 24 (2.40%) |
## Wallet Metrics

|Metric                         | Median     | Average    | Min        | Max|
|---|---|---|---|---|
|Spend per Wallet               | $55        | $2,775     | $0         | $1,032,650|
|Balance per Wallet             | $6         | $33        | $0         | $11,949|
|Transaction Count per Wallet   | 144        | 228        | 0          | 7853|
|Spend Games per Wallet         | $0         | $42        | $0         | $21,982|
|Transaction Value              | $12        | N/A        | N/A        | N/A|
|Wallet Age (days)              | 552        | 518        | 66         | 2369|

## Bot Report

### IsBot: False

| Median Spend | $54 (Count: 976) |
| Median Transaction Count | 143 (Count: 976) |
### IsBot: True

| Median Spend | $525 (Count: 24) |
| Median Transaction Count | 322 (Count: 24) |
### Bot Behaviors

| Temporal Activity | 2 (8.33%) |
| Transaction Velocity | 0 (0.00%) |
| Continuous Engagement | 7 (29.17%) |
| Funding Network | 18 (75.00%) |
## Anomaly Detection

### Anomalies in Spend

|Wallet Address                             |          Spend|
|---|---|
|0xb2be9ab5fa90b084057943192a49c1647fe4b35a |     $1,032,650|
|0x119f37db41c88095f3a52572222c74499b7c7972 |       $528,636|
|0xf2881caed705571bc7eaad6ca8e126d88f17a237 |       $165,246|

### Anomalies in Total Balance

|Wallet Address                             |  Total Balance|
|---|---|
|0xc460d68c36beb93460c1651f77cf2372b19766e9 |        $11,949|
|0xf2881caed705571bc7eaad6ca8e126d88f17a237 |         $2,073|

## Top 10 Transaction Count, Non-Bots

|Wallet Address                             |    Transaction Count|
|---|---|
|0x8d5bb5aa462cd3a200c0010b66fde3b3c87cfca5 |                 7853|
|0x4168abe9065c3cc4415b1bceedc041cc12743724 |                 7309|
|0xef41421593f0211154665670ffb925c63243c3c6 |                 6745|
|0xbd680338b781ccbdaafdf25e902f54b4a4974600 |                 5785|
|0xc1545b0f9bd5882824aabe72bd322bd46c492f7e |                 5110|
|0xb429dace2e76a7542aa1f4d8ffbdc27e693c5b3c |                 3410|
|0xb4f0c739fa3c9fcb577b7002d8c292f2078fb14f |                 3084|
|0x5a8bf7fdc5be87012203233845dfe208e337529d |                 3066|
|0x1fa406da31eea33752481c526a249c06279fd9a5 |                 2701|
|0x988527874c7e3f02115f89a6a97135c70b6a47fc |                 2663|

## Oldest Wallets

|Wallet Address                             | Created At           | Days Old|
|---|---|---|
|0xad2dea1a2e4b068b33e1eb3850288a4c44c13d30 | 2017-12-31 23:25:48  |     2369|
|0xb4f0c739fa3c9fcb577b7002d8c292f2078fb14f | 2019-08-08 21:28:49  |     1784|
|0xefba6008c20dbc538081fdbc42b0d0c7e072d6f2 | 2019-08-22 20:15:10  |     1770|
|0xf900d6ecfb5702ce3e9e698d9a355223b15990a1 | 2019-10-11 12:56:28  |     1720|
|0xcea51cfee389c2c6bd7d6cfa47921932931230c9 | 2020-02-15 03:51:01  |     1594|
|0x6f3e91a50b8c381fd3de973da7d7adf70c5d748a | 2020-07-26 22:32:37  |     1431|
|0xca435d48fe79dcabf5e0ffe37d80bae1393d201b | 2020-09-28 23:25:40  |     1367|
|0x6eb0f29b8fc7a29e517ba56dd79287b3ccac64f3 | 2020-09-30 20:47:14  |     1365|
|0xc460d68c36beb93460c1651f77cf2372b19766e9 | 2020-10-07 08:42:20  |     1359|
|0x7ecdd06fd90ea3a81e6250f001e8ac459210246e | 2020-10-21 13:49:34  |     1344|

## Daily Transactions Leaderboard (Non-Bots, >10 Days Old)

|Wallet Address                             |   Daily Transactions |   Days Old|
|---|---|---|
|0xef41421593f0211154665670ffb925c63243c3c6 |                 8.86 |        761|
|0xbd680338b781ccbdaafdf25e902f54b4a4974600 |                 8.82 |        656|
|0x8d5bb5aa462cd3a200c0010b66fde3b3c87cfca5 |                 8.28 |        948|
|0x4168abe9065c3cc4415b1bceedc041cc12743724 |                 6.53 |       1119|
|0xb429dace2e76a7542aa1f4d8ffbdc27e693c5b3c |                 5.37 |        635|
|0xc1545b0f9bd5882824aabe72bd322bd46c492f7e |                 4.57 |       1119|
|0x5a8bf7fdc5be87012203233845dfe208e337529d |                 4.07 |        754|
|0x0357543c6ffde1cc28e13dbe8b6d3e8a3b372cb1 |                 3.01 |        502|
|0x6c4d39f9e53e4edcc4593defdc811fdf8bc52c30 |                 2.63 |        607|
|0x988527874c7e3f02115f89a6a97135c70b6a47fc |                 2.62 |       1016|
