"""Read snapshots from the active MT5 account or a fictional demo."""

from collections import deque
from importlib import import_module
import math
from threading import Lock
import time


POSITION_SIDES = {0: "Buy", 1: "Sell"}
PENDING_ORDER_SIDES = {
    2: "Buy Limit",
    3: "Sell Limit",
    4: "Buy Stop",
    5: "Sell Stop",
    6: "Buy Stop Limit",
    7: "Sell Stop Limit",
}


def _load_vendor():
    return import_module("MetaTrader5")


def _number(record, name):
    value = getattr(record, name, None)
    if type(value) in (int, float) and math.isfinite(value):
        return value
    return None


def _price(record, name):
    # MT5 uses zero for unset stops and absent quote prices.
    return _number(record, name) or None


def _quote_timestamp(tick):
    milliseconds = _number(tick, "time_msc")
    if milliseconds is not None and milliseconds > 0:
        return int(milliseconds)
    seconds = _number(tick, "time")
    if seconds is not None and seconds > 0:
        return int(seconds * 1000)
    return None


def _digits(metadata):
    digits = getattr(metadata, "digits", None)
    if type(digits) is int and digits >= 0:
        return digits
    return None


def _account_fields(account):
    return {
        "currency": account.currency or None,
        "balance": _number(account, "balance"),
        "equity": _number(account, "equity"),
        "floating_pnl": _number(account, "profit"),
        "free_margin": _number(account, "margin_free"),
        "margin_level": _number(account, "margin_level"),
    }


def _position_fields(position, digits):
    return {
        "ticket": str(position.ticket),
        "symbol": position.symbol,
        "side": POSITION_SIDES[position.type],
        "volume": _number(position, "volume"),
        "entry": _number(position, "price_open"),
        "price": _price(position, "price_current"),
        "stop_loss": _price(position, "sl"),
        "take_profit": _price(position, "tp"),
        "pnl": _number(position, "profit"),
        "swap": _number(position, "swap"),
        "digits": digits,
    }


def _order_fields(order, digits):
    return {
        "ticket": str(order.ticket),
        "symbol": order.symbol,
        "side": PENDING_ORDER_SIDES[order.type],
        "volume": _number(order, "volume_current"),
        "price": _number(order, "price_open"),
        "stop_loss": _price(order, "sl"),
        "take_profit": _price(order, "tp"),
        "digits": digits,
    }


class _Unavailable(Exception):
    """An MT5 state that can be described without exposing vendor error details."""


class LiveProvider:
    def __init__(
        self, terminal=None, *, history_limit=360, load_vendor=_load_vendor,
        clock=time.time, monotonic=time.monotonic,
    ):
        self._terminal = terminal
        self._load_vendor = load_vendor
        self._clock = clock
        self._monotonic = monotonic
        self._history = deque(maxlen=history_limit)
        self._lock = Lock()
        self._vendor = None
        self._initialized = False
        self._identity = None
        self._retry_at = 0
        self._message = None

    def _connect(self):
        if self._vendor is None:
            try:
                self._vendor = self._load_vendor()
            except Exception:
                raise _Unavailable(
                    "The MetaTrader5 Python package could not load. Install it in this Python environment."
                ) from None

        args = () if self._terminal is None else (self._terminal,)
        if not self._vendor.initialize(*args, timeout=5000):
            raise _Unavailable("Could not reach MetaTrader 5. Open your terminal or check the terminal path.")
        self._initialized = True

    def _disconnect(self):
        if self._vendor is not None:
            try:
                self._vendor.shutdown()
            except Exception:
                pass
        self._initialized = False
        self._identity = None
        self._history.clear()

    def _unavailable(self, message):
        self._disconnect()
        self._message = message
        self._retry_at = self._monotonic() + 3
        return self._empty_snapshot()

    def _empty_snapshot(self):
        return {
            "mode": "live", "status": "unavailable", "message": self._message,
            "timestamp": None, "account": None, "positions": [], "orders": [],
            "quotes": [], "equity_history": [],
        }

    def _current_account(self):
        terminal = self._vendor.terminal_info()
        if terminal is None:
            raise _Unavailable("MetaTrader 5 did not respond. Open the terminal to reconnect.")
        if not terminal.connected:
            raise _Unavailable("MetaTrader 5 is offline. Check the connection in your terminal.")

        account = self._vendor.account_info()
        if account is None or not account.login:
            raise _Unavailable("No MT5 account is available. Sign in to an account in your terminal.")
        return account

    def _quote(self, symbol):
        # Some broker symbols have no available market data. Preserve the trade rows.
        try:
            metadata = self._vendor.symbol_info(symbol)
        except Exception:
            metadata = None
        try:
            tick = self._vendor.symbol_info_tick(symbol)
        except Exception:
            tick = None
        return {
            "symbol": symbol, "bid": _price(tick, "bid"), "ask": _price(tick, "ask"),
            "digits": _digits(metadata), "timestamp": _quote_timestamp(tick),
        }

    def _read_snapshot(self):
        account = self._current_account()
        identity = (account.login, account.server)
        positions = self._vendor.positions_get()
        orders = self._vendor.orders_get()
        if positions is None or orders is None:
            raise _Unavailable("MetaTrader 5 did not return position or order data. Retrying automatically.")

        positions = [position for position in positions if position.type in POSITION_SIDES]
        orders = [order for order in orders if order.type in PENDING_ORDER_SIDES]
        symbols = dict.fromkeys(trade.symbol for trade in positions + orders)
        quotes = {symbol: self._quote(symbol) for symbol in symbols}

        # Terminal users can switch accounts while these separate reads are in progress.
        account = self._current_account()
        if identity != (account.login, account.server):
            raise _Unavailable("The active MT5 account changed. Refreshing the dashboard.")
        if identity != self._identity:
            self._history.clear()
            self._identity = identity

        timestamp = int(self._clock() * 1000)
        account_data = _account_fields(account)
        equity = account_data["equity"]
        if equity is not None:
            while self._history and timestamp <= self._history[-1][0]:
                self._history.pop()
            self._history.append((timestamp, equity))

        return {
            "mode": "live", "status": "connected", "message": None,
            "timestamp": timestamp, "account": account_data,
            "positions": [
                _position_fields(position, quotes[position.symbol]["digits"]) for position in positions
            ],
            "orders": [_order_fields(order, quotes[order.symbol]["digits"]) for order in orders],
            "quotes": list(quotes.values()),
            "equity_history": [list(point) for point in self._history],
        }

    def snapshot(self):
        with self._lock:
            if self._monotonic() < self._retry_at:
                return self._empty_snapshot()
            try:
                if not self._initialized:
                    self._connect()
                return self._read_snapshot()
            except _Unavailable as error:
                return self._unavailable(str(error))
            except Exception:
                return self._unavailable("Could not read the MetaTrader 5 terminal. Retrying automatically.")

    def close(self):
        with self._lock:
            self._disconnect()


class DemoProvider:
    def __init__(self, *, clock=time.time):
        self._clock = clock

    def snapshot(self):
        timestamp = int(self._clock() * 1000)
        equity = 25486.32
        equity_values = (
            24926.72, 24942.52, 24915.87, 24979.87, 25023.17, 25002.29,
            24982.30, 25097.82, 25125.38, 25108.22, 25167.61, 25161.30,
            25187.94, 25169.05, 25109.71, 25152.21, 25190.80, 25263.77,
            25244.96, 25313.02, 25284.78, 25295.19, 25214.49, 25235.66,
            25274.15, 25322.49, 25303.24, 25360.76, 25351.55, 25407.93,
            25394.07, 25426.52, 25461.57, 25432.72, 25456.91, equity,
        )
        start = timestamp - (len(equity_values) - 1) * 60000
        return {
            "mode": "demo", "status": "connected", "message": None,
            "timestamp": timestamp,
            "account": {
                "currency": "USD", "balance": 25000.0, "equity": equity,
                "floating_pnl": 486.32, "free_margin": 24366.32, "margin_level": 2275.56,
            },
            "positions": [
                {"ticket": "240001", "symbol": "EURUSD", "side": "Buy", "volume": 0.6,
                 "entry": 1.08145, "price": 1.08670, "stop_loss": 1.07920, "take_profit": 1.09000,
                 "pnl": 315.00, "swap": -2.18, "digits": 5},
                {"ticket": "240002", "symbol": "XAUUSD", "side": "Buy", "volume": 0.10,
                 "entry": 2323.62, "price": 2349.11, "stop_loss": 2314.00, "take_profit": 2365.00,
                 "pnl": 254.90, "swap": -1.40, "digits": 2},
                {"ticket": "240003", "symbol": "USDJPY", "side": "Sell", "volume": 0.20,
                 "entry": 149.299, "price": 149.899, "stop_loss": 150.200, "take_profit": 148.150,
                 "pnl": -80.00, "swap": 0.0, "digits": 3},
            ],
            "orders": [
                {"ticket": "240012", "symbol": "EURUSD", "side": "Buy Limit", "volume": 0.20,
                 "price": 1.08250, "stop_loss": 1.07900, "take_profit": 1.09000, "digits": 5},
            ],
            "quotes": [
                {"symbol": "EURUSD", "bid": 1.08670, "ask": 1.08682, "digits": 5, "timestamp": timestamp},
                {"symbol": "XAUUSD", "bid": 2349.11, "ask": 2349.45, "digits": 2, "timestamp": timestamp},
                {"symbol": "USDJPY", "bid": 149.882, "ask": 149.899, "digits": 3, "timestamp": timestamp},
            ],
            "equity_history": [[start + index * 60000, value] for index, value in enumerate(equity_values)],
        }
