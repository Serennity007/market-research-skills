![Market research workbench](.github/cover.svg)

# Market Research Skills

黄金、原油、欧线 EC、大 A 股指。四个独立研究 Skill，各自运行；也可以一条命令生成四份报告。

**Python 3.10+ · 标准库 · 离线报告 · 输入可复查 · MIT**

## 选一个开始

| Skill | 研究重点 | 本轮新增 | 直接看运行结果 |
|---|---|---|---|
| [黄金](https://github.com/Serennity007/gold-research-skill) | 利率美元、金银联动、多周期结构 | 共同日期的宏观对照、金银比、实际利率 bp 变化 | [模拟报告](https://github.com/Serennity007/gold-research-skill/blob/main/examples/workbench/REPORT.md) |
| [原油](https://github.com/Serennity007/crude-oil-research-skill) | 供需、运输冲击与期限结构 | 同一组合约的跨月价差变化，避免换月端点干扰 | [模拟报告](https://github.com/Serennity007/crude-oil-research-skill/blob/main/examples/workbench/REPORT.md) |
| [欧线 EC](https://github.com/Serennity007/ec-shipping-research-skill) | 航路、有效运力与已公布 SCFIS | 绕航周转、受影响运力和需求变化的情景测算 | [模拟报告](https://github.com/Serennity007/ec-shipping-research-skill/blob/main/examples/workbench/REPORT.md) |
| [大 A 股指](https://github.com/Serennity007/a-share-index-research-skill) | 指数结构、宽度与大小盘风格 | 四指数共同窗口收益、相对强弱和百分点差 | [模拟报告](https://github.com/Serennity007/a-share-index-research-skill/blob/main/examples/workbench/REPORT.md) |

每个仓库都是一个完整 Skill，有指令、方法、数据规范、计算脚本、示例和测试；不需要安装其余项目。本仓库负责导航、机器可读登记和多报告演示入口。

## 一次研究留下什么

输入 CSV 和带截止时间的配置，会得到：

- **HTML 研究面板**：关键观测、价格折线、信号分歧、缺失证据、下次检查和可展开计算明细。
- **Markdown + JSON**：方便写笔记，也方便其他程序读取。
- **冻结输入 + 重跑配置**：原始字节、来源声明和 SHA-256 随报告保存，重跑不依赖原文件位置。
- **明确完成状态**：全部导出完成才写 COMPLETE.json；重复运行保留旧快照。

报告使用本地字体与图形，无外部 JS、字体或行情请求；直接下载各仓库的 HTML 样例即可在浏览器打开。GitHub 文件页只展示 HTML 源码。

## 单独运行

以黄金为例，其余项目命令结构相同：

```bash
git clone https://github.com/Serennity007/gold-research-skill.git
cd gold-research-skill
python scripts/run_research.py --config examples/workbench.json --out output
python -m unittest discover -s tests -v
```

终端打印 REPORT.html 路径。每个仓库的 `references/workbench.md` 解释实际数据的导入方式、来源字段与计算口径。

## 一次运行四个

把五个仓库放在同一父目录，首次可这样准备：

```bash
git clone https://github.com/Serennity007/market-research-skills.git
git clone https://github.com/Serennity007/gold-research-skill.git
git clone https://github.com/Serennity007/crude-oil-research-skill.git
git clone https://github.com/Serennity007/ec-shipping-research-skill.git
git clone https://github.com/Serennity007/a-share-index-research-skill.git
cd market-research-skills
python scripts/run_all.py --local-root .. --out output
```

打开输出的 index.html，即可进入四份独立报告。运行器只执行已克隆仓库的 synthetic 示例，不联网下载数据、不替换安装，也不将四份报告合成交易评分。失败会保留 FAILURE.json，整次运行不会标记完成。

## 交给 Agent

完整仓库根目录就是技能目录，保留仓库名即可。Codex 可放进用户技能目录 `~/.codex/skills/`，其他工具按各自约定安装。

```text
使用 $gold-research-skill，标的是……，截止时间是……，数据来源是……。
运行研究工作台，说明价格与宏观证据的分歧，给出失效条件和下次检查事件。
```

[六个研究任务示例](docs/research-playbook.md) 覆盖盘前计划、事件研判、盘后复盘和跨市场对照。原油、欧线、股指的调用名分别是 `$crude-oil-research-skill`、`$ec-shipping-research-skill`、`$a-share-index-research-skill`。

## 验证范围

2026-10-25 本地通过：黄金 **17**、原油 **26**、欧线 **27**、股指 **27**、导航 **7** 项测试。另实际执行四仓库联合演示，核对生成入口与报告文件。共同引擎和工作台测试在各仓库分别执行，不将总测试数量当成独立研究能力或策略有效性。

测试覆盖计算算术、截止时间、公布时滞、合约对齐、部分样本、未来信息排除、输入冻结重跑、跨目录调用及 HTML 转义。示例全部标注 **synthetic 构造数据**；个人历史观点保留其原始证据等级。没有将示例包装成实盘经历、预测成功率或收益。

真实数据可按规范导入，来源字段必须填写；`imported_observations` 表示导入观测，不等于数据已经被工具认证。当前不内置实时取数、自动下单和收益回测。

## 导航与本地自检

[registry.json](registry.json) 登记技能名、仓库地址、版本、入口、脚本和演示配置。

```bash
python scripts/validate_registry.py
python scripts/validate_registry.py --local-root ..
python -m unittest discover -s tests -v
```

## 相邻项目

[awesome-stock-quant-skills](https://github.com/Serennity007/awesome-stock-quant-skills) 是已有个股选股与量化技能合集，可与股指/宏观研究配合使用。这里保留四个独立项目的边界。

MIT · [Serennity007](https://github.com/Serennity007)
