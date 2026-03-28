import customtkinter as ctk
from datetime import date
from constants import BG, SURFACE, SURFACE2, BORDER, ACCENT, TEXT, MUTED
from ui.widgets import make_table, form_field
from data.store import read_csv, append_csv, INC_FILE


class IncomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self._build()

    def _build(self):
        # Header row
        hdr = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        hdr.pack(fill="x", padx=36, pady=(28, 14))
        ctk.CTkLabel(hdr, text="Income",
                     font=("Georgia", 26, "bold"), text_color=TEXT).pack(side="left")
        ctk.CTkButton(
            hdr, text="+ Record Income", font=("Courier", 12),
            fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
            height=36, corner_radius=6, command=self._show_form
        ).pack(side="right")

        # Main area
        self.main_area = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main_area.pack(fill="both", expand=True, padx=36, pady=(0, 16))

        self._build_history()
        self._build_form()

    def _build_history(self):
        self.history_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        tf, self.tv = make_table(
            self.history_frame,
            ["Amount", "Date", "Source"],
            [130, 120, 260]
        )
        tf.pack(fill="both", expand=True)

    def _build_form(self):
        self.form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        inner = ctk.CTkFrame(self.form_frame, fg_color=SURFACE,
                             corner_radius=8, border_width=1, border_color=BORDER)
        inner.pack(anchor="nw", ipadx=24, ipady=8)

        ctk.CTkLabel(inner, text="Record Income",
                     font=("Georgia", 18, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=24, pady=(20, 14))

        fields = ctk.CTkFrame(inner, fg_color="transparent")
        fields.pack(fill="x", padx=24)

        self.amt_entry    = form_field(fields, "AMOUNT (₹)", "e.g. 50000")
        self.date_entry   = form_field(fields, "DATE (YYYY-MM-DD)", str(date.today()))
        self.date_entry.insert(0, str(date.today()))
        self.source_entry = form_field(fields, "SOURCE", "e.g. Salary, Freelance")

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(anchor="w", padx=24, pady=(4, 20))
        ctk.CTkButton(
            btn_row, text="Save Income", font=("Courier", 12),
            fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
            height=36, corner_radius=6, command=self._save
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            btn_row, text="Cancel", font=("Courier", 12),
            fg_color=SURFACE2, text_color=TEXT, hover_color=BORDER,
            height=36, corner_radius=6, command=self._show_history
        ).pack(side="left")

    # ── View switching ─────────────────────────────────────────────────────────
    def _show_history(self):
        self.form_frame.pack_forget()
        self.history_frame.pack(fill="both", expand=True)
        self._refresh()

    def _show_form(self):
        self.history_frame.pack_forget()
        self.amt_entry.delete(0, "end")
        self.source_entry.delete(0, "end")
        self.form_frame.pack(fill="both", expand=True)

    # ── Data ───────────────────────────────────────────────────────────────────
    def _save(self):
        amt    = self.amt_entry.get().strip()
        dt     = self.date_entry.get().strip()
        source = self.source_entry.get().strip()

        if not amt or not dt or not source:
            self.app.toast("Please fill all fields", error=True)
            return
        try:
            float(amt)
        except ValueError:
            self.app.toast("Amount must be a number", error=True)
            return

        append_csv(INC_FILE, [amt, dt, source])
        self.app.toast("Income recorded!")
        self._show_history()

    def _refresh(self):
        self.tv.delete(*self.tv.get_children())
        for r in read_csv(INC_FILE):
            try:
                self.tv.insert("", "end",
                               values=(f"+₹{float(r[0]):,.0f}", r[1], r[2]))
            except Exception:
                pass

    def on_show(self):
        self._show_history()