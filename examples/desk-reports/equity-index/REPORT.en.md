# A-share index futures · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | IF |
| contract | IF_DEMO_202512 |
| currency | CNY |
| unit | index_points |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 4019 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 0.47500 |
| atr14 simple | 4 |
| previous trade date | 2025-09-25 |
| previous volume | 1180 |
| open interest change | 20 |

| Observation | Value |
|---|---|
| method | explicit sessions |
| latest completed trade date | 2025-09-26 |
| within coverage | True |

## Published fundamentals

| Observation | Value |
|---|---|
| metric | advancing_fraction |
| value | 105 |
| unit | declared_demo_units |
| observed at | 2025-09-26T10:00:00+08:00 |
| available at | 2025-09-26T12:05:00+08:00 |
| previous observed at | 2024-09-26T10:00:00+08:00 |
| change from previous observation | -5 |
| prior season samples | 4 |
| prior only percentile | 50.0 |

## Comparable basis

| Observation | Value |
|---|---|
| status | calculated |
| spot minus future | 5 |
| pct of future | 0.1244090569793480965414282160 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | IF_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | IF_DEMO_202512 |
| far | IF_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 1.009095684388045671947139844 |

Simple annualization excludes carry, financing, tax and roll execution; it is not an arbitrage return.

## Declared processing recipes

Not supplied / not calculable

## Hypothetical capacity and stress

| Observation | Value |
|---|---|
| status | calculated |
| spec version | SYNTHETIC-1 |
| spec source | synthetic://not-an-exchange-rule |
| currency | CNY |
| lots ceiling | 11 |
| ceilings | {   "risk_budget": 11,   "margin_budget": 24,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "risk_budget",   "previous_volume" ] |
| planned loss per lot | 85.0330 |
| fees at stop per lot | 15.0330 |
| slippage per lot | 20 |
| initial margin per lot | 4019.00 |
| planned loss total | 935.3630 |
| initial margin total | 44209.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 3697.48 |
| stress loss | 35749.081280 |
| remaining equity | 964250.918720 |
| stress margin | 101680.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Use an actual dated futures contract and its exact underlying index. A stock index level is not an executable futures quote.

Align spot/futures timestamps before basis. Financing, expected dividends and expiry matter; an annualized point discount is not a risk-free expected return.

Record breadth universe, constituent date, suspension treatment and coverage denominator. Survivorship-biased breadth can reverse an explanation.

Separate large/small-cap style and industry composition from broad market direction. Do not add total market turnover to overlapping subsets.

Falsify a broad recovery if index gains rely on a narrowing constituent set. Close-today costs and cash-settlement rules require dated official verification.

## Next evidence to check

Check dividend assumptions, expiry and quote synchronization.

Rebuild breadth with the as-of constituent universe and coverage denominator.

Confirm open/close/close-today fee schedules with effective dates.

## Source declarations

| Observation | Value |
|---|---|
| source | bars |
| name | Constructed example |
| policy | synthetic |

| Observation | Value |
|---|---|
| source | sessions |
| name | Constructed example |
| policy | synthetic |

| Observation | Value |
|---|---|
| source | fundamentals |
| name | Constructed example |
| policy | synthetic |

| Observation | Value |
|---|---|
| source | spot |
| name | Constructed example |
| policy | synthetic |

| Observation | Value |
|---|---|
| source | curve |
| name | Constructed example |
| policy | synthetic |

| Observation | Value |
|---|---|
| source | spec |
| name | Constructed example |
| policy | synthetic |

[JSON](bundle.json) · [English](REPORT.en.html) · [中文](REPORT.zh-CN.html)
