# orders.py - handles order execution and output formatting

import logging
from bot.client import BinanceFuturesClient

log = logging.getLogger("trading_bot")


def print_summary(params):
    """Show what we're about to send."""
    print("\n--- Order Request ---")
    print(f"  Symbol:   {params['symbol']}")
    print(f"  Side:     {params['side']}")
    print(f"  Type:     {params['order_type']}")
    print(f"  Quantity: {params['quantity']}")

    if params["order_type"] == "LIMIT":
        print(f"  Price:    {params['price']}")
    elif params["order_type"] == "STOP_MARKET":
        print(f"  Stop:     {params['price']}")
    print()


def print_response(resp):
    """Show the important fields from the API response."""
    print("--- Order Response ---")
    print(f"  Order ID:     {resp.get('orderId', 'N/A')}")
    print(f"  Status:       {resp.get('status', 'N/A')}")
    print(f"  Symbol:       {resp.get('symbol', 'N/A')}")
    print(f"  Side:         {resp.get('side', 'N/A')}")
    print(f"  Type:         {resp.get('type', 'N/A')}")
    print(f"  Orig Qty:     {resp.get('origQty', 'N/A')}")
    print(f"  Executed Qty: {resp.get('executedQty', 'N/A')}")
    print(f"  Avg Price:    {resp.get('avgPrice', 'N/A')}")

    stop = resp.get("stopPrice")
    if stop and stop != "0.00":
        print(f"  Stop Price:   {stop}")
    print()


def execute_order(client: BinanceFuturesClient, params: dict):
    """
    Takes validated params, calls the right client method,
    and prints both the request summary and API response.
    """
    print_summary(params)

    otype = params["order_type"]
    sym = params["symbol"]
    side = params["side"]
    qty = params["quantity"]
    price = params["price"]

    log.info("Executing %s %s %s %s", otype, side, qty, sym)

    if otype == "MARKET":
        resp = client.market_order(sym, side, qty)
    elif otype == "LIMIT":
        resp = client.limit_order(sym, side, qty, price)
    elif otype == "STOP_MARKET":
        resp = client.stop_market_order(sym, side, qty, price)
    else:
        raise ValueError(f"Unknown order type: {otype}")

    print_response(resp)
    print("Order placed successfully!\n")
    log.info("Done. orderId=%s", resp.get("orderId"))

    return resp
