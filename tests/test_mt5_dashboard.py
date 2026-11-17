import contextlib
import http.client
import importlib
import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
from threading import Barrier, BrokenBarrierError, Thread
from types import SimpleNamespace
import unittest


class FakeMT5:
    def __init__(self):
        self.can_initialize = True
        self.connected = True
        self.initializations = []
        self.closed = 0
        self.account = SimpleNamespace(
            login=1234567890,
            server="Private-Broker-Server",
            name="Private Account Holder",
            company="Private Broker Company",
            currency="USD",
            balance=10000.0,
            equity=10193.0,
            profit=193.0,
            margin=210.0,
            margin_free=9983.0,
            margin_level=4853.81,
        )
        self.positions = (
            SimpleNamespace(
                ticket=9007199254740999,
                symbol="EURUSD.pro",
                type=0,
                volume=0.2,
                price_open=1.08,
                price_current=1.088,
                sl=0.0,
                tp=1.092,
                profit=160.0,
                swap=-2.0,
                comment="Private Position Comment",
            ),
            SimpleNamespace(
                ticket=101,
                symbol="EURUSD.pro",
                type=1,
                volume=0.1,
                price_open=1.0915,
                price_current=1.0882,
                sl=1.094,
                tp=0.0,
                profit=33.0,
                swap=0.0,
            ),
        )
        self.orders = (
            SimpleNamespace(
                ticket=82,
                symbol="USDJPY.pro",
                type=7,
                volume_current=0.15,
                volume_initial=0.20,
                price_open=153.525,
                price_stoplimit=153.625,
                sl=0.0,
                tp=153.0,
            ),
            SimpleNamespace(ticket=83, symbol="MarketOnly", type=0),
        )
        self.quote_symbols = []

    def initialize(self, *args, **kwargs):
        self.initializations.append((args, kwargs))
        return self.can_initialize

    def shutdown(self):
        self.closed += 1

    def terminal_info(self):
        return SimpleNamespace(connected=self.connected)

    def account_info(self):
        return self.account

    def positions_get(self):
        return self.positions

    def orders_get(self):
        return self.orders

    def symbol_info(self, symbol):
        if symbol == "EURUSD.pro":
            return SimpleNamespace(digits=5)
        return None

    def symbol_info_tick(self, symbol):
        self.quote_symbols.append(symbol)
        if symbol == "EURUSD.pro":
            return SimpleNamespace(bid=1.088, ask=1.0882, time_msc=1760020000123)
        return SimpleNamespace(bid=153.542, ask=float("nan"), time=1760020001)


