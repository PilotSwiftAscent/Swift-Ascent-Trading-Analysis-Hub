import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LEGACY_TOTALS = """
<tr><td>Total Trades:</td><td>2</td><td>Short Trades (won %):</td><td>1 (0%)</td>
    <td>Long Trades (won %):</td><td>1 (100%)</td></tr>
<tr><td>Total Trades:</td><td>4</td><td>Profit Trades (% of total):</td><td>1 (50%)</td>
    <td>Loss Trades (% of total):</td><td>1 (50%)</td></tr>
"""
LEDGER = """
<tr><th colspan="7">Orders</th></tr>
<tr><td>Time</td><td>Order</td><td>Type</td><td>Direction</td><td>Commission</td></tr>
<tr><td>2024.01.01 01:00</td><td>123</td><td>buy</td><td>in</td><td>999</td></tr>
<tr><th colspan="7">Deals</th></tr>
<tr><td>Time</td><td>Trade</td><td>Symbol</td><td>Type</td><td>Direction</td>
    <td>Commission</td><td>Comment</td></tr>
<tr><td>2024.01.01 00:00</td><td>381</td><td></td><td>balance</td><td></td><td>400</td><td></td></tr>
<tr><td>2024.01.01 01:00</td><td>390</td><td>PRIVATE_INSTRUMENT</td><td>buy</td><td>in</td>
    <td>0.00</td><td>PRIVATE_ROW</td></tr>
<tr><td>2024.01.01 02:00</td><td>391</td><td>PRIVATE_INSTRUMENT</td><td>sell</td><td>out</td>
    <td>0.00</td><td></td></tr>
<tr><td>2024.01.02 03:00</td><td>392</td><td>PRIVATE_INSTRUMENT</td><td>sell</td><td>in/out</td>
    <td>0.00</td><td></td></tr>
<tr><td>2024.01.02 04:00</td><td>393</td><td>PRIVATE_INSTRUMENT</td><td>buy</td><td>out by</td>
    <td>0.00</td><td></td></tr>
<tr><td colspan="5"></td><td>400</td><td></td></tr>
"""


def report(totals, settings="", ledger=""):
    return f"""<!doctype html><html><head><title>Strategy Tester Report</title></head>
    <body><table><tr><th colspan="6">Strategy Tester Report</th></tr>
    <tr><th colspan="6">Settings</th></tr>
    <tr><td>Expert:</td><td><b>PRIVATE_EXPERT</b></td></tr>
    <tr><td>Broker:</td><td>PRIVATE_BROKER</td></tr>
    <tr><td>Parameters:</td><td>PRIVATE_PARAMETERS</td></tr>
    <tr><td>Period:</td><td><b>H1 (2024.01.01 - 2024.02.01)</b></td></tr>
    <tr><td>Currency:</td><td>USD</td></tr>
    <tr><td>Initial Deposit:</td><td>10&nbsp;000.00</td></tr>
    {settings}
    <tr><th colspan="6">Outputs</th></tr>
    <tr><td>History Quality:</td><td>100%</td></tr>
    <tr><td>Net profit:</td><td>17.74</td>
        <td>Equity Drawdown Maximal:</td><td>8.02 (0.08%)</td>
        <td>Balance Drawdown Maximal:</td><td>6.72 (0.07%)</td></tr>
    <tr><td>Profit Factor:</td><td>1.68</td></tr>
    {totals}</table><table>{ledger}</table></body></html>"""


