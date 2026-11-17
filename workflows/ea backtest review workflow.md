# EA Backtest Review Workflow

Use the [Backtest Review Template](../templates/backtest%20review%20template.md) to gather the tester report, settings, and applicable validation results. Record unavailable inputs as **Missing** and cite a report section, tester setting, input file, or trade export for each finding.

## Required Inputs

- EA name
- Symbol
- Timeframe
- Backtest period
- Optimization and out-of-sample date ranges, selection criterion, and number of configurations tried, if optimized
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
- Spread, commission, slippage, and execution-delay assumptions
- Tester report, EA build and settings, and trade export, where available
- Planned acceptance criteria and required evidence for demo forward testing

## Step 1: Performance Review

Use the [Quant Performance Analyst](../personas/01%20quant%20performance%20analyst.md).

Focus on:

- Profit factor
- Drawdown
- Win rate
- Trade count
- Equity curve stability
- Long versus short performance
- Outlier dependency

## Step 2: Statistical Review

Use the [Financial Statistician](../personas/02%20financial%20statistician.md).

Focus on:

- Whether the sample size is enough
- Whether the result is likely overfit
- Whether the EA needs walk forward testing
- Whether parameter sensitivity should be tested

## Step 3: Risk Review

Use the [Risk and Portfolio Analyst](../personas/03%20risk%20and%20portfolio%20analyst.md).

Focus on:

- Whether the account can survive losing streaks
- Whether risk per trade is too aggressive
- Whether daily limits are needed
- Whether lot sizing should be adjusted

## Step 4: Market Regime Review

Use the [Market Regime Analyst](../personas/04%20market%20regime%20analyst.md).

Focus on:

- Whether the EA performs only in certain market types
- Whether trend, chop, compression, and breakout conditions should be separated
- Whether the timeframe fits the intended holding time

## Step 5: Robustness and Execution Review

Use the [Robust Backtesting and Validation Advisor](../personas/10%20robust%20backtesting%20and%20validation%20advisor.md).

- Check which period selected parameters and which evaluated them. If the evaluation period influenced further tuning, request a fresh holdout or another independent evaluation.
- Compare in-sample and out-of-sample trade count, net results, and drawdown using consistent units. Check available walk-forward, parameter-stability, and stress-test results against the stated criteria.
- Record which costs the tester modeled and which were assumed. Flag missing or unsupported spread, commission, slippage, or latency inputs when they materially affect the strategy.
- Cite the evidence for each finding and identify the next test. See [MetaQuotes’ forward testing documentation](https://www.metatrader5.com/en/terminal/help/algotrading/strategy_optimization#forward) and [Bailey et al. on backtest overfitting](https://escholarship.org/content/qt4w1110bb/qt4w1110bb.pdf).

## Review Outcome

- **Check failed** when a completed check produces a documented result outside its acceptance criteria. Name the criterion and cite the result. List missing evidence separately.
- **Evidence missing** when a required test has yet to run or the supplied material cannot establish its result. Identify what to obtain or rerun.
- **Ready for demo forward testing** when the supplied results meet the stated criteria and a reviewer confirms the key findings. Record the demo test plan and stop criteria.

## Final Output

```text
EA Backtest Review

EA Name:
Symbol:
Timeframe:
Backtest Period:

Outcome:
Check failed / Evidence missing / Ready for demo forward testing

Performance Summary:

Statistical and robustness evidence:
Execution assumptions and evidence:
Risk and market regime findings:

Finding | Evidence reference | Criterion or limitation | Next test

Missing artifacts or fields:
Demo test criteria and reviewer confirmation, if applicable:

```
