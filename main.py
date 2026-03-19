"""
main.py - Entry point for the Stock Portfolio Tracker.
Runs the Flask web application with all routes.
"""

import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from db.queries import add_user, initialize_database
from portfolio.tracker import buy_stock, sell_stock
from portfolio.analyzer import analyze_portfolio, get_sector_allocation
from data.fetcher import fetch_stock_info
from reports.report import generate_console_report
from db.queries import get_transactions
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)
app.secret_key = "super_secret_portfolio_key"  # Needed for flash messages

# Default user for demo (auto-created on first run)
DEFAULT_USER_ID = None


def ensure_default_user():
    global DEFAULT_USER_ID
    if DEFAULT_USER_ID is None:
        DEFAULT_USER_ID = add_user("demo_user", "demo@portfolio.com")


# ─── Web Routes ─────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Main dashboard with portfolio overview."""
    ensure_default_user()
    portfolio = analyze_portfolio(DEFAULT_USER_ID)
    sectors = get_sector_allocation(DEFAULT_USER_ID)
    return render_template(
        "dashboard.html",
        portfolio=portfolio,
        sectors=sectors,
        user_id=DEFAULT_USER_ID,
    )


@app.route("/add_stock", methods=["POST"])
def add_stock_route():
    """Add a new stock and record a BUY transaction."""
    ensure_default_user()
    symbol = request.form.get("symbol", "").strip().upper()
    quantity = float(request.form.get("quantity", 0))
    price = request.form.get("price", "").strip()
    price = float(price) if price else None

    if symbol and quantity > 0:
        if buy_stock(DEFAULT_USER_ID, symbol, quantity, price):
            flash(f"Successfully bought {quantity} shares of {symbol}.", "success")
        else:
            flash(f"Failed to buy {symbol}. Please check the symbol and try again.", "error")

    return redirect(url_for("dashboard"))


@app.route("/sell_stock", methods=["POST"])
def sell_stock_route():
    """Record a SELL transaction."""
    ensure_default_user()
    symbol = request.form.get("symbol", "").strip().upper()
    quantity = float(request.form.get("quantity", 0))
    price = request.form.get("price", "").strip()
    price = float(price) if price else None

    if symbol and quantity > 0:
        try:
            if sell_stock(DEFAULT_USER_ID, symbol, quantity, price):
                flash(f"Successfully sold {quantity} shares of {symbol}.", "success")
            else:
                flash(f"Failed to sell {symbol}. Make sure the symbol is correct.", "error")
        except ValueError as e:
            flash(str(e), "error")

    return redirect(url_for("dashboard"))


@app.route("/transactions")
def transactions():
    """View transaction history."""
    ensure_default_user()
    txns = get_transactions(DEFAULT_USER_ID, limit=100)
    return render_template("transactions.html", transactions=txns)


@app.route("/report")
def report():
    """Generate and print a console report, then redirect to dashboard."""
    ensure_default_user()
    generate_console_report(DEFAULT_USER_ID)
    return redirect(url_for("dashboard"))


# ─── REST API Endpoints ────────────────────────────────────────

@app.route("/api/stock/<symbol>")
def api_stock_info(symbol):
    """REST API endpoint for live stock info."""
    info = fetch_stock_info(symbol)
    if info:
        return jsonify(info)
    return jsonify({"error": "Stock not found"}), 404


@app.route("/api/portfolio")
def api_portfolio():
    """REST API endpoint for portfolio analysis."""
    ensure_default_user()
    return jsonify(analyze_portfolio(DEFAULT_USER_ID))


# ─── Run ────────────────────────────────────────────────────────

if __name__ == "__main__":
    initialize_database()
    print("[OK] Starting Stock Portfolio Tracker...")
    print(f"[OK] Open http://localhost:{FLASK_PORT} in your browser.")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
