"""
reports/report.py - Generates portfolio summary reports.
Can be used for console output or data export.
"""

from portfolio.analyzer import analyze_portfolio, get_sector_allocation
from config import CURRENCY_SYMBOL


def generate_console_report(user_id):
    """Print a formatted portfolio report to the console."""
    data = analyze_portfolio(user_id)

    print("\n" + "=" * 70)
    print("  STOCK PORTFOLIO REPORT")
    print("=" * 70)

    if not data["holdings"]:
        print("  No holdings in portfolio.")
        print("=" * 70)
        return data

    # Holdings
    print(f"\n  {'Symbol':<8} {'Company':<20} {'Shares':<8} {'Avg Cost':<10} "
          f"{'CMP':<10} {'P&L':<12} {'Return':<8}")
    print("  " + "-" * 76)

    for h in data["holdings"]:
        pnl_str = f"{CURRENCY_SYMBOL}{h['pnl']:,.2f}"
        print(f"  {h['symbol']:<8} {h['company'][:18]:<20} {h['shares']:<8.2f} "
              f"{CURRENCY_SYMBOL}{h['avg_cost']:<9,.2f} {CURRENCY_SYMBOL}{h['current_price']:<9,.2f} "
              f"{pnl_str:<12} {h['pnl_pct']:+.2f}%")

    # Summary
    print("\n  " + "-" * 76)
    print(f"  Total Invested:    {CURRENCY_SYMBOL}{data['total_invested']:,.2f}")
    print(f"  Current Value:     {CURRENCY_SYMBOL}{data['total_current_value']:,.2f}")
    print(f"  Overall P&L:       {CURRENCY_SYMBOL}{data['overall_pnl']:,.2f} "
          f"({data['overall_pnl_pct']:+.2f}%)")

    # Sector Allocation
    sectors = get_sector_allocation(user_id)
    if sectors:
        print(f"\n  Sector Allocation:")
        for s in sectors:
            bar = "#" * int(s["allocation_pct"] / 2)
            print(f"    {s['sector'] or 'Other':<18} {s['allocation_pct']:>5.1f}%  {bar}")

    print("=" * 70 + "\n")
    return data


def get_report_data(user_id):
    """Return report data as a dictionary (for JSON export or UI)."""
    return {
        "portfolio": analyze_portfolio(user_id),
        "sectors": get_sector_allocation(user_id),
    }
