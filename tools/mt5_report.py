"""Extract review evidence from an English MT5 Strategy Tester HTML report."""

import argparse
import codecs
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path


REPORT_TITLE = "strategy tester report"
COUNT = r"(?:[0-9]{1,3}(?: [0-9]{3})+|[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)"
NUMBER = rf"[+-]?{COUNT}(?:\.[0-9]+)?"
PERCENT = rf"{NUMBER}%"
BREAKDOWN = rf"({COUNT})(?: \({PERCENT}\))?"
MAX_DRAWDOWN = rf"{NUMBER} \({PERCENT}\)"
RELATIVE_DRAWDOWN = rf"{PERCENT} \({NUMBER}\)"
DATE = r"[0-9]{4}[.-][0-9]{2}[.-][0-9]{2}"
DATE_RANGE = rf"({DATE})\s*[-\u2013\u2014]\s*({DATE})"
PERIOD = rf"([MHDW][0-9]+|MN[0-9]+) \({DATE_RANGE}\)"
TICK_MODE = (
    r"every tick(?: based on real ticks)?|real ticks|(?:1 minute|m1) ohlc|"
    r"open prices? only|math calculations"
)
FORWARD_SETTING = rf"no|yes|off|on|disabled|enabled|1/[234]|custom|{DATE}"
SPREAD = rf"current|floating|variable|{NUMBER}(?: (?:points?|pips?))?"
COMMISSION = (
    rf"none|no commission|{PERCENT}|(?:[a-z]{{3}} )?{NUMBER}"
    r"(?: [a-z]{3})?(?: (?:per|/) (?:lot|side|deal|trade))?"
)
SLIPPAGE = rf"none|no slippage|{NUMBER}(?: (?:points?|pips?))?"
DURATION = rf"{NUMBER} ?(?:ms|s)"
DELAY = rf"no delay|random delay|fixed delay|{DURATION}|fixed delay \({DURATION}\)"

BREAKDOWN_LABELS = (
    "Short Trades (won %)",
    "Long Trades (won %)",
    "Profit Trades (% of total)",
    "Loss Trades (% of total)",
)
LEDGER_COUNT_SOURCE = "Deals / Type and Direction (buy and sell rows)"
LEDGER_COMMISSION_SOURCE = "Deals / Commission on directional buy and sell rows"
TRADE_BREAKDOWN_SOURCE = " and ".join(
    (" + ".join(BREAKDOWN_LABELS[:2]), " + ".join(BREAKDOWN_LABELS[2:]))
)


class ReportRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.rows = []
        self.in_title = False
        self.table_depth = 0
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "table":
            self.table_depth += 1
        elif self.table_depth == 1:
            if tag == "tr":
                self.row = []
            elif tag in ("th", "td") and self.row is not None:
                self.cell = []
            elif tag == "br" and self.cell is not None:
                self.cell.append(" ")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "table":
            self.table_depth -= 1
        elif self.table_depth == 1:
            if tag in ("th", "td") and self.cell is not None:
                self.row.append(" ".join("".join(self.cell).split()))
                self.cell = None
            elif tag == "tr" and self.row is not None:
                self.rows.append(self.row)
                self.row = None
                self.cell = None

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.table_depth == 1 and self.cell is not None:
            self.cell.append(data)


def label_key(label):
    return label.rstrip(":").strip().casefold()


def section(row):
    cells = [cell.casefold() for cell in row if cell]
    return cells[0] if len(cells) == 1 else ""


def report_fields(rows):
    fields = defaultdict(list)
    for row in rows:
        if section(row) in {"orders", "deals"}:
            break
        for label, value in zip(row, row[1:]):
            if label.endswith(":"):
                fields[label_key(label)].append((label.rstrip(":"), value))
    return fields


def one_field(fields, labels):
    matches = [item for label in labels for item in fields.get(label_key(label), [])]
    if len(matches) == 1:
        return matches[0]
    return labels[0], ""


def matching(pattern, value):
    return re.fullmatch(pattern, value, flags=re.IGNORECASE | re.ASCII)


def reported(fields, name, pattern, *labels):
    label, value = one_field(fields, labels)
    return evidence(name, value if matching(pattern, value) else None, label)


def evidence(name, value, source, status="Reported"):
    return (name, status, str(value), source) if value is not None else (name, "Missing", "-", source)


