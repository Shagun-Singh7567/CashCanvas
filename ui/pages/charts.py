import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.figure as mplf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from constants import BG, SURFACE, SURFACE2, BORDER, ACCENT, TEAL, MUTED, TEXT, CHART_COLORS
from data.store import read_csv, TX_FILE


class ChartsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self._canvas_widget = None
        self._build()

    def _build(self):
        # Header
        ctk.CTkLabel(self, text="Charts",
                     font=("Georgia", 26, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=36, pady=(28, 4))
        ctk.CTkLabel(self, text="Visualise your spending patterns",
                     font=("Courier", 11), text_color=MUTED
                     ).pack(anchor="w", padx=36, pady=(0, 16))

        # Chart-type tab switcher
        tab_row = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=8,
                               border_width=1, border_color=BORDER)
        tab_row.pack(fill="x", padx=36, pady=(0, 16))

        self.tab_btns = {}
        tabs = [
            ("pie",  "Pie — Monthly by Category"),
            ("bar",  "Bar — Monthly Totals"),
            ("line", "Line — Daily Expenses"),
        ]
        for key, label in tabs:
            b = ctk.CTkButton(
                tab_row, text=label, font=("Courier", 11),
                fg_color="transparent", text_color=MUTED,
                hover_color=SURFACE2, corner_radius=6, height=36,
                command=lambda k=key: self._switch_tab(k)
            )
            b.pack(side="left", padx=4, pady=4)
            self.tab_btns[key] = b

        # Controls container (pie / bar / line controls swap here)
        self.ctrl_frame = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=8,
                                       border_width=1, border_color=BORDER)
        self.ctrl_frame.pack(fill="x", padx=36, pady=(0, 16))
        self._build_controls()

        # Chart canvas area
        self.chart_area = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=8,
                                       border_width=1, border_color=BORDER)
        self.chart_area.pack(fill="both", expand=True, padx=36, pady=(0, 24))
        self.placeholder = ctk.CTkLabel(
            self.chart_area,
            text="◎\n\nSelect a chart type and click Generate",
            font=("Courier", 13), text_color=MUTED
        )
        self.placeholder.pack(expand=True)

        self._switch_tab("pie")

    def _build_controls(self):
        """Build all three control rows (only one is visible at a time)."""

        # Pie controls
        self.pie_ctrl = ctk.CTkFrame(self.ctrl_frame, fg_color="transparent")
        ctk.CTkLabel(self.pie_ctrl, text="MONTH (MM)", font=("Courier", 9),
                     text_color=MUTED).grid(row=0, column=0, sticky="w", padx=(16, 4), pady=12)
        self.pie_month = ctk.CTkEntry(self.pie_ctrl, placeholder_text="03", width=70,
                                      fg_color=BG, border_color=BORDER, text_color=TEXT)
        self.pie_month.grid(row=0, column=1, padx=4)
        ctk.CTkLabel(self.pie_ctrl, text="YEAR (YYYY)", font=("Courier", 9),
                     text_color=MUTED).grid(row=0, column=2, sticky="w", padx=(16, 4))
        self.pie_year = ctk.CTkEntry(self.pie_ctrl, placeholder_text="2025", width=90,
                                     fg_color=BG, border_color=BORDER, text_color=TEXT)
        self.pie_year.grid(row=0, column=3, padx=4)
        ctk.CTkButton(self.pie_ctrl, text="Generate", font=("Courier", 12),
                      fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
                      height=32, corner_radius=6,
                      command=self._render_pie).grid(row=0, column=4, padx=16)

        # Bar controls
        self.bar_ctrl = ctk.CTkFrame(self.ctrl_frame, fg_color="transparent")
        ctk.CTkLabel(self.bar_ctrl, text="YEAR (YYYY)", font=("Courier", 9),
                     text_color=MUTED).grid(row=0, column=0, sticky="w", padx=(16, 4), pady=12)
        self.bar_year = ctk.CTkEntry(self.bar_ctrl, placeholder_text="2025", width=90,
                                     fg_color=BG, border_color=BORDER, text_color=TEXT)
        self.bar_year.grid(row=0, column=1, padx=4)
        ctk.CTkButton(self.bar_ctrl, text="Generate", font=("Courier", 12),
                      fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
                      height=32, corner_radius=6,
                      command=self._render_bar).grid(row=0, column=2, padx=16)

        # Line controls
        self.line_ctrl = ctk.CTkFrame(self.ctrl_frame, fg_color="transparent")
        ctk.CTkLabel(self.line_ctrl, text="MONTH (YYYY-MM)", font=("Courier", 9),
                     text_color=MUTED).grid(row=0, column=0, sticky="w", padx=(16, 4), pady=12)
        self.line_month = ctk.CTkEntry(self.line_ctrl, placeholder_text="2025-03", width=110,
                                       fg_color=BG, border_color=BORDER, text_color=TEXT)
        self.line_month.grid(row=0, column=1, padx=4)
        ctk.CTkButton(self.line_ctrl, text="Generate", font=("Courier", 12),
                      fg_color=ACCENT, text_color=BG, hover_color="#cef79a",
                      height=32, corner_radius=6,
                      command=self._render_line).grid(row=0, column=2, padx=16)

    # ── Tab switching ──────────────────────────────────────────────────────────
    def _switch_tab(self, tab):
        self.active_tab = tab
        for k, b in self.tab_btns.items():
            b.configure(
                text_color=ACCENT if k == tab else MUTED,
                fg_color=SURFACE2 if k == tab else "transparent"
            )
        for ctrl in [self.pie_ctrl, self.bar_ctrl, self.line_ctrl]:
            ctrl.pack_forget()
        {"pie": self.pie_ctrl, "bar": self.bar_ctrl, "line": self.line_ctrl}[tab].pack(fill="x")

    # ── Chart helpers ──────────────────────────────────────────────────────────
    def _clear_chart(self):
        if self._canvas_widget:
            self._canvas_widget.get_tk_widget().destroy()
            self._canvas_widget = None
        self.placeholder.pack(expand=True)

    def _show_fig(self, fig):
        self.placeholder.pack_forget()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._canvas_widget = canvas

    def _styled_fig(self):
        """Return a (fig, ax) pair pre-styled to match the dark theme."""
        fig = mplf.Figure(figsize=(8, 4), facecolor=SURFACE)
        ax = fig.add_subplot(111)
        ax.set_facecolor(SURFACE)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        return fig, ax

    # ── Renderers ──────────────────────────────────────────────────────────────
    def _render_pie(self):
        month = self.pie_month.get().strip().zfill(2)
        year  = self.pie_year.get().strip()
        if not month or not year:
            self.app.toast("Enter month and year", error=True)
            return

        cats = {}
        for r in read_csv(TX_FILE):
            try:
                y, m = r[1][:4], r[1][5:7]
                if y == year and m == month:
                    cats[r[3]] = cats.get(r[3], 0) + float(r[0])
            except Exception:
                pass

        if not cats:
            self.app.toast("No records for that period", error=True)
            return

        self._clear_chart()
        fig, ax = self._styled_fig()
        wedges, texts, autotexts = ax.pie(
            cats.values(), labels=cats.keys(),
            autopct="%1.1f%%", colors=CHART_COLORS,
            wedgeprops={"edgecolor": SURFACE, "linewidth": 2}
        )
        for t in texts:    t.set_color(TEXT); t.set_fontsize(10)
        for a in autotexts: a.set_color(BG);  a.set_fontsize(9)
        ax.set_title(f"Expenses  {month}/{year}", color=MUTED, fontsize=12, pad=14)
        self._show_fig(fig)

    def _render_bar(self):
        year = self.bar_year.get().strip()
        if not year:
            self.app.toast("Enter a year", error=True)
            return

        months = {}
        for r in read_csv(TX_FILE):
            try:
                if r[1][:4] == year:
                    key = r[1][:7]
                    months[key] = months.get(key, 0) + float(r[0])
            except Exception:
                pass

        if not months:
            self.app.toast("No records for that year", error=True)
            return

        self._clear_chart()
        fig, ax = self._styled_fig()
        keys = sorted(months)
        ax.bar(keys, [months[k] for k in keys],
               color=ACCENT + "99", edgecolor=ACCENT, linewidth=1.2)
        ax.set_title(f"Monthly Expenses — {year}", color=MUTED, fontsize=12, pad=14)
        ax.set_ylabel("Amount (₹)", color=MUTED)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", color=MUTED, fontsize=9)
        fig.tight_layout()
        self._show_fig(fig)

    def _render_line(self):
        month = self.line_month.get().strip()
        if not month or len(month) < 7:
            self.app.toast("Enter month as YYYY-MM", error=True)
            return

        days = {}
        for r in read_csv(TX_FILE):
            try:
                if r[1].startswith(month):
                    days[r[1]] = days.get(r[1], 0) + float(r[0])
            except Exception:
                pass

        if not days:
            self.app.toast("No records for that month", error=True)
            return

        self._clear_chart()
        fig, ax = self._styled_fig()
        keys = sorted(days)
        ax.plot(keys, [days[k] for k in keys],
                color=TEAL, linewidth=2, marker="o",
                markersize=6, markerfacecolor=TEAL)
        ax.fill_between(keys, [days[k] for k in keys], alpha=0.15, color=TEAL)
        ax.set_title(f"Daily Expenses — {month}", color=MUTED, fontsize=12, pad=14)
        ax.set_ylabel("Amount (₹)", color=MUTED)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", color=MUTED, fontsize=9)
        fig.tight_layout()
        self._show_fig(fig)

    def on_show(self):
        pass