# 公开日线取数与计算记录

取数时间：2026-10-25T10:00:16.384543+00:00。来源：新浪财经固定合约日线接口；测试命令使用 examples/sina-request.json。raw/ 保存当次响应，SOURCE_COMPLETE.json 记录来源、SHA-256 和过滤情况。

| 合约 | 接收的日线条数 | 首日 | 末日 |
|---|---:|---|---|
| AU2612 | 225 | 2025-11-18 | 2026-10-23 |
| RB2701 | 184 | 2026-01-16 | 2026-10-23 |
| M2701 | 183 | 2026-01-19 | 2026-10-23 |

共同日期共183个，报告终点为2026-10-23。实际板块报告见 [REPORT.md](../real-workbench/REPORT.md)，配置的3个合约分属3个板块；100%覆盖只对各自这一个代表品种成立。

这份记录核验公开取数、字段转换、来源冻结和板块计算。它使用取数时可见版本，每根 K 线的 available_at 为当次下载时间；回填更早 as_of 会排除这些数据。日收盘时刻由请求文件声明，排除取数当日，不能据此宣称已还原历史首次公布时点。

close 使用接口 c 字段，s 结算字段保存在原始响应中但未用于收盘价变化；此处的涨跌幅不是按昨结计算的交易所涨跌，也不是账户收益。

校验原始响应与输入：

```bash
python scripts/bundle_integrity.py examples/real-source
python scripts/bundle_integrity.py examples/real-workbench
python scripts/run_sectors.py --config examples/real-workbench/config.snapshot.json --out output
```

重新下载使用 examples/sina-request.json；其中的合约是本次明确选择的样例，不自动标为主力。request.snapshot.json 保留原请求字节供核对，其相对路径属于原请求位置。源站接口和后续数据可能变化，重取结果不要求与本次哈希相同。
