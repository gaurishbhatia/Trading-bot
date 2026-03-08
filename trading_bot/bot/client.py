# client.py - Binance Futures Testnet API wrapper
# Uses direct REST calls with HMAC-SHA256 signing

import hashlib
import hmac
import logging
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

log = logging.getLogger("trading_bot")

BASE_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
    """Handles all communication with the Binance Futures Testnet API."""

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise EnvironmentError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in your .env file."
            )

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        log.info("Client initialized for testnet")

    def _sign(self, params):
        """Adds timestamp + HMAC signature to the request params."""
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        sig = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = sig
        return params

    def _send_request(self, method, endpoint, params):
        """Signs and sends a request, returns parsed JSON or raises on error."""
        url = BASE_URL + endpoint
        signed = self._sign(params)
        log.debug("Request: %s %s %s", method, endpoint, signed)

        try:
            resp = self.session.request(method, url, params=signed)
        except requests.exceptions.ConnectionError:
            log.error("Could not connect to %s", BASE_URL)
            raise RuntimeError("Network error - check your internet connection")
        except requests.exceptions.Timeout:
            log.error("Request to %s timed out", endpoint)
            raise RuntimeError("Request timed out")

        data = resp.json()

        if resp.status_code != 200:
            msg = data.get("msg", "Unknown error")
            code = data.get("code", -1)
            log.error("API error %d: %s (HTTP %d)", code, msg, resp.status_code)
            raise RuntimeError(f"Binance API error [{code}]: {msg}")

        log.debug("Response: %s", data)
        return data

    def market_order(self, symbol, side, quantity):
        """Place a market order."""
        log.info("MARKET %s %s %s", side, quantity, symbol)
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
        })

    def limit_order(self, symbol, side, quantity, price):
        """Place a limit order (GTC)."""
        log.info("LIMIT %s %s %s @ %s", side, quantity, symbol, price)
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC",
        })

    def stop_market_order(self, symbol, side, quantity, stop_price):
        """Place a stop-market order."""
        log.info("STOP_MARKET %s %s %s stop@%s", side, quantity, symbol, stop_price)
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "STOP_MARKET",
            "quantity": quantity,
            "stopPrice": stop_price,
        })
