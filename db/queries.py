"""
db/queries.py - All SQL query functions for the Stock Portfolio Tracker.
Handles connection management, schema initialization, and CRUD operations.
"""

import os
import sqlite3
from config import DB_PATH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_connection():
    """Create and return a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_database():
    """Run the schema.sql script to create all tables, views, and indexes."""
    schema_path = os.path.join(BASE_DIR, "db", "schema.sql")
    conn = get_connection()
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully.")


# ═══════════════════════════════════════════════════════════════
#  CREATE Operations
# ═══════════════════════════════════════════════════════════════

def add_user(username, email):
    """Insert a new user and return user_id."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        row = conn.execute(
            "SELECT user_id FROM users WHERE username = ?", (username,)
        ).fetchone()
        return row["user_id"] if row else None
    finally:
        conn.close()


def add_stock(symbol, company, sector=None):
    """Insert a stock into the master table; return stock_id."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO stocks (symbol, company, sector) VALUES (?, ?, ?)",
            (symbol.upper(), company, sector),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        row = conn.execute(
            "SELECT stock_id FROM stocks WHERE symbol = ?", (symbol.upper(),)
        ).fetchone()
        return row["stock_id"] if row else None
    finally:
        conn.close()


def record_transaction(user_id, stock_id, txn_type, quantity, price_per_share):
    """Record a BUY or SELL transaction."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO transactions
           (user_id, stock_id, txn_type, quantity, price_per_share)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, stock_id, txn_type.upper(), quantity, price_per_share),
    )
    conn.commit()
    conn.close()


def save_price_history(stock_id, records):
    """Bulk-insert price history rows (list of dicts)."""
    conn = get_connection()
    conn.executemany(
        """INSERT OR IGNORE INTO price_history
           (stock_id, date, open, high, low, close, volume)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            (stock_id, r["date"], r["open"], r["high"], r["low"], r["close"], r["volume"])
            for r in records
        ],
    )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════
#  READ Operations (Optimized Queries)
# ═══════════════════════════════════════════════════════════════

def get_holdings(user_id):
    """Fetch current holdings for a user (uses the holdings VIEW)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM holdings WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_transactions(user_id, limit=50):
    """Fetch recent transactions for a user, newest first."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT t.*, s.symbol, s.company
           FROM transactions t
           JOIN stocks s ON s.stock_id = t.stock_id
           WHERE t.user_id = ?
           ORDER BY t.txn_date DESC
           LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_portfolio_summary(user_id):
    """Aggregated portfolio summary grouped by sector."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT
               s.sector,
               COUNT(DISTINCT s.stock_id) AS num_stocks,
               ROUND(SUM(h.shares_held), 4) AS total_shares,
               ROUND(SUM(h.shares_held * h.avg_cost), 2) AS total_invested
           FROM holdings h
           JOIN stocks s ON s.symbol = h.symbol
           WHERE h.user_id = ?
           GROUP BY s.sector
           ORDER BY total_invested DESC""",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_stocks():
    """Return all stocks in the master table."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM stocks ORDER BY symbol").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stock_id_by_symbol(symbol):
    """Look up stock_id by ticker symbol."""
    conn = get_connection()
    row = conn.execute(
        "SELECT stock_id FROM stocks WHERE symbol = ?", (symbol.upper(),)
    ).fetchone()
    conn.close()
    return row["stock_id"] if row else None
