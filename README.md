# Market Research Skills

我的跨市场研究工具箱：**黄金、原油、欧线 EC、大 A 股指**。

四个独立仓库，每个都包含可直接读取的 Skill、研究方法、数据约定、离线计算、模拟样例和测试。本仓库只负责导航和登记，不需要把整个合集装进代理。

| 研究对象 | 独立仓库 | 主要问题 | 随带计算 |
| --- | --- | --- | --- |
| 黄金 | [gold-research-skill](https://github.com/Serennity007/gold-research-skill) | 利率美元与价格是否共振？关键位修复是否足够？ | 已收盘 MA/MACD、关键位观察、参考窗口 |
| 原油 | [crude-oil-research-skill](https://github.com/Serennity007/crude-oil-research-skill) | 供需与物流冲击是否落实到库存和期限结构？ | K 线结构、同基准跨月曲线、价差与时效 |
| 欧线 EC | [ec-shipping-research-skill](https://github.com/Serennity007/ec-shipping-research-skill) | 绕航如何传导到有效运力和已公布运价？ | K 线结构、按公布时间过滤的 SCFIS 对比 |
| 大 A 股指 | [a-share-index-research-skill](https://github.com/Serennity007/a-share-index-research-skill) | 指数上涨是否有市场宽度支持？大小盘风格如何？ | K 线结构、成分样本宽度与成交集中度 |

## 怎么选

- 只研究黄金 → 选择黄金仓库；金银联动用于辅助，不把白银当成相同资产。
- 研究 WTI/Brent/SC → 选择原油仓库；跨基准比较先解决币种、品质和交割差异。
- 研究 EC → 选择欧线仓库；区分 SCFIS、SCFI 和船司报价，核对合约月份与信息可见时间。
- 研究沪深300/上证50/中证500/中证1000与 IF/IH/IC/IM → 选择股指仓库。
- 研究多资产事件 → 分别调用对应 Skill，共用一个截止时间，再比较相互支持和矛盾的证据。不能把对 EC 的观点自动扩展为黄金或原油方向。

这些项目的重点是把研究变得可检查：信息何时可知、数据是什么、计算是否可复现、观点何时失效、复盘是否保留原记录。

## 下载与使用

每个项目的仓库根目录就是一个完整 Skill。可以单独 clone，直接在根目录运行 README 中的 Python 命令；只需 Python 3.10+ 标准库，无需账户、API Key 或其他仓库。

```bash
git clone https://github.com/Serennity007/gold-research-skill.git
cd gold-research-skill
python scripts/analyze_structure.py --csv examples/bars.csv --instrument GOLD_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00Z --data-kind synthetic --support 100 --out output/first-run.json
python -m unittest discover -s tests -v
```

要供代理调用，把需要的仓库完整放进该工具的技能目录，保留仓库名。例如 Codex 用户目录 `~/.codex/skills/`。不同代理的安装约定以其工具说明为准。

```text
使用 $gold-research-skill，标的 XAUUSD，截止时间……，数据来源……。
请区分已知事实、情景假设与缺失数据，给出关键位失效条件和下次复查点。
```

原油、欧线、股指分别使用 `$crude-oil-research-skill`、`$ec-shipping-research-skill`、`$a-share-index-research-skill`。

## 验证与证据等级

| 项目 | 当前随仓库提供 | 尚不能据此证明 |
| --- | --- | --- |
| 计算 | 本地运行的标准库脚本、单元测试、输入/输出 SHA-256 | 实时数据接入、交易执行能力 |
| 示例 | 全部明确标注 synthetic 的模拟样例 | 实盘记录、历史预测成功率 |
| 研究 | 各品种方法、官方入口、情景与复盘字段 | 策略有效性、收益或胜率 |
| 个人回顾 | 作者提供且标明证据限制的观点 | 缺少同期原始记录的已验证战绩 |

当前不内置网络取数、自动下单、实时监控和收益回测。真实数据可按各仓库约定导入，`imported_observations` 表示导入观测，不等于来源已认证。

## 导航自检

[registry.json](registry.json) 提供机器可读登记。以下检查不联网，适合验证目录和链接约定；带 `--local-root` 时，核对四个相邻本地仓库的技能名、入口及脚本存在性。

```bash
python scripts/validate_registry.py
python scripts/validate_registry.py --local-root ..
python -m unittest discover -s tests -v
```

## 相邻项目

[awesome-stock-quant-skills](https://github.com/Serennity007/awesome-stock-quant-skills) 是已有的个股选股与量化技能合集。它与这里的大 A 股指研究定位不同，可按具体任务搭配使用。

MIT · [Serennity007](https://github.com/Serennity007)

本地验证（2026-10-25）：黄金8项、原油17项、欧线18项、股指18项、导航4项测试通过；四个 Skill 入口结构与相邻仓库登记检查通过。共同 K 线引擎的测试在各仓库分别运行，不将其表述为65种独立研究能力。
