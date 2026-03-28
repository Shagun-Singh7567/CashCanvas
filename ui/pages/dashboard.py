import customtkinter as ctk
from constants import BG, MUTED, TEXT, ACCENT, RED, TEAL
from ui.widgets import stat_card, make_table
from data.store import read_csv, TX_FILE, INC_FILE


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=36, pady=28)

        # Header
        ctk.CTkLabel(scroll, text="Dashboard",
                     font=("Georgia", 26, "bold"), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(scroll, text="Your financial overview at a glance",
                     font=("Courier", 11), text_color=MUTED).pack(anchor="w", pady=(4, 22))

        # Stat cards
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 24))
        cards_frame.columnconfigure((0, 1, 2), weight=1)

        self.inc_lbl = stat_card(cards_frame, "TOTAL INCOME",   "₹0", ACCENT, 0)
        self.exp_lbl = stat_card(cards_frame, "TOTAL EXPENSES", "₹0", RED,    1)
        self.bal_lbl = stat_card(cards_frame, "NET BALANCE",    "₹0", TEAL,   2)

        # Recent tables side by side
        bottom = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom.pack(fill="both", expand=True)
        bottom.columnconfigure((0, 1), weight=1)

        left = ctk.CTkFrame(bottom, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="RECENT TRANSACTIONS",
                     font=("Courier", 9), text_color=MUTED).pack(anchor="w", pady=(0, 6))
        tf, self.tx_tv = make_table(left, ["Amount", "Date", "Category"], [110, 100, 130])
        tf.pack(fill="both", expand=True)

        right = ctk.CTkFrame(bottom, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(right, text="RECENT INCOME",
                     font=("Courier", 9), text_color=MUTED).pack(anchor="w", pady=(0, 6))
        inf, self.inc_tv = make_table(right, ["Amount", "Date", "Source"], [110, 100, 140])
        inf.pack(fill="both", expand=True)

    def on_show(self):
        txs  = read_csv(TX_FILE)
        incs = read_csv(INC_FILE)
        total_exp = sum(float(r[0]) for r in txs  if r)
        total_inc = sum(float(r[0]) for r in incs if r)
        bal = total_inc - total_exp

        self.inc_lbl.configure(text=f"₹{total_inc:,.0f}")
        self.exp_lbl.configure(text=f"₹{total_exp:,.0f}")
        self.bal_lbl.configure(text=f"₹{abs(bal):,.0f}",
                               text_color=RED if bal < 0 else TEAL)

        for tv, rows, fmt in [
            (self.tx_tv,  txs[:5],  lambda r: (f"−₹{float(r[0]):,.0f}", r[1], r[3])),
            (self.inc_tv, incs[:5], lambda r: (f"+₹{float(r[0]):,.0f}", r[1], r[2])),
        ]:
            tv.delete(*tv.get_children())
            for r in rows:
                try:
                    tv.insert("", "end", values=fmt(r))
                except Exception:
                    pass