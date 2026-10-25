[English](README.md) · [简体中文](README.zh-CN.md)

# Agricultural balances and crushing

A self-contained research Skill for oilseeds, meal/oil crushing and declared agricultural balances, crop-year seasonality, arrivals and inventories (农产品、豆粕、豆油、压榨、作物年度). It combines domain guidance with an offline, publication-aware research desk. Python 3.10+, standard library only, MIT.

```bash
python scripts/run_desk.py run --config examples/desk-demo/agriculture/config.json --out output
python -m unittest discover -s tests -q
```

Every run produces **English and Chinese** HTML/Markdown, machine-readable calculations, source declarations, frozen inputs and exact SHA-256 manifests. Download the installable Skill from the [suite releases](https://github.com/Serennity007/taotao-futures-research/releases), extract its single Skill folder into your Skill directory, and restart the host to discover it. Other agents can read `SKILL.md` and run the same Python command.

Supports explicit daily session calendars, as-of revisions, basis, dated spreads, prior-only seasonal percentiles and versioned fee/margin stress arithmetic. Processing recipes use user-declared coefficients and costs. Source/installed packages keep the shared core version explicit.

[Skill entrypoint](SKILL.md) · [Research playbook](references/research-playbook.md) · [Input contract](docs/desk-data-contract.md) · [Capacity model](docs/desk-risk-model.md) · [Source policy](docs/desk-source-policy.md)

The bundled dataset, calendar, rule schedule and account are **synthetic**. No live data subscription, strategy backtest, order execution, guaranteed stop loss or portfolio risk model is included. A calculation passing its configured checks does not establish source authenticity or predictive validity.
