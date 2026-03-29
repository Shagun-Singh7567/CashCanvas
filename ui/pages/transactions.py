import threading
import customtkinter as ctk
from datetime import date
from constants import BG, SURFACE, SURFACE2, BORDER, ACCENT, TEXT, MUTED, GOLD
from ui.widgets import make_table, form_field
from data.store import read_csv, append_csv, TX_FILE
from ai.categorizer import suggest_category

CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping",
    "Entertainment", "Health", "Utilities", "Education", "Other"
]


class TransactionsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self._build()

    def _build(self):
        # Header row
        hdr = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        hdr.pack(fill="x", padx=36, pady=(28, 14))
        ctk.CTkLabel(hdr, text="Transactions",
                     font=("Georgia", 26, "bold"), text_color=TEXT).pack(side="left")
        ctk.CTkButton(
            hdr, text="+ New Transaction", font=("Courier", 12),
            fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
            height=36, corner_radius=6, command=self._show_form
        ).pack(side="right")

        self.main_area = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main_area.pack(fill="both", expand=True, padx=36, pady=(0, 16))

        self._build_history()
        self._build_form()

    def _build_history(self):
        self.history_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        tf, self.tv = make_table(
            self.history_frame,
            ["Amount", "Date", "Description", "Category"],
            [110, 100, 260, 140]
        )
        tf.pack(fill="both", expand=True)

    def _build_form(self):
        self.form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        inner = ctk.CTkFrame(self.form_frame, fg_color=SURFACE,
                             corner_radius=8, border_width=1, border_color=BORDER)
        inner.pack(anchor="nw", ipadx=24, ipady=8)

        ctk.CTkLabel(inner, text="New Transaction",
                     font=("Georgia", 18, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=24, pady=(20, 14))

        fields = ctk.CTkFrame(inner, fg_color="transparent")
        fields.pack(fill="x", padx=24)

        self.amt_entry  = form_field(fields, "AMOUNT (Rs)", "e.g. 500")
        self.date_entry = form_field(fields, "DATE (YYYY-MM-DD)", str(date.today()))
        self.date_entry.insert(0, str(date.today()))
        self.desc_entry = form_field(fields, "DESCRIPTION", "e.g. Groceries at BigMart")

        # AI suggest row — label + button on same line, dropdown below
        cat_header = ctk.CTkFrame(fields, fg_color="transparent")
        cat_header.pack(fill="x", pady=(0, 3))
        ctk.CTkLabel(cat_header, text="CATEGORY",
                     font=("Courier", 9), text_color=MUTED).pack(side="left")
        self.suggest_btn = ctk.CTkButton(
            cat_header,
            text="AI Suggest",
            font=("Courier", 9), height=22,
            fg_color=GOLD, text_color=BG,
            hover_color="#f5d68a", corner_radius=4,
            command=self._suggest_category
        )
        self.suggest_btn.pack(side="right")

        self.cat_entry = ctk.CTkOptionMenu(
            fields, values=CATEGORIES,
            fg_color=BG, button_color=SURFACE2,
            button_hover_color=BORDER,
            text_color=TEXT, font=("Courier", 12)
        )
        self.cat_entry.pack(fill="x", pady=(0, 12))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(anchor="w", padx=24, pady=(4, 20))
        ctk.CTkButton(
            btn_row, text="Save Transaction", font=("Courier", 12),
            fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
            height=36, corner_radius=6, command=self._save
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            btn_row, text="Cancel", font=("Courier", 12),
            fg_color=SURFACE2, text_color=TEXT, hover_color=BORDER,
            height=36, corner_radius=6, command=self._show_history
        ).pack(side="left")

    # AI suggestion
    def _suggest_category(self):
        description = self.desc_entry.get().strip()
        if not description:
            self.app.toast("Enter a description first", error=True)
            return
        self.suggest_btn.configure(text="Thinking...", state="disabled")

        def worker():
            try:
                category = suggest_category(description)
                self.after(0, lambda: self._apply_suggestion(category))
            except RuntimeError as e:
                self.after(0, lambda: self.app.toast(str(e)[:80], error=True))
                self.after(0, lambda: self.suggest_btn.configure(
                    text="AI Suggest", state="normal"))

        threading.Thread(target=worker, daemon=True).start()

    def _apply_suggestion(self, category: str):
        self.cat_entry.set(category)
        self.suggest_btn.configure(text="AI Suggest", state="normal")
        self.app.toast(f"Suggested: {category}")

    def _show_history(self):
        self.form_frame.pack_forget()
        self.history_frame.pack(fill="both", expand=True)
        self._refresh()

    def _show_form(self):
        self.history_frame.pack_forget()
        self.amt_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.form_frame.pack(fill="both", expand=True)

    def _save(self):
        amt  = self.amt_entry.get().strip()
        dt   = self.date_entry.get().strip()
        desc = self.desc_entry.get().strip()
        cat  = self.cat_entry.get()
        if not amt or not dt or not desc:
            self.app.toast("Please fill all fields", error=True)
            return
        try:
            float(amt)
        except ValueError:
            self.app.toast("Amount must be a number", error=True)
            return
        append_csv(TX_FILE, [amt, dt, desc, cat])
        self.app.toast("Transaction saved!")
        self._show_history()

    def _refresh(self):
        self.tv.delete(*self.tv.get_children())
        for r in read_csv(TX_FILE):
            try:
                self.tv.insert("", "end",
                               values=(f"-Rs{float(r[0]):,.0f}", r[1], r[2], r[3]))
            except Exception:
                pass

    def on_show(self):
        self._show_history()
