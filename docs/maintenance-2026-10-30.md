# Export maintenance / 发布导出维护 · 2026-10-30

The suite builder previously included local `.env` and virtual-environment files in release staging; direct ZIP export also bypassed the staging exclusions. Synthetic fixtures reproduced both cases. This check does not establish that any published archive contained real credentials.

Specialist staging, master staging and direct ZIP export now use the same filename exclusions. Normal source, example configurations, catalogs and checksums remain in the export. Changing excluded local settings no longer changes ZIP bytes. The exporter does not scan arbitrary file contents for secrets.

## Verification / 验证

| Repository / 仓库 | Tests / 测试 |
| --- | ---: |
| taotao-futures-research | 101 passed |
| a-share-index-research-skill | 36 passed |
| gold-research-skill | 26 passed |
| crude-oil-research-skill | 35 passed |
| ec-shipping-research-skill | 36 passed |
| Total / 合计 | 234 passed |

Three new regression tests cover direct ZIPs, all eight specialist exports plus master/combined-suite exports, checksums, preservation of source originals and deterministic results when local settings change. All settings in these tests are fake.

The real source checkout produced 10 ZIPs. Checksums and archive paths were checked, nine Skills were installed into a workspace-only directory, and all eight specialist desk examples completed without configured evidence gaps. Inputs were synthetic prices, calendars and hypothetical rules. [Machine-readable record](verification/2026-10-30-export.json).

```bash
python -m unittest discover -s tests -p test_suite_export.py -v
python -m unittest discover -s tests -q
python tools/build_skill_suite.py --out output/new-export --specialists-root ..
```

The four standalone repositories passed their existing tests without runtime changes. Existing release assets were not replaced. The temporary installation did not touch the host's actual Skill directory. Verification ran on Windows / Python 3.11; dates use Asia/Shanghai.

## 中文

本次修复发布脚本把本地 `.env`、虚拟环境等开发文件带入 ZIP 的问题。复制暂存和直接压缩使用同一过滤规则，不修改原始工作目录；这不是通用凭据扫描器，也没有据此断言旧版公开附件含有真实凭据。

五个仓库共 234 项测试通过；实际导出的 10 个 ZIP、校验清单、临时安装的 9 个 Skill 和 8 个专项离线示例已验证。未修改计算公式、旧冻结报告或四个独立仓库的运行代码，未替换已有 Release 附件。
