# Strategy Rule Conversion Skill

## Purpose

The Strategy Rule Conversion Skill converts discretionary trading ideas into precise, mechanical rules that can be coded, tested, and rejected if they fail.

This skill exists because many trading concepts sound strong in plain language but fail when translated into EA logic.

## Core Principle

If a rule cannot be measured, it cannot be trusted by an EA.

A good EA rule must define:

- What is being measured.
- Which timeframe is used.
- Which candle or data point confirms the rule.
- Whether the rule is checked on every tick or only on a new candle.
- What invalidates the setup.
- What blocks the setup.

## Conversion Process

### 1. Identify the Discretionary Statement

Example:

```text
Enter after a strong rejection from support.
```

### 2. Define the Market Object

Example:

```text
Support is the lowest low of the previous 20 candles that has been retested at least once.
```

### 3. Define the Trigger

Example:

```text
A rejection candle must wick below support and close back above support.
```

### 4. Define Confirmation

Example:

```text
The next candle must close bullish or break the rejection candle high.
```

### 5. Define Invalidation

Example:

```text
The setup is invalid if price closes below the rejection candle low before entry.
```

### 6. Define Trade Management

Example:

```text
Stop loss below rejection candle low. Take profit at next resistance or fixed R multiple if enough room exists.
```

## Required Rule Categories

Every strategy must define:

- Market regime filter.
- Entry setup.
- Entry confirmation.
- Stop loss.
- Take profit.
- Break-even rule.
- Partial close rule if used.
- Trailing rule if used.
- Time filter.
- Spread filter.
- No-trade conditions.
- Exit conditions.
- Risk controls.

## Bad Rule Examples

Reject vague rules such as:

- Enter when the market looks strong.
- Avoid choppy conditions.
- Trade when institutions are buying.
- Buy after manipulation.
- Sell when price is exhausted.
- Use smart money confirmation.

These must be translated into measurable behavior before coding.

## Output Format

```text
Strategy Rule Conversion Review

Original Idea:
-

Vague Parts Found:
-

Mechanical Entry Rule:
-

Mechanical Confirmation Rule:
-

Mechanical Exit Rule:
-

Invalidation Rule:
-

No-Trade Rule:
-

Data Needed:
-

EA Coding Readiness:
Ready / Needs detail / Too discretionary / Not suitable
```

## Skill Rule

Do not allow emotional, visual, or hindsight-based language to pass as EA-ready logic.