def iso_window(start, end):
    try:
        start = date.fromisoformat(start.replace(".", "-"))
        end = date.fromisoformat(end.replace(".", "-"))
    except ValueError:
        return None
    if start < end:
        return f"{start.isoformat()} to {end.isoformat()}"
    return None


def windows(fields):
    period_label, period = one_field(fields, ("Period", "Test Period"))
    timeframe_match = matching(PERIOD, period)
    timeframe = timeframe_match[1].upper() if timeframe_match else None
    window_match = timeframe_match or matching(DATE_RANGE, period)
    window = iso_window(*window_match.groups()[-2:]) if window_match else None

    forward_labels = ("Forward Period", "Forward Test Period", "Forward Testing Period", "Holdout Period")
    forward_label, forward = one_field(fields, forward_labels)
    forward_match = matching(DATE_RANGE, forward)
    forward_window = iso_window(*forward_match.groups()) if forward_match else None
    return [
        evidence("Test date window", window, period_label),
        evidence("Timeframe", timeframe, period_label),
        reported(fields, "Forward setting", FORWARD_SETTING, "Forward", "Forward Mode"),
        evidence("Forward date window", forward_window, forward_label),
    ]


def decimal_value(value):
    if matching(NUMBER, value):
        return Decimal(value.replace(" ", "").replace(",", ""))
    return None


def deal_aggregates(rows):
    columns = None
    count = 0
    commission = Decimal("0.00")
    for row in rows:
        if columns is None:
            header = [label_key(cell) for cell in row]
            if {"time", "type", "direction"}.issubset(header):
                columns = header
            elif any(row):
                return None, None
            continue

        cells = dict(zip(columns, row))
        if cells.get("type", "").casefold() not in {"buy", "sell"}:
            continue
        direction = cells.get("direction", "").casefold()
        if direction not in {"in", "out", "in/out", "inout", "out by", "outby"}:
            return None, None
        count += 1
        amount = decimal_value(cells.get("commission", ""))
        commission = commission + amount if commission is not None and amount is not None else None
    if columns is None:
        return None, None
    return count, format(commission, "f") if count and commission is not None else None


def breakdown_total(fields):
    counts = []
    for label in BREAKDOWN_LABELS:
        _, value = one_field(fields, (label,))
        match = matching(BREAKDOWN, value)
        if not match:
            return None
        counts.append(int(decimal_value(match[1])))
    short, long, wins, losses = counts
    return short + long if short + long == wins + losses else None


def totals(fields, deal_count):
    trades = fields.get("total trades", [])
    trade = reported(fields, "Trades", COUNT, "Total Trades")
    deals = reported(fields, "Trading deals", COUNT, "Total Deals", "(Total Deals)")
    if len(trades) != 2 or "total deals" in fields or "(total deals)" in fields:
        notes = []
        if deals[1] == "Reported" and deal_count is not None and decimal_value(deals[2]) != deal_count:
            notes.append("The reported deal count differs from the directional deal rows.")
        return [trade, deals], notes

    counts = [int(decimal_value(value)) for _, value in trades if matching(COUNT, value)]
    source = "Total Trades (appears twice)"
    shown_counts = " / ".join(str(count) for count in counts) if len(counts) == 2 else None
    duplicate = evidence("Duplicate trade labels", shown_counts, source)
    trade_count = breakdown_total(fields)
    if (
        trade_count is not None
        and deal_count is not None
        and sorted(counts) == sorted((trade_count, deal_count))
    ):
        trade = evidence("Trades", trade_count, f"{source} and {TRADE_BREAKDOWN_SOURCE}", "Calculated")
        deals = evidence("Trading deals", deal_count, f"{source} and {LEDGER_COUNT_SOURCE}", "Calculated")
    else:
        source = f"{source} and reconciliation from summary and ledger"
        trade = evidence("Trades", None, source)
        deals = evidence("Trading deals", None, source)
    return [trade, deals, duplicate], [
        "The duplicate trade labels require agreement among both summary breakdowns and the directional deal count."
    ]


