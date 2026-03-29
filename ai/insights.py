from ai.client import ask
from data.store import read_csv, TX_FILE, INC_FILE
from collections import defaultdict

SYSTEM_PROMPT = "You are a finance assistant. Give 3 short spending insights based on the data. One per line."


def _build_summary() -> str:
    """Turn the CSV data into a compact text summary for the AI to read."""
    txs  = read_csv(TX_FILE)
    incs = read_csv(INC_FILE)

    if not txs:
        return ""

    total_exp = sum(float(r[0]) for r in txs)
    total_inc = sum(float(r[0]) for r in incs)

    # Category breakdown
    cat_totals: dict = defaultdict(float)
    for r in txs:
        try:
            cat_totals[r[3]] += float(r[0])
        except Exception:
            pass

    # Month breakdown
    month_totals: dict = defaultdict(float)
    for r in txs:
        try:
            month_totals[r[1][:7]] += float(r[0])
        except Exception:
            pass

    cat_lines = "\n".join(
        f"  {cat}: ₹{amt:,.0f}"
        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1])
    )
    month_lines = "\n".join(
        f"  {m}: ₹{amt:,.0f}"
        for m, amt in sorted(month_totals.items())
    )

    return (
        f"Income: Rs{total_inc:,.0f}, Expenses: Rs{total_exp:,.0f}, Balance: Rs{total_inc - total_exp:,.0f}\n"
        f"By category: {', '.join(f'{c}: Rs{a:,.0f}' for c, a in cat_totals.items())}\n"
        f"By month: {', '.join(f'{m}: Rs{a:,.0f}' for m, a in month_totals.items())}"
    )

def get_insights() -> str:
    """
    Returns a multi-line string of spending insights.
    Returns an empty string if there is no data yet.
    Raises RuntimeError (from client.py) on API failure.
    """
    summary = _build_summary()
    if not summary:
        return ""

    return ask(SYSTEM_PROMPT, f"Here is my financial data:\n\n{summary}")