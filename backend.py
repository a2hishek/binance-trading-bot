import logging
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException
from pydantic import ValidationError
from schemas import OrderInput, OrderResponse

logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)

        # Fix for potential timestamp errors
        server_time = self.client.get_server_time()
        self.client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
        logging.info("Bot Initialized: Connected to Binance Testnet.")

    def get_symbols(self):
        info = self.client.futures_exchange_info()
        symbols = [s["symbol"] for s in info["symbols"]]
        return symbols
    
    def get_balance(self):
        balances = self.client.futures_account_balance()
        return next((b["balance"] for b in balances if b["asset"] == "USDT"), "0.00")

    def get_price(self, symbol):
        ticker = self.client.futures_symbol_ticker(symbol=symbol.upper())
        return float(ticker["price"])

    def place_order(self, symbol, side, order_type, quantity, price=None):

        # Log the Request
        log_msg = f"REQUEST: {side.upper()} {order_type} | {quantity} {symbol.upper()}"
        if price: log_msg += f" @ {price}"
        logging.info(log_msg)

        try:
            
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity,
            }
            if order_type.upper() == "LIMIT":
                params.update({"price": price, "timeInForce": "GTC"})

            validated_input = OrderInput(**params)
            logging.info(f"INPUT VALIDATED! - Proceeding with the request")

            order_params = validated_input.model_dump(exclude_none=True)
            response = self.client.futures_create_order(**order_params)
            logging.info(f"RESPONSE SUCCESS: OrderID {response.get('orderId')}")

            validated_output = OrderResponse(**response)
            logging.info(f"OUTPUT VALIDATED: Order ID - {validated_output.orderId}")
            
            return validated_output.model_dump()
        
        except BinanceAPIException as e:
            logging.error(f"RESPONSE ERROR: {e.status_code} - {e.message}")
            return {"error": e.message}
        
        except ValidationError as e:
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            logging.error(f"VALIDATION ERROR:  {' || '.join(error_messages)}")
            return {"validation_error": error_messages}
        
# import os
# from dotenv import load_dotenv
# import pprint

# load_dotenv()

# api_key = os.getenv("API_KEY")
# secret_key = os.getenv("SECRET_KEY")

# bot = BasicBot(api_key=api_key, api_secret=secret_key)

# response = bot.place_order(symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.001)
# pprint.pprint(response)