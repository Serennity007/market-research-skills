# Install and use / 安装与使用

Download the desired individual Skill ZIP, or the complete suite, from [the suite releases](https://github.com/Serennity007/taotao-futures-research/releases). Source code is also usable directly with Python 3.10+; base commands need no third-party packages. Windows, macOS and Linux use the same Python entrypoints. This release contains source/Skills rather than native desktop executables.

For an individual Skill, extract its top-level folder into your host's Skill directory. For Codex that normally means `~/.codex/skills/<skill-name>/SKILL.md` (Windows: `%USERPROFILE%\.codex\skills\<skill-name>\SKILL.md`). Avoid a second redundant folder level. Do not place API secrets in the Skill folder.

For all eight specialists plus the master, download these four assets into one directory:

- `futures-research-suite-3.0.0.zip`
- `SUITE.json`
- `SHA256SUMS.txt`
- `install_suite.py`

```bash
python install_suite.py --bundle futures-research-suite-3.0.0.zip
```

The installer checks the archive against the downloaded checksum list, validates archive paths and Skill identities, and refuses to replace any existing Skill. A conflict leaves existing Skills untouched and stops before copying. Use `--dest /your/skill/directory` to choose another directory. The checksum list is a local consistency check, not a digital signature; obtain all assets from the trusted repository release.

Restart the host or start a new session after installation to discover new Skills. Then ask, for example:

```text
Use $ferrous-futures-research to review my supplied RB dated-contract bars,
inventory releases and processing assumptions as of the stated cutoff.
Keep facts, hypotheses, contrary evidence and missing inputs distinct.
Write the report in Chinese and preserve a reproducible bundle.
```

No current data are included or assumed. Copy the matching example input directory and replace the synthetic files with authorized observations, source policies, effective rules and the user's requested cutoff. See [input contracts](desk-data-contract.md), [capacity assumptions](desk-risk-model.md) and [source policy](desk-source-policy.md).

| Profile | Invocation |
|---|---|
| Gold | `$gold-research-skill` |
| Crude oil | `$crude-oil-research-skill` |
| Europe container freight | `$ec-shipping-research-skill` |
| A-share index | `$a-share-index-research-skill` |
| Ferrous | `$ferrous-futures-research` |
| Nonferrous | `$nonferrous-futures-research` |
| Chemicals | `$chemicals-futures-research` |
| Agriculture | `$agri-futures-research` |
| Sector workbench / routing | `$taotao-futures-research` |

## 中文

单独安装：从发布页下载对应 ZIP，将顶层 Skill 文件夹解压到宿主 Skill 目录，确认直接存在 `<skill-name>/SKILL.md`。完整安装：把套件 ZIP、`SUITE.json`、`SHA256SUMS.txt`、`install_suite.py` 下载到同一目录，运行上面的安装命令；已有同名 Skill 时会停止，不覆盖原文件。

重启宿主或开启新会话后发现新增 Skill。可以直接说“使用 `$ferrous-futures-research`，按我给定的截止时点分析这些固定合约、库存公布和加工假设；分别写事实、假设、反证与缺口，输出中文可复核报告”。

Windows、macOS、Linux 采用相同 Python 命令；此次是源码／Skill 发布，不是系统原生安装器。示例不是现行行情，实际使用须替换为自己有权使用的数据、来源、交易时段与有效规则。中英报告会同时生成，默认首页可由 `--lang` 选择。
