# 数据与计算格式

运行 Python 3.10+，只用标准库。CSV 为 UTF-8，时间用带时区的 ISO-8601；交易日和观察日期用 YYYY-MM-DD。

## 配置

参考 `examples/sector-demo/config.json`：

| 字段 | 用途 |
|---|---|
| data_kind | synthetic 或 imported_observations |
| as_of | 本次能够看到信息的截止时刻 |
| trade_date | 比较的共同终点交易日，由数据提供者定义 |
| windows | 名称到 label/start_date 的映射，起点必须早于终点 |
| universe | symbol、具体 contract、currency、unit、volume_unit=contracts |
| catalog | 研究分类 JSON 路径 |
| files | panel 必需，evidence 与 curves 可选；相对路径按配置文件位置解析 |
| minimum_sector_coverage | (0,1] 内的显式覆盖门槛 |
| max_bar_age_hours | 终点日线陈旧阈值，按自然小时；交易日历需另查 |

每个 universe 项可以有 structure，按周期填写人工关键位和参照。例如：

```json
"structure": {
  "H4": {
    "support": 100,
    "reference_time": "2024-01-06T00:00:00Z",
    "window_bars": 12
  }
}
```

support/resistance 说明来源与选择理由；reference_time 必须匹配一根已包含的收盘柱，计数不包含该参照柱。H4 12根窗口是参数示例，不是固定预测规则。

## panel.csv

`symbol,contract,timeframe,trade_date,close_time,open,high,low,close,volume,open_interest,currency,unit`

timeframe 支持 MN1、W1、D1、H4、H1、M30。每品种每交易日只能有一根 D1；同品种同周期不能重复收盘时间。close_time 表示已收盘时刻。夜盘 trade_date 采用供应商约定，不从自然日猜。

程序先排除晚于 cutoff 的行，再排除晚于目标交易日或不属于所选合约的行。其余价格须有限、OHLC 上下界一致；目录默认要求正价格，仅 SC 演示支持历史有符号价格。volume/open_interest 是非负整手数，原始来源的单边/双边统计仍需核对，不能混用后声称净流入。

日线端点缺失就留空。终点过旧也不参与排名；起点价格非正时普通百分比变化留空。缺根、交易所日历、复权和主连拼接没有自动校验。

MA5/10/20 按该周期已收盘行数计算。MACD 为 EMA12−EMA26、EMA9 信号，柱值为2×(DIF−DEA)，首价初始化，35根才标就绪。ATR14 是最后14个真实波幅的简单均值，至少15根日线，未使用 Wilder 平滑。成交量比值为当前日量/之前5根日线均量，不含当天；基准为零时留空。日增仓只记录手数变化。

## evidence.csv（可选）

`sector,metric,observed_at,published_at,value,unit,source`

sector 使用目录的板块 id，value 为有限数值，同一板块同一 metric 保持单位一致。observed_at 不晚于 published_at；公布晚于 cutoff 的版本排除。同一指标选最新观测期在截止时点可见的最新版本，不拿旧期后来的修订替换新期。重复观测/公布组合报错。

source 记录来源说明或链接；进口模式仍需配置 sources 中的取数信息。字段正确不等于来源已经认证。

## curves.csv（可选）

`symbol,contract,delivery_month,quote_time,price,currency,unit`

同品种一份快照，每个合约和 YYYY-MM 交割月唯一，至少两个月。报价按 cutoff 截断；单位与所选品种声明一致。按月份判断 contango/backwardation/flat/mixed，近月减远月计算绝对价差，同时报告报价时间跨度和最旧报价年龄。没有进行跨币种换算、到期日校验、价差年化或最终结算计算。

## 来源与重跑

真实观测模式为每个输入角色填写 sources：name 和带时区的 retrieved_at 必需，url 可选。下载时间与首次公布时间分开，历史版本由提供者保留。

输出冻结 CSV 原始字节和 catalog.json，并保存 SHA-256。config.snapshot.json 的路径改为 inputs/，可移走原文件后重跑。哈希可检查文件是否相同，不能证明来源真实性。示例所有数值、合约名称与单位均明确标注为模拟。
