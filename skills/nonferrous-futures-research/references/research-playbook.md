# Nonferrous metals / 有色金属

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Separate mine supply, concentrate treatment charges, smelter output and fabricated demand; tight concentrate does not immediately equal tight refined metal.
- Inventory comparisons require exchange/warehouse geography, bonded status and warrant eligibility. Cancelled warrants and warehouse stock are not independent additive supplies.
- An import comparison needs synchronized FX, tax, freight, grade and location. A raw domestic/overseas price ratio is not an executable import margin.
- Physical premium, near/far spread and inventory draw should confirm the same location and period before inferring shortage.
- Falsify a demand-led rally if downstream utilization and premia weaken; distinguish supply maintenance from permanent capacity closures.

## Representative evidence series

- `exchange_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `physical_premium`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `smelter_utilization`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Reconcile exchange stocks with warrants using documented inclusion rules.
- Check smelter maintenance, concentrate availability and downstream orders.
- Rebuild landed-cost assumptions before interpreting cross-market spreads.

## 中文研究要点

- 矿端、精矿加工费、冶炼产量与加工需求分开；精矿紧张不等于精炼金属立即短缺。
- 库存比较要匹配交易所、仓库地区、保税状态和仓单资格；注销仓单与仓库库存不是独立可加供应。
- 进口比较需要同步汇率、税费、运费、品级和地区；内外比价不能直接解释为可执行进口利润。
- 实物升水、近远月差与去库须在相同地区和时期相互确认，再讨论短缺。
- 下游开工和升水转弱时，应检验需求拉动上涨；检修停产与永久关停分开。

- 按明确包含关系核对交易所库存与仓单。
- 核对冶炼检修、精矿可得性与下游订单。
- 解释跨市场价差前重建到岸成本假设。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
