"""
data/loader.py - Bulk loads and caches price history into the database.
"""

from db.queries import get_stock_id_by_symbol, save_price_history
from data.fetcher import fetch_price_history


def load_and_cache_history(symbol, period="1mo"):
    """
    Fetch historical price data from the API and bulk-insert
    it into the price_history table for fast future retrieval.
    Uses INSERT OR IGNORE to avoid duplicates.
    """
    stock_id = get_stock_id_by_symbol(symbol)
    if not stock_id:
        return []

    records = fetch_price_history(symbol, period)
    if records:
        save_price_history(stock_id, records)

    return records
