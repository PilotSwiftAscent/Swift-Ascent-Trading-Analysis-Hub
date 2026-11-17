# Worked Backtest Review

This fictional MT5 example shows how to review a report that covers only the period used to tune the EA. The figures and acceptance criteria belong to this example.

## Input Report

| Reference | Report field | Supplied value |
| --- | --- | --- |
| A1 | Tester settings | Optimization and reported backtest both cover 2024-01-01 through 2024-12-31. Forward testing is disabled. |
| A2 | Optimization summary | 96 configurations tried. The report shows the configuration with the highest in-sample profit factor. |
| A3 | Report summary | 230 in-sample trades, profit factor 1.62, maximum equity drawdown 9.0%. |
| A4 | Cost settings | Fixed spread of 0.5 pip. Commission, slippage, and execution-delay assumptions are missing from the packet. |
| A5 | Acceptance criteria | Before a demo test, require an untouched historical evaluation with positive net results, maximum equity drawdown of 12% or less, and documented execution assumptions. |

## Review

**Outcome: Evidence missing.** The supplied evidence cannot establish the demo-test criteria in A5.

| Finding | Evidence | Criterion or limitation | Next test |
| --- | --- | --- | --- |
| Out-of-sample performance is missing. | A1 and A2 | The reported run is from the period used to choose among 96 configurations. A3 describes the selected in-sample result. | Freeze the selected settings, run them on a later period kept outside selection, and record net results, trade count, and equity drawdown. |
| Execution assumptions are incomplete. | A4 | The report documents a fixed spread. It supplies no basis for judging the other costs or delay. | Record how spread, commissions, slippage, and delay are modeled, then compare the untouched-period result with the stated criteria. |

Use the [backtest review workflow](../workflows/ea%20backtest%20review%20workflow.md) for your own report. Use this input packet as Case A in the [review comparison](backtest%20review%20comparison.md).
