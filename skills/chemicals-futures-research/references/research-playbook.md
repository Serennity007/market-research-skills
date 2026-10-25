# Chemical processing chains / 化工加工链

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Choose one chain first: PX/PTA/polyester, naphtha/olefins or coal/methanol. Their feedstock, co-product and capacity economics are not interchangeable.
- A processing spread needs explicit conversion yield, currency, tax, freight, energy and fixed-cost scope. Declared coefficients are assumptions, not a full cash-profit statement.
- Separate nameplate capacity, effective utilization and realized output. An announced maintenance schedule needs observed start, duration and restart evidence.
- Reconcile upstream stocks with downstream order coverage and product inventories; avoid aggregating nested inventories as independent demand.
- Falsify a margin-led restart thesis if cash constraints, feedstock availability or downstream demand prevent production despite a wider calculated spread.

## Representative evidence series

- `plant_utilization`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `product_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `downstream_orders`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Validate feedstock/yield assumptions and test a range of energy/freight costs.
- Compare announced outages with realized plant output.
- Check product inventory days and downstream order duration using the same survey coverage.

## 中文研究要点

- 先选定 PX—PTA—聚酯、石脑油—烯烃或煤—甲醇中的一条链；原料、副产品和产能经济性不能混用。
- 加工价差显式声明收率、币种、税费、运费、能源和固定成本；系数是假设，不等于完整现金利润表。
- 名义产能、有效开工与实际产量分开；宣布检修要核验实际开始、持续时间和重启。
- 上游库存与下游订单覆盖、产品库存交叉核对；嵌套库存不重复计作独立需求。
- 计算价差扩大但资金、原料或下游需求阻止开工时，应证伪利润驱动重启假设。

- 核验原料与收率假设，并测试能源运费区间。
- 对照宣布停产与实际装置产量。
- 用相同调查覆盖核对产品库存天数与下游订单长度。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
