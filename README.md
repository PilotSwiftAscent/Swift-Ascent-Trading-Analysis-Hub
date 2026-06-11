# Swift Ascent Trading Analysis Hub

A GitHub-ready repository containing 6 professional personas designed to improve trading documentation, strategy analysis, financial statistics, backtest review, and quantification workflows.

This repository is built for traders, EA developers, quant researchers, analysts, and trading system builders who need a structured way to review ideas before they become live systems.

## Purpose

The purpose of this repository is to create a repeatable review system for trading strategies and trading tools.

Instead of asking a model to simply “review a strategy,” each persona focuses on a specific role:

1. Quant Performance Analyst
2. Financial Statistician
3. Risk and Portfolio Analyst
4. Market Regime Analyst
5. Trading Documentation Auditor
6. Professional Trading Advisor

Together, these personas help detect weak assumptions, poor testing, overfitting, vague strategy rules, poor risk control, and missing documentation.

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
│   └── 05 trading documentation auditor.md
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
│   └── trading documentation workflow.md
│
└── examples/
    └── example prompt.md
```

## Best Use Cases

Use this repository when you need to:

- Review an EA before coding or refactoring.
- Audit a trading strategy after a backtest.
- Convert a rough trading idea into structured documentation.
- Check whether results are statistically meaningful.
- Review risk exposure before live trading.
- Prepare developer-ready prompts for Codex or another coding assistant.
- Build professional trading documentation for clients, partners, or internal use.

## Recommended Review Order

For best results, use the personas in this order:

1. Trading Documentation Auditor
2. Market Regime Analyst
3. Quant Performance Analyst
4. Financial Statistician
5. Risk and Portfolio Analyst

This order moves from strategy clarity to market fit, then performance, statistical reliability, and finally capital protection.

## Core Principle

A profitable backtest is not enough.

A strategy should also have:

- Clear rules
- Enough trades
- Stable performance
- Controlled drawdown
- Realistic execution assumptions
- Symbol and timeframe awareness
- Risk controls that survive losing streaks
- Documentation clear enough for a developer to implement correctly

## How To Use

Copy the persona prompt you need, then paste your trading strategy, EA logic, backtest report, or documentation underneath it.

For a complete review, use the full strategy review workflow inside the workflows folder.

## Important Note

These personas do not guarantee profitable trading. They are designed to improve analysis quality, reduce weak assumptions, and make strategy development more disciplined.
