# Research suite qualification / 研究套件验证

[2026-10-30 export maintenance and five-repository recheck / 导出维护与五仓库复验](maintenance-2026-10-30.md)

This release upgrades the four existing specialists and adds four focused Skills. Its acceptance conditions concern calculation correctness, evidence timing, explicit assumptions and reproducible delivery. They do **not** concern investment returns or the performance of a trading strategy.

## Tested properties

- Hand-computed ATR, fixed-contract changes, basis, adjacent spreads, prior-only percentile, declared processing arithmetic, fees, slippage, whole-lot flooring and stress.
- Future publications excluded; later revisions enter only when available; equivalent UTC-offset timestamps identify the same event; duplicate vintages fail.
- Friday-night sessions do not complete Monday daily bars; missing completed sessions, overlapping sessions, mismatched daily closes and coverage horizons are detected.
- Contract rolls, currency/unit/scope contradictions, malformed CSV/JSON, booleans, nonfinite numbers, unzoned timestamps and unsafe file paths fail.
- Zero/boundary budgets, liquidity and margin ceilings, wrong-side/tick stops, expired or overlapping rules and missing close-today fees are covered.
- Both report languages, escaped HTML/Markdown, offline content policy, immutable raw snapshots, exact hash/file-set checks, tamper rejection, same-code replay and changed-code rejection are exercised.
- Installer checksum/catalog checks, traversal/duplicate rejection, identity checks and refusal to replace existing Skills are exercised.
- Existing sector and four specialist regression suites remain included. Original frozen workbench/source examples are preserved.

The release asset `QUALIFICATION.json` records the actual isolated archive test counts and CLI checks. Each specialist ZIP is extracted outside the checkout, tested using only its own contents, run from a different working directory, verified and replayed. Core manifests are checked against the bundled files. The master ZIP is tested separately. `SHA256SUMS.txt` covers the downloadable release artifacts, including that receipt. These are local qualification records, not hosted CI attestations or signed build provenance.

## Reproduce

```bash
python -m unittest discover -s tests -q
python tools/build_skill_suite.py --out output/my-new-release
```

The builder requires the four independently cloned specialist repositories beside this hub (or `--specialists-root`). It exports eight individual specialist ZIPs, the master ZIP and a combined suite. Core source/profile bytes originate in `desk_core` in this repository; specialists' `CORE-MANIFEST.json` makes their mirrored version explicit. Do not edit a specialist's core independently without resynchronizing and requalifying the suite. Frozen reports hash their producing core and require that exact release for replay.

Staging and ZIP writing exclude `.env`, `.env.*`, `.venv`, `venv`, `.git`, `node_modules`, `__pycache__`, `*.pyc`, `output` and `.DS_Store`. These filename exclusions do not scan for credentials embedded in other files.

## Evidence examples

- [Constructed ferrous report](../examples/desk-reports/ferrous/REPORT.en.md) / [中文](../examples/desk-reports/ferrous/REPORT.zh-CN.md)
- [Constructed chemical report](../examples/desk-reports/chemicals/REPORT.en.md)
- [Constructed agricultural report](../examples/desk-reports/agriculture/REPORT.en.md)
- [Recorded AU2612 snapshot study](../examples/desk-reports/gold-imported/REPORT.en.md), with [conversion provenance](../examples/desk-imported/gold/README.md).

The imported study uses a previously recorded Sina download, not a fresh retrieval or exchange-certified feed. Its initial publication version is unknown; the conservative first-seen timestamp prevents using it before retrieval. Missing sessions and fundamental evidence remain explicit. The eight synthetic reports use constructed prices, calendars, coefficients and rule/account inputs. No current live fee schedule or exchange calendar is claimed.

## Remaining boundaries

Tests establish specific program behavior; they do not establish source authenticity, historical availability beyond a declared archive, complete market coverage, predictive validity, practical fills, official contract eligibility or portfolio risk. Domain playbooks provide questions and falsification checks; they have not been independently benchmarked as an autonomous analyst. Runtime qualification was performed on Windows/Python 3.11; the standard-library source targets Python 3.10+ across platforms, but macOS/Linux runtimes have not been executed here.

## 中文

本次验证覆盖计算、数据公布版本、夜盘、缺失交易日、单位合约、费用保证金、压力情景、双语输出、哈希重跑及安装边界；保留原回归测试。发布附件 `QUALIFICATION.json` 记录实际解压测试数和运行结果。它是本地验证记录，不是托管 CI 签名证明。

真实导入演示复用先前记录的新浪快照，不冒充本次取数或交易所认证行情；首次发布与历史修订未知。其他演示均为构造数据。运行环境实际验证为 Windows／Python 3.11；代码面向 Python 3.10+，未在本次会话中执行 macOS／Linux。测试通过不能证明收益、实际成交或自动分析判断质量。
