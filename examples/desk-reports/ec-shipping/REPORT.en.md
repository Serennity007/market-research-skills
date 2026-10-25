# Europe container freight · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | EC |
| contract | EC_DEMO_202512 |
| currency | CNY |
| unit | index_points |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 1519 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 1.266666666666666666666666700 |
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
| metric | settlement_index |
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
| pct of future | 0.3291639236339697169190256748 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | EC_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | EC_DEMO_202512 |
| far | EC_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 2.669885158364421037232096939 |

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
| ceilings | {   "risk_budget": 12,   "margin_budget": 65,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "previous_volume" ] |
| planned loss per lot | 80.0330 |
| fees at stop per lot | 10.0330 |
| slippage per lot | 20 |
| initial margin per lot | 1519.00 |
| planned loss total | 880.3630 |
| initial margin total | 16709.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 1397.48 |
| stress loss | 13696.281280 |
| remaining equity | 986303.718720 |
| stress margin | 38430.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Identify the exact published settlement-index series, covered route and release time. A spot booking quotation is not a settlement-index observation.

Compare futures points with the matching index definition and settlement window. A point premium is descriptive, not a cash-and-carry opportunity.

A rerouting scenario changes voyage duration and effective capacity only under stated fleet, speed, idle-time and demand assumptions; do not equate delay with lost cargo.

Separate announced blank sailings, realized sailings, booking demand and realized load factors. Avoid adding overlapping capacity reductions.

Falsify a disruption-led premium if effective capacity recovers or bookings weaken while futures remain elevated. Verify the latest official settlement rules separately.

## Next evidence to check

Verify the index provider&#x27;s publication calendar and observed release vintage.

Map contract expiry and the applicable settlement observation window from official notices.

Test rerouting and demand jointly; retain the original fleet denominator.

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
