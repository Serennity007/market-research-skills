---
name: nonferrous-futures-research
description: Research copper/aluminium and other base-metal supply chains, physical premiums, exchange stocks, warrants and declared import-cost assumptions (有色、铜、铝、仓单) using dated futures, publication-aware evidence, comparable basis/curves and reproducible bilingual reports. Use for supply-demand research and scenario review; not order execution, options pricing or a validated return forecast.
license: MIT
metadata:
  author: Serennity007
  version: "1.0.0"
---

# Nonferrous metals / 有色金属

Produce an evidence-based study in the user's language. Use supplied data or identify the exact missing evidence; the included demo is constructed and cannot stand in for current observations.

Read [the chain playbook](references/research-playbook.md) for the relevant mechanisms, contrary evidence and series definitions. For input preparation, publication/revision handling and interpretation boundaries, read [the desk contract](docs/desk-data-contract.md). Read [the capacity model](docs/desk-risk-model.md) only when budgets, sizing or margin stress are requested. Use [the source policy](docs/desk-source-policy.md) for official rule and provenance checks.

## Calculation entrypoint

Run from this Skill directory (or pass absolute script/config paths from elsewhere):

```bash
python scripts/run_desk.py run --config examples/desk-demo/nonferrous/config.json --out output --lang en
python scripts/run_desk.py verify output/desk-EXACT-RUN-DIRECTORY
python scripts/run_desk.py replay output/desk-EXACT-RUN-DIRECTORY --out output --lang zh-CN
```

Python 3.10+; no dependency installation. Every run writes English and Chinese HTML/Markdown, JSON, frozen inputs and a hashed completion manifest. The CLI is restricted to this profile. The source tree shares the hub's core; release/installed packages include their own identical versioned core.

Use exact dated contracts and offset-aware cutoffs. Daily bars must be complete; Friday night is not a completed Monday daily bar. Never replace missing historical availability with a current download timestamp presented as a past release. Revisions enter only when available. Split roll changes, units, grades, locations and coverage explicitly.

Treat processing coefficients and costs as declared assumptions. Report observed facts, hypotheses, contrary evidence, uncertainty and the next falsification check. Keep blocked calculations visible. A planned stop loss does not cap gap loss; hypothetical capacity covers one unencumbered position, not a portfolio. These tools do not place orders or validate predictive performance.
