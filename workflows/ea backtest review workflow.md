# EA Backtest Review Workflow

Use this workflow when reviewing an Expert Advisor backtest.

## Required Inputs

- EA name
- Symbol
- Timeframe
- Backtest period
- Modeling type
- Starting balance
- Ending balance
- Profit factor
- Win rate
- Total trades
- Maximum drawdown
- Average win
- Average loss
- Largest win
- Largest loss
- Spread and commission assumptions
- Screenshot or report summary, if available

## Step 1: Performance Review

Use the Quant Performance Analyst.

Focus on:

- Profit factor
- Drawdown
- Win rate
- Trade count
- Equity curve stability
- Long versus short performance
- Outlier dependency

## Step 2: Statistical Review

Use the Financial Statistician.

Focus on:

- Whether the sample size is enough
- Whether the result is likely overfit
- Whether the EA needs walk forward testing
- Whether parameter sensitivity should be tested

## Step 3: Risk Review

Use the Risk and Portfolio Analyst.

Focus on:

- Whether the account can survive losing streaks
- Whether risk per trade is too aggressive
- Whether daily limits are needed
- Whether lot sizing should be adjusted

## Step 4: Market Regime Review

Use the Market Regime Analyst.

Focus on:

- Whether the EA performs only in certain market types
- Whether trend, chop, compression, and breakout conditions should be separated
- Whether the timeframe fits the intended holding time

## Final Output

```text
EA Backtest Review

EA Name:
Symbol:
Timeframe:
Backtest Period:

Overall Result:
Pass / Needs More Testing / Fail

Performance Summary:

Statistical Confidence:

Risk Rating:

Market Regime Fit:

Main Problems Found:
- 

Recommended Fixes:
- 

Forward Test Requirements:
- 

Final Verdict:

```
