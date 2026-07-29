"""
main.py
Ranui Family Clothing Allowance App — Tkinter GUI entry point.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from models   import Child, Family, ANNUAL_ALLOWANCE, BONUS_THRESHOLD
from database import (init_db, load_children, save_balance,
                      reset_all_balances, record_transaction, get_transactions,
                      clear_transactions)

# ── Palette ─────────────────────────────────────────────────
BG       = "#f0f4f8"
DARK     = "#2c3e50"
BLUE     = "#3498db"
GREEN    = "#27ae60"
ORANGE   = "#e67e22"
PURPLE   = "#8e44ad"
RED      = "#e74c3c"
WHITE    = "#ffffff"
GREY     = "#bdc3c7"
SUBTEXT  = "#7f8c8d"
HEADER   = "#1a252f"

CHILD_COLOURS = {"Nikau": "#3498db", "Hana": "#e91e8c", "Tia": "#27ae60"}


# ════════════════════════════════════════════════════════════
#  App
# ════════════════════════════════════════════════════════════
class RanuiApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ranui Family — Clothing Allowance")
        self.root.geometry("540x620")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── Bootstrap ────────────────────────────────────
        init_db()
        self.family = Family("Ranui")
        self._load_family()

        # ── Build UI ─────────────────────────────────────
        self._build_menu()
        self._build_header()
        self._build_dashboard()
        self._build_purchase_panel()
        self._build_footer()

    # ── Data helpers ─────────────────────────────────────
    def _load_family(self):
        self.family = Family("Ranui")
        for row in load_children():
            self.family.add_child(Child(row["name"], row["balance"]))

    def _sync_db(self):
        for child in self.family.children:
            save_balance(child.name, child.balance)

    # ── Menu bar ─────────────────────────────────────────
    def _build_menu(self):
        menubar = tk.Menu(self.root)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="View Transaction History", command=self.show_history)
        file_menu.add_separator()
        file_menu.add_command(label="Reset All Allowances",     command=self.reset_allowances)
        file_menu.add_command(label="Clear Transaction History", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Year End
        year_menu = tk.Menu(menubar, tearoff=0)
        year_menu.add_command(label="End of Year Summary", command=self.end_of_year)
        menubar.add_cascade(label="Year End", menu=year_menu)

        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    # ── Header ───────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=HEADER, height=75)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Ranui Family", font=("Arial", 22, "bold"),
                 bg=HEADER, fg=WHITE).pack(pady=(12, 0))
        tk.Label(hdr, text="Clothing Allowance Tracker", font=("Arial", 10),
                 bg=HEADER, fg=GREY).pack()

    # ── Dashboard cards ──────────────────────────────────
    def _build_dashboard(self):
        self.card_frame = tk.Frame(self.root, bg=BG)
        self.card_frame.pack(fill="x", padx=18, pady=14)
        self.cards: dict[str, dict] = {}
        self._render_cards()

    def _render_cards(self):
        for w in self.card_frame.winfo_children():
            w.destroy()
        for child in self.family.children:
            self._make_card(child)

    def _make_card(self, child: Child):
        colour = CHILD_COLOURS.get(child.name, BLUE)
        card = tk.Frame(self.card_frame, bg=WHITE, bd=0, relief="flat",
                        highlightbackground=colour, highlightthickness=2)
        card.pack(side="left", expand=True, fill="both", padx=5)

        # Colour strip
        tk.Frame(card, bg=colour, height=6).pack(fill="x")

        tk.Label(card, text=child.name, font=("Arial", 13, "bold"),
                 bg=WHITE, fg=DARK).pack(pady=(8, 2))

        bal_colour = GREEN if child.balance > BONUS_THRESHOLD else (ORANGE if child.balance > 0 else RED)
        bal_lbl = tk.Label(card, text=f"${child.balance:.2f}",
                           font=("Arial", 18, "bold"), bg=WHITE, fg=bal_colour)
        bal_lbl.pack()

        tk.Label(card, text="remaining", font=("Arial", 8),
                 bg=WHITE, fg=SUBTEXT).pack()

        # Progress bar
        pct = child.balance / ANNUAL_ALLOWANCE
        bar_bg = tk.Frame(card, bg="#e0e0e0", height=8, width=120)
        bar_bg.pack(pady=5)
        bar_bg.pack_propagate(False)
        bar_fill = tk.Frame(bar_bg, bg=bal_colour, height=8,
                            width=max(0, int(120 * pct)))
        bar_fill.place(x=0, y=0)

        bonus_colour = GREEN if child.on_target_for_bonus else RED
        tk.Label(card, text=child.bonus_status, font=("Arial", 8),
                 bg=WHITE, fg=bonus_colour, wraplength=120).pack(pady=(0, 10))

        self.cards[child.name] = {"bal_lbl": bal_lbl, "bar_fill": bar_fill}

    def _refresh_cards(self):
        self._render_cards()

    # ── Purchase panel ───────────────────────────────────
    def _build_purchase_panel(self):
        panel = tk.LabelFrame(self.root, text="  Make a Purchase  ",
                              font=("Arial", 11, "bold"),
                              bg=BG, fg=DARK, bd=1, relief="groove",
                              padx=15, pady=12)
        panel.pack(fill="x", padx=18, pady=(0, 10))

        # Row 1: Child selector
        row1 = tk.Frame(panel, bg=BG)
        row1.pack(fill="x", pady=4)
        tk.Label(row1, text="Child:", font=("Arial", 10, "bold"),
                 bg=BG, fg=DARK, width=12, anchor="w").pack(side="left")
        self.selected_child = tk.StringVar(value=self.family.children[0].name)
        for child in self.family.children:
            colour = CHILD_COLOURS.get(child.name, BLUE)
            tk.Radiobutton(row1, text=child.name, variable=self.selected_child,
                           value=child.name, bg=BG, fg=colour,
                           selectcolor=BG, activebackground=BG,
                           font=("Arial", 10, "bold")).pack(side="left", padx=10)

        # Row 2: Amount
        row2 = tk.Frame(panel, bg=BG)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text="Amount ($):", font=("Arial", 10, "bold"),
                 bg=BG, fg=DARK, width=12, anchor="w").pack(side="left")
        self.amount_var = tk.StringVar()
        tk.Entry(row2, textvariable=self.amount_var, font=("Arial", 11),
                 width=12, relief="solid", bd=1).pack(side="left", padx=5)

        # Row 3: Description
        row3 = tk.Frame(panel, bg=BG)
        row3.pack(fill="x", pady=4)
        tk.Label(row3, text="Item (optional):", font=("Arial", 10, "bold"),
                 bg=BG, fg=DARK, width=12, anchor="w").pack(side="left")
        self.desc_var = tk.StringVar()
        tk.Entry(row3, textvariable=self.desc_var, font=("Arial", 10),
                 width=24, relief="solid", bd=1).pack(side="left", padx=5)

        # Button
        tk.Button(panel, text="💳  Confirm Purchase",
                  command=self.make_purchase,
                  bg=GREEN, fg=WHITE, font=("Arial", 11, "bold"),
                  padx=20, pady=7, relief="flat", cursor="hand2").pack(pady=(8, 0))

    # ── Footer ───────────────────────────────────────────
    def _build_footer(self):
        tk.Label(self.root,
                 text="Data saved to SQLite  •  Ranui Family App  •  © 2025",
                 font=("Arial", 8), bg=BG, fg=GREY).pack(side="bottom", pady=6)

    # ════════════════════════════════════════════════════
    #  Actions
    # ════════════════════════════════════════════════════

    def make_purchase(self):
        name   = self.selected_child.get()
        desc   = self.desc_var.get().strip()
        child  = self.family.get_child(name)

        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid dollar amount.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than $0.")
            return

        success = child.spend(amount)
        if not success:
            messagebox.showerror(
                "Purchase Declined ❌",
                f"{name} only has ${child.balance:.2f} remaining.\n"
                f"This purchase of ${amount:.2f} would exceed their allowance."
            )
            return

        save_balance(name, child.balance)
        record_transaction(name, amount, desc)
        self.amount_var.set("")
        self.desc_var.set("")
        self._refresh_cards()

        messagebox.showinfo(
            "Purchase Approved ✅",
            f"${amount:.2f} deducted from {name}'s allowance.\n"
            f"Remaining balance: ${child.balance:.2f}\n"
            f"Bonus status: {child.bonus_status}"
        )

    def reset_allowances(self):
        if messagebox.askyesno("Reset Allowances",
                               "Reset ALL balances back to $300?\nThis cannot be undone."):
            self.family.reset_all()
            reset_all_balances()
            self._refresh_cards()
            messagebox.showinfo("Reset Complete", "All allowances reset to $300.00.")

    def clear_history(self):
        if messagebox.askyesno("Clear History",
                               "Delete all transaction history?\nThis cannot be undone."):
            clear_transactions()
            messagebox.showinfo("Cleared", "Transaction history cleared.")

    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("Transaction History")
        win.geometry("580x400")
        win.configure(bg=BG)

        tk.Label(win, text="Transaction History", font=("Arial", 14, "bold"),
                 bg=BG, fg=DARK).pack(pady=10)

        # Filter
        filter_frame = tk.Frame(win, bg=BG)
        filter_frame.pack(fill="x", padx=15)
        tk.Label(filter_frame, text="Filter by child:", bg=BG,
                 font=("Arial", 10)).pack(side="left")
        filter_var = tk.StringVar(value="All")
        names = ["All"] + [c.name for c in self.family.children]
        cb = ttk.Combobox(filter_frame, textvariable=filter_var,
                          values=names, state="readonly", width=12)
        cb.pack(side="left", padx=8)

        # Table
        cols = ("Child", "Amount", "Item", "Date/Time")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=14)
        for col in cols:
            tree.heading(col, text=col)
        tree.column("Child",     width=90)
        tree.column("Amount",    width=80)
        tree.column("Item",      width=180)
        tree.column("Date/Time", width=150)

        sb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=8)
        sb.pack(side="right", fill="y", pady=8, padx=(0, 15))

        def reload_tree(*_):
            tree.delete(*tree.get_children())
            child_filter = filter_var.get()
            txns = get_transactions(None if child_filter == "All" else child_filter)
            for t in txns:
                tree.insert("", "end", values=(
                    t["child_name"],
                    f"${t['amount']:.2f}",
                    t["description"] or "—",
                    t["timestamp"]
                ))

        cb.bind("<<ComboboxSelected>>", reload_tree)
        reload_tree()

    def end_of_year(self):
        win = tk.Toplevel(self.root)
        win.title("End of Year Summary")
        win.geometry("420x380")
        win.configure(bg=BG)

        tk.Label(win, text="End of Year Summary", font=("Arial", 15, "bold"),
                 bg=BG, fg=DARK).pack(pady=12)

        for child in self.family.children:
            colour = CHILD_COLOURS.get(child.name, BLUE)
            row = tk.Frame(win, bg=WHITE, bd=1, relief="solid")
            row.pack(fill="x", padx=25, pady=4)

            tk.Frame(row, bg=colour, width=6).pack(side="left", fill="y")
            info = tk.Frame(row, bg=WHITE)
            info.pack(side="left", fill="x", expand=True, padx=10, pady=8)

            tk.Label(info, text=child.name, font=("Arial", 12, "bold"),
                     bg=WHITE, fg=DARK).pack(anchor="w")
            tk.Label(info, text=f"Balance remaining: ${child.balance:.2f}",
                     font=("Arial", 10), bg=WHITE, fg=SUBTEXT).pack(anchor="w")

            bc = GREEN if child.on_target_for_bonus else RED
            tk.Label(info, text=child.bonus_status,
                     font=("Arial", 10, "bold"), bg=WHITE, fg=bc).pack(anchor="w")

        # Record bonus activities
        eligible = self.family.bonus_eligible()
        if eligible:
            tk.Label(win, text="Record bonus activities below:",
                     font=("Arial", 10, "bold"), bg=BG, fg=DARK).pack(pady=(12, 4))

            def record():
                for child in eligible:
                    act = simpledialog.askstring(
                        "Bonus Activity 🎉",
                        f"{child.name} earns a bonus!\nEnter their chosen activity:",
                        parent=win
                    )
                    if act:
                        messagebox.showinfo("Recorded ✅",
                                            f"{child.name}'s bonus: {act}", parent=win)

            tk.Button(win, text="🎉  Record Bonus Activities", command=record,
                      bg=PURPLE, fg=WHITE, font=("Arial", 11, "bold"),
                      padx=15, pady=7, relief="flat", cursor="hand2").pack()
        else:
            tk.Label(win, text="No children qualify for a bonus this year.",
                     font=("Arial", 10), bg=BG, fg=SUBTEXT).pack(pady=10)

        tk.Button(win, text="Close", command=win.destroy,
                  bg=GREY, fg=DARK, font=("Arial", 10),
                  padx=20, pady=5, relief="flat").pack(pady=12)

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Ranui Family Clothing Allowance App\n\n"
            "Built with Python + Tkinter + SQLite\n"
            "Uses OOP: Family & Child classes\n\n"
            "Annual allowance: $300 per child\n"
            "Bonus threshold:  >$50 remaining\n\n"
            "© 2025 — IT Internship Project"
        )


# ── Entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = RanuiApp(root)
    root.mainloop()
