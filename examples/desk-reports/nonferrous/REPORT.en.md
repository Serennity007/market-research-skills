# Nonferrous metals · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | CU |
| contract | CU_DEMO_202512 |
| currency | CNY |
| unit | CNY/tonne |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 78019 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 0.024358974358974358974359000 |
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
| metric | exchange_inventory |
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
| pct of future | 0.006408695317807200810059088171 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | CU_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | CU_DEMO_202512 |
| far | CU_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 0.051981639799991739903812700 |

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
| lots ceiling | 1 |
| ceilings | {   "risk_budget": 4,   "margin_budget": 1,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "margin_budget" ] |
| planned loss per lot | 233.0330 |
| fees at stop per lot | 163.0330 |
| slippage per lot | 20 |
| initial margin per lot | 78019.00 |
| planned loss total | 233.0330 |
| initial margin total | 78019.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 71777.48 |
| stress loss | 62591.996480 |
| remaining equity | 937408.003520 |
| stress margin | 179443.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Separate mine supply, concentrate treatment charges, smelter output and fabricated demand; tight concentrate does not immediately equal tight refined metal.

Inventory comparisons require exchange/warehouse geography, bonded status and warrant eligibility. Cancelled warrants and warehouse stock are not independent additive supplies.

An import comparison needs synchronized FX, tax, freight, grade and location. A raw domestic/overseas price ratio is not an executable import margin.

Physical premium, near/far spread and inventory draw should confirm the same location and period before inferring shortage.

Falsify a demand-led rally if downstream utilization and premia weaken; distinguish supply maintenance from permanent capacity closures.

## Next evidence to check

Reconcile exchange stocks with warrants using documented inclusion rules.

Check smelter maintenance, concentrate availability and downstream orders.

Rebuild landed-cost assumptions before interpreting cross-market spreads.

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
