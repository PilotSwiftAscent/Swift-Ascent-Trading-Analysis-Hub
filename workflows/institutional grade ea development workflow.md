# Institutional Grade EA Development Workflow

## Purpose

This workflow converts a trading idea into professional EA-ready logic using the repository personas and skills.

It is designed to prevent weak, vague, platform-mismatched, overfit, or risk-heavy strategies from reaching live trading.

## Core Principle

A trading idea must pass through strategy clarity, market behavior analysis, trade quality review, exposure control, platform validation, code-efficiency review, and robustness testing before live deployment.

## Workflow Order

### 1. Source Knowledge Map

Identify the source concept or trading school behind the idea.

Examples:

- Naked Forex-style rejection.
- KAMA adaptive filtering.
- ICT-style liquidity sweep.
- Wyckoff-style accumulation or distribution.
- Quant validation principle.

Output required:

- Source concept.
- Original meaning in plain language.
- Observable market behavior.
- Mechanical EA translation.

### 2. Trading Documentation Auditor

Clarify the strategy before analysis.

Output required:

- Entry rules.
- Exit rules.
- Risk rules.
- Timeframe.
- Symbol type.
- No-trade conditions.
- Assumptions.

### 3. Strategy Rule Conversion Skill

Convert discretionary language into measurable EA rules.

Output required:

- Mechanical entry rule.
- Confirmation rule.
- Invalidation rule.
- Stop loss rule.
- Target rule.
- No-trade rule.

### 4. Market Regime Analyst

Identify which market conditions the strategy is designed for.

Output required:

- Trending, ranging, choppy, volatile, or compression environment.
- Suitable and unsuitable market conditions.
- Regime filter recommendations.

### 5. Market Pattern and Algorithmic Behavior Analyst

Review whether the strategy is based on repeatable observable market behavior.

Output required:

- Pattern family.
- Liquidity behavior.
- Compression or expansion behavior.
- Fakeout risk.
- EA detection possibility.

### 6. Professional Trading Advisor

Review the actual trade logic and price-action quality.

Output required:

- Key zones.
- KAMA read if used.
- Price-action read.
- Trade quality rating.
- Invalidation logic.

### 7. Institutional Hedging and Exposure Analyst

Review account-level exposure and hedge behavior.

Output required:

- Net exposure risk.
- Correlation risk.
- Hedge requirement.
- Position stacking risk.
- Basket drawdown protection.

### 8. EA Builder Skill

Assemble the approved logic into EA-ready specifications.

Output required:

- Target platform.
- Mechanical rules.
- Risk controls.
- Efficiency requirements.
- Backtest requirements.
- EA readiness verdict.

### 9. EA Platform and Code Efficiency Advisor

Review platform compatibility and performance efficiency.

Output required:

- Target platform match.
- MT4/MT5 compliance.
- Execution safety.
- Overcalculation risks.
- Broker compatibility risks.

### 10. Quant Performance Analyst

Review backtest performance quality.

Output required:

- Profit factor.
- Win rate.
- Drawdown.
- Trade count.
- Equity curve stability.
- Outlier dependency.

### 11. Financial Statistician

Review statistical reliability.

Output required:

- Sample size concerns.
- Significance concerns.
- Variance.
- Expectancy.
- Confidence level.

### 12. Robust Backtesting and Validation Advisor

Review in-sample, out-of-sample, walk-forward, Monte Carlo, and parameter stability results.

Output required:

- In-sample result.
- Out-of-sample result.
- Walk-forward result.
- Monte Carlo result.
- Parameter stability.
- Edge confidence.

### 13. Risk and Portfolio Analyst

Make the final capital-protection decision.

Output required:

- Risk exposure.
- Max drawdown concern.
- Daily loss protection.
- Account suitability.
- Forward-test readiness.

### 14. Validation and Rejection Skill

Make the final approval or rejection decision.

Output required:

- Approved for coding.
- Approved for backtesting.
- Approved for forward testing.
- Not approved.

## Final EA Readiness Checklist

Before coding:

- Strategy rules are clear.
- Target platform is defined.
- Rules are measurable.
- Risk model is defined.
- No-trade conditions are defined.

Before backtesting:

- EA compiles without errors.
- EA matches the target platform.
- The EA does not overcalculate.
- Duplicate entries are controlled.
- Broker constraints are respected.

Before forward testing:

- In-sample and out-of-sample tests are complete.
- Monte Carlo stress test is complete.
- Parameter stability is acceptable.
- Drawdown is controlled.
- Execution assumptions are realistic.

Before live trading:

- Forward testing is complete.
- Broker execution is verified.
- Risk limits are active.
- Emergency stop rules exist.
- The trader understands the expected drawdown and losing streak behavior.

## Workflow Rule

Do not rush from idea to code.

Professional EA development requires structured translation, platform correctness, efficiency, validation, and capital protection.
