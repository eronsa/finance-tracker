import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import json
import os

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
    if not entries:
        messagebox.showinfo("Log", "No entries to show.")
        return

    log_window = tk.Toplevel(root)
    log_window.title("Budget Log")
    log_window.geometry("350x300")

    tk.Label(log_window, text="Your Budget Log", font=("Helvetica", 12, "bold")).pack(pady=5)

    log_text = tk.Text(log_window, wrap=tk.WORD, width=40, height=15)
    log_text.pack(padx=10, pady=5)

    for e in entries:
        log_text.insert(tk.END, f"{e['date']} {e['type']}: ${e['amount']} - {e['description']}\n")

    log_text.config(state=tk.DISABLED)  # Make it read-only

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