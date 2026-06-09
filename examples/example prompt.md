# Example Prompt

Use this prompt when asking an assistant or coding model to review a trading system using the repository personas.

```text
I want you to review the trading strategy below using the five Analysis Personas.

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
