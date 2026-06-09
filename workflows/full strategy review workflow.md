# Full Strategy Review Workflow

Use this workflow when reviewing a complete trading strategy from idea to testing readiness.

## Step 1: Documentation Audit

Use the Trading Documentation Auditor first.

Goal:

- Find vague rules.
- Identify missing entry and exit logic.
- Make the strategy developer-ready.

Do not move forward until the rules are clear enough to code.

## Step 2: Market Regime Review

Use the Market Regime Analyst second.

Goal:

- Define the market condition the strategy needs.
- Identify market conditions that should be avoided.
- Check whether the strategy fits the symbol and timeframe.

## Step 3: Quant Performance Review

Use the Quant Performance Analyst third.

Goal:

- Review performance metrics.
- Assess drawdown, trade count, profit factor, and equity curve quality.
- Decide whether the strategy deserves further testing.

## Step 4: Statistical Review

Use the Financial Statistician fourth.

Goal:

- Check whether the results are statistically meaningful.
- Detect randomness risk.
- Detect overfitting risk.
- Require more testing if confidence is weak.

## Step 5: Risk Review

Use the Risk and Portfolio Analyst last.

Goal:

- Make sure the strategy can survive real losses.
- Review lot sizing and drawdown exposure.
- Define daily loss limits and account protection rules.

## Final Output

At the end, produce one combined report with this structure:

```text
Complete Strategy Review

Overall Verdict:

Documentation Status:

Market Fit:

Performance Quality:

Statistical Confidence:

Risk Rating:

Must Fix Before Coding:
- 

Must Fix Before Backtesting:
- 

Must Fix Before Live Trading:
- 

Final Recommendation:

```