def dashboard_module(test, name):
    try:
        return importlib.import_module(f"tools.mt5_dashboard.{name}")
    except ModuleNotFoundError as error:
        if error.name not in {"tools", "tools.mt5_dashboard", f"tools.mt5_dashboard.{name}"}:
            raise
        test.fail(f"Dashboard {name} module is missing")


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.provider_module = dashboard_module(self, "provider")
        self.mt5 = FakeMT5()
        self.now = 1760020000.5
        self.retry_time = 100.0

    def live(self, **options):
        return self.provider_module.LiveProvider(
            load_vendor=options.pop("load_vendor", lambda: self.mt5),
            clock=lambda: self.now,
            monotonic=lambda: self.retry_time,
            **options,
        )

    def test_live_snapshot_contains_only_requested_fields_and_distinct_pending_symbols(self):
        provider = self.live(terminal=r"C:\Local Terminal\terminal64.exe")
        snapshot = provider.snapshot()

        self.assertEqual(snapshot["mode"], "live")
        self.assertEqual(snapshot["status"], "connected")
        self.assertIsNone(snapshot["message"])
        self.assertEqual(snapshot["timestamp"], 1760020000500)
        self.assertEqual(snapshot["account"], {
            "currency": "USD", "balance": 10000.0, "equity": 10193.0,
            "floating_pnl": 193.0, "free_margin": 9983.0, "margin_level": 4853.81,
        })
        self.assertEqual(snapshot["positions"][0], {
            "ticket": "9007199254740999", "symbol": "EURUSD.pro", "side": "Buy",
            "volume": 0.2, "entry": 1.08, "price": 1.088, "stop_loss": None,
            "take_profit": 1.092, "pnl": 160.0, "swap": -2.0, "digits": 5,
        })
        self.assertEqual(snapshot["positions"][1]["side"], "Sell")
        self.assertEqual(snapshot["orders"], [{
            "ticket": "82", "symbol": "USDJPY.pro", "side": "Sell Stop Limit",
            "volume": 0.15, "price": 153.525, "stop_loss": None,
            "take_profit": 153.0, "digits": None,
        }])
        self.assertEqual(snapshot["quotes"], [
            {"symbol": "EURUSD.pro", "bid": 1.088, "ask": 1.0882, "digits": 5,
             "timestamp": 1760020000123},
            {"symbol": "USDJPY.pro", "bid": 153.542, "ask": None, "digits": None,
             "timestamp": 1760020001000},
        ])
        self.assertEqual(self.mt5.quote_symbols, ["EURUSD.pro", "USDJPY.pro"])
        self.assertEqual(snapshot["equity_history"], [[1760020000500, 10193.0]])
        self.assertNotIn("Private", json.dumps(snapshot, allow_nan=False))
        args, kwargs = self.mt5.initializations[0]
        self.assertEqual(args, (r"C:\Local Terminal\terminal64.exe",))
        self.assertEqual(set(kwargs), {"timeout"})

    def test_empty_trade_lists_are_connected_and_missing_ticks_are_nullable(self):
        provider = self.live()
        original_orders = self.mt5.orders
        self.mt5.positions = ()
        self.mt5.orders = ()
        snapshot = provider.snapshot()
        self.assertEqual(snapshot["status"], "connected")
        self.assertEqual(snapshot["positions"], [])
        self.assertEqual(snapshot["orders"], [])
        self.assertEqual(snapshot["quotes"], [])

        self.mt5.orders = original_orders
        self.mt5.symbol_info_tick = lambda _: None
        self.assertEqual(provider.snapshot()["quotes"], [{
            "symbol": "USDJPY.pro", "bid": None, "ask": None, "digits": None,
            "timestamp": None,
        }])

    def test_retry_recovers_after_failed_initialization_and_discards_disconnected_data(self):
        provider = self.live()
        self.mt5.can_initialize = False
        self.assertEqual(provider.snapshot()["status"], "unavailable")
        self.mt5.can_initialize = True
        self.assertEqual(provider.snapshot()["status"], "unavailable")
        self.assertEqual(len(self.mt5.initializations), 1)
        self.assertEqual(self.mt5.initializations[0][0], ())
        self.retry_time += 60
        self.assertEqual(provider.snapshot()["status"], "connected")

        self.mt5.connected = False
        unavailable = provider.snapshot()
        self.assertEqual(unavailable["status"], "unavailable")
        self.assertIsNone(unavailable["account"])
        self.assertIsNone(unavailable["timestamp"])
        for key in ("positions", "orders", "quotes", "equity_history"):
            self.assertEqual(unavailable[key], [])

        self.mt5.connected = True
        self.mt5.account.equity = 337.0
        self.retry_time += 60
        self.now += 60
        self.assertEqual(provider.snapshot()["equity_history"], [[1760020060500, 337.0]])
        provider.close()
        self.assertGreaterEqual(self.mt5.closed, 2)

    def test_vendor_import_failure_leaves_an_unavailable_live_snapshot(self):
        module = self.mt5

        def missing_vendor():
            if self.retry_time < 110:
                raise ImportError("Private module path")
            return module

        provider = self.live(load_vendor=missing_vendor)
        unavailable = provider.snapshot()
        self.assertEqual(unavailable["mode"], "live")
        self.assertEqual(unavailable["status"], "unavailable")
        self.assertIn("MetaTrader5", unavailable["message"])
        self.assertNotIn("Private", json.dumps(unavailable))
        self.retry_time += 60
        self.assertEqual(provider.snapshot()["status"], "connected")

    def test_failed_trades_read_never_passes_for_an_empty_account(self):
        provider = self.live()
        provider.snapshot()
        self.mt5.orders = None
        unavailable = provider.snapshot()
        self.assertEqual(unavailable["status"], "unavailable")
        self.assertIsNone(unavailable["account"])
        self.assertEqual(unavailable["positions"], [])
        self.assertEqual(unavailable["equity_history"], [])

    def test_equity_history_is_bounded_and_cleared_when_the_account_changes(self):
        provider = self.live(history_limit=3)
        for equity in range(9, 14):
            self.now += 1
            self.mt5.account.equity = equity
            snapshot = provider.snapshot()
        self.assertEqual(snapshot["equity_history"], [
            [1760020003500, 11], [1760020004500, 12], [1760020005500, 13],
        ])

        self.mt5.account.server = "Another Server With Same Account Number"
        self.now += 1
        self.mt5.account.equity = 25
        self.assertEqual(provider.snapshot()["equity_history"], [[1760020006500, 25]])

    def test_backward_system_clock_keeps_equity_history_ordered(self):
        provider = self.live()
        provider.snapshot()
        self.now += 1
        provider.snapshot()
        self.now += 1
        provider.snapshot()
        self.now -= 1.5
        self.mt5.account.equity = 14.0
        self.assertEqual(provider.snapshot()["equity_history"], [
            [1760020000500, 10193.0], [1760020001000, 14.0],
        ])

    def test_account_switch_during_snapshot_drops_potentially_mixed_data(self):
        provider = self.live()
        provider.snapshot()

        def orders_after_switch():
            self.mt5.account.login = 9876543
            return self.mt5.orders

        self.mt5.orders_get = orders_after_switch
        snapshot = provider.snapshot()
        self.assertEqual(snapshot["status"], "unavailable")
        self.assertIsNone(snapshot["account"])
        self.assertEqual(snapshot["positions"], [])
        self.assertEqual(snapshot["equity_history"], [])

    def test_concurrent_snapshots_serialize_the_vendor_connection(self):
        provider = self.live()
        workers = Barrier(4)
        original_positions_get = self.mt5.positions_get
        vendor_active = Barrier(2, timeout=0.025)
        overlapped = []

        def read_positions():
            try:
                vendor_active.wait()
            except BrokenBarrierError:
                vendor_active.reset()
            else:
                overlapped.append(True)
            return original_positions_get()

        def fetch(_):
            workers.wait(timeout=2)
            return provider.snapshot()["status"]

        self.mt5.positions_get = read_positions
        with ThreadPoolExecutor(max_workers=4) as executor:
            self.assertEqual(list(executor.map(fetch, range(4))), ["connected"] * 4)
        self.assertEqual(overlapped, [])
        self.assertEqual(len(self.mt5.initializations), 1)

    def test_demo_is_connected_with_fictional_history_and_no_vendor(self):
        demo = self.provider_module.DemoProvider(clock=lambda: self.now)
        snapshot = demo.snapshot()
        self.assertEqual(snapshot["mode"], "demo")
        self.assertEqual(snapshot["status"], "connected")
        self.assertEqual(len(snapshot["positions"]), 3)
        self.assertEqual(len(snapshot["orders"]), 1)
        self.assertEqual(len(snapshot["quotes"]), 3)
        self.assertGreaterEqual(len(snapshot["equity_history"]), 30)
        self.assertEqual(snapshot["equity_history"][-1], [1760020000500, snapshot["account"]["equity"]])
        self.assertLess(snapshot["equity_history"][0][0], snapshot["timestamp"])


class HttpTests(unittest.TestCase):
    def setUp(self):
        provider_module = dashboard_module(self, "provider")
        server_module = dashboard_module(self, "server")
        self.mt5 = FakeMT5()
        provider = provider_module.LiveProvider(load_vendor=lambda: self.mt5)
        self.addCleanup(provider.close)
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        web_root = Path(temp_dir.name)
        (web_root / "index.html").write_text("<title>Dashboard</title>", encoding="utf-8")
        (web_root / "styles.css").write_text("body { color: black; }", encoding="utf-8")
        (web_root / "dashboard.js").write_text("const dashboard = {};", encoding="utf-8")
        (web_root / "private.txt").write_text("Private Test File", encoding="utf-8")
        self.server = server_module.create_server(provider, port=0, web_root=web_root)
        self.addCleanup(self.server.server_close)
        worker = Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        worker.start()
        self.addCleanup(worker.join, 2)
        self.addCleanup(self.server.shutdown)

    def request(self, method, path, **headers):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        try:
            conn.request(method, path, headers=headers)
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def test_only_fixed_dashboard_assets_and_snapshot_route_are_exposed(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        for path, content_type in {
            "/": "text/html", "/styles.css": "text/css", "/dashboard.js": "text/javascript",
        }.items():
            status, headers, _ = self.request("GET", path)
            self.assertEqual(status, 200)
            self.assertTrue(headers["Content-Type"].startswith(content_type))
        for path in ("/private.txt", "/%2e%2e/private.txt", "/api/trade", "/api/snapshot?debug=1", "//api/snapshot"):
            self.assertEqual(self.request("GET", path)[0], 404)
        self.assertIn(self.request("POST", "/api/snapshot")[0], (405, 501))
        self.assertIn(self.request("OPTIONS", "/api/snapshot")[0], (405, 501))

        status, headers, body = self.request("GET", "/api/snapshot")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertTrue(headers["Content-Type"].startswith("application/json"))
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(json.loads(body)["positions"][0]["ticket"], "9007199254740999")

    def test_untrusted_host_and_cross_origin_requests_cannot_read_snapshot(self):
        port = self.server.server_port
        for headers in (
            {"Host": f"attacker.example:{port}"},
            {"Host": f"localhost.attacker.example:{port}"},
            {"Host": f"127.0.0.1:{port + 1}"},
            {"Host": ""},
            {"Origin": "https://attacker.example"},
            {"Sec-Fetch-Site": "cross-site"},
        ):
            with self.subTest(headers=headers):
                status, response_headers, body = self.request("GET", "/api/snapshot", **headers)
                self.assertEqual(status, 403)
                self.assertNotIn("Access-Control-Allow-Origin", response_headers)
                self.assertNotIn(b"9007199254740999", body)
        self.assertEqual(self.mt5.initializations, [])
        self.assertEqual(self.request("GET", "/api/snapshot", Host=f"localhost:{port}")[0], 200)

    def test_paths_and_vendor_exceptions_keep_private_values_out_of_logs(self):
        def failed_read():
            raise RuntimeError("Private-Broker-Server account 1234567890 ticket 9007199254740999")

        self.mt5.positions_get = failed_read
        logs = io.StringIO()
        with contextlib.redirect_stderr(logs), contextlib.redirect_stdout(logs):
            self.assertEqual(self.request("GET", "/9007199254740999")[0], 404)
            status, _, body = self.request("GET", "/api/snapshot")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "unavailable")
        for secret in ("Private-Broker-Server", "1234567890", "9007199254740999"):
            self.assertNotIn(secret, logs.getvalue())
            self.assertNotIn(secret.encode(), body)
