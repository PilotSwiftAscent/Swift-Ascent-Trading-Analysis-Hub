# Real MT5 Strategy Tester Report Review

This case uses a real Strategy Tester export from a historical simulation. Dmitry Fedoseev published the export as an attachment to an [MQL5 article on parsing HTML reports](https://www.mql5.com/en/articles/5436#attachments). The review packet omits the strategy name, broker, symbol, input settings, and individual orders and deals. The original public source remains attributable.

## Review Packet

| Evidence ID | Report evidence |
| --- | --- |
| D1 | Tester settings: H1, 2018-11-01 through 2018-12-01, and a simulated USD 10,000 starting deposit. |
| D2 | Summary: USD 17.74 net profit, profit factor 1.68, and maximum equity drawdown of USD 8.02 (0.08%). The summary displays two rows with the same total-trade label, with values 23 and 44. It reports history quality of 100%. |
| D3 | Summary breakdown: 11 short and 12 long trades, with 10 winning and 13 losing trades. The deal ledger has 44 trading entries after excluding the initial balance entry, and records USD 0.00 commission on each trading entry. |
| D4 | The supplied report contains one date range. It does not identify a separate holdout, how the parameters were selected, or the spread, commission schedule, slippage, and execution delay assumptions. No demo-test acceptance criteria or reviewer confirmation are supplied with the packet. |

## Annotated Review

**Outcome: Evidence missing.** The export gives results for one historical period. The packet lacks the evidence needed to recommend a demo forward test.

| Finding | Evidence | Next check |
| --- | --- | --- |
| The two total-trade labels refer to different counts. The breakdown reconciles to 23 trades and the ledger to 44 trading deals. | D2 and D3 | Use 23 as the trade count and 44 as the deal-entry count in analysis. Preserve the source-label discrepancy in the audit notes. |
| Holdout evidence and parameter-selection history are missing. | D1 and D4 | Obtain the selection dates and settings, then verify whether a separate evaluation used fixed settings. |
| Booked commission is zero in this ledger. The cost assumptions and their representativeness remain unverified. | D3 and D4 | Record the spread, commission schedule, slippage, and delay settings and obtain the agreed acceptance criteria before comparing cost-adjusted results. |

[MetaTrader 5’s Testing Report documentation](https://www.metatrader5.com/en/terminal/help/algotrading/testing_report) defines the reported metrics. A history-quality figure describes characteristics of the price data and provides no evidence here about the specific tick mode.

## Source Verification

The [article’s attachment](https://www.mql5.com/en/articles/download/5436/mql5.zip) contains `MQL5/Files/ReportTester-555849.html`. The SHA-256 of that HTML entry is `0c2972f198191dd5afb1379871c30f209943328799823c13515a279d6b8af820`. The metrics above were checked against that entry. The 44 deal entries and their commission values were counted from its deal table. This case uses the Strategy Tester export alone.
