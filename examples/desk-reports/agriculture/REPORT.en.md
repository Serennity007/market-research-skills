# Agricultural balances and crushing · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | M |
| contract | M_DEMO_202512 |
| currency | CNY |
| unit | CNY/tonne |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 3019 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 0.633333333333333333333333300 |
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
| metric | mill_inventory |
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
| pct of future | 0.1656177542232527326929446837 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | M_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | M_DEMO_202512 |
| far | M_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 1.343344006477494387398329233 |

Simple annualization excludes carry, financing, tax and roll execution; it is not an arbitrage return.

## Declared processing recipes

| Observation | Value |
|---|---|
| name | agriculture_illustrative_processing |
| status | calculated |
| value | 460.00 |
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
| ceilings | {   "risk_budget": 12,   "margin_budget": 33,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "previous_volume" ] |
| planned loss per lot | 83.0330 |
| fees at stop per lot | 13.0330 |
| slippage per lot | 20 |
| initial margin per lot | 3019.00 |
| planned loss total | 913.3630 |
| initial margin total | 33209.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 2777.48 |
| stress loss | 26927.961280 |
| remaining equity | 973072.038720 |
| stress margin | 76380.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Declare commodity, origin, quality and crop/marketing year before a supply-demand balance. Calendar-year totals and marketing-year totals cannot be silently combined.

A crush recipe must include meal/oil yields, moisture, input quality, FX, freight, tax and costs. Meal strength alone does not prove crush profitability.

Keep shipments, customs arrivals, port unloading, mill receipts and actual crushing separate; transit lead times can shift the apparent balance.

Match seasonal comparisons by crop phase or declared week key. Use only earlier years; weather anecdotes require acreage, timing and realized yield evidence.

Falsify a feed-demand recovery if offtake and comparable inventories diverge. Crop report revisions must enter only after their actual availability.

## Next evidence to check

Align marketing years, units and first-release/revision calendars.

Reconcile vessel arrivals, mill stocks, crushing and downstream offtake.

Stress both meal and oil yields/prices; retain origin and quality adjustments.

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
