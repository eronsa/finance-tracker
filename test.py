import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import json
import os
import csv

DATA_FILE = "budget_data.json"
entries = []

def load_entries():
    global entries
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []

def save_entries():
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def show_logs():
    def update_log_display():
        filter_type = type_filter_var.get()
        date_filter = date_entry.get().strip()

        filtered = [
            e for e in entries
            if (filter_type == "All" or e["type"] == filter_type)
            and (not date_filter or e["date"].startswith(date_filter))  # Match full or partial date
        ]

        log_text.config(state=tk.NORMAL)
        log_text.delete("1.0", tk.END)

        for e in filtered:
            log_text.insert(tk.END, f"{e['date']} - {e['type']}: ${e['amount']} - {e['description']}\n")

        log_text.config(state=tk.DISABLED)

    def export_to_csv():
        filename = "budget_log.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "type", "amount", "description"])
            writer.writeheader()
            for e in entries:
                writer.writerow(e)
        messagebox.showinfo("Export Successful", f"Log exported to {filename}")

    if not entries:
        messagebox.showinfo("Log", "No entries to show.")
        return

    log_window = tk.Toplevel(root)
    log_window.title("Budget Log")
    log_window.geometry("450x450")

    tk.Label(log_window, text="Your Budget Log", font=("Helvetica", 12, "bold")).pack(pady=5)

    # Filters
    filter_frame = tk.Frame(log_window)
    filter_frame.pack()

    type_filter_var = tk.StringVar(value="All")
    tk.OptionMenu(filter_frame, type_filter_var, "All", "Income", "Expense").pack(side=tk.LEFT, padx=5)

    tk.Label(filter_frame, text="Date (YYYY-MM or YYYY-MM-DD):").pack(side=tk.LEFT)
    date_entry = tk.Entry(filter_frame, width=12)
    date_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(filter_frame, text="Apply Filter", command=update_log_display).pack(padx=5)

    # Log text area
    log_text = tk.Text(log_window, wrap=tk.WORD, width=50, height=15)
    log_text.pack(padx=10, pady=5)

    tk.Button(log_window, text="Export to CSV", command=export_to_csv).pack(pady=5)

    update_log_display()


    # Header
    tk.Label(log_window, text="Your Budget Log", font=("Helvetica", 12, "bold")).pack(pady=5)

    # Filter options
    filter_frame = tk.Frame(log_window)
    filter_frame.pack()

    tk.Button(filter_frame, text="All", command=lambda: update_log_display("All")).pack(side=tk.LEFT, padx=5)
    tk.Button(filter_frame, text="Date", command=lambda: update_log_display("Date")).pack(side=tk.LEFT, padx=5)
    tk.Button(filter_frame, text="Income", command=lambda: update_log_display("Income")).pack(side=tk.LEFT, padx=5)
    tk.Button(filter_frame, text="Expense", command=lambda: update_log_display("Expense")).pack(side=tk.LEFT, padx=5)

    # Text box for entries
    log_text = tk.Text(log_window, wrap=tk.WORD, width=40, height=15)
    log_text.pack(padx=10, pady=5)

    # Export to CSV button
    tk.Button(log_window, text="Export to CSV", command=export_to_csv).pack(pady=5)

    update_log_display()  # Show all entries by default

def add_entry():
    amount = amount_entry.get()
    description = desc_entry.get()
    entry_type = type_var.get()
    date_of_entry = cal_entry.get_date()

    if not amount or not description or not entry_type:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return

    entry = {'date': date_of_entry,'amount': amount, 'description': description, 'type': entry_type}
    entries.append(entry)
    save_entries()

    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    update_summary()

def update_summary():
    income = sum(e['amount'] for e in entries if e['type'] == 'Income')
    expenses = sum(e['amount'] for e in entries if e['type'] == 'Expense')
    balance = income - expenses
    summary_label.config(text=f"Income: ${income:.2f} | Expenses: ${expenses:.2f} | Balance: ${balance:.2f}")
    print(entries)

# GUI Setup
root = tk.Tk()
root.title("Personal Budget Tracker")
root.geometry("600x500")

# Entry Fields
tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Description:").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Date:").pack()
cal_entry = Calendar(root, selectmode = 'day', year = datetime.now().year , month = datetime.now().month,
               day = datetime.now().day)
cal_entry.pack()

tk.Label(root, text="Type:").pack()
type_var = tk.StringVar()
tk.Radiobutton(root, text="Income", variable=type_var, value="Income").pack()
tk.Radiobutton(root, text="Expense", variable=type_var, value="Expense").pack()

tk.Button(root, text="Add Entry", command=add_entry).pack(pady=10)

summary_label = tk.Label(root, text="Income: $0.00 | Expenses: $0.00 | Balance: $0.00")
summary_label.pack(pady=10)

tk.Button(root, text="View Logs", command=show_logs).pack(pady=10)

load_entries()
update_summary()

root.mainloop()