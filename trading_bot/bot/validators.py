# validators.py - sanity checks before we hit the API

SIDES = ("BUY", "SELL")
ORDER_TYPES = ("MARKET", "LIMIT", "STOP_MARKET")


def validate_symbol(symbol):
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty")
    symbol = symbol.strip().upper()
    if not symbol.isalpha() or len(symbol) < 5:
        raise ValueError(f"'{symbol}' doesn't look like a valid trading pair")
    return symbol


def validate_side(side):
    side = side.strip().upper()
    if side not in SIDES:
        raise ValueError(f"Side must be BUY or SELL, got '{side}'")
    return side


def validate_order_type(order_type):
    order_type = order_type.strip().upper()
    if order_type not in ORDER_TYPES:
        raise ValueError(f"Order type must be one of {ORDER_TYPES}, got '{order_type}'")
    return order_type


def validate_quantity(qty):
    try:
        qty = float(qty)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity must be a number, got '{qty}'")
    if qty <= 0:
        raise ValueError(f"Quantity must be positive, got {qty}")
    return qty


def validate_price(price, order_type):
    """Price is only needed for LIMIT and STOP_MARKET orders."""
    if order_type == "MARKET":
        return None

    if price is None:
        if order_type == "LIMIT":
            raise ValueError("--price is required for LIMIT orders")
        else:
            raise ValueError("--stop-price is required for STOP_MARKET orders")

    try:
        price = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Price must be a number, got '{price}'")

    if price <= 0:
        raise ValueError(f"Price must be positive, got {price}")
    return price


def validate_order_params(args):
    """Run all checks on CLI args and return a clean dict."""
    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    order_type = validate_order_type(args.type)
    qty = validate_quantity(args.quantity)

    # stop-market uses --stop-price, limit uses --price
    if order_type == "STOP_MARKET":
        price = validate_price(getattr(args, "stop_price", None), order_type)
    else:
        price = validate_price(getattr(args, "price", None), order_type)

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": qty,
        "price": price,
    }
