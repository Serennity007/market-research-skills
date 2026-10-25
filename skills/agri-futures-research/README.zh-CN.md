[English](README.md) · [简体中文](README.zh-CN.md)

# 农产品供需与压榨

可独立安装的期货研究 Skill，包含产业链研究指导、离线计算、公布时点与版本控制、基差和月差、季节分位、费用保证金及压力情景。需要 Python 3.10+，基础命令无第三方依赖。

```bash
python scripts/run_desk.py run --config examples/desk-demo/agriculture/config.json --out output --lang zh-CN
python -m unittest discover -s tests -q
```

一次运行同时生成**中英双语** HTML／Markdown、JSON、来源声明、冻结输入及 SHA-256 清单。到[套件发布页](https://github.com/Serennity007/taotao-futures-research/releases)下载对应 ZIP，将其中单个 Skill 文件夹解压进本机 Skill 目录并重启宿主发现。其他代理也可以读取 `SKILL.md` 并运行相同 Python 命令。

[研究入口](SKILL.md) · [产业研究手册](references/research-playbook.md) · [输入约定与中文要点](docs/desk-data-contract.md) · [容量模型](docs/desk-risk-model.md)

示例行情、交易日历、合约规则和账户参数全部为构造数据，不代表现行交易所规则、真实历史业绩或建议风险参数。加工配方中的收率与成本需要研究者声明。工具不下单、不保证止损成交，不覆盖组合风险；文件哈希只核对本地一致性，不能认证来源。
