import threading
import customtkinter as ctk
from constants import BG, SURFACE, SURFACE2, BORDER, ACCENT, GOLD, TEXT, MUTED, RED
from ai.insights import get_insights
from ai.tips     import get_tips


class AIAssistantPage(ctk.CTkFrame):
    """
    A page with two panels:
      - Spending Insights: AI analysis of patterns in the user's data
      - Budget Tips:       Actionable advice tailored to their spending
    Each panel has a "Generate" button that calls the API in a background
    thread so the UI never freezes.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=36, pady=28)

        # ── Page header ────────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="AI Assistant",
                     font=("Georgia", 26, "bold"), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(
            scroll,
            text="Powered by Claude — insights and tips based on your real data",
            font=("Courier", 11), text_color=MUTED
        ).pack(anchor="w", pady=(4, 28))

        # ── Two panels side by side ────────────────────────────────────────────
        panels = ctk.CTkFrame(scroll, fg_color="transparent")
        panels.pack(fill="both", expand=True)
        panels.columnconfigure((0, 1), weight=1)

        self.insights_box = self._build_panel(
            panels, col=0,
            title="Spending Insights",
            subtitle="What your data says about your habits",
            btn_text="Generate Insights",
            btn_color=ACCENT,
            handler=self._run_insights,
        )

        self.tips_box = self._build_panel(
            panels, col=1,
            title="Budget Tips",
            subtitle="Personalised advice to help you save more",
            btn_text="Generate Tips",
            btn_color=GOLD,
            handler=self._run_tips,
        )

    def _build_panel(self, parent, col, title, subtitle, btn_text, btn_color, handler):
        """
        Builds one card panel and returns the CTkTextbox inside it
        so the caller can write AI output into it later.
        """
        card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=8,
                            border_width=1, border_color=BORDER)
        card.grid(row=0, column=col,
                  padx=(0 if col == 0 else 12, 0),
                  sticky="nsew", pady=0)

        # Coloured top bar
        ctk.CTkFrame(card, height=3, fg_color=btn_color,
                     corner_radius=0).pack(fill="x")

        # Title + subtitle
        ctk.CTkLabel(card, text=title,
                     font=("Georgia", 16, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(card, text=subtitle,
                     font=("Courier", 10), text_color=MUTED).pack(anchor="w", padx=20)

        # Output textbox (read-only)
        textbox = ctk.CTkTextbox(
            card, height=260,
            fg_color=SURFACE2, border_color=BORDER, border_width=1,
            text_color=TEXT, font=("Courier", 12),
            corner_radius=6, wrap="word", state="disabled"
        )
        textbox.pack(fill="both", expand=True, padx=20, pady=(14, 12))

        # Generate button
        btn = ctk.CTkButton(
            card, text=btn_text, font=("Courier", 12),
            fg_color=btn_color,
            text_color=BG if btn_color == ACCENT else BG,
            hover_color="#cef79a" if btn_color == ACCENT else "#f5d68a",
            height=36, corner_radius=6,
            command=handler
        )
        btn.pack(anchor="w", padx=20, pady=(0, 20))

        return textbox

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _set_text(self, textbox: ctk.CTkTextbox, text: str):
        """Replace all text in a textbox (must be called from the main thread)."""
        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        textbox.insert("0.0", text)
        textbox.configure(state="disabled")

    def _run_in_thread(self, textbox: ctk.CTkTextbox, fn, empty_msg: str):
        """
        Show a loading message, then call fn() in a background thread.
        When done, write the result (or error) back into the textbox.
        This keeps the UI responsive while waiting for the API.
        """
        self._set_text(textbox, "⏳  Thinking…")

        def worker():
            try:
                result = fn()
                text = result if result else empty_msg
            except RuntimeError as e:
                text = f"⚠️  Error:\n\n{e}"
            # Schedule the UI update back on the main thread
            self.after(0, lambda: self._set_text(textbox, text))

        threading.Thread(target=worker, daemon=True).start()

    # ── Button handlers ────────────────────────────────────────────────────────
    def _run_insights(self):
        self._run_in_thread(
            self.insights_box,
            get_insights,
            "📭  No transaction data yet.\nAdd some transactions first!"
        )

    def _run_tips(self):
        self._run_in_thread(
            self.tips_box,
            get_tips,
            "📭  No transaction data yet.\nAdd some transactions first!"
        )

    def on_show(self):
        pass