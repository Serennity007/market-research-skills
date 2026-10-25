"""Maintain bilingual domain guidance and deterministic synthetic fixtures.

Development tool: writes only desk_core/profiles.json and examples/desk-demo.
All dates, session schedules, quotes and specifications below are artificial.
"""
import csv
import io
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def bilingual(en, zh):
    return {"en": en, "zh-CN": zh}


PROFILES = {
    "gold": {
        "skill": "gold-research-skill", "product": "AU", "base": 700, "unit": "CNY/gram",
        "title": bilingual("Gold", "黄金"),
        "questions": bilingual([
            "Separate USD gold, CNY gold and FX conversion before attributing a domestic move. Match quote times, mass units, fineness and tax/delivery scope.",
            "A real-yield or dollar move is an explanatory hypothesis, not a deterministic gold signal. Align publication clocks and state the observation window.",
            "A gold/silver ratio requires synchronized currencies and mass units. Ratio extremes alone do not demonstrate mean reversion.",
            "Distinguish physical premium, exchange inventory, ETF holdings and central-bank announcements; their frequencies, revisions and coverage differ.",
            "Falsify a shortage explanation if physical premia and deliverable supply fail to confirm it; keep geopolitical narratives separate from observed flows."
        ], [
            "先区分美元金价、人民币金价与汇率折算，再归因国内变化。报价时点、质量单位、成色及税费交割口径必须一致。",
            "实际利率与美元变化只是解释假设，不是确定的黄金信号；对齐公布时间并写清观察窗口。",
            "金银比需要同步币种与质量单位；比值极端不能单独证明均值回归。",
            "实物升水、交易所库存、ETF持仓与央行公告的频率、修订和覆盖不同，分别记录。",
            "实物升水与可交割供应不确认时，应降低短缺解释的置信度；地缘叙事与实际流量分开。"
        ]),
        "next_checks": bilingual(["Check official rate/FX releases and the same observation window.", "Reconcile premium, warehouse and holdings evidence without double counting.", "Recheck the effective contract and broker margin/fee notices before capacity arithmetic."], ["核对官方利率／汇率发布与相同观察窗口。", "交叉核对升水、仓储和持仓证据，避免重复计数。", "容量计算前重新核对有效合约规则和经纪商保证金、费用通知。"]),
        "metrics": ["real_yield_pct", "physical_premium", "inventory"]
    },
    "crude-oil": {
        "skill": "crude-oil-research-skill", "product": "SC", "base": 550, "unit": "CNY/barrel", "allow_signed_prices": True,
        "title": bilingual("Crude oil", "原油"),
        "questions": bilingual([
            "Do not splice SC, Brent and WTI levels: grade, currency, location, freight, tax and delivery terms differ.",
            "Read dated spreads together with inventories, refinery runs and product demand; backwardation alone does not prove a physical shortage.",
            "Separate crude, products, strategic stocks, floating storage and transit volumes; weekly changes need comparable coverage and revisions.",
            "Trace an outage through lost production, export loadings, transit and refinery substitution. Announced cuts and realized exports are different evidence.",
            "Falsify a demand-led explanation if refinery throughput and product stocks deteriorate despite stronger flat prices. Signed prices disable ordinary return ratios."
        ], [
            "SC、Brent、WTI不能直接拼接价格：油种、币种、地点、运费、税费和交割条件不同。",
            "月差须与库存、炼厂开工和成品需求一起研究；近强远弱不能单独证明实物短缺。",
            "原油、成品油、战略库存、浮仓与在途分别统计；周变化须核对覆盖和修订。",
            "从损失产量、装船、运输和炼厂替代逐段追踪停产；宣布减产与实际出口不是同一证据。",
            "平价上涨但加工量和成品库存恶化时，应证伪需求拉动叙事；非正价格不使用普通收益率公式。"
        ]),
        "next_checks": bilingual(["Confirm benchmark and delivery scope of every curve point.", "Compare the first published inventory release with later revisions.", "Update freight, outage realization and product cracks using explicit conversion recipes."], ["核对每个曲线点的基准和交割口径。", "比较库存首次公布与后续修订。", "使用显式转换配方更新运费、实际停产和成品裂解口径。"]),
        "metrics": ["commercial_crude_inventory", "refinery_runs", "product_inventory"]
    },
    "ec-shipping": {
        "skill": "ec-shipping-research-skill", "product": "EC", "base": 1500, "unit": "index_points",
        "title": bilingual("Europe container freight", "欧线集运 EC"),
        "questions": bilingual([
            "Identify the exact published settlement-index series, covered route and release time. A spot booking quotation is not a settlement-index observation.",
            "Compare futures points with the matching index definition and settlement window. A point premium is descriptive, not a cash-and-carry opportunity.",
            "A rerouting scenario changes voyage duration and effective capacity only under stated fleet, speed, idle-time and demand assumptions; do not equate delay with lost cargo.",
            "Separate announced blank sailings, realized sailings, booking demand and realized load factors. Avoid adding overlapping capacity reductions.",
            "Falsify a disruption-led premium if effective capacity recovers or bookings weaken while futures remain elevated. Verify the latest official settlement rules separately."
        ], [
            "核对具体结算指数、航线覆盖与发布时间；即期订舱报价不是结算指数观测。",
            "期货点数须匹配指数定义与结算窗口；点数升水只是描述，不能解释为现货持有套利机会。",
            "绕航只在船队、航速、停泊与需求假设下改变航程和有效运力；延误不等于货量消失。",
            "宣布停航、实际开航、订舱需求和实际装载率分开；重叠运力削减不重复相加。",
            "运力恢复或订舱转弱而期价仍高时，应检验并证伪扰动溢价叙事；另查最新官方结算规则。"
        ]),
        "next_checks": bilingual(["Verify the index provider's publication calendar and observed release vintage.", "Map contract expiry and the applicable settlement observation window from official notices.", "Test rerouting and demand jointly; retain the original fleet denominator."], ["核验指数机构的发布日历与实际公布版本。", "根据官方通知核对合约到期及适用的结算观察窗口。", "联合检验绕航和需求变化，保留原始船队分母。"]),
        "metrics": ["settlement_index", "effective_capacity", "load_factor"]
    },
    "equity-index": {
        "skill": "a-share-index-research-skill", "product": "IF", "base": 4000, "unit": "index_points",
        "title": bilingual("A-share index futures", "A股股指期货"),
        "questions": bilingual([
            "Use an actual dated futures contract and its exact underlying index. A stock index level is not an executable futures quote.",
            "Align spot/futures timestamps before basis. Financing, expected dividends and expiry matter; an annualized point discount is not a risk-free expected return.",
            "Record breadth universe, constituent date, suspension treatment and coverage denominator. Survivorship-biased breadth can reverse an explanation.",
            "Separate large/small-cap style and industry composition from broad market direction. Do not add total market turnover to overlapping subsets.",
            "Falsify a broad recovery if index gains rely on a narrowing constituent set. Close-today costs and cash-settlement rules require dated official verification."
        ], [
            "使用实际到期期货合约及准确标的指数；股票指数点位不是可成交期货报价。",
            "先同步现货与期货时点再算基差；融资、预期分红和到期日影响可比性，年化贴水不是无风险预期收益。",
            "广度记录股票池、成分日期、停牌处理和覆盖分母；幸存者偏差可能推翻解释。",
            "大小盘风格及行业权重与全市场方向分开；全市场成交额不与重叠子集相加。",
            "指数上涨但参与成分持续收窄时，应证伪全面修复叙事；平今费用和现金交割须核对有效官方规则。"
        ]),
        "next_checks": bilingual(["Check dividend assumptions, expiry and quote synchronization.", "Rebuild breadth with the as-of constituent universe and coverage denominator.", "Confirm open/close/close-today fee schedules with effective dates."], ["核对分红假设、到期与报价同步。", "按当时成分与覆盖分母重建市场广度。", "确认开仓、平仓、平今费用及其生效日期。"]),
        "metrics": ["advancing_fraction", "index_turnover", "dividend_estimate"]
    },
    "ferrous": {
        "skill": "ferrous-futures-research", "product": "RB", "base": 3200, "unit": "CNY/tonne",
        "title": bilingual("Ferrous supply chain", "黑色产业链"),
        "questions": bilingual([
            "Trace ore/coal/coke to hot metal, steel output and end-use demand. Blast-furnace and electric-arc routes require different costs and supply responses.",
            "Reconcile mill and social inventories using non-overlapping coverage. Apparent consumption needs consistent production, imports, exports and stock changes.",
            "A steel margin recipe must declare yields, ore/coke quality, wet/dry basis, tax, energy, transport and by-products. The example is not a universal furnace formula.",
            "Match spot basis to location, grade, delivery eligibility and warehouse date; screen warehouse warrants separately from total inventory.",
            "Falsify a demand recovery if shipments and comparable inventory drawdowns fail to confirm it; distinguish policy announcements from actual starts and purchases."
        ], [
            "从矿、煤、焦追踪到铁水、钢材与终端需求；高炉和电炉成本、供给响应应分别处理。",
            "钢厂与社会库存先去重再核对；表观消费需要同口径产量、进出口和库存变化。",
            "钢厂利润配方必须声明收得率、矿焦品质、干湿基、税费、能源、运输和副产品；示例不是通用高炉公式。",
            "现货基差匹配地区、品级、交割资格和仓储日期；仓单与总库存单独核验。",
            "发运与可比去库不确认时，应证伪需求修复；政策宣布与实际开工采购分开。"
        ]),
        "next_checks": bilingual(["Reconcile hot metal, furnace utilization and actual construction/manufacturing orders.", "Audit inventory survey coverage changes and recipe sensitivities.", "Check grade premiums, delivery rules and remaining contract liquidity."], ["交叉核对铁水、炉况与建筑制造实际订单。", "审计库存调查覆盖变化并对配方做敏感性分析。", "核对品级升贴水、交割规则与合约剩余流动性。"]),
        "metrics": ["hot_metal_output", "mill_inventory", "social_inventory"]
    },
    "nonferrous": {
        "skill": "nonferrous-futures-research", "product": "CU", "base": 78000, "unit": "CNY/tonne",
        "title": bilingual("Nonferrous metals", "有色金属"),
        "questions": bilingual([
            "Separate mine supply, concentrate treatment charges, smelter output and fabricated demand; tight concentrate does not immediately equal tight refined metal.",
            "Inventory comparisons require exchange/warehouse geography, bonded status and warrant eligibility. Cancelled warrants and warehouse stock are not independent additive supplies.",
            "An import comparison needs synchronized FX, tax, freight, grade and location. A raw domestic/overseas price ratio is not an executable import margin.",
            "Physical premium, near/far spread and inventory draw should confirm the same location and period before inferring shortage.",
            "Falsify a demand-led rally if downstream utilization and premia weaken; distinguish supply maintenance from permanent capacity closures."
        ], [
            "矿端、精矿加工费、冶炼产量与加工需求分开；精矿紧张不等于精炼金属立即短缺。",
            "库存比较要匹配交易所、仓库地区、保税状态和仓单资格；注销仓单与仓库库存不是独立可加供应。",
            "进口比较需要同步汇率、税费、运费、品级和地区；内外比价不能直接解释为可执行进口利润。",
            "实物升水、近远月差与去库须在相同地区和时期相互确认，再讨论短缺。",
            "下游开工和升水转弱时，应检验需求拉动上涨；检修停产与永久关停分开。"
        ]),
        "next_checks": bilingual(["Reconcile exchange stocks with warrants using documented inclusion rules.", "Check smelter maintenance, concentrate availability and downstream orders.", "Rebuild landed-cost assumptions before interpreting cross-market spreads."], ["按明确包含关系核对交易所库存与仓单。", "核对冶炼检修、精矿可得性与下游订单。", "解释跨市场价差前重建到岸成本假设。"]),
        "metrics": ["exchange_inventory", "physical_premium", "smelter_utilization"]
    },
    "chemicals": {
        "skill": "chemicals-futures-research", "product": "TA", "base": 5000, "unit": "CNY/tonne",
        "title": bilingual("Chemical processing chains", "化工加工链"),
        "questions": bilingual([
            "Choose one chain first: PX/PTA/polyester, naphtha/olefins or coal/methanol. Their feedstock, co-product and capacity economics are not interchangeable.",
            "A processing spread needs explicit conversion yield, currency, tax, freight, energy and fixed-cost scope. Declared coefficients are assumptions, not a full cash-profit statement.",
            "Separate nameplate capacity, effective utilization and realized output. An announced maintenance schedule needs observed start, duration and restart evidence.",
            "Reconcile upstream stocks with downstream order coverage and product inventories; avoid aggregating nested inventories as independent demand.",
            "Falsify a margin-led restart thesis if cash constraints, feedstock availability or downstream demand prevent production despite a wider calculated spread."
        ], [
            "先选定 PX—PTA—聚酯、石脑油—烯烃或煤—甲醇中的一条链；原料、副产品和产能经济性不能混用。",
            "加工价差显式声明收率、币种、税费、运费、能源和固定成本；系数是假设，不等于完整现金利润表。",
            "名义产能、有效开工与实际产量分开；宣布检修要核验实际开始、持续时间和重启。",
            "上游库存与下游订单覆盖、产品库存交叉核对；嵌套库存不重复计作独立需求。",
            "计算价差扩大但资金、原料或下游需求阻止开工时，应证伪利润驱动重启假设。"
        ]),
        "next_checks": bilingual(["Validate feedstock/yield assumptions and test a range of energy/freight costs.", "Compare announced outages with realized plant output.", "Check product inventory days and downstream order duration using the same survey coverage."], ["核验原料与收率假设，并测试能源运费区间。", "对照宣布停产与实际装置产量。", "用相同调查覆盖核对产品库存天数与下游订单长度。"]),
        "metrics": ["plant_utilization", "product_inventory", "downstream_orders"]
    },
    "agriculture": {
        "skill": "agri-futures-research", "product": "M", "base": 3000, "unit": "CNY/tonne",
        "title": bilingual("Agricultural balances and crushing", "农产品供需与压榨"),
        "questions": bilingual([
            "Declare commodity, origin, quality and crop/marketing year before a supply-demand balance. Calendar-year totals and marketing-year totals cannot be silently combined.",
            "A crush recipe must include meal/oil yields, moisture, input quality, FX, freight, tax and costs. Meal strength alone does not prove crush profitability.",
            "Keep shipments, customs arrivals, port unloading, mill receipts and actual crushing separate; transit lead times can shift the apparent balance.",
            "Match seasonal comparisons by crop phase or declared week key. Use only earlier years; weather anecdotes require acreage, timing and realized yield evidence.",
            "Falsify a feed-demand recovery if offtake and comparable inventories diverge. Crop report revisions must enter only after their actual availability."
        ], [
            "供需平衡先声明品种、产地、质量和作物／市场年度；自然年与市场年度不能静默拼接。",
            "压榨配方须包含粕油收率、水分、原料质量、汇率、运费、税费与成本；粕价强不等于压榨盈利。",
            "装运、海关到港、港口卸货、油厂入库与实际压榨分开；在途时差会改变表观平衡。",
            "季节比较匹配作物阶段或声明周键，只用往年；天气叙事须核验面积、时点和实际单产。",
            "提货与可比库存背离时，应证伪饲料需求恢复；作物报告修订仅在实际可用后纳入。"
        ]),
        "next_checks": bilingual(["Align marketing years, units and first-release/revision calendars.", "Reconcile vessel arrivals, mill stocks, crushing and downstream offtake.", "Stress both meal and oil yields/prices; retain origin and quality adjustments."], ["对齐市场年度、单位及首次公布／修订日历。", "核对船期到港、油厂库存、压榨与下游提货。", "联合测试粕油收率与价格，保留产地品质调整。"]),
        "metrics": ["mill_inventory", "crushing_volume", "downstream_offtake"]
    }
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")


def write_csv(path, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8", newline="")


def clock(d, time="15:00:00"):
    return f"{d}T{time}+08:00"


def build():
    write_json(ROOT/"desk_core/profiles.json", PROFILES)
    dates = [date(2025,9,1)+timedelta(days=i) for i in range(26) if (date(2025,9,1)+timedelta(days=i)).weekday()<5]
    for key, profile in PROFILES.items():
        out = ROOT/"examples/desk-demo"/key
        out.mkdir(parents=True, exist_ok=True)
        product, base, unit = profile["product"], profile["base"], profile["unit"]
        contract = product+"_DEMO_202512"
        bars, sessions = [], []
        for i,d in enumerate(dates):
            close = base+i
            bars.append(dict(product=product,contract=contract,trade_date=str(d),observed_at=clock(d),published_at=clock(d,"15:01:00"),available_at=clock(d,"15:02:00"),open=close-1,high=close+2,low=close-2,close=close,volume=1000+i*10,open_interest=2000+i*20,currency="CNY",unit=unit))
        for d in [*dates, date(2025,9,29)]:
            if key not in ("equity-index", "ec-shipping"):
                previous = d-timedelta(days=3 if d.weekday()==0 else 1)
                sessions.append(dict(product=product,trade_date=str(d),start_time=clock(previous,"21:00:00"),end_time=clock(previous,"23:00:00")))
            sessions.append(dict(product=product,trade_date=str(d),start_time=clock(d,"09:00:00"),end_time=clock(d)))
        write_csv(out/"bars.csv", bars)
        write_csv(out/"sessions.csv", sessions)
        fundamentals = []
        for year,value in [(2021,100),(2022,120),(2023,80),(2024,110),(2025,105)]:
            d = f"{year}-09-26"
            fundamentals.append(dict(metric=profile["metrics"][0],value=value,unit="declared_demo_units",season_key="crop_or_season_week_39_demo",observed_at=clock(d,"10:00:00"),published_at=clock(d,"12:00:00"),available_at=clock(d,"12:05:00")))
        # A later revision is deliberately not available at this report cutoff.
        fundamentals.append(dict(fundamentals[-1],value=999,published_at=clock("2025-09-29","12:00:00"),available_at=clock("2025-09-29","12:05:00")))
        write_csv(out/"fundamentals.csv", fundamentals)
        times = dict(observed_at=clock(dates[-1]),published_at=clock(dates[-1],"15:01:00"),available_at=clock(dates[-1],"15:02:00"))
        scope = "DEMO matching grade/location/tax/index definition; not a live quote"
        write_csv(out/"spot.csv", [dict(spot_id="comparable_spot",price=base+24,currency="CNY",unit=unit,scope=scope,**times)])
        write_csv(out/"curve.csv", [dict(product=product,scope=scope,contract=contract,delivery_date="2025-12-15",price=base+19,currency="CNY",unit=unit,**times),dict(product=product,scope=scope,contract=product+"_DEMO_202603",delivery_date="2026-03-15",price=base+29,currency="CNY",unit=unit,**times)])
        spec = dict(version="SYNTHETIC-1",source="synthetic://not-an-exchange-rule",contract=contract,currency="CNY",price_unit=unit,multiplier="10",tick="1",margin_rate="0.10",last_trade_at="2025-12-15T15:00:00+08:00",effective_at="2025-09-01T00:00:00+08:00",expires_at="2025-12-01T00:00:00+08:00",observed_at="2025-08-01T10:00:00+08:00",published_at="2025-08-01T10:00:00+08:00",available_at="2025-08-01T10:05:00+08:00",fees={k:dict(per_contract="2" if k!="close_today" else "5",ad_valorem="0.0001") for k in ("open","close","close_today")})
        write_json(out/"spec.json",[spec])
        config = dict(schema_version=1,profile=key,data_kind="synthetic",as_of="2025-09-26T17:00:00+08:00",instrument=dict(product=product,contract=contract,currency="CNY",unit=unit),files={k:k+(".json" if k=="spec" else ".csv") for k in ("bars","sessions","fundamentals","spot","curve","spec")},limits=dict(quote_age_hours=24,quote_skew_minutes=5,publication_grace_minutes=5),calendar_valid_until="2025-09-29T23:59:00+08:00",basis=dict(spot_id="comparable_spot",scope=scope),risk=dict(currency="CNY",side="long",entry=str(base+19),stop=str(base+14),close_kind="close_today",unencumbered_equity="1000000",risk_budget="1000",margin_budget="100000",max_lots=100,max_previous_volume_fraction="0.01",slippage_ticks_per_side=1,stress=[dict(name="hypothetical gap and margin increase",adverse_price_fraction="0.08",margin_rate="0.25")]))
        config["curve_scope"] = scope
        if key in ("ferrous","chemicals","agriculture"):
            write_csv(out/"prices.csv",[dict(price_id=name,price=value,currency="CNY",unit="CNY/tonne",**times) for name,value in [("output",4000),("feedstock",3000),("co_product",2000)]])
            config["files"]["prices"] = "prices.csv"
            quantities = [("output","1"),("feedstock","-1.2")] if key=="ferrous" else [("output","1"),("feedstock","-0.65")] if key=="chemicals" else [("output","0.8"),("co_product","0.18"),("feedstock","-1")]
            config["recipes"] = [dict(name=key+"_illustrative_processing",currency="CNY",output_unit="tonne_of_declared_output_basis",fixed_cost_per_output="100",assumption="CONSTRUCTED coefficients and costs, not plant economics / 构造收率与成本，不代表装置实际利润",terms=[dict(price_id=name,input_unit="CNY/tonne",quantity_per_output=q,quantity_unit="tonnes_per_declared_output_basis") for name,q in quantities])]
        write_json(out/"config.json",config)
    print("Authored 8 profiles and 8 deterministic synthetic input sets.")


if __name__ == "__main__":
    build()
