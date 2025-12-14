# Member A - Input Module
# Collect expense entries and store them for later visualization.

import csv
import os
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "expenses.csv")
FIELDS = ["date", "amount", "category", "note"]


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()


def parse_date(s: str) -> str:
    s = s.strip()
    if s.lower() in ("today", "t"):
        return datetime.now().strftime("%Y-%m-%d")
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError("Invalid date format. Use YYYY-MM-DD or YYYY/MM/DD (or 'today').")


def parse_amount(s: str) -> float:
    s = s.strip()
    val = float(s)
    if val < 0:
        raise ValueError("Amount must be non-negative.")
    return val


def add_entry(date_str: str, amount: float, category: str, note: str = ""):
    ensure_storage()
    row = {
        "date": date_str,
        "amount": f"{amount:.2f}",
        "category": category.strip(),
        "note": note.strip(),
    }
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writerow(row)


def prompt_loop():
    print("=== Expense Input (Member A) ===")
    print("Format: date amount category [note]")
    print("Example: 2025-12-14 120 lunch bubbletea")
    print("Type 'q' to quit.\n")

    while True:
        line = input("> ").strip()
        if not line:
            continue
        if line.lower() in ("q", "quit", "exit"):
            break

        parts = line.split()
        if len(parts) < 3:
            print("Need at least: date amount category (note optional).")
            continue

        date_raw, amount_raw, category = parts[0], parts[1], parts[2]
        note = " ".join(parts[3:]) if len(parts) > 3 else ""

        try:
            d = parse_date(date_raw)
            a = parse_amount(amount_raw)
            add_entry(d, a, category, note)
            print(f"Saved: {d}, {a:.2f}, {category}" + (f", note={note}" if note else ""))
        except Exception as e:
            print("Error:", e)

    print("\nBye! Data saved to:", DATA_FILE)


if __name__ == "__main__":
    prompt_loop()
