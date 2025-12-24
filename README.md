# Binance Trading Bot

A web-based cryptocurrency trading bot built with Streamlit and Python that allows you to trade on Binance Testnet. This bot provides an intuitive interface for placing orders, monitoring market data, and tracking your trading history.

## Features

- 🔐 **Secure API Connection**: Connect to Binance Testnet using your API credentials
- 📊 **Real-time Market Data**: View current prices and available trading pairs
- 💰 **Balance Monitoring**: Check your USDT balance in real-time
- 🛒 **Order Placement**: Execute MARKET and LIMIT orders with ease
- ✅ **Input Validation**: Robust validation using Pydantic to ensure order integrity
- 📜 **Order History**: Track all executed orders with detailed information
- 📝 **Comprehensive Logging**: All trading activities are logged for audit purposes

## Technologies Used

- **Python 3.x**: Core programming language
- **Streamlit**: Web-based user interface
- **python-binance**: Binance API integration
- **Pydantic**: Data validation and schema management
- **Pandas**: Data manipulation and display

## Installation

### Prerequisites

- Python 3.7 or higher
- Binance Testnet API credentials (Get them from [Binance Testnet](https://testnet.binancefuture.com/))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/a2hishek/binance-trading-bot.git
   cd "Trading Bot"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit pandas python-binance pydantic
   ```
   Or

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Streamlit application**
   ```bash
   streamlit run frontend.py
   ```

2. **Configure API credentials**
   - Enter your Binance Testnet API Key in the sidebar
   - Enter your Binance Testnet API Secret in the sidebar
   - Click "Connect Bot" to establish connection

3. **Start Trading**
   - Select a trading pair from the dropdown
   - View current price and your USDT balance
   - Place orders:
     - Choose BUY or SELL
     - Select order type (MARKET or LIMIT)
     - Enter quantity
     - Enter limit price (if using LIMIT order)
     - Click "Execute Trade"

4. **Monitor Orders**
   - View order history in the Order Details section
   - Check logs in `trading_bot.log` for detailed information

## Project Structure

```
Trading Bot/
├── backend.py          # Core bot logic and Binance API integration
├── frontend.py         # Streamlit web interface
├── schemas.py          # Pydantic models for data validation
├── trading_bot.log     # Application logs
└── README.md          # Project documentation
```

## Configuration

The bot is configured to use **Binance Testnet** by default, which allows you to practice trading without using real funds. To switch to the live Binance environment, modify the `BasicBot` initialization in `backend.py`:

```python
bot = BasicBot(api_key=api_key, api_secret=secret_key, testnet=False)
```

⚠️ **Warning**: Only use live trading with real funds if you fully understand the risks and have thoroughly tested the bot.

## Key Components

### Backend (`backend.py`)
- `BasicBot` class: Handles all Binance API interactions
- Methods:
  - `get_symbols()`: Fetch available trading pairs
  - `get_balance()`: Get USDT balance
  - `get_price()`: Get current price for a symbol
  - `place_order()`: Execute buy/sell orders with validation

### Frontend (`frontend.py`)
- Streamlit-based web interface
- Session state management
- Real-time market data display
- Order placement forms
- Order history tracking

### Schemas (`schemas.py`)
- `OrderInput`: Validates order input parameters
- `OrderResponse`: Validates Binance API responses

## Logging

All trading activities, errors, and API interactions are logged to `trading_bot.log` with timestamps. This helps with:
- Debugging issues
- Auditing trades
- Tracking API responses

## Security Notes

- ⚠️ **Never commit your API keys** to version control
- 🔒 Store API keys securely (consider using environment variables)
- 🧪 Always test on Testnet before using real funds
- 📝 Review logs regularly for any suspicious activity



