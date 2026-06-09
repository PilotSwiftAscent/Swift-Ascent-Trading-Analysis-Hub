# Trading Documentation Workflow

Use this workflow when turning a rough trading idea into clean documentation.

## Step 1: Capture The Raw Idea

Write the strategy exactly as it currently exists, even if it is messy.

## Step 2: Define The Strategy Type

Choose one primary type:

- Trend continuation
- Breakout
- Reversal
- Mean reversion
- Volatility compression breakout
- Session breakout
- Hybrid strategy

## Step 3: Define The Market Condition

Explain the condition where the strategy should perform best.

## Step 4: Define Entry Rules

Separate buy and sell rules.

Every rule must be testable.

Bad example:

```text
Buy when market looks strong.
```

Better example:

```text
Buy only after price closes above the range high by at least 0.3 times ATR, while the higher timeframe trend is bullish.
```

## Step 5: Define Exit Rules

Include:

- Stop loss
- Take profit
- Break even
- Trailing stop
- Early exit conditions

## Step 6: Define Risk Rules

Include:

- Risk per trade
- Maximum trades per day
- Daily loss limit
- Daily profit limit
- Maximum open trades
- Cooldown after loss

## Step 7: Define Avoid Trade Conditions

Include when the strategy must not trade.

## Step 8: Developer Handoff

Use the Trading Documentation Auditor to check whether the final document can be coded without guessing.
