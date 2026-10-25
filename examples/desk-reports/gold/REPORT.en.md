# Gold · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | AU |
| contract | AU_DEMO_202512 |
| currency | CNY |
| unit | CNY/gram |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 719 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 2.714285714285714285714285700 |
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
| metric | real_yield_pct |
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
| pct of future | 0.6954102920723226703755215577 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | AU_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | AU_DEMO_202512 |
| far | AU_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 5.640550146808839437490341461 |

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
| ceilings | {   "risk_budget": 12,   "margin_budget": 139,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "previous_volume" ] |
| planned loss per lot | 78.4330 |
| fees at stop per lot | 8.4330 |
| slippage per lot | 20 |
| initial margin per lot | 719.00 |
| planned loss total | 862.7630 |
| initial margin total | 7909.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 661.48 |
| stress loss | 6639.385280 |
| remaining equity | 993360.614720 |
| stress margin | 18190.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Separate USD gold, CNY gold and FX conversion before attributing a domestic move. Match quote times, mass units, fineness and tax/delivery scope.

A real-yield or dollar move is an explanatory hypothesis, not a deterministic gold signal. Align publication clocks and state the observation window.

A gold/silver ratio requires synchronized currencies and mass units. Ratio extremes alone do not demonstrate mean reversion.

Distinguish physical premium, exchange inventory, ETF holdings and central-bank announcements; their frequencies, revisions and coverage differ.

Falsify a shortage explanation if physical premia and deliverable supply fail to confirm it; keep geopolitical narratives separate from observed flows.

## Next evidence to check

Check official rate/FX releases and the same observation window.

Reconcile premium, warehouse and holdings evidence without double counting.

Recheck the effective contract and broker margin/fee notices before capacity arithmetic.

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
