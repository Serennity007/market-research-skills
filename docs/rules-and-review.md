# 条件写在前面，结果另记

在 universe 对应品种里填 setups。例如仓库的模拟 AU 条件：

```json
"setups": [{
  "name": "模拟支撑收复后再测试",
  "timeframe": "M30",
  "side": "support_reclaim",
  "anchor_time": "2024-01-08T01:00:00Z",
  "declared_at": "2024-01-08T01:00:00Z",
  "level": 100,
  "invalidation_level": 97,
  "retest_tolerance": 0.5,
  "validation_bars": 3
}]
```

## 每个字段做什么

anchor_time 必须对应已观察的破位收盘柱。support_reclaim 要求参照收盘低于 level；反向的 resistance_rejection 要求高于 level。declared_at 不早于参照收盘，它是使用者填写的声明时间，冻结文件使后续改动可检查，不能凭这个字段证明当时存在原计划。

level、失效位和容许范围用价格单位的 JSON 数值，容许范围不是百分数。validation_bars 按参照之后的可用柱数，不含参照；缺根和交易日历另查，不能按自然分钟换算。

## 怎么记录阶段

支撑例子先等后续收盘回到 level 及以上，再等另一根柱的最低价进入 level+tolerance 范围，且收盘仍在 level 及以上。收回那根不能同时算后续测试；反向规则镜像处理。

任一后续柱最低价触及或低于失效位，就记 invalidated；反向看最高价。没有完成后续测试且验证柱数用完，记 expired。窗口内已经记录测试守住，之后触及失效位仍会记失效，不因为先前满足观察就停止复查。

晚声明的规则不会补领声明前已经发生的正向阶段；若原参照在声明前已经触及失效位，保留这项已知反证。声明时间晚于截止时刻或缺参照柱时，分别给出未可知、缺数据状态。

这些状态说明手填规则在输入里发生了什么，不是已验证买点或收益结论。风险手数、真实委托和成交仍需额外资料，触及失效位也不保证按该价成交。

## 查看一对模拟记录

```bash
python scripts/compare_reports.py --before examples/review-before --after examples/review-after --out output/reviews
```

[前次](../examples/review-before/REPORT.md)、[后次](../examples/review-after/REPORT.md)、[复盘对照](../examples/review-result/REVIEW.md) 使用固定12月8日窗口锚点，分别截至1月9日和10日。AU 的 M30 练习先记录收回/后续测试，后来触及97失效位。原输入还包含下一日样例，用来检查截止时间过滤；这些都是构造练习，不是作者历史交易。

对照前先校验两份快照。换合约、币种、单位或缺少端点，不算固定合约变化；数据标签或目录版本不一致就拒绝。窗口锚点变化、样本不全或条件修改单独说明，不能把修改后的条件接成同一原计划。review.json 保留两份输入 bundle 的哈希。

## 冻结文件怎么核对

```bash
python scripts/bundle_integrity.py examples/sector-workbench
python scripts/run_sectors.py --config examples/sector-workbench/config.snapshot.json --out output
```

新版 COMPLETE.json 记录所有快照文件的 SHA-256。输入、配置、页面和表格改动，或者多出未登记文件，都会报错；重跑冻结配置前自动检查。旧版仍核对输入、目录与配置身份，但没有新版全部文件的检查范围。

把复盘笔记放在冻结目录之外。需要修改输入或参数，就复制到新的研究配置另跑一份。哈希能核对文件一致性，不能独立认证来源或证明过去的计划时间。
