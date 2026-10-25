# Chemical processing chains · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | TA |
| contract | TA_DEMO_202512 |
| currency | CNY |
| unit | CNY/tonne |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 5019 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 0.3800 |
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
| metric | plant_utilization |
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
| pct of future | 0.09962143853357242478581390715 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | TA_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | TA_DEMO_202512 |
| far | TA_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 0.8080405569945318899293794111 |

Simple annualization excludes carry, financing, tax and roll execution; it is not an arbitrage return.

## Declared processing recipes

| Observation | Value |
|---|---|
| name | chemicals_illustrative_processing |
| status | calculated |
| value | 1950.00 |
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
| ceilings | {   "risk_budget": 11,   "margin_budget": 19,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "risk_budget",   "previous_volume" ] |
| planned loss per lot | 87.0330 |
| fees at stop per lot | 17.0330 |
| slippage per lot | 20 |
| initial margin per lot | 5019.00 |
| planned loss total | 957.3630 |
| initial margin total | 55209.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 4617.48 |
| stress loss | 44570.201280 |
| remaining equity | 955429.798720 |
| stress margin | 126980.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Choose one chain first: PX/PTA/polyester, naphtha/olefins or coal/methanol. Their feedstock, co-product and capacity economics are not interchangeable.

A processing spread needs explicit conversion yield, currency, tax, freight, energy and fixed-cost scope. Declared coefficients are assumptions, not a full cash-profit statement.

Separate nameplate capacity, effective utilization and realized output. An announced maintenance schedule needs observed start, duration and restart evidence.

Reconcile upstream stocks with downstream order coverage and product inventories; avoid aggregating nested inventories as independent demand.

Falsify a margin-led restart thesis if cash constraints, feedstock availability or downstream demand prevent production despite a wider calculated spread.

## Next evidence to check

Validate feedstock/yield assumptions and test a range of energy/freight costs.

Compare announced outages with realized plant output.

Check product inventory days and downstream order duration using the same survey coverage.

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
