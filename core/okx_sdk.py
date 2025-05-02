import time
import hmac
import base64
import hashlib
import json
import requests

class OKXClient:
    def __init__(self, api_key=None, api_secret=None, passphrase=None):
        self.api_key = api_key
        self.api_secret = api_secret.encode() if api_secret else None
        self.passphrase = passphrase
        self.base_url = "https://www.okx.com"

    def _get_timestamp(self):
        return str(time.time())

    def _sign(self, timestamp, method, request_path, body=''):
        if not self.api_secret:
            return ''
        message = f"{timestamp}{method}{request_path}{body}"
        mac = hmac.new(self.api_secret, message.encode(), hashlib.sha256)
        return base64.b64encode(mac.digest()).decode()

    def _headers(self, method, path, body=''):
        headers = {"Content-Type": "application/json"}
        if self.api_key and self.api_secret and self.passphrase:
            timestamp = self._get_timestamp()
            sign = self._sign(timestamp, method, path, body)
            headers.update({
                "OK-ACCESS-KEY": self.api_key,
                "OK-ACCESS-SIGN": sign,
                "OK-ACCESS-TIMESTAMP": timestamp,
                "OK-ACCESS-PASSPHRASE": self.passphrase
            })
        return headers

    def _request(self, method, path, params=None, body=None):
        url = self.base_url + path
        body_data = json.dumps(body) if body else ''
        headers = self._headers(method, path, body_data)
        try:
            response = requests.request(method, url, headers=headers, params=params, data=body_data, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # === MARKET DATA ===
    def get_kline(self, symbol, interval='1m', limit=100):
        return self._request("GET", "/api/v5/market/candles", params={
            "instId": symbol,
            "bar": interval,
            "limit": str(limit)
        })

    def get_ticker(self, inst_id):
        return self._request("GET", "/api/v5/market/ticker", params={"instId": inst_id})

    # === ACCOUNT INFO ===
    def get_account_balance(self):
        return self._request("GET", "/api/v5/account/balance")

    # === REAL TRADING ORDER ===
    def place_order(self, inst_id, side, size, type="market", reduce_only=False):
        """
        Place market/limit order
        side: "buy" or "sell"
        type: "market" or "limit"
        reduce_only: True/False (for closing)
        """
        body = {
            "instId": inst_id,
            "tdMode": "isolated",  # Futures isolated mode
            "side": side,
            "ordType": type,
            "sz": str(size)
        }
        if reduce_only:
            body["reduceOnly"] = True
        return self._request("POST", "/api/v5/trade/order", body=body)

    # === PLACE TP/SL TRIGGER ORDER ===
    def place_trigger_order(self, inst_id, side, trigger_price, order_type="market", size=0.001):
        """
        Place a TP/SL (trigger) order
        side: "buy" or "sell"
        trigger_price: price where order triggered
        order_type: "market" or "limit"
        """
        body = {
            "instId": inst_id,
            "tdMode": "isolated",
            "side": side,
            "ordType": order_type,
            "sz": str(size),
            "triggerPx": str(trigger_price),
            "triggerPxType": "last",  # based on last traded price
            "posSide": "net"
        }
        return self._request("POST", "/api/v5/trade/order-algo", body=body)