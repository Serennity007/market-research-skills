# Crude oil · Futures research desk

synthetic · 2025-09-26T09:00:00+00:00

SYNTHETIC EXAMPLE — constructed observations and hypothetical account/rule inputs; no historical performance.

Descriptive observations, evidence gaps and hypothetical capacity arithmetic. Source claims and file hashes do not authenticate market data. A stop is not a maximum-loss guarantee.

## Quality gates

Configured checks passed; completeness and predictive validity are not established.

Publication, availability and retrieval are separate clocks. Later data are excluded, not backfilled.

## Fixed-contract observations

| Observation | Value |
|---|---|
| product | SC |
| contract | SC_DEMO_202512 |
| currency | CNY |
| unit | CNY/barrel |
| trade date | 2025-09-26 |
| observed at | 2025-09-26T15:00:00+08:00 |
| available at | 2025-09-26T15:02:00+08:00 |
| close | 569 |
| observations | 20 |
| first trade date | 2025-09-01 |
| fixed contract change pct | 3.454545454545454545454545500 |
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
| metric | commercial_crude_inventory |
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
| pct of future | 0.8787346221441124780316344464 |
| scope | DEMO matching grade/location/tax/index definition; not a live quote |
| spot observed at | 2025-09-26T15:00:00+08:00 |
| contract | SC_DEMO_202512 |

## Dated spreads

| Observation | Value |
|---|---|
| status | calculated |

| Observation | Value |
|---|---|
| near | SC_DEMO_202512 |
| far | SC_DEMO_202603 |
| near minus far | -10 |
| delivery day gap | 90 |
| simple annualized far premium pct | 7.127514157391134544034368317 |

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
| ceilings | {   "risk_budget": 12,   "margin_budget": 175,   "user_cap": 100,   "previous_volume": 11 } |
| binding constraints | [   "previous_volume" ] |
| planned loss per lot | 78.1330 |
| fees at stop per lot | 8.1330 |
| slippage per lot | 20 |
| initial margin per lot | 569.00 |
| planned loss total | 859.4630 |
| initial margin total | 6259.00 |
| entry minus latest quote | 0 |
| model | single unencumbered position no netting |

| Observation | Value |
|---|---|
| name | hypothetical gap and margin increase |
| price | 523.48 |
| stress loss | 5316.217280 |
| remaining equity | 994683.782720 |
| stress margin | 14395.7000 |
| margin shortfall | 0 |

Calculated lots are an upper ceiling under the supplied assumptions, not an order suggestion.

The model covers one hypothetical position using unencumbered equity. It excludes portfolio correlation, margin offsets, broker add-ons and daily settlement cash paths. Gaps and margin increases can exceed the loss budget.

## Research questions and falsification

Do not splice SC, Brent and WTI levels: grade, currency, location, freight, tax and delivery terms differ.

Read dated spreads together with inventories, refinery runs and product demand; backwardation alone does not prove a physical shortage.

Separate crude, products, strategic stocks, floating storage and transit volumes; weekly changes need comparable coverage and revisions.

Trace an outage through lost production, export loadings, transit and refinery substitution. Announced cuts and realized exports are different evidence.

Falsify a demand-led explanation if refinery throughput and product stocks deteriorate despite stronger flat prices. Signed prices disable ordinary return ratios.

## Next evidence to check

Confirm benchmark and delivery scope of every curve point.

Compare the first published inventory release with later revisions.

Update freight, outage realization and product cracks using explicit conversion recipes.

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
