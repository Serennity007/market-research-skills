# 明确合约的公开日线

默认板块演示离线运行。需要公开历史日线时，另调用 fetch_sina.py，它只请求指定合约，不自动扫描69个品种。

```bash
python scripts/fetch_sina.py --request examples/sina-request.json --out output/sources --analyze
```

请求文件中每个合约写 symbol、contract、currency、unit、session_close。例如 AU2612 配 CNY、CNY_per_gram 和15:00:00+08:00。日期代码由你明确填写，当前挂牌、单位和收盘时刻查交易所；示例合约只对应本次功能实测，不自动续成下一主力。

脚本最多请求6个合约，单次请求超时15秒，响应上限4MB，不自动无限重试。它用 JSON 解析固定格式的回调数据，不执行响应中的脚本；拒绝连续/主力代码、重复品种、重复日期、异常 OHLC 和不合法手数。源站变化或无数据时，FAILURE.json 保留已完成的来源，不把失败标成成功。

## 时间与价格口径

日线日期来自提供者，日收盘时刻使用请求文件中的声明，排除北京时间取数当日及以后的记录。available_at 写本次下载时间。这是当前取数版本，不能用更早 as_of 把它当作过去已知的资料；若有供应商提供的真实历史版本，可另外按其公布时点导入。

close 用原始 c 字段，s 是结算字段，仅留在原始响应中。报告计算收盘/收盘的变化，不能写成按昨结计算的交易所日涨跌或账户盈亏。v/p 按接口成交/持仓手数转换，统计单双边和供应商定义仍需核对。

零成交且 OHLC 全零的占位行会列明原因后排除。其余异常不自动填值。只有全部所选合约至少有21个共同日期，才建立最近1/5/20段共同观测窗口；这里按可用观测计数，没有假装核验完整交易日历。

max_bar_age_hours 是使用者声明的自然小时阈值，示例96用于包含周末的这次快照，不等于任何市场的流动性标准或实时行情保证。

## 保存什么

raw/ 保留当次原始响应，SOURCE_COMPLETE.json 记录来源、时间、哈希、日期范围与排除行。panel.csv 是转换结果，catalog.json 保留研究分类，config.json 供报告使用。request.snapshot.json 保存原请求字节供核对，相对路径属于原请求位置；重新下载使用原 request 文件。

```bash
python scripts/bundle_integrity.py 取数目录
python scripts/run_sectors.py --config 取数目录/config.json --out output
```

报告读取完整取数目录的 config.json 时，会先核对源快照。网络失败记录留在取数目录，完整报告用另外的 COMPLETE.json 标明导出成功，两者分别判断。

## 实测与来源

[2026-10-25 取数记录](../examples/real-source/VERIFICATION.md) 保存3个固定合约与计算结果；示例使用新浪财经日线，不代表交易所认证或策略绩效。

接口路径与字段核对参考 [AKShare 的公开实现](https://github.com/akfamily/akshare/blob/main/akshare/futures/futures_zh_sina.py)，本脚本用标准库实现，不要求安装 AKShare。原始行情来自新浪财经，数据保留来源信息；MIT 用于本仓库的程序和整理文本，不据此改变提供者原始资料的权利。
