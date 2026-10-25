# Ferrous supply chain · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | RB |
| contract | RB_DEMO_202512 |
| currency | CNY |
| unit | CNY/tonne |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 3219 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 0.5937500 |
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
| metric | hot_metal_output |
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
| pct of future | 0.1553277415346380863622242933 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | RB_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | RB_DEMO_202512 |
| far | RB_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 1.259880570225397811604708211 |

Simple annualization excludes carry, financing, tax and roll execution; it is not an arbitrage return.

## Declared processing recipes

| Observation | Value |
|---|---|
| name | ferrous_illustrative_processing |
| status | calculated |
| value | 300.0 |
| currency | CNY |
| output unit | tonne_of_declared_output_basis |
| assumption | CONSTRUCTED coefficients and costs, not plant economics / 构造收率与成本，不代表装置实际利润 |
| fixed cost per output | 100 |

## Hypothetical capacity and stress

| Observation | Value |
|---|---|
| status | calculated |
| spec version | SYNTHETIC-1 |
| spec source | synthetic://not-an-exchange-rule |
| currency | CNY |
| lots ceiling | 11 |
| ceilings | {   "risk_budget": 11,   "margin_budget": 31,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "risk_budget",   "previous_volume" ] |
| planned loss per lot | 83.4330 |
| fees at stop per lot | 13.4330 |
| slippage per lot | 20 |
| initial margin per lot | 3219.00 |
| planned loss total | 917.7630 |
| initial margin total | 35409.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 2961.48 |
| stress loss | 28692.185280 |
| remaining equity | 971307.814720 |
| stress margin | 81440.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Trace ore/coal/coke to hot metal, steel output and end-use demand. Blast-furnace and electric-arc routes require different costs and supply responses.

Reconcile mill and social inventories using non-overlapping coverage. Apparent consumption needs consistent production, imports, exports and stock changes.

A steel margin recipe must declare yields, ore/coke quality, wet/dry basis, tax, energy, transport and by-products. The example is not a universal furnace formula.

Match spot basis to location, grade, delivery eligibility and warehouse date; screen warehouse warrants separately from total inventory.

Falsify a demand recovery if shipments and comparable inventory drawdowns fail to confirm it; distinguish policy announcements from actual starts and purchases.

## Next evidence to check

Reconcile hot metal, furnace utilization and actual construction/manufacturing orders.

Audit inventory survey coverage changes and recipe sensitivities.

Check grade premiums, delivery rules and remaining contract liquidity.

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

| Observation | Value |
|---|---|
| source | prices |
| name | Constructed example |
| policy | synthetic |

[JSON](bundle.json) · [English](REPORT.en.html) · [中文](REPORT.zh-CN.html)