def review(html):
    parser = ReportRows()
    parser.feed(html)
    parser.close()
    fields = report_fields(parser.rows)
    named_report = " ".join("".join(parser.title).casefold().split()) == REPORT_TITLE
    marked_report = any(section(row) == REPORT_TITLE for row in parser.rows)
    summary_labels = {"history quality", "total net profit", "net profit", "profit factor", "total trades", "total deals"}
    if not (named_report or marked_report) or len(summary_labels.intersection(fields)) < 2:
        raise ValueError("Expected an English MT5 Strategy Tester HTML report with a tester summary.")

    deals_start = next((index + 1 for index, row in enumerate(parser.rows) if section(row) == "deals"), None)
    deal_count, commission = deal_aggregates(parser.rows[deals_start:] if deals_start is not None else [])
    count_rows, count_notes = totals(fields, deal_count)
    measurements = [
        *windows(fields),
        reported(fields, "Tick mode", TICK_MODE, "Modeling", "Modelling", "Model", "Tick Mode", "Tick Generation Mode"),
        reported(fields, "History quality", PERCENT, "History Quality"),
        reported(fields, "Currency", r"[a-z]{3}", "Currency"),
        reported(fields, "Initial deposit", NUMBER, "Initial Deposit"),
        reported(fields, "Net profit", NUMBER, "Total Net Profit", "Net Profit"),
        reported(fields, "Gross profit", NUMBER, "Gross Profit"),
        reported(fields, "Gross loss", NUMBER, "Gross Loss"),
        reported(fields, "Profit factor", NUMBER, "Profit Factor"),
        reported(fields, "Absolute balance drawdown", NUMBER, "Balance Drawdown Absolute", "Absolute Balance Drawdown"),
        reported(fields, "Maximum balance drawdown", MAX_DRAWDOWN, "Balance Drawdown Maximal", "Maximal Balance Drawdown"),
        reported(fields, "Relative balance drawdown", RELATIVE_DRAWDOWN, "Balance Drawdown Relative", "Relative Balance Drawdown"),
        reported(fields, "Absolute equity drawdown", NUMBER, "Equity Drawdown Absolute", "Absolute Equity Drawdown"),
        reported(fields, "Maximum equity drawdown", MAX_DRAWDOWN, "Equity Drawdown Maximal", "Maximal Equity Drawdown"),
        reported(fields, "Relative equity drawdown", RELATIVE_DRAWDOWN, "Equity Drawdown Relative", "Relative Equity Drawdown"),
        *count_rows,
        *(reported(fields, label, BREAKDOWN, label) for label in BREAKDOWN_LABELS),
        evidence("Directional deal rows", deal_count, LEDGER_COUNT_SOURCE, "Calculated"),
        evidence("Booked trading deal commission", commission, LEDGER_COMMISSION_SOURCE, "Calculated"),
        reported(fields, "Spread assumption", SPREAD, "Spread", "Spread Setting"),
        reported(fields, "Commission assumption", COMMISSION, "Commission", "Commission Schedule", "Commission Setting"),
        reported(fields, "Slippage assumption", SLIPPAGE, "Slippage", "Slippage Setting"),
        reported(fields, "Execution delay", DELAY, "Execution Delay", "Execution", "Latency", "Delay"),
    ]
    lines = [
        "# MT5 Strategy Tester report review",
        "",
        "| Evidence | Status | Value | Source field |",
        "| --- | --- | --- | --- |",
        *("| " + " | ".join(row) + " |" for row in measurements),
        "",
        "- History quality describes the price data. The tick mode requires a separate setting.",
        "- A forward setting or date window records what the report states. Independent holdout review also requires parameter selection history and results for the separate period.",
        "- Booked commission covers the directional buy and sell rows. The commission schedule requires its own setting.",
        *(f"- {note}" for note in count_notes),
    ]
    return "\n".join(lines) + "\n"


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("report", type=Path, help="UTF-8 or BOM-marked UTF-16 Strategy Tester HTML export")
    cli.add_argument("--output", type=Path, help="write Markdown to this file (defaults to stdout)")
    args = cli.parse_args(argv)
    try:
        data = args.report.read_bytes()
        encoding = "utf-16" if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)) else "utf-8-sig"
        markdown = review(data.decode(encoding))
        if args.output is None:
            sys.stdout.write(markdown)
        elif args.output.resolve() == args.report.resolve():
            raise ValueError("Choose an output file different from the source report.")
        else:
            args.output.write_text(markdown, encoding="utf-8")
    except UnicodeError:
        cli.exit(2, "Could not decode the report. Use a UTF-8 or BOM-marked UTF-16 export.\n")
    except (OSError, ValueError) as error:
        cli.exit(2, f"{error}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
