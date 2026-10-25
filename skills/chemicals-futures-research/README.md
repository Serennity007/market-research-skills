[English](README.md) · [简体中文](README.zh-CN.md)

# Chemical processing chains

A self-contained research Skill for PTA/PX/polyester and other explicitly selected chemical chains, maintenance, utilization, inventories and declared processing spreads (化工、PTA、PX、聚酯). It combines domain guidance with an offline, publication-aware research desk. Python 3.10+, standard library only, MIT.

```bash
python scripts/run_desk.py run --config examples/desk-demo/chemicals/config.json --out output
python -m unittest discover -s tests -q
```

Every run produces **English and Chinese** HTML/Markdown, machine-readable calculations, source declarations, frozen inputs and exact SHA-256 manifests. Download the installable Skill from the [suite releases](https://github.com/Serennity007/taotao-futures-research/releases), extract its single Skill folder into your Skill directory, and restart the host to discover it. Other agents can read `SKILL.md` and run the same Python command.

Supports explicit daily session calendars, as-of revisions, basis, dated spreads, prior-only seasonal percentiles and versioned fee/margin stress arithmetic. Processing recipes use user-declared coefficients and costs. Source/installed packages keep the shared core version explicit.

[Skill entrypoint](SKILL.md) · [Research playbook](references/research-playbook.md) · [Input contract](docs/desk-data-contract.md) · [Capacity model](docs/desk-risk-model.md) · [Source policy](docs/desk-source-policy.md)

The bundled dataset, calendar, rule schedule and account are **synthetic**. No live data subscription, strategy backtest, order execution, guaranteed stop loss or portfolio risk model is included. A calculation passing its configured checks does not establish source authenticity or predictive validity.
