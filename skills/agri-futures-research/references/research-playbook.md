# Agricultural balances and crushing / 农产品供需与压榨

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Declare commodity, origin, quality and crop/marketing year before a supply-demand balance. Calendar-year totals and marketing-year totals cannot be silently combined.
- A crush recipe must include meal/oil yields, moisture, input quality, FX, freight, tax and costs. Meal strength alone does not prove crush profitability.
- Keep shipments, customs arrivals, port unloading, mill receipts and actual crushing separate; transit lead times can shift the apparent balance.
- Match seasonal comparisons by crop phase or declared week key. Use only earlier years; weather anecdotes require acreage, timing and realized yield evidence.
- Falsify a feed-demand recovery if offtake and comparable inventories diverge. Crop report revisions must enter only after their actual availability.

## Representative evidence series

- `mill_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `crushing_volume`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `downstream_offtake`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Align marketing years, units and first-release/revision calendars.
- Reconcile vessel arrivals, mill stocks, crushing and downstream offtake.
- Stress both meal and oil yields/prices; retain origin and quality adjustments.

## 中文研究要点

- 供需平衡先声明品种、产地、质量和作物／市场年度；自然年与市场年度不能静默拼接。
- 压榨配方须包含粕油收率、水分、原料质量、汇率、运费、税费与成本；粕价强不等于压榨盈利。
- 装运、海关到港、港口卸货、油厂入库与实际压榨分开；在途时差会改变表观平衡。
- 季节比较匹配作物阶段或声明周键，只用往年；天气叙事须核验面积、时点和实际单产。
- 提货与可比库存背离时，应证伪饲料需求恢复；作物报告修订仅在实际可用后纳入。

- 对齐市场年度、单位及首次公布／修订日历。
- 核对船期到港、油厂库存、压榨与下游提货。
- 联合测试粕油收率与价格，保留产地品质调整。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
