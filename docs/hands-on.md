# 四个实操例子

这四个例子使用模拟数据。日期是练习标签，输入文件和计算结果都放在各品种仓库里。先看懂一组数字，再换自己的数据。

## 黄金：收复支撑后，再看金银和利率

进入 `gold-research-skill`，运行：

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

先打开 `examples/bars.csv`。最后两根收盘是98和102，配置里的支撑为100，所以程序记为“跌破后收复”。报告中 MA5=97.6、MA10=98.8、MA20约102.238，均线仍向下排列。先记下局部修复，再观察后续收盘是否守住100。

`examples/macro.csv` 是另一组对照数据：

| 项目 | 前值 | 后值 | 算法与结果 |
|---|---:|---:|---|
| 黄金 | 2000 | 2040 | 2040/2000−1=2% |
| 白银 | 25 | 24 | 24/25−1=−4% |
| 美元指数 | 100 | 101 | 101/100−1=1% |
| 10年实际利率 | 2.0% | 2.1% | 上升0.1个百分点，也就是10个基点 |
| 金银比 | 2000/25 | 2040/24 | 从80升到85 |

这组练习里，黄金、美元和实际利率同涨。把这个现象写下来，再找其他解释；仅凭这两天的变化，不能判断谁导致谁上涨。K 线和宏观 CSV 是两组独立的构造数据，不把102与2040当作同一条报价。

要复查宏观计算，可单独运行：

```bash
python scripts/analyze_gold_drivers.py --csv examples/macro.csv --as-of 2024-01-09T15:00:00+08:00 --data-kind synthetic --out output/macro-check.json
```

## 原油：比较同一对合约的价差

进入 `crude-oil-research-skill`，先看 `examples/previous-curve.csv` 和 `examples/curve.csv`，再运行：

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

两份文件的合约数量不同，前一份多了 DEMO_OLD。用它们各自排在最前的合约比较，会混入端点变化。程序取两份文件共有的 DEMO_NEAR 和 DEMO_FAR：

| 合约 | 前次价格 | 本次价格 |
|---|---:|---:|
| DEMO_NEAR | 79 | 80 |
| DEMO_FAR | 77.5 | 77 |

原价差是79−77.5=1.5，本次是80−77=3，扩大1.5美元/桶。先确认这个计算，再结合库存、交付和报价时间解释原因。这里没有买入卖出记录，价差变化不能当作持仓收益。

换数据时保留具体合约名、交割月、币种和报价时刻。WTI、Brent、SC 分开整理，脚本会检查两次快照的基准与单位是否相同。

## 欧线：先查公布时间，再算绕航情景

进入 `ec-shipping-research-skill`，运行同一条报告命令：

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

在 `examples/settlement-index.csv` 中，有一条数值1400的观测，它到1月10日才公布。练习截止时间是1月9日，所以程序只使用已公布的1000。同期输入的期价是1200，两者差200，相对差20%。这项比较参照的是已公布的滞后指数，最终结算还要按目标合约规则计算。

接着看 `examples/route-scenarios.csv`。假设原来往返需要60天，绕航增加20天，影响50%的基准运力。其他条件不变时：

```text
运力比例 = 50% + 50% × 60/(60+20) = 87.5%
运力减少 = 1−87.5% = 12.5%
货量不变：相对需求压力 = 1/87.5% ≈ 1.1429
货量下降20%：相对需求压力 = 80%/87.5% ≈ 0.9143
```

同样的绕航假设，货量变化后，结论会不同。这只是固定船队下的敏感性计算。实际研究还需要船队调配、新船、货量等资料，不能把1.1429写成 EC 会涨14.29%。

## 大 A 股指：领先指数和上涨家数分开看

进入 `a-share-index-research-skill`，运行：

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

`examples/indices.csv` 用100作为四个指数的起点，末值分别为：沪深300是102、上证50是101、中证500是103、中证1000是104。中证1000涨4%，沪深300涨2%，两者收益差2个百分点；相对比变化则是：

```text
1.04/1.02−1 ≈ 1.9608%
```

再看 `examples/breadth.csv`：只有6个样本，配置声明完整范围应有10个，覆盖率60%。其中3个上涨、2个下跌、1个平盘，上涨比例为3/6=50%。这6个样本的等权收益约1.6667%，与官方加权指数涨幅是不同口径。

记录时可以写“这组指数样例中小盘表现领先，成分样本只覆盖60%”。等补齐缺失成分，再判断行情有没有扩散。

## 保存一次练习

打开终端打印的报告目录，检查 `COMPLETE.json` 是否存在。里面的 `inputs/` 是程序本次读到的文件，`bundle.json` 里能找到各文件的 SHA-256。

在对应品种仓库，使用这份冻结配置再跑一次：

```bash
python scripts/run_research.py --config 原报告目录/config.snapshot.json --out output
```

把“原报告目录”换成实际路径。两次报告的生成时间不同，输入相同时，计算值应一致。需要重跑单项命令时，请换一个输出文件名；单项脚本会拒绝覆盖已有文件。
