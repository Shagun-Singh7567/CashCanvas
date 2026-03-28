import csv
import os

# ── File paths ─────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TX_FILE  = os.path.join(DATA_DIR, "Transactions.csv")
INC_FILE = os.path.join(DATA_DIR, "Income.csv")

# ── Setup ──────────────────────────────────────────────────────────────────────
def ensure_files():
    """Create the data directory and CSV files with headers if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TX_FILE):
        with open(TX_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Amount", "Date", "Description", "Category"])
    if not os.path.exists(INC_FILE):
        with open(INC_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Amount", "Date", "Source"])

# ── Read / Write ───────────────────────────────────────────────────────────────
def read_csv(path):
    """Return all non-empty data rows from a CSV, skipping the header."""
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if any(cell.strip() for cell in row):
                rows.append(row)
    return rows

def append_csv(path, row):
    """Append a single row to a CSV file."""
    with open(path, "a", newline="") as f:
        csv.writer(f).writerow(row)