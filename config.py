"""
config.py - Central configuration for the Stock Portfolio Tracker.
"""

import os

# ── Database Configuration ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")

# ── Currency ───────────────────────────────────────────────────
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

# ── API Configuration ─────────────────────────────────────────
# yfinance is free and does not require an API key.
# If you switch to Alpha Vantage or another provider, set keys here.
API_KEYS = {
    "alpha_vantage": os.environ.get("ALPHA_VANTAGE_KEY", ""),
}

# ── Flask Configuration ───────────────────────────────────────
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True
