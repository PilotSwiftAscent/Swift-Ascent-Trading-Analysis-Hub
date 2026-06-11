# Validation and Rejection Skill

## Purpose

The Validation and Rejection Skill defines when a trading idea, EA rule, backtest, or optimization result should be rejected before it reaches live trading.

This skill protects the trader from forcing weak ideas into production.

## Core Principle

A rejected idea saves capital.

The goal is not to approve every strategy. The goal is to identify which ideas deserve more testing and which ideas should be abandoned, rewritten, or simplified.

## Rejection Categories

### 1. Rule Rejection

Reject the idea if:

- Entry rules are vague.
- Exit rules are missing.
- Stop loss logic is arbitrary.
- The setup depends on hindsight.
- The idea cannot be coded objectively.
- The strategy has no no-trade condition.

### 2. Platform Rejection

Reject the build if:

- MT4 and MT5 code are mixed.
- The wrong language is used for the target platform.
- The EA uses unsupported functions.
- Broker conditions are ignored.
- Code is too inefficient for live execution.

### 3. Risk Rejection

Reject the strategy if:

- Drawdown is too high for the intended user.
- Risk per trade is excessive.
- Correlated exposure is uncontrolled.
- Position stacking has no limit.
- Hedge logic traps drawdown instead of reducing risk.
- Daily loss and maximum drawdown rules are missing.

### 4. Backtest Rejection

Reject or downgrade the result if:

- Trade count is too low.
- Out-of-sample testing is missing.
- Monte Carlo testing is missing.
- Results collapse under realistic spread or slippage.
- Equity curve depends on a small number of outlier trades.
- Parameter changes destroy performance.
- The strategy only works in one optimized market window.

### 5. Live Readiness Rejection

Reject live deployment if:

- Forward testing is missing.
- Broker execution has not been tested.
- Spread conditions are not realistic.
- The EA has unresolved compile warnings or runtime errors.
- The EA lacks emergency stop behavior.
- The user does not understand the expected drawdown and losing streak behavior.

## Approval Levels

Use these levels:

### Approved for Coding

The logic is clear enough to build but still needs testing.

### Approved for Backtesting

The EA is platform-correct and safe enough to test.

### Approved for Forward Testing

The EA has survived initial robustness testing and can be tested on demo or controlled live conditions.

### Not Approved

The idea or EA has issues that must be fixed first.

## Output Format

```text
Validation and Rejection Review

Review Area:
Idea / Rules / Code / Backtest / Risk / Live Readiness

Approval Level:
Approved for Coding / Approved for Backtesting / Approved for Forward Testing / Not Approved

Reasons for Approval or Rejection:
-

Critical Issues:
-

Required Fixes:
-

Retest Requirements:
-

Final Decision:
```

## Skill Rule

Do not be afraid to reject weak work. The framework is strongest when it blocks fragile strategies before they reach live trading.
