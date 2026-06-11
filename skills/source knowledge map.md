# Source Knowledge Map

## Purpose

The Source Knowledge Map defines how professional trading concepts, books, market educators, and systematic trading ideas may be used inside this repository.

The goal is to draw intelligence from respected sources while keeping all outputs original, ethical, testable, and suitable for EA development.

## Core Rule

Use concepts, not copied text.

Do not copy protected book passages, paid course material, proprietary wording, or private training content.

Summarize ideas in original language and convert them into measurable trading logic.

## Approved Source Usage

Sources may be used for:

- Concept inspiration.
- Market behavior frameworks.
- Risk management principles.
- Backtesting discipline.
- Strategy validation methods.
- Trader psychology principles.
- Systematic trading structure.

Sources must not be used for:

- Copying copyrighted material.
- Claiming guaranteed profitability.
- Claiming exact institutional intent.
- Recreating paid/private course content.
- Presenting discretionary ideas as proven mechanical edge without testing.

## Example Knowledge Families

### Naked Forex-Style Price Action

Useful for:

- Clean chart reading.
- Market zones.
- Rejection behavior.
- Failed breakouts.
- Room-to-move logic.
- Pattern context.

EA translation:

- Define zones mechanically.
- Define rejection with wick/body/close rules.
- Define failed breakout behavior.
- Require target space before entry.

### Kaufman Adaptive Methods

Useful for:

- Adaptive moving average logic.
- Efficiency ratio thinking.
- Trend efficiency filtering.
- Noise reduction.
- Systematic market adaptation.

EA translation:

- Use KAMA as a filter, not a standalone trigger.
- Detect clean movement versus noisy movement.
- Use slope and price relation to support regime logic.

### ICT-Style Liquidity Concepts

Useful for:

- Liquidity sweeps.
- Displacement.
- Fair value gap-style imbalance thinking.
- Market structure shifts.
- Session timing.
- Premium and discount logic.

EA translation:

- Avoid vague claims about smart money.
- Define sweeps, closes, displacement, and invalidation mechanically.
- Require objective confirmation.

### Wyckoff-Style Market Structure

Useful for:

- Accumulation.
- Distribution.
- Springs.
- Upthrusts.
- Effort versus result.
- Range behavior.

EA translation:

- Convert phases into measurable range, volume if available, rejection, and breakout behavior.

### Trader Psychology Sources

Useful for:

- Discipline.
- Probabilistic thinking.
- Avoiding revenge trading.
- Consistency.
- No-trade decisions.

EA translation:

- Build rules that prevent emotional overrides.
- Define daily limits.
- Define cooldowns.
- Define maximum consecutive-loss behavior.

### Quant and Validation Sources

Useful for:

- Overfitting awareness.
- Walk-forward testing.
- Monte Carlo stress testing.
- Parameter stability.
- Out-of-sample validation.

EA translation:

- Require robustness tests before trusting the system.
- Reject strategies that only work in optimized windows.

## Source-to-Rule Conversion Template

```text
Source Concept:
-

Original Meaning in Plain Language:
-

Observable Market Behavior:
-

Mechanical EA Rule:
-

Required Filters:
-

Invalidation Rule:
-

Backtest Requirement:
-

Risk Warning:
-
```

## Knowledge Map Rule

Professional concepts are starting points, not proof.

Every borrowed idea must become testable logic before it is used in an EA.
