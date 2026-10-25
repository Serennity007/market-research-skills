# Ferrous supply chain / 黑色产业链

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Trace ore/coal/coke to hot metal, steel output and end-use demand. Blast-furnace and electric-arc routes require different costs and supply responses.
- Reconcile mill and social inventories using non-overlapping coverage. Apparent consumption needs consistent production, imports, exports and stock changes.
- A steel margin recipe must declare yields, ore/coke quality, wet/dry basis, tax, energy, transport and by-products. The example is not a universal furnace formula.
- Match spot basis to location, grade, delivery eligibility and warehouse date; screen warehouse warrants separately from total inventory.
- Falsify a demand recovery if shipments and comparable inventory drawdowns fail to confirm it; distinguish policy announcements from actual starts and purchases.

## Representative evidence series

- `hot_metal_output`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `mill_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `social_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Reconcile hot metal, furnace utilization and actual construction/manufacturing orders.
- Audit inventory survey coverage changes and recipe sensitivities.
- Check grade premiums, delivery rules and remaining contract liquidity.

## 中文研究要点

- 从矿、煤、焦追踪到铁水、钢材与终端需求；高炉和电炉成本、供给响应应分别处理。
- 钢厂与社会库存先去重再核对；表观消费需要同口径产量、进出口和库存变化。
- 钢厂利润配方必须声明收得率、矿焦品质、干湿基、税费、能源、运输和副产品；示例不是通用高炉公式。
- 现货基差匹配地区、品级、交割资格和仓储日期；仓单与总库存单独核验。
- 发运与可比去库不确认时，应证伪需求修复；政策宣布与实际开工采购分开。

- 交叉核对铁水、炉况与建筑制造实际订单。
- 审计库存调查覆盖变化并对配方做敏感性分析。
- 核对品级升贴水、交割规则与合约剩余流动性。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
