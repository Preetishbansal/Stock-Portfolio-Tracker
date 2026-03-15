
-- Enable WAL mode for better concurrent read performance
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Users Table 
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    NOT NULL UNIQUE,
    email       TEXT    NOT NULL UNIQUE,
    created_at  TEXT    DEFAULT (datetime('now'))
);

-- Stocks Master Table 
CREATE TABLE IF NOT EXISTS stocks (
    stock_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol      TEXT    NOT NULL UNIQUE,
    company     TEXT    NOT NULL,
    sector      TEXT,
    added_at    TEXT    DEFAULT (datetime('now'))
);

-- ── Transactions Table (BUY / SELL) ────────────────────────────
CREATE TABLE IF NOT EXISTS transactions (
    txn_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL,
    stock_id         INTEGER NOT NULL,
    txn_type         TEXT    NOT NULL CHECK(txn_type IN ('BUY','SELL')),
    quantity         REAL    NOT NULL CHECK(quantity > 0),
    price_per_share  REAL    NOT NULL CHECK(price_per_share > 0),
    txn_date         TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)  REFERENCES users(user_id),
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

-- ── Price History Table (cached market data) 
CREATE TABLE IF NOT EXISTS price_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id    INTEGER NOT NULL,
    date        TEXT    NOT NULL,
    open        REAL,
    high        REAL,
    low         REAL,
    close       REAL,
    volume      INTEGER,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
    UNIQUE(stock_id, date)
);

-- ── Holdings View ──────────────────────────────────────────────
-- Automatically calculates current shares held and average cost
-- from the transactions table using aggregation.
CREATE VIEW IF NOT EXISTS holdings AS
SELECT
    t.user_id,
    s.symbol,
    s.company,
    s.sector,
    ROUND(SUM(CASE WHEN t.txn_type='BUY' THEN t.quantity ELSE -t.quantity END), 4) AS shares_held,
    ROUND(
        SUM(CASE WHEN t.txn_type='BUY' THEN t.quantity * t.price_per_share
                 ELSE -t.quantity * t.price_per_share END)
        / NULLIF(SUM(CASE WHEN t.txn_type='BUY' THEN t.quantity ELSE -t.quantity END), 0),
    2) AS avg_cost
FROM transactions t
JOIN stocks s ON s.stock_id = t.stock_id
GROUP BY t.user_id, s.stock_id
HAVING shares_held > 0;

-- ── Indexes for optimized query performance ────────────────────
CREATE INDEX IF NOT EXISTS idx_txn_user    ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_txn_stock   ON transactions(stock_id);
CREATE INDEX IF NOT EXISTS idx_txn_date    ON transactions(txn_date);
CREATE INDEX IF NOT EXISTS idx_price_stock ON price_history(stock_id);
CREATE INDEX IF NOT EXISTS idx_price_date  ON price_history(date);
CREATE INDEX IF NOT EXISTS idx_stock_sym   ON stocks(symbol);
