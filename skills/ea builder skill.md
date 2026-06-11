# EA Builder Skill

## Purpose

The EA Builder Skill converts professional trading concepts into mechanical, testable, platform-ready Expert Advisor logic.

This skill coordinates the repository personas so that trading ideas are not rushed into code before they are clear, measurable, risk-controlled, and backtest-ready.

## Core Principle

A trading idea is not EA-ready until it can be expressed as rules.

Every rule must be:

- Observable.
- Measurable.
- Non-repainting.
- Platform-compatible.
- Risk-controlled.
- Backtestable.
- Efficient to calculate.
- Clear enough for a developer or AI coding assistant to implement correctly.

## EA Development Pipeline

### 1. Source Idea Intake

Identify the concept being used.

Examples:

- Naked Forex-style rejection.
- KAMA efficiency filter.
- Liquidity sweep.
- Compression expansion.
- Breakout retest.
- Session manipulation.
- Trend continuation.
- Mean reversion.
- Hedge protection.

### 2. Concept Translation

Translate the trading idea into plain market behavior.

Weak version:

```text
The market is manipulated before the real move.
```

EA-ready version:

```text
Price sweeps a previous swing high, closes back below the level, then produces a bearish displacement candle with enough range expansion.
```

### 3. Mechanical Rule Design

Define exactly what the EA can detect.

Required rule categories:

- Market regime rule.
- Entry setup rule.
- Confirmation rule.
- Invalidation rule.
- Stop loss rule.
- Take profit rule.
- Trade management rule.
- Risk control rule.
- No-trade rule.

### 4. Platform Selection

Specify the target platform before coding.

Examples:

- MT4 / MQL4.
- MT5 / MQL5.
- TradingView / Pine Script.
- Python broker API.
- cTrader / cAlgo.

The skill must reject platform-mixed logic.

### 5. Risk and Exposure Design

Define:

- Risk per trade.
- Maximum open trades.
- Maximum symbol exposure.
- Maximum daily loss.
- Maximum drawdown rule.
- Break-even rule.
- Partial close rule.
- Trailing stop rule.
- Hedge rule if applicable.

### 6. Efficiency Design

The EA should avoid overcalculations.

Require:

- New-candle control where appropriate.
- Cached indicator handles where platform requires it.
- Minimal CopyBuffer usage.
- No repeated full-history calculations every tick.
- No alert spam.
- No duplicate execution paths.
- Early exits for invalid market conditions.

### 7. Backtest and Validation Plan

Before coding is considered complete, define:

- In-sample test.
- Out-of-sample test.
- Walk-forward test.
- Monte Carlo stress test.
- Parameter stability test.
- Forward-test plan.

## Required Persona Order

Use the personas in this order for EA creation:

1. Trading Documentation Auditor.
2. Market Regime Analyst.
3. Market Pattern and Algorithmic Behavior Analyst.
4. Professional Trading Advisor.
5. Institutional Hedging and Exposure Analyst.
6. EA Platform and Code Efficiency Advisor.
7. Quant Performance Analyst.
8. Financial Statistician.
9. Robust Backtesting and Validation Advisor.
10. Risk and Portfolio Analyst.

## Output Format

```text
EA Builder Skill Output

Strategy Concept:
-

Target Platform:
-

Market Regime:
-

Mechanical Entry Rules:
-

Mechanical Exit Rules:
-

Risk and Exposure Rules:
-

No-Trade Conditions:
-

Efficiency Requirements:
-

Backtest Requirements:
-

Implementation Warnings:
-

EA Readiness Verdict:
Ready for coding / Needs rules / Needs risk design / Needs validation plan / Not ready
```

## Skill Rule

Do not allow a trading idea to become code until it is measurable, platform-correct, efficient, and testable.
