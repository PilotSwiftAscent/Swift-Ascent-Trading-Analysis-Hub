"""Run the dashboard with ``python -m tools.mt5_dashboard``."""

import argparse
from contextlib import ExitStack
import sys

from .provider import DemoProvider, LiveProvider
from .server import create_server


def main(argv=None):
    parser = argparse.ArgumentParser(description="Serve the read-only MT5 dashboard on this computer.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--demo", action="store_true", help="Use fictional data without MetaTrader 5.")
    source.add_argument("--terminal", metavar="PATH", help="Path to the MT5 terminal executable.")
    parser.add_argument("--port", type=int, default=8765, help="Local HTTP port (default: 8765).")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    with ExitStack() as resources:
        if args.demo:
            provider = DemoProvider()
        else:
            provider = LiveProvider(terminal=args.terminal)
            resources.callback(provider.close)

        try:
            server = resources.enter_context(create_server(provider, args.port))
        except OSError:
            print(f"Could not listen on 127.0.0.1:{args.port}. Try a different --port.", file=sys.stderr)
            return 1

        print(f"MT5 dashboard at http://127.0.0.1:{server.server_port}/ (Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
