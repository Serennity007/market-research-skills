# 原有四个专题报告

总 Skill 的板块报告不依赖这四个目录。需要同时体验四个专题工具时，在同一父目录准备：

```bash
git clone https://github.com/Serennity007/taotao-futures-research.git
git clone https://github.com/Serennity007/gold-research-skill.git
git clone https://github.com/Serennity007/crude-oil-research-skill.git
git clone https://github.com/Serennity007/ec-shipping-research-skill.git
git clone https://github.com/Serennity007/a-share-index-research-skill.git
cd taotao-futures-research
python scripts/run_all.py --local-root .. --out output
python scripts/validate_registry.py --local-root ..
```

这个入口继续运行四个已克隆项目的模拟例子。`registry.json` 的 skills 列表只登记四个专题，root_skill 另记本仓库的板块入口。
