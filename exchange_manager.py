import asyncio
import json
import ccxt.async_support as ccxt
import yaml
import math

EXCHANGE_CLASSES = {
    "binance": ccxt.binance,
    "gateio": ccxt.gateio,
    "bybit": ccxt.bybit,
    "bitget": ccxt.bitget,
    "bingx": ccxt.bingx,
    "okx": ccxt.okx,
}


class ExchangeManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.exchanges: dict = {}
        self._load_config(config_path)

    def _load_config(self, config_path: str):
        with open(config_path) as f:
            config = yaml.safe_load(f)

        for name, settings in config.get("exchanges", {}).items():
            cls = EXCHANGE_CLASSES.get(name)
            if not cls:
                continue
            exchange = cls({
                "apiKey": settings["api_key"],
                "secret": settings["api_secret"],
                "password": settings.get("passwd", ""),
                'options': {
                    'defaultType': settings.get("type", ""),
                }
            })
            if settings.get("testnet"):
                if 'binance'in name:
                    exchange.enable_demo_trading(True)
                else:
                    exchange.set_sandbox_mode(True)
            if exchange.check_required_credentials():
                print("Success Loading",name)
            self.exchanges[name] = exchange

    async def load_all_markets(self):
        for name, exchange in self.exchanges.items():
            try:
                markets = await exchange.load_markets()
                # with open(f"markets_{name}.txt", "w") as mf:
                #     mf.write("\n".join(markets.keys()))
                # print(f"[{name}] markets saved to markets_{name}.txt")
            except Exception as e:
                print(f"[{name}] failed to load markets: {e}")

    def get_available_exchanges(self) -> list:
        return list(self.exchanges.keys())

    async def _place_single_order(self, exchange_name: str, symbol: str, side: str, amount: float) -> dict:
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            return {"exchange": exchange_name, "success": False, "error": "Exchange not configured"}
        try:
            if exchange_name in ["gateio", "okx"]:
                exchange.verbose = True
                market = exchange.market(symbol+":USDT")
                order = await exchange.create_order(symbol+":USDT", 'market', side, amount / market.get('contractSize'))
            elif exchange_name == "bingx":
                position_side = "LONG" if side == "buy" else "SHORT"
                order = await exchange.create_order(symbol+":USDT", 'market', side, amount, params={"positionSide": position_side})
            elif exchange_name in ['bitget', 'bybit']:
                order = await exchange.create_order(symbol+":USDT", 'market', side, amount)
            else:
                order = await exchange.create_order(symbol, 'market', side, amount)
            # print(f"[{exchange_name}] raw order response:\n{json.dumps(order, indent=2, default=str)}")
            return {
                "exchange": exchange_name,
                "success": True,
                "order_id": str(order.get("id")),
                "symbol": order.get("symbol"),
                "side": order.get("side"),
                "amount": order.get("amount"),
                "price": order.get("average") or order.get("price"),
            }
        except Exception as e:
            print(f"[{exchange_name}] order FAILED: {e}")
            return {"exchange": exchange_name, "success": False, "error": str(e)}

    async def place_orders(self, exchanges: list, symbol: str, side: str, amount: float) -> list:
        tasks = [
            self._place_single_order(name, symbol, side, amount)
            for name in exchanges
        ]
        return list(await asyncio.gather(*tasks))

    async def close(self):
        for exchange in self.exchanges.values():
            await exchange.close()
