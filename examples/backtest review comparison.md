# Backtest Review Comparison

Use these fictional cases to check whether the Hub’s personas improve issue detection and evidence use. The cases provide a small manual benchmark. Record your own results and expand the fixture set before drawing conclusions about review accuracy.

## Run the Comparison

1. Open separate fresh chats for each case and condition. Use the same model, settings, input packet, and checklist in both conditions. Keep the worked answer and scoring key out of both chats.
2. For the **Checklist** condition, provide only the common prompt below and the selected case’s inputs. For the **Checklist plus personas** condition, also provide the five persona texts linked in the [backtest review workflow](../workflows/ea%20backtest%20review%20workflow.md), in workflow order. Use the common prompt’s output format in both conditions.
3. Save the outputs with the model name and date. Score them against the key without looking at the condition labels. Repeat with fresh chats if you want to measure variation across runs.

```text
Review the supplied backtest packet for readiness to start a demo forward test.
1. Check whether the reported holdout was separate from parameter selection.
2. Check whether spread, commission, slippage, and delay are documented.
3. Compare available results with the supplied acceptance criteria. Mark absent evidence as missing.
4. Record each finding with its evidence ID and the next check or action.
Choose Check failed if a completed check produced a documented result outside its acceptance criteria. Otherwise choose Evidence missing if a required test has yet to run or its result is unavailable. Choose Ready for demo forward testing only when the packet meets its stated criteria and records reviewer confirmation.
Use this output format: Outcome, followed by Findings with columns Finding, Evidence ID, and Next check or action.
```

## Input Packets

### Case A

Copy only the [input report table](worked%20backtest%20review.md#input-report) in the worked review.

### Case B

| Reference | Supplied value |
| --- | --- |
| B1 | Optimization ran on 2024 data across 64 configurations. The selected configuration was frozen before the January–June 2025 holdout and was never retuned using it. |
| B2 | The original holdout was net positive with 8.0% maximum equity drawdown. The report documents spread, commissions, slippage, and delay. |
| B3 | The same holdout with the predefined execution-cost stress produced 15.6% maximum equity drawdown. |
| B4 | The review plan requires maximum equity drawdown of 12% or less under the stress case before a demo forward test. |

### Case C

| Reference | Supplied value |
| --- | --- |
| C1 | Optimization covered January–September 2024 and compared 32 configurations. The selected configuration was frozen before testing on October–December 2024. The holdout was not used for tuning. |
| C2 | The holdout included 80 trades. Net P&L after costs was positive, and maximum equity drawdown was 6.4% in the predefined cost stress. The packet records spread, commissions, slippage, and delay. |
| C3 | The review plan requires an untouched holdout with at least 60 trades, positive net P&L after costs, and at most 10% equity drawdown under cost stress. |
| C4 | A human reviewer checked the tester and execution settings, confirmed the criteria were met, and recorded the demo plan and stop criteria. |

## Scoring Key

| Case | Expected outcome | Required findings |
| --- | --- | --- |
| A | Evidence missing | Identify the missing holdout using A1/A2. Identify the incomplete execution assumptions using A4. |
| B | Check failed | Cite B3/B4 and compare the observed 15.6% drawdown with the 12% limit. |
| C | Ready for demo forward testing | Cite C1–C4 for the untouched window, measured results, stated criteria, and reviewer confirmation. |

For each case, record the correct outcome as yes or no, count required findings that cite the correct evidence, and count unsupported claims. For example, count an invented commission rate or a claim of live readiness as unsupported. Report raw per-case results for both conditions.

The comparison design draws on [NIST’s generative AI guidance on verifying sources](https://nvlpubs.nist.gov/nistpubs/AI/NIST.AI.600-1.pdf) and [evaluation guidance on task-specific cases](https://developers.openai.com/api/docs/guides/evaluation-best-practices). The [EMNLP persona study](https://aclanthology.org/2024.findings-emnlp.888/) tested factual questions, so this comparison uses backtest review cases.
