# Local MT5 Tools

Run the commands below from the repository root. The report checker and dashboard demo use Python’s standard library. Live monitoring uses MetaQuotes’ Python package on 64-bit Windows.

## Report Checker

Export the MT5 Strategy Tester report as HTML, then run this command in PowerShell.

```powershell
py -m tools.mt5_report "C:\path\to\StrategyTester.html" --output "review.md"
```

Omit `--output` to print the packet in your terminal. The checker reads English Strategy Tester reports in UTF-8 or BOM-marked UTF-16. It marks evidence as **Reported**, **Calculated**, or **Missing**, and keeps equity and balance drawdown separate. It can reconcile old exports with two trade-count labels when the breakdown and deal ledger support the distinction. It includes summary evidence and omits account identifiers, EA inputs, and individual deal rows.

The Hub’s [real MT5 report review](../examples/mt5%20tester%20report%20case.md) shows a worked example. For field definitions, refer to [MetaTrader 5’s Testing Report documentation](https://www.metatrader5.com/en/terminal/help/algotrading/testing_report).

## Live Dashboard

The monitor shows the connected account’s equity, balance, floating P/L, free margin, open positions, and pending orders. It polls about every two seconds and shows the last bid, ask, and tick time for each symbol with a position or order. Quotes can remain unchanged when a market is closed.

To preview the dashboard with fictional data, run this command and open the loopback address printed in the terminal.

```powershell
py -m tools.mt5_dashboard --demo
```

For live data, open your Windows MT5 terminal and sign in to the account you want to monitor. On that computer, install the official [MetaTrader5 Python package](https://pypi.org/project/metatrader5/) into a virtual environment and start the dashboard.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install MetaTrader5
.\.venv\Scripts\python.exe -m tools.mt5_dashboard
```

Open [127.0.0.1:8765](http://127.0.0.1:8765/) on the same computer. To select a particular MT5 installation, supply `--terminal "C:\Program Files\MetaTrader 5\terminal64.exe"` with the actual path. Use `--port 8766` if the default port is occupied. Press **Ctrl+C** in the shell to stop the monitor.

The dashboard uses the terminal’s active account through [MetaQuotes’ Python integration](https://www.mql5.com/en/docs/python_metatrader5). It serves account snapshots on loopback and keeps the session equity chart in memory. The session starts with the first successful update and resets when the account changes or disconnects. The API is read-only.

## Tests

```powershell
py -B -m unittest discover -s tests
```
