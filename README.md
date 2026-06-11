# Swift Ascent Trading Analysis Hub

A GitHub-ready repository containing ten professional trading personas, reusable EA-building skills, templates, and workflows designed to improve trading documentation, strategy analysis, EA development, backtest validation, platform compliance, and risk control.

This repository is built for traders, EA developers, quant researchers, analysts, and trading system builders who need a structured way to review ideas before they become live systems.

## Purpose

The purpose of this repository is to create a repeatable review system for trading strategies, trading tools, and Expert Advisor development.

Instead of asking a model to simply “review a strategy,” each persona or skill focuses on a specific role:

1. Quant Performance Analyst
2. Financial Statistician
3. Risk and Portfolio Analyst
4. Market Regime Analyst
5. Trading Documentation Auditor
6. Professional Trading Advisor
7. Market Pattern and Algorithmic Behavior Analyst
8. Institutional Hedging and Exposure Analyst
9. EA Platform and Code Efficiency Advisor
10. Robust Backtesting and Validation Advisor

Together, these resources help detect weak assumptions, poor testing, overfitting, vague strategy rules, platform mismatch, inefficient code, poor risk control, unclear trade logic, weak market context, fragile hedge behavior, and missing documentation.

## Repository Structure

```text
analysis personas/
│
├── README.md
├── LICENSE
│
├── personas/
│   ├── 01 quant performance analyst.md
│   ├── 02 financial statistician.md
│   ├── 03 risk and portfolio analyst.md
│   ├── 04 market regime analyst.md
│   ├── 05 trading documentation auditor.md
│   ├── 06 professional trading advisor.md
│   ├── 07 market pattern and algorithmic behavior analyst.md
│   ├── 08 institutional hedging and exposure analyst.md
│   ├── 09 ea platform and code efficiency advisor.md
│   └── 10 robust backtesting and validation advisor.md
│
├── skills/
│   ├── ea builder skill.md
│   ├── source knowledge map.md
│   ├── strategy rule conversion skill.md
│   └── validation and rejection skill.md
│
├── templates/
│   ├── persona usage template.md
│   ├── backtest review template.md
│   ├── strategy documentation template.md
│   └── quant audit report template.md
│
├── workflows/
│   ├── full strategy review workflow.md
│   ├── ea backtest review workflow.md
│   ├── trading documentation workflow.md
│   └── institutional grade ea development workflow.md
│
└── examples/
    └── example prompt.md
```

## Best Use Cases

Use this repository when you need to:

- Review an EA before coding or refactoring.
- Convert a discretionary trading idea into mechanical EA rules.
- Audit a trading strategy after a backtest.
- Check whether results are statistically meaningful.
- Review risk exposure before live trading.
- Review chart-based trade ideas before execution.
- Validate whether an EA is built for the correct platform.
- Check whether MT4 and MT5 logic are being mixed incorrectly.
- Reduce overcalculation and inefficient EA structure.
- Review in-sample, out-of-sample, walk-forward, and Monte Carlo test quality.
- Prepare developer-ready prompts for any capable AI assistant, coding assistant, or documentation workflow.
- Build professional trading documentation for clients, partners, or internal use.

## Recommended EA Development Order

For institutional-grade EA development, use the resources in this order:

1. Source Knowledge Map
2. Trading Documentation Auditor
3. Strategy Rule Conversion Skill
4. Market Regime Analyst
5. Market Pattern and Algorithmic Behavior Analyst
6. Professional Trading Advisor
7. Institutional Hedging and Exposure Analyst
8. EA Builder Skill
9. EA Platform and Code Efficiency Advisor
10. Quant Performance Analyst
11. Financial Statistician
12. Robust Backtesting and Validation Advisor
13. Risk and Portfolio Analyst
14. Validation and Rejection Skill

This order moves from source concept to strategy clarity, market behavior, EA-ready rules, platform correctness, performance quality, statistical reliability, robustness validation, and final capital protection.

## Core Principle

A profitable backtest is not enough.

A strategy should also have:

- Clear rules
- Enough trades
- Stable performance
- Controlled drawdown
- Realistic execution assumptions
- Symbol and timeframe awareness
- Clean market-context logic
- Correct platform targeting
- Efficient code structure
- In-sample and out-of-sample validation
- Monte Carlo stress testing
- Risk controls that survive losing streaks
- Documentation clear enough for a developer to implement correctly

## How To Use

Copy the persona, skill, or workflow prompt you need, then paste your trading strategy, EA logic, backtest report, chart idea, or documentation underneath it.

For a complete EA development review, use the institutional grade EA development workflow inside the workflows folder.

## Important Note

These personas and skills do not guarantee profitable trading. They are designed to improve analysis quality, reduce weak assumptions, protect capital, improve platform correctness, and make strategy development more disciplined.
