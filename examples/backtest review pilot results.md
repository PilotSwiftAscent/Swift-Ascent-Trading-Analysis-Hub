# Backtest Review Pilot Results

On 2026-11-17, eight separate Codex review sessions evaluated the same four packets, once per condition. The packets include three fictional cases and a [redacted excerpt from a real MT5 Strategy Tester export](mt5%20tester%20report%20case.md).

## Results

| Condition | Correct outcomes | Required findings with evidence | Unsupported factual claims |
| --- | ---: | ---: | ---: |
| Checklist | 4/4 | 7/7 | 0 |
| Checklist plus personas | 4/4 | 7/7 | 0 |

Both conditions received the same scores on the predefined checks. On the real report, both reconciled the trade and deal counts and flagged the missing holdout and unverified execution assumptions. The persona response also requested a review of profit concentration and performance by market regime. These results describe this four-packet pilot. A larger set of real reports, repeat runs, and human review would be needed to estimate performance more reliably.

## Method

- Each review used a fresh session with the same inherited Codex configuration. Both conditions received the [same checklist and evidence packets](backtest%20review%20comparison.md). The second condition also received the five persona texts linked in the [backtest workflow at the source revision](https://github.com/PilotSwiftAscent/Swift-Ascent-Trading-Analysis-Hub/blob/b255b564071fe536a6bea8ac71ab54c0f967c2f2/workflows/ea%20backtest%20review%20workflow.md), in workflow order.
- Reviewer sessions received only their input packet and prompt materials. A separate model scorer read the unlabeled responses, packets, and scoring key before the condition labels were joined to the scores.
- A required finding earned credit when the response made the correct observation and cited the corresponding evidence IDs. The seven finding checks were distributed across the four packets. The scorer counted distinct unsupported factual claims separately.

## Case Scores

| Case | Condition | Outcome correct | Required findings with evidence | Unsupported factual claims |
| --- | --- | --- | ---: | ---: |
| A | Checklist | Yes | 2/2 | 0 |
| A | Checklist plus personas | Yes | 2/2 | 0 |
| B | Checklist | Yes | 1/1 | 0 |
| B | Checklist plus personas | Yes | 1/1 | 0 |
| C | Checklist | Yes | 1/1 | 0 |
| C | Checklist plus personas | Yes | 1/1 | 0 |
| D | Checklist | Yes | 3/3 | 0 |
| D | Checklist plus personas | Yes | 3/3 | 0 |

## Review Outputs

<details>
<summary>Case A · Checklist (run 06)</summary>

﻿## Outcome

Evidence missing

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| An untouched historical evaluation is missing. Optimization and the reported backtest both used January 1 through December 31, 2024. The report selected the highest in-sample profit factor from 96 configurations with forward testing disabled. | A1, A2, A5 | Freeze the selected parameters and run a historical evaluation on data that was never used for parameter selection. |
| Positive net results on untouched data are missing. The reported profit factor of 1.62 is in-sample. | A3, A5 | Record net profit after execution costs on the untouched data and check that it is positive. |
| Maximum equity drawdown on untouched data is missing. The reported 9.0% is below the 12% ceiling and applies to the in-sample run. | A3, A5 | Measure maximum equity drawdown on the untouched data and verify it is 12% or less. |
| A fixed spread of 0.5 pip is documented. Commission, slippage, and execution delay are missing. | A4, A5 | Document the three missing assumptions, including zero values if applicable, and use the documented execution assumptions in the evaluation. |
| The counts refer to different quantities. Optimization tried 96 configurations, and the reported in-sample run had 230 trades. | A2, A3 | Record the untouched evaluation's trade count when that run is available. |
| Reviewer confirmation is missing from the supplied packet. | A1–A5 | Record reviewer confirmation once the untouched evaluation and execution assumptions meet the acceptance criteria. |

</details>

<details>
<summary>Case A · Checklist plus personas (run 02)</summary>

﻿## Outcome

Evidence missing

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The selected configuration recorded 230 in-sample trades and a profit factor of 1.62. The required positive net result on untouched data is missing. | A3, A5 | Report net profit or loss after modeled execution costs on untouched data. Review the trade log for profit concentration and the equity curve for stability. |
| The 96 configurations tried and 230 reported trades count different things. The 230 trades belong to the selected configuration. | A2, A3 | Label the configuration count and trade count separately in the validation report. |
| Optimization and the reported backtest both covered 2024-01-01 through 2024-12-31. Forward testing was disabled, and selection favored the highest in-sample profit factor. An independent holdout result is missing. | A1, A2, A5 | Freeze the selected parameters and document a historical evaluation window that was untouched during development and selection. Check nearby configurations on development data for parameter sensitivity. |
| The reported 9.0% maximum equity drawdown is below the 12% cap numerically. The required drawdown measurement for the untouched window is missing. | A3, A5 | Measure maximum equity drawdown on the untouched equity curve under the documented execution assumptions and compare it with the 12% cap. |
| Regime-level performance is unavailable from the aggregate in-sample report. | A1, A3 | Review how returns and drawdown vary across market conditions in the validation data. |
| A fixed spread of 0.5 pip is documented. Commission, slippage, and execution-delay assumptions are missing. | A4, A5 | Record the commission schedule and the slippage and delay models, then apply the documented assumptions in the historical evaluation. |
| Reviewer confirmation is missing from the supplied packet. | A1–A5 | Record reviewer confirmation once the independent test results and execution assumptions are available and the stated criteria are met. |

</details>

<details>
<summary>Case B · Checklist (run 03)</summary>

﻿## Outcome

**Check failed**

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The holdout was separate from parameter selection. Optimization evaluated 64 configurations on 2024 data. The selected configuration was frozen before the January–June 2025 holdout and was never retuned on it. | B1 | Keep the configuration frozen for confirmation testing. Use a fresh holdout if parameter selection changes. |
| The holdout report documents spread, commissions, slippage, and delay. | B2 | Retain those assumptions with the review record. |
| The baseline holdout was net positive and had 8.0% maximum equity drawdown. The predefined execution-cost stress on the same holdout produced 15.6% maximum equity drawdown, exceeding the 12% ceiling by 3.6 percentage points. | B2, B3, B4 | Resolve the stress drawdown failure and demonstrate a result at or below 12% before starting demo forward testing. |
| Reviewer confirmation is missing from the packet. | B1–B4 | Record reviewer confirmation after the stress criterion is met. |

</details>

<details>
<summary>Case B · Checklist plus personas (run 07)</summary>

﻿## Outcome

Check failed

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The original holdout was net positive with 8.0% maximum equity drawdown. The 12% limit applies to the execution-cost stress case. | B2, B4 | Record the original result as the baseline for the stressed comparison. |
| Trade count, profit factor, and equity curve are missing. The 64 figure counts configurations, and the packet contains no conflicting counts to reconcile. | B1, B2 | Obtain the holdout trade log and equity series to assess sample size, profit concentration, and recovery. |
| The holdout was separate from parameter selection. Optimization used 2024 data, and the selected configuration was frozen before the January–June 2025 holdout and never retuned on it. Nearby-parameter results are missing. | B1 | Retain the dated configuration and run records. Check nearby settings for stability before selecting any revision. |
| The completed execution-cost stress produced 15.6% maximum equity drawdown, exceeding the 12% acceptance limit by 3.6 percentage points. | B3, B4 | Defer demo forward testing. Investigate the drawdown increase. If the configuration changes, freeze the revision and rerun the predefined stress on a fresh, untouched holdout. |
| Results by market regime, symbol, and timeframe are missing. | None supplied | Break down the holdout results by regime, symbol, and timeframe where trade counts support comparison. |
| The report documents spread, commissions, slippage, and delay. The packet records the predefined execution-cost stress result. | B2, B3 | Retain the baseline and stressed cost settings with their respective run records. |
| Walk-forward and Monte Carlo validation results are missing. Reviewer confirmation is missing. | None supplied | Retrieve or run the additional robustness checks and record reviewer confirmation once the stated demo criterion is met. |

</details>

<details>
<summary>Case C · Checklist (run 08)</summary>

## Outcome

Ready for demo forward testing

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The October–December 2024 holdout was separate from parameter selection. The configuration was selected from 32 candidates using January–September 2024 data and frozen before holdout testing. | C1, C3 | Use the frozen configuration for the demo. |
| The packet documents spread, commissions, slippage, and delay. | C2 | Use the reviewed execution settings for the demo. |
| The holdout recorded 80 trades, meeting the 60-trade minimum. | C2, C3 | Record the demo trade count separately. |
| Holdout net P&L was positive after costs, meeting the profitability criterion. | C2, C3 | Track net P&L after costs during the demo. |
| Maximum equity drawdown was 6.4% under the predefined cost stress, within the 10% limit. | C2, C3 | Monitor equity drawdown against the recorded demo stop criteria. |
| A human reviewer checked tester and execution settings, confirmed the criteria were met, and recorded the demo plan and stop criteria. | C4 | Start the demo forward test under the recorded plan. |

</details>

<details>
<summary>Case C · Checklist plus personas (run 04)</summary>

# Outcome

Ready for demo forward testing

# Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The October–December 2024 holdout was separate from January–September 2024 optimization. The selected configuration was frozen before the holdout and the holdout was untouched by tuning. | C1, C3 | Use the frozen configuration in the demo. |
| The holdout had 80 trades, meeting the 60-trade minimum. The 32 configurations were candidates compared during optimization, so the two counts measure different things. | C1, C2, C3 | Track demo trades separately from optimization configurations. |
| Holdout net P&L was positive after costs, meeting the profitability criterion. | C2, C3 | Track demo net P&L after execution costs. |
| Under the predefined cost stress, maximum equity drawdown was 6.4%, within the 10% limit. | C2, C3 | Monitor demo equity drawdown against the recorded stop criteria. |
| Spread, commissions, slippage, and delay are documented. | C2 | Compare demo spreads, commissions, slippage, and delays with the documented assumptions. |
| A human reviewer checked the tester and execution settings, confirmed the criteria were met, and recorded the demo plan and stop criteria. | C4 | Start the demo under the recorded plan and apply its stop criteria. |

</details>

<details>
<summary>Case D · Checklist (run 01)</summary>

﻿Outcome: Evidence missing

Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| Holdout independence is unverified. The H1 report covers only 2018-11-01 through 2018-12-01 and does not say when or how parameters were selected. | D1, D4 | Obtain the parameter selection record and test date ranges. Verify that parameters were frozen before a separate, untouched holdout was evaluated; run one if needed. |
| Spread, slippage, and execution delay assumptions are missing. The ledger records USD 0.00 commission on each trading entry, but the commission schedule and modeling assumptions are missing. | D3, D4 | Obtain the tester settings and intended demo conditions for all four items. Confirm whether zero commission is appropriate and rerun if the tested assumptions differ from those required. |
| The breakdowns support 23 trades: 11 short plus 12 long, and 10 winning plus 13 losing. The ledger contains 44 trading entries after excluding the opening balance entry. The duplicate summary label conflates the two counts. | D2, D3 | Label the figures separately as total trades (23) and trading ledger entries (44). Check deal and position IDs if an exact mapping is needed. |
| The report shows USD 17.74 net profit, a 1.68 profit factor, and USD 8.02 (0.08%) maximum equity drawdown. Acceptance criteria are missing, so no pass or failure can be established. | D2, D4 | Obtain the stated acceptance criteria and compare them with the verified holdout results. |
| Reviewer confirmation is missing. | D4 | Record reviewer confirmation after evaluating the required evidence against the stated criteria. |

</details>

<details>
<summary>Case D · Checklist plus personas (run 05)</summary>

## Outcome

Evidence missing

## Findings

| Finding | Evidence ID | Next check or action |
| --- | --- | --- |
| The duplicate total-trade rows reconcile to 23 trades and 44 trading deal entries. Both trade breakdowns sum to 23 (11 short + 12 long and 10 wins + 13 losses). The ledger has 44 trading entries after excluding the initial balance entry. | D2, D3 | Correct the summary labels to distinguish total trades from trading deal entries. |
| The reported H1 run shows USD 17.74 net profit on a simulated USD 10,000 deposit, a 1.68 profit factor, and 10 wins in 23 trades (43.5%). Evidence on equity-curve stability and dependence on individual trades is missing. | D1, D2, D3 | Review the equity curve and per-trade P&L to check losing streaks, recovery, and profit concentration. |
| Holdout separation is unverified. The packet shows one date range and does not document how or when parameters were selected. | D1, D4 | Obtain the selection dates, selected settings, and holdout dates. If an untouched holdout cannot be established, freeze the settings and test on a fresh window. |
| The reported maximum equity drawdown was USD 8.02 (0.08%). The packet supplies no drawdown limit or evidence on sizing and exposure, so the result cannot be assessed against a demo risk limit. | D1, D2, D4 | Obtain the applicable drawdown limit and confirm the sizing and exposure used in the run. |
| Spread, commission schedule, slippage, and execution delay assumptions are missing. The ledger records USD 0.00 commission on each trading entry, but the applicable commission schedule is undocumented. | D3, D4 | Obtain the tester's spread, commission, slippage, and delay settings and verify their match to the intended demo conditions. |
| The report covers only H1 from 2018-11-01 through 2018-12-01. Regime-specific performance and behavior outside that window are unverified. | D1, D4 | Identify the intended market conditions and examine performance across relevant periods and regimes. |
| Demo acceptance criteria and reviewer confirmation are missing. The reported results cannot be classified as a pass or a failure without the criteria. Walk-forward, parameter stability, and Monte Carlo results are also missing from the packet. | D2, D4 | Obtain the stated acceptance criteria, identify which validation results they require, compare documented results with each criterion, and record reviewer confirmation before starting the demo. |

</details>