class ReportCliTests(unittest.TestCase):
    def run_checker(self, source, encoding="utf-8", write_output=False):
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp, "PRIVATE_FILENAME.html")
            input_path.write_text(source, encoding=encoding)
            output_path = Path(temp, "review.md")
            command = [sys.executable, "-B", "-m", "tools.mt5_report", str(input_path)]
            if write_output:
                command.extend(["--output", str(output_path)])
            result = subprocess.run(command, cwd=REPO, capture_output=True, encoding="utf-8")
            output = output_path.read_text(encoding="utf-8") if output_path.is_file() else None
            return result, output

    def test_distinct_summary_labels_survive_utf16_file_output(self):
        totals = "<tr><td>Total Trades:</td><td>7</td><td>Total Deals:</td><td>12</td></tr>"
        settings = """
        <tr><td>Modeling:</td><td>Every tick based on real ticks</td></tr>
        <tr><td>Forward:</td><td>1/4</td></tr>
        <tr><td>Forward Period:</td><td>2024.01.25 - 2024.02.01</td></tr>
        <tr><td>Spread:</td><td>Current</td></tr>
        <tr><td>Execution:</td><td>Random Delay</td></tr>
        """
        result, output = self.run_checker(report(totals, settings), "utf-16", write_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("| Trades | Reported | 7 | Total Trades |", output)
        self.assertIn("| Trading deals | Reported | 12 | Total Deals |", output)
        self.assertIn("| Test date window | Reported | 2024-01-01 to 2024-02-01 | Period |", output)
        self.assertIn("| Timeframe | Reported | H1 | Period |", output)
        self.assertIn("| Initial deposit | Reported | 10 000.00 | Initial Deposit |", output)
        self.assertIn("| Tick mode | Reported | Every tick based on real ticks | Modeling |", output)
        self.assertIn("| Forward setting | Reported | 1/4 | Forward |", output)
        self.assertIn("| Forward date window | Reported | 2024-01-25 to 2024-02-01 | Forward Period |", output)
        self.assertIn("| Spread assumption | Reported | Current | Spread |", output)
        self.assertIn("| Execution delay | Reported | Random Delay | Execution |", output)
        self.assertIn("| Maximum equity drawdown | Reported | 8.02 (0.08%) | Equity Drawdown Maximal |", output)
        self.assertIn("| Maximum balance drawdown | Reported | 6.72 (0.07%) | Balance Drawdown Maximal |", output)

    def test_legacy_totals_follow_both_breakdowns_and_the_directional_ledger(self):
        totals = LEGACY_TOTALS.replace("</td><td>2</td>", "</td><td>4</td>", 1)
        totals = totals.replace("</td><td>4</td><td>Profit", "</td><td>2</td><td>Profit", 1)
        result, _ = self.run_checker(report(totals, ledger=LEDGER))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trades | Calculated | 2 |", result.stdout)
        self.assertIn("| Trading deals | Calculated | 4 |", result.stdout)
        self.assertIn("| Duplicate trade labels | Reported | 4 / 2 | Total Trades (appears twice) |", result.stdout)
        self.assertIn("Short Trades (won %)", result.stdout)
        self.assertIn("Profit Trades (% of total)", result.stdout)
        self.assertIn("Deals / Type and Direction", result.stdout)
        self.assertNotIn("PRIVATE_", result.stdout)
        self.assertNotIn("2024.01.02 04:00", result.stdout)

    def test_conflicting_trade_breakdowns_leave_duplicate_totals_unresolved(self):
        totals = LEGACY_TOTALS.replace("1 (50%)", "3 (75%)", 1)
        result, _ = self.run_checker(report(totals, ledger=LEDGER))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trades | Missing |", result.stdout)
        self.assertIn("| Trading deals | Missing |", result.stdout)
        self.assertIn("| Duplicate trade labels | Reported | 2 / 4 |", result.stdout)

    def test_malformed_direction_leaves_duplicate_totals_unresolved(self):
        ledger = LEDGER.replace("<td>out by</td>", "<td></td>")
        result, _ = self.run_checker(report(LEGACY_TOTALS, ledger=ledger))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trades | Missing |", result.stdout)
        self.assertIn("| Trading deals | Missing |", result.stdout)
        self.assertIn("| Directional deal rows | Missing |", result.stdout)

    def test_directional_ledger_must_match_one_duplicate_summary_value(self):
        totals = LEGACY_TOTALS.replace("</td><td>4</td><td>Profit", "</td><td>5</td><td>Profit")
        result, _ = self.run_checker(report(totals, ledger=LEDGER))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trades | Missing |", result.stdout)
        self.assertIn("| Trading deals | Missing |", result.stdout)
        self.assertIn("| Directional deal rows | Calculated | 4 |", result.stdout)

    def test_reported_deal_count_kept_when_ledger_differs(self):
        totals = "<tr><td>Total Trades:</td><td>2</td><td>Total Deals:</td><td>5</td></tr>"
        result, _ = self.run_checker(report(totals, ledger=LEDGER))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trading deals | Reported | 5 | Total Deals |", result.stdout)
        self.assertIn("| Directional deal rows | Calculated | 4 |", result.stdout)
        self.assertIn("The reported deal count differs from the directional deal rows", result.stdout)

    def test_absolute_drawdowns_keep_their_source_labels(self):
        source = report(LEGACY_TOTALS, ledger=LEDGER).replace(
            "<tr><td>Profit Factor:",
            "<tr><td>Balance Drawdown Absolute:</td><td>1.24</td>"
            "<td>Absolute equity drawdown:</td><td>2.73</td></tr><tr><td>Profit Factor:",
        )
        result, _ = self.run_checker(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Absolute balance drawdown | Reported | 1.24 | Balance Drawdown Absolute |", result.stdout)
        self.assertIn("| Absolute equity drawdown | Reported | 2.73 | Absolute equity drawdown |", result.stdout)

    def test_booked_zero_commission_does_not_supply_cost_or_tick_settings(self):
        result, _ = self.run_checker(report(LEGACY_TOTALS, ledger=LEDGER))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Booked trading deal commission | Calculated | 0.00 |", result.stdout)
        self.assertIn("| Commission assumption | Missing |", result.stdout)
        self.assertIn("| Spread assumption | Missing |", result.stdout)
        self.assertIn("| Slippage assumption | Missing |", result.stdout)
        self.assertIn("| Execution delay | Missing |", result.stdout)
        self.assertIn("| Tick mode | Missing |", result.stdout)
        self.assertIn("| Forward date window | Missing |", result.stdout)

    def test_blank_commission_is_missing_instead_of_zero(self):
        ledger = LEDGER.replace("<td>0.00</td>", "<td></td>", 1)
        result, _ = self.run_checker(report(LEGACY_TOTALS, ledger=ledger))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Trading deals | Calculated | 4 |", result.stdout)
        self.assertIn("| Booked trading deal commission | Missing |", result.stdout)

    def test_commission_sum_retains_sign_and_exact_cents(self):
        ledger = LEDGER.replace("<td>0.00</td>", "<td>-0.31</td>", 1)
        ledger = ledger.replace("<td>0.00</td>", "<td>0.12</td>", 1)
        result, _ = self.run_checker(report(LEGACY_TOTALS, ledger=ledger))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Booked trading deal commission | Calculated | -0.19 |", result.stdout)

    def test_unrelated_html_does_not_create_output(self):
        result, output = self.run_checker(
            "<title>Account History</title><table><tr><td>Profit Factor:</td><td>1.2</td></tr></table>",
            write_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("English MT5 Strategy Tester", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIsNone(output)


if __name__ == "__main__":
    unittest.main()
