![涛涛的期货研究](.github/cover.svg)

# 涛涛的期货研究

可读懂、可复现的期货研究实操。

这里放我整理的黄金、原油、欧线 EC 和大 A 股指研究方法。每个例子都有输入文件、运行命令和计算结果，照着做就能核对。练习用的是仓库自带的模拟数据；跑通后，可以换成自己的 CSV。

## 四个仓库

| 品种 | 仓库 | 里面的实操 |
|---|---|---|
| 黄金 | [黄金研究](https://github.com/Serennity007/gold-research-skill) | 看支撑收复、算金银比，对照美元和实际利率 |
| 原油 | [原油研究](https://github.com/Serennity007/crude-oil-research-skill) | 比较两天的跨月价差，核对是不是换了合约 |
| 欧线 EC | [欧线研究](https://github.com/Serennity007/ec-shipping-research-skill) | 区分已公布运价和期价，算绕航、货量变化对运力压力的影响 |
| 大 A 股指 | [股指研究](https://github.com/Serennity007/a-share-index-research-skill) | 比较大小盘表现，检查上涨家数、样本覆盖和成交集中度 |

每个仓库可以单独用，Python 3.10 及以上版本即可，脚本只用标准库。

## 先跑一个例子

以黄金为例：

```bash
git clone https://github.com/Serennity007/gold-research-skill.git
cd gold-research-skill
python scripts/run_research.py --config examples/workbench.json --out output
```

终端会打印 `REPORT.html` 的位置，用浏览器打开。你会看到价格图、计算值、还缺哪些资料，以及下一次要检查什么。每次运行会新建一个目录，方便保留前后两次记录。

这个例子里，收盘价从98回到102，收复了人工设定的100，但均线仍向下排列。读结果时要把“收复了一个位置”和“趋势已经转向”分开。

[四个例子的操作步骤与手算过程](docs/hands-on.md) 写了每项输入在哪里、会算出什么、该怎么解释。已有运行结果也能直接看：

[黄金](https://github.com/Serennity007/gold-research-skill/blob/main/examples/workbench/REPORT.md) · [原油](https://github.com/Serennity007/crude-oil-research-skill/blob/main/examples/workbench/REPORT.md) · [欧线](https://github.com/Serennity007/ec-shipping-research-skill/blob/main/examples/workbench/REPORT.md) · [股指](https://github.com/Serennity007/a-share-index-research-skill/blob/main/examples/workbench/REPORT.md)

## 四个一起跑

把这五个仓库放在同一个目录下：

```bash
git clone https://github.com/Serennity007/taotao-futures-research.git
git clone https://github.com/Serennity007/gold-research-skill.git
git clone https://github.com/Serennity007/crude-oil-research-skill.git
git clone https://github.com/Serennity007/ec-shipping-research-skill.git
git clone https://github.com/Serennity007/a-share-index-research-skill.git
cd taotao-futures-research
python scripts/run_all.py --local-root .. --out output
```

打开终端打印的 `index.html`，从里面进入各品种报告。已经下载过的仓库可以继续用，更新到最新版本即可。

## 换成自己的数据

先复制所选仓库的 `examples/workbench.json`，再修改标的、截止时间和 CSV 路径。导入观测时，把 `data_kind` 改为 `imported_observations`，为每个文件填写来源名称与取数时间。

各仓库的 `references/workbench.md` 列了字段格式。K 线时间填收盘时间；利率按百分数输入；欧线要填写运价公布时间；股指样本要说明完整成分数量。这些地方填错，结果也会跟着错。

## 留下计算和复盘记录

报告目录里，`REPORT.md` 适合看文字，`bundle.json` 保存计算明细，`inputs/` 保存这次读入的文件。想复核旧报告，可以用随附的配置重跑：

```bash
python scripts/run_research.py --config 旧报告目录/config.snapshot.json --out output
```

这条命令在对应品种仓库运行，把“旧报告目录”换成实际路径。

复盘时保留旧报告，另写新记录：原来等什么条件，后来有没有发生，哪条判断需要修改。有成交记录再讨论执行和盈亏；本仓库的模拟例子只演示计算与研究步骤。

[研究问题和复盘写法](docs/research-playbook.md) · [四个项目的登记文件](registry.json)

## 检查程序

在品种仓库里运行：

```bash
python -m unittest discover -s tests -v
```

在本导航仓库里，还可以检查四个本地目录是否齐全：

```bash
python scripts/validate_registry.py --local-root ..
```

我另外整理了 [A 股选股与量化工具](https://github.com/Serennity007/awesome-stock-quant-skills)，需要做个股筛选时可以一起用。

[Serennity007](https://github.com/Serennity007) · MIT
