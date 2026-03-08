# Binance Futures Testnet Trading Bot

A Python CLI tool for placing orders on the Binance Futures Testnet (USDT-M). Supports Market, Limit, and Stop-Market orders with input validation and structured logging.

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # API wrapper (REST + HMAC signing)
    orders.py          # order execution & output formatting
    validators.py      # input validation
    logging_config.py  # logging setup
  cli.py               # CLI entry point
  .env.example         # API key template
  requirements.txt
  logs/
    trading_bot.log    # auto-generated log file
```

## Setup

### 1. Get Testnet API Keys

1. Go to https://testnet.binancefuture.com
2. Log in with GitHub
3. Go to API Management and create a new API key

### 2. Install Dependencies

```bash
cd trading_bot
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env   # on Windows: copy .env.example .env
```

Then edit `.env` and add your keys:

```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

## Usage

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 50000
```

### Stop-Market Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.002 --stop-price 80000
```

### Help

```bash
python cli.py --help
```

## Example Output

```
--- Order Request ---
  Symbol:   BTCUSDT
  Side:     BUY
  Type:     MARKET
  Quantity: 0.002

--- Order Response ---
  Order ID:     12702686994
  Status:       NEW
  Symbol:       BTCUSDT
  Side:         BUY
  Type:         MARKET
  Orig Qty:     0.002
  Executed Qty: 0.000
  Avg Price:    0.00

Order placed successfully!
```

## Logging

Logs go to both the console and `logs/trading_bot.log`. The file logger captures DEBUG-level details (full API requests/responses), while the console only shows INFO and above.

Log files rotate automatically at 5MB with 3 backups.

## Assumptions

- This only works with the **Binance Futures Testnet**, not production. Don't use real API keys.
- All orders are USDT-margined futures.
- Limit orders use GTC (Good Till Cancel) by default.
- The bot places individual orders — no position management or trading strategies.
- Minimum order notional is 100 USDT (enforced by Binance). For BTCUSDT, use at least 0.002 qty.

## Requirements

- Python 3.10+
- requests
- python-dotenv
