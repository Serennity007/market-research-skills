[English](README.md) · [简体中文](README.zh-CN.md)

![Futures research](.github/cover.svg)

# Futures Research Workbench

[Project navigator](https://github.com/Serennity007/repo-catalog) · [Maintenance check · 2026-10-30](docs/maintenance-2026-10-30.md)

<!-- futures-desk-v3 -->
## Eight specialist Skills · research desk v3.0

Gold, crude oil, Europe container freight, A-share index, ferrous, nonferrous, chemicals and agriculture now have focused research entrypoints and a shared, tested offline desk. Every new desk run emits **English and Chinese HTML/Markdown**, JSON, frozen inputs and SHA-256 manifests. Supports as-of revisions, explicit session calendars, comparable basis/curves, prior-only seasonality, declared processing recipes, Decimal fee/margin capacity and gap stress.

```bash
python scripts/run_desk.py run --config examples/desk-demo/ferrous/config.json --out output
python -m unittest discover -s tests -q
```

[Installable suite and individual Skill ZIPs](https://github.com/Serennity007/taotao-futures-research/releases) · [Eight-Skill catalog](suite.json) · [Input contract](docs/desk-data-contract.md) · [Risk model](docs/desk-risk-model.md) · [Evidence policy](docs/desk-source-policy.md)

Python 3.10+, no third-party dependencies for base commands. These are research Skills with runnable tools, not a desktop installer or validated trading strategy. All new fixtures use synthetic observations and fictional rules. Original eleven-sector commands, archived demonstrations and Chinese research references remain available below.


Compare sectors first, then study individual futures contracts. The workflow separates sector comparisons, industry evidence and price structure. Scripts compare fixed contracts over matching date windows and retain the inputs, commands and outputs needed to inspect or rerun the calculation.

[Language coverage](docs/LANGUAGES.md) · [Agent Skill](SKILL.md) · [MIT](LICENSE)

This is a source / Agent Skill project. The entry guides and release notes are bilingual; the original research instructions, reference notes and generated workbench reports currently retain Chinese text.

## Run the offline workbench

Python 3.10+ is required. Scripts use only the standard library.

```bash
git clone https://github.com/Serennity007/taotao-futures-research.git
cd taotao-futures-research
python scripts/run_sectors.py --config examples/sector-demo/config.json --out output
```

Open the printed `index.html` path. Filter sectors or product codes, change comparison windows and inspect the sector pages. Each run saves Markdown, JSON, CSV and its inputs in a new directory.

Inspect the [committed synthetic report](examples/sector-workbench/REPORT.md), follow the [hands-on checks](docs/sector-hands-on.md), or view the [11-sector screenshot](.github/sector-preview.jpg). The catalog contains 69 product identifiers; the demo selects 30 representative products across 11 research sectors. This is synthetic practice data, not a trading record.

## Fetch an explicit set of public daily observations

```bash
python scripts/fetch_sina.py --request examples/sina-request.json --out output/sources --analyze
```

The command requests only contracts explicitly listed in the request file, up to six per batch. Retrieval, raw-response preservation, normalization and report generation run in sequence. The default demo remains offline.

The recorded 2026-10-25 check retrieved 225, 184 and 183 daily observations for AU2612, RB2701 and M2701. Their latest common date was 2026-10-23. These are selected fixed contracts, not automatically identified as active front-month contracts. Raw responses, retrieval times, inputs and hashes are preserved in the [retrieval record](examples/real-source/VERIFICATION.md) and [snapshot report](examples/real-workbench/REPORT.md).

These are the historical versions visible at retrieval time. Every bar records `available_at`; data downloaded today must not be treated as if that version were known in the past. The retrieval day's bar is excluded, and the request declares daily closing times. See [public-data handling](docs/public-data.md).

![Three-contract retrieval snapshot](.github/source-preview.jpg)

## Check integrity and compare records

```bash
python scripts/bundle_integrity.py examples/sector-workbench
python scripts/bundle_integrity.py examples/real-source
python scripts/compare_reports.py --before examples/review-before --after examples/review-after --out output/reviews
```

Bundles include SHA-256 checks for inputs, configuration, pages and tables. Rerunning a frozen configuration first verifies it and rejects modified artifacts. Integrity checks establish file consistency, not source authenticity.

Comparisons use the same contract. Contract rolls, unit changes, different window starts and missing samples are reported separately. Changes to manually declared levels or reference bars remain in the record. The [synthetic review](examples/review-result/REVIEW.md) illustrates a condition that first meets a reclaim/retest observation and later reaches its invalidation level.

## Research sectors

| Sector | Catalog identifiers |
| --- | --- |
| [Precious metals](references/sectors/precious-metals.md) | AU, AG |
| [Nonferrous and new-energy materials](references/sectors/nonferrous.md) | CU, AL, ZN, PB, NI, SN, AO, BC, LC, SI |
| [Ferrous](references/sectors/ferrous.md) | RB, HC, I, J, JM, SF, SM, SS |
| [Energy](references/sectors/energy.md) | SC, FU, LU, PG, BU |
| [Chemicals](references/sectors/chemicals.md) | TA, MA, EG, EB, L, PP, V, PF, PX, SH, UR, FG, SA, RU, NR, BR, SP |
| [Oilseeds and oils](references/sectors/oilseeds.md) | A, B, M, Y, P, OI, RM, PK |
| [Grains and livestock](references/sectors/grains-livestock.md) | C, CS, RR, JD, LH |
| [Soft commodities and specialty agriculture](references/sectors/softs.md) | CF, CY, SR, AP, CJ |
| [Shipping](references/sectors/shipping.md) | EC |
| [Equity indices](references/sectors/equity-index.md) | IF, IH, IC, IM |
| [Rates](references/sectors/rates.md) | TS, TF, T, TL |

These are research groupings rather than an official exchange taxonomy. The catalog matches input identifiers; current listings, active contracts and trading rules require exchange documentation.

## What the reports retain

- **Sector comparisons:** equal-weight price changes over a common window, advance/decline counts and representative-product coverage. Missing data remains visible; ranking normally requires complete samples.
- **Individual products:** fixed-contract price changes, changes from the previous volume/open-interest observation, five-prior-bar volume comparisons and ATR14, including the prior observation date.
- **Price structure:** daily and H4/H1/M30 moving averages and MACD, manually supplied support/resistance, reference bars and expiry windows.
- **Industry evidence:** observation period, publication time, value, units and source. Versions published after the cutoff are excluded.
- **Calendar curves:** delivery-month comparisons, quote-time differences, currency and unit checks.

These are observations and calculations. Sector pages list supply, demand, inventory, cost and event evidence still to examine; disagreements between price and explanation remain explicit.

## Price-structure conditions

The [method](references/price-structure.md) records larger-timeframe context, H4 boundaries, H1/M30 triggers, reclaim/retest conditions, time windows and risk-budget inputs.

State observation conditions before evaluating closes and later retests. Declare the reference bar, verification window, tolerance and invalidation level in advance. The program distinguishes reclaims, later tests, expiry and invalidation; a reclaim bar cannot also count as its later retest. Retain the declaration time and source. A met observation condition does not establish a validated trading edge; position sizing additionally requires actual contract and cost information.

[Comparison conventions](references/sector-workflow.md) · [Event transmission](references/event-transmission.md) · [Data contract](references/data-contract.md) · [Rules and reviews](docs/rules-and-review.md) · [Official source entry points](references/sources.md)

## Supply your own inputs

Copy `examples/sector-demo/config.json`; select actual contracts in `universe` and declare common trading dates, windows, currencies and units. Set `data_kind` to `imported_observations` and record a source name and retrieval time for each file. This label identifies the input type, not its authenticity or historical version.

`panel.csv` supplies prices, volume and open interest. `evidence.csv` and `curves.csv` are optional. See the [hands-on input guide](docs/sector-hands-on.md).

## Use as an Agent Skill

The repository root is the Skill, with [SKILL.md](SKILL.md) as its entry. Copy the whole directory into your agent's skill location, keeping the name `taotao-futures-research`.

```text
Use $taotao-futures-research with my supplied data and explicit cutoff.
Check common windows and coverage, then inspect sector dispersion,
published industry evidence and multi-timeframe structure.
Save the report and explain observations, missing evidence, invalidation
conditions and the next review event in English.
```

An English response request does not automatically translate the script-generated research artifacts.

## Specialist repositories

[Gold](https://github.com/Serennity007/gold-research-skill) · [Crude oil](https://github.com/Serennity007/crude-oil-research-skill) · [EC shipping](https://github.com/Serennity007/ec-shipping-research-skill) · [A-share indices](https://github.com/Serennity007/a-share-index-research-skill)

Each retains specialist calculations and examples. The main workbench runs independently; the earlier four-report demo is documented in [the legacy guide](docs/four-specialists.md).

## Verify and rerun

```bash
python -m unittest discover -s tests -v
python scripts/run_sectors.py --config /path/to/previous-run/config.snapshot.json --out output
```

Replace the example path with a real saved run. Frozen inputs do not depend on their original locations. Tests cover common dates, missing observations, publication cutoffs, contract-roll separation and reruns.

[Research notes](docs/research-playbook.md) · [Stock and quant Skill collection](https://github.com/Serennity007/awesome-stock-quant-skills)

Research and learning only. Calculations and examples do not establish future returns. [Serennity007](https://github.com/Serennity007) · MIT
