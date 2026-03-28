import customtkinter as ctk
from constants import BG, SURFACE, SURFACE2, BORDER, ACCENT, MUTED, RED, TEXT
from ui.pages.dashboard    import DashboardPage
from ui.pages.transactions import TransactionsPage
from ui.pages.income       import IncomePage
from ui.pages.charts       import ChartsPage
from data.store import ensure_files

ensure_files()


class CashCanvas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CashCanvas — Finance Tracker")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(fg_color=BG)

        self._build_sidebar()
        self._build_content()
        self.show_page("dashboard")

    # ── Sidebar ────────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=210, fg_color=SURFACE, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=22, pady=(28, 18))
        ctk.CTkLabel(logo_frame, text="CashCanvas",
                     font=("Georgia", 22, "bold"), text_color=ACCENT).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="FINANCE TRACKER",
                     font=("Courier", 9), text_color=MUTED).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(fill="x")

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("dashboard",    "◈  Dashboard"),
            ("transactions", "↕  Transactions"),
            ("income",       "↑  Income"),
            ("charts",       "◎  Charts"),
        ]
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(16, 0))
        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav_frame, text=label, anchor="w",
                font=("Courier", 12), height=40,
                fg_color="transparent", hover_color=SURFACE2,
                text_color=MUTED, corner_radius=0,
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        ctk.CTkLabel(self.sidebar, text="v1.0",
                     font=("Courier", 10), text_color=MUTED).pack(side="bottom", pady=16)

    def _set_active_nav(self, key):
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(text_color=ACCENT, fg_color=SURFACE2)
            else:
                btn.configure(text_color=MUTED, fg_color="transparent")

    # ── Content area ───────────────────────────────────────────────────────────
    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        for name, cls in [
            ("dashboard",    DashboardPage),
            ("transactions", TransactionsPage),
            ("income",       IncomePage),
            ("charts",       ChartsPage),
        ]:
            page = cls(self.content, self)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[name] = page

    def show_page(self, key):
        self._set_active_nav(key)
        for k, page in self.pages.items():
            if k == key:
                page.lift()
                page.on_show()

    # ── Toast notification ─────────────────────────────────────────────────────
    def toast(self, msg, error=False):
        color = RED if error else ACCENT
        t = ctk.CTkToplevel(self)
        t.overrideredirect(True)
        t.attributes("-topmost", True)
        t.configure(fg_color=color)
        x = self.winfo_x() + self.winfo_width() - 320
        y = self.winfo_y() + self.winfo_height() - 80
        t.geometry(f"280x44+{x}+{y}")
        ctk.CTkLabel(
            t, text=msg,
            font=("Courier", 12, "bold"),
            text_color="#0d0f0e" if not error else TEXT
        ).pack(expand=True)
        t.after(2500, t.destroy)