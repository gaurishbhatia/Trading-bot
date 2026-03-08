#!/usr/bin/env python3
"""
Entry point for the trading bot CLI.

Examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
    python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 50000
    python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.002 --stop-price 80000
"""

import argparse
import sys
import logging

from bot.logging_config import setup_logging
from bot.validators import validate_order_params
from bot.client import BinanceFuturesClient
from bot.orders import execute_order

log = logging.getLogger("trading_bot")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.002\n"
            "  python cli.py --symbol ETHUSDT --side SELL --type LIMIT  --quantity 0.05 --price 3000\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.002 --stop-price 80000\n"
        ),
    )

    parser.add_argument("--symbol", required=True, help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
                        help="BUY or SELL")
    parser.add_argument("--type", required=True,
                        choices=["MARKET", "LIMIT", "STOP_MARKET", "market", "limit", "stop_market"],
                        help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, default=None, help="Limit price (for LIMIT orders)")
    parser.add_argument("--stop-price", type=float, default=None, dest="stop_price",
                        help="Stop price (for STOP_MARKET orders)")

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_args()
    log.info("Started with: %s", vars(args))

    # validate inputs
    try:
        params = validate_order_params(args)
    except ValueError as e:
        log.error("Validation failed: %s", e)
        print(f"\nError: {e}\n")
        sys.exit(1)

    # connect to binance testnet
    try:
        client = BinanceFuturesClient()
    except EnvironmentError as e:
        log.error("Config error: %s", e)
        print(f"\nError: {e}\n")
        sys.exit(1)
    except Exception as e:
        log.error("Connection failed: %s", e)
        print(f"\nError: Could not connect to Binance Testnet - {e}\n")
        sys.exit(1)

    # place the order
    try:
        execute_order(client, params)
    except Exception as e:
        log.error("Order failed: %s", e)
        print(f"\nError: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
