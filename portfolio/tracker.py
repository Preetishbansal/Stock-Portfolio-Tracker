"""
portfolio/tracker.py - Buy and Sell logic for the Stock Portfolio Tracker.
"""

from db.queries import add_stock, record_transaction, get_stock_id_by_symbol, get_holdings
from data.fetcher import fetch_stock_info, fetch_current_price
from data.loader import load_and_cache_history


def buy_stock(user_id, symbol, quantity, price=None):
    """
    Execute a BUY transaction:
    1. Fetch stock info from the live API.
    2. Insert into stocks master table if new.
    3. Record the BUY transaction.
    4. Cache recent price history.
    Returns True on success, False on failure.
    """
    symbol = symbol.strip().upper()
    info = fetch_stock_info(symbol)

    if info:
        company = info["company"]
        sector = info["sector"]
        if not price:
            price = info["price"]
    else:
        company = symbol
        sector = "N/A"
        if not price:
            return False  # Cannot buy without a price

    stock_id = add_stock(symbol, company, sector)
    if stock_id and price > 0:
        record_transaction(user_id, stock_id, "BUY", quantity, price)
        load_and_cache_history(symbol, period="1mo")
        return True
    return False


def sell_stock(user_id, symbol, quantity, price=None):
    """
    Execute a SELL transaction:
    1. Look up the stock_id.
    2. Check current holdings.
    3. Fetch current market price if not provided.
    4. Record the SELL transaction.
    Returns True on success, False on failure.
    """
    symbol = symbol.strip().upper()
    stock_id = get_stock_id_by_symbol(symbol)

    if not stock_id:
        raise ValueError(f"You don't own any shares of '{symbol}'.")

    # Validation: Ensure user owns enough shares before selling
    holdings = get_holdings(user_id)
    owned_quantity = 0
    for h in holdings:
        if h["symbol"] == symbol:
            owned_quantity = h["shares_held"]
            break

    if quantity > owned_quantity:
        # Instead of just printing, we raise an error so the frontend can display it
        raise ValueError(f"Cannot sell {quantity} shares of {symbol}. You only own {owned_quantity}.")

    if not price:
        price = fetch_current_price(symbol)

    if price and price > 0:
        record_transaction(user_id, stock_id, "SELL", quantity, price)
        return True
    return False
