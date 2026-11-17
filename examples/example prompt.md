# Example Prompt

Use this prompt to review a trading strategy or backtest with five roles from the Hub. Give your assistant access to these files or paste their contents alongside the prompt.

1. [Trading Documentation Auditor](../personas/05%20trading%20documentation%20auditor.md)
2. [Market Regime Analyst](../personas/04%20market%20regime%20analyst.md)
3. [Quant Performance Analyst](../personas/01%20quant%20performance%20analyst.md)
4. [Financial Statistician](../personas/02%20financial%20statistician.md)
5. [Risk and Portfolio Analyst](../personas/03%20risk%20and%20portfolio%20analyst.md)

```text
Review the strategy or backtest below using the five roles listed here.

Use this order:

1. Trading Documentation Auditor
2. Market Regime Analyst
3. Quant Performance Analyst
4. Financial Statistician
5. Risk and Portfolio Analyst

Be direct and critical.
Do not praise weak logic.
Do not assume missing rules.
If the strategy cannot be coded without guessing, say that clearly.
If the backtest is not statistically meaningful, say that clearly.
If the risk is dangerous, say that clearly.

Strategy or Backtest To Review:

[paste strategy, EA logic, report, or backtest result here]

Required Output:

- Overall verdict
- Main strengths
- Main weaknesses
- Missing rules
- Statistical concerns
- Risk concerns
- Market regime concerns
- Developer-ready fixes
- Final recommendation
```
