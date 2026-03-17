"""
portfolio/analyzer.py - Portfolio performance analysis engine.
Computes P&L, returns, and sector allocation metrics.
"""

from db.queries import get_holdings, get_portfolio_summary
from data.fetcher import fetch_current_price


def analyze_portfolio(user_id):
    """
    Compute detailed performance metrics for each holding:
    - Current value, total invested, profit/loss, and % return.
    """
    holdings = get_holdings(user_id)
    analysis = []
    total_invested = 0
    total_current = 0

    for h in holdings:
        current_price = fetch_current_price(h["symbol"])
        if current_price is None:
            current_price = h["avg_cost"]  # fallback

        invested = round(h["shares_held"] * h["avg_cost"], 2)
        current_val = round(h["shares_held"] * current_price, 2)
        pnl = round(current_val - invested, 2)
        pnl_pct = round((pnl / invested) * 100, 2) if invested else 0

        total_invested += invested
        total_current += current_val

        analysis.append({
            "symbol": h["symbol"],
            "company": h["company"],
            "sector": h["sector"],
            "shares": h["shares_held"],
            "avg_cost": h["avg_cost"],
            "current_price": current_price,
            "invested": invested,
            "current_value": current_val,
            "pnl": pnl,
            "pnl_pct": pnl_pct,
        })

    overall_pnl = round(total_current - total_invested, 2)
    overall_pct = round((overall_pnl / total_invested) * 100, 2) if total_invested else 0

    return {
        "holdings": analysis,
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current, 2),
        "overall_pnl": overall_pnl,
        "overall_pnl_pct": overall_pct,
    }


def get_sector_allocation(user_id):
    """Return sector-wise allocation percentages."""
    summary = get_portfolio_summary(user_id)
    total = sum(s["total_invested"] for s in summary)
    for s in summary:
        s["allocation_pct"] = round((s["total_invested"] / total) * 100, 2) if total else 0
    return summary
