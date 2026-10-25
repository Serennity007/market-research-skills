# 从一份板块报告开始

## 运行

```bash
git clone https://github.com/Serennity007/taotao-futures-research.git
cd taotao-futures-research
python scripts/run_sectors.py --config examples/sector-demo/config.json --out output
```

打开终端给出的 index.html，选择区间，在搜索框输入“黑色”或“AU”，点击板块名称查看品种明细。每次运行保存新目录，旧报告不覆盖。

## 先核对三件事

这份练习选30个代表品种，覆盖11个研究板块。目录里的69个标识用于路由；本次未配置的品种不计入覆盖率，也不假装已经分析。

日线、H4、H1 和产业数值均为独立构造的练习数据，使用 demo_points/demo_units，不代表真实合约点位。2024年的日期只是标签，不能视为当年的作者记录。H4/H1 片段用来演示周期分歧，不是从日线样例下采样出的同一真实行情。

## 手算贵金属单日均值

panel.csv 中 AU 的日线起末价格为80.896428和80.583926，AG 为88.245146和88.059354：

```text
AU：80.583926/80.896428−1 ≈ −0.386299%
AG：88.059354/88.245146−1 ≈ −0.210541%
样本等权：(−0.386299%−0.210541%)/2 ≈ −0.298420%
```

它是这两个固定合约的价格变化均值，不是资金组合收益。你可以在 bundle.json 的 products 与 sectors 中核对未舍入值。

## 看一个缺数据的板块

有色样例配置 CU、AL、LC，但 LC 缺目标交易日数据。覆盖率只有2/3。报告保留 CU/AL 的观察均值，默认不列这个板块的排名。把旧 LC 报价塞进终点会改变比较区间，因此程序留空。

想降低门槛，显式修改 minimum_sector_coverage，报告仍显示实际分母。先问缺失会不会改变样本代表性，再决定如何使用均值。

## 看多周期冲突和时间窗口

点进贵金属，AU 的 H4 片段包含跌破100后收回，H4 均线仍下降；H1 片段均线向上排列。报告分别显示。人工参照柱定在1月6日，窗口12根；已完成18根，标记过期，不移动参照来延长旧假设。

三阶段回踩确认与风险条件见 [完整价格方法](../references/price-structure.md)。这次把区间边缘、突破回踩、参照柱、风险预算和反手条件都整理进总 Skill；程序自动算出的范围见数据格式；新增的 M30 setups 会记录后续测试和下一日触及失效位的模拟变化，规则见 [条件与复盘](rules-and-review.md)。

## 核对产业数据公布时间

evidence.csv 里有一个能源指标到1月10日才公布。报告截止1月9日，排除这条999的未来观测，保留之前可知版本。所有指标名都带 DEMO，数值是练习，不是库存或产量实测。

curves.csv 提供三个品种的跨月快照：SC 80/78/77为反向结构；RB 100/102/101有拐点，标为 mixed；EC 1200/1180/1150为反向结构。它们也是独立构造数据，不与日线练习拼成价格连续序列。

## 保存与重跑

```bash
python scripts/run_sectors.py --config 原报告目录/config.snapshot.json --out output
```

把“原报告目录”换成实际路径。输入和目录文件随结果冻结，两次生成时间不同，计算值应一致。COMPLETE.json 只表示导出完成。

## 换自己的文件

复制示例配置，在 universe 选实际合约，填写价格单位和币种；选择共同交易日与区间。导入模式改成 imported_observations，为 panel/evidence/curves 中实际使用的文件补 name、retrieved_at，url 可选。

例如 sources 中 panel 的名称写实际数据提供者、代码、周期与口径，不要写“真实数据”了事。时间与字段详见 [数据格式](../references/data-contract.md)。新报告产生后，对照原计划的确认、失效条件另写复盘，保留旧文件。

真实日线入口与模拟练习分开，取数命令见 [公开日线说明](public-data.md)，已有实测见 [来源记录](../examples/real-source/VERIFICATION.md)。
