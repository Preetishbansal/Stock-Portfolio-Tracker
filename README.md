# Stock Portfolio Tracker

A full-stack **Stock Portfolio Tracker** built with **Python**, **SQL (SQLite)**, and **Flask** to efficiently store, manage, and analyse investment data in real time. All values are displayed in **Indian Rupees (INR)**.

## Features

| Feature | Description |
|---|---|
| **Relational DB Schema** | Normalized tables with foreign keys, indexes, and a `holdings` SQL VIEW |
| **Live Market Data** | Fetches real-time stock prices using the `yfinance` API |
| **Buy / Sell Stocks** | Record transactions and automatically update holdings |
| **Portfolio Analytics** | Automated P&L, return %, and sector allocation analysis |
| **Price History Cache** | Stores fetched price history in SQLite for fast retrieval |
| **REST API** | JSON endpoints at `/api/stock/<symbol>` and `/api/portfolio` |
| **Console Reports** | Formatted portfolio summary report via `reports/report.py` |
| **Web Dashboard** | Beautiful dark-themed UI with responsive design |

## Tech Stack

- **Python 3.10+** - Core application logic
- **SQLite** - Lightweight relational database
- **Flask** - Web framework
- **yfinance** - Yahoo Finance market data API
- **HTML/CSS/JS** - Responsive front-end

## Project Structure

```
Stock-Portfolio-Tracker/
├── db/
│   ├── schema.sql          # Table creation scripts
│   └── queries.py          # All SQL query functions
├── data/
│   ├── fetcher.py          # yfinance / API calls
│   └── loader.py           # Bulk insert price history
├── portfolio/
│   ├── tracker.py          # Buy/sell logic
│   └── analyzer.py         # P&L, returns, metrics
├── reports/
│   └── report.py           # Summary output
├── templates/
│   ├── dashboard.html      # Main dashboard UI
│   └── transactions.html   # Transaction history page
├── config.py               # DB path, API keys
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
└── README.md
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Open in Browser

Navigate to **http://localhost:5000**

## Database Schema

### Tables
- **users** - User accounts
- **stocks** - Master stock list (symbol, company, sector)
- **transactions** - Buy/Sell records with FK to users and stocks
- **price_history** - Cached historical price data

### SQL View
- **holdings** - Derived view calculating shares held and avg cost from transactions

### Indexes
- Optimized indexes on `user_id`, `stock_id`, `txn_date`, `symbol`, `date` for fast lookups

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Dashboard with portfolio overview |
| `/add_stock` | POST | Buy a stock |
| `/sell_stock` | POST | Sell a stock |
| `/transactions` | GET | Transaction history page |
| `/api/stock/<symbol>` | GET | Get stock info (JSON) |
| `/api/portfolio` | GET | Get full portfolio analysis (JSON) |

## Indian Stock Symbols

Use `.NS` suffix for NSE stocks and `.BO` for BSE stocks:
- `RELIANCE.NS` - Reliance Industries (NSE)
- `TCS.NS` - Tata Consultancy Services (NSE)
- `INFY.NS` - Infosys (NSE)
- `HDFCBANK.NS` - HDFC Bank (NSE)

## License

This project is for educational purposes.
