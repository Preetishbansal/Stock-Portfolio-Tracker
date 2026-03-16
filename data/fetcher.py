"""
data/fetcher.py - Fetches live stock data from Yahoo Finance API via yfinance.
"""

import yfinance as yf


def fetch_current_price(symbol):
    """Return the latest market price for a stock symbol."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        return round(info.get("lastPrice", info.get("last_price", 0)), 2)
    except Exception:
        return None


def fetch_stock_info(symbol):
    """Return company name, sector, current price, and key metrics."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol.upper(),
            "company": info.get("shortName", symbol.upper()),
            "sector": info.get("sector", "N/A"),
            "price": round(info.get("currentPrice", info.get("regularMarketPrice", 0)), 2),
            "currency": info.get("currency", "INR"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", None),
            "52w_high": info.get("fiftyTwoWeekHigh", None),
            "52w_low": info.get("fiftyTwoWeekLow", None),
        }
    except Exception:
        return None


def fetch_price_history(symbol, period="1mo"):
    """
    Download historical OHLCV data from Yahoo Finance.
    Returns a list of dicts ready for database insertion.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return []

        records = []
        for date, data in df.iterrows():
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(data["Open"], 2),
                "high": round(data["High"], 2),
                "low": round(data["Low"], 2),
                "close": round(data["Close"], 2),
                "volume": int(data["Volume"]),
            })
        return records
    except Exception:
        return []
