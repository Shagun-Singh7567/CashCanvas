import customtkinter as ctk
from tkinter import ttk
from constants import SURFACE, SURFACE2, BORDER, TEXT, MUTED, BG, ACCENT

# ── Section label ──────────────────────────────────────────────────────────────
def section_label(parent, text):
    """Small uppercase muted label used above tables and sections."""
    ctk.CTkLabel(
        parent, text=text,
        font=("Courier", 9), text_color=MUTED
    ).pack(anchor="w", pady=(0, 4))


# ── Stat card ──────────────────────────────────────────────────────────────────
def stat_card(parent, label, value, color, col):
    """
    A summary card with a colored top bar, a label, and a large value.
    Returns the value CTkLabel so the caller can update it later.
    """
    card = ctk.CTkFrame(
        parent, fg_color=SURFACE,
        corner_radius=8, border_width=1, border_color=BORDER
    )
    card.grid(row=0, column=col, padx=(0 if col == 0 else 10, 0), sticky="nsew")

    ctk.CTkFrame(card, height=3, fg_color=color, corner_radius=0).pack(fill="x")
    ctk.CTkLabel(
        card, text=label,
        font=("Courier", 9), text_color=MUTED
    ).pack(anchor="w", padx=16, pady=(10, 2))

    val_label = ctk.CTkLabel(
        card, text=value,
        font=("Georgia", 26, "bold"), text_color=color
    )
    val_label.pack(anchor="w", padx=16, pady=(0, 14))
    return val_label


# ── Data table ─────────────────────────────────────────────────────────────────
def make_table(parent, columns, col_widths=None):
    """
    Creates a styled ttk.Treeview inside a CTkFrame.
    Returns (frame, treeview) so the caller can pack the frame and populate the tv.
    """
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "CC.Treeview",
        background=SURFACE, fieldbackground=SURFACE,
        foreground=TEXT, rowheight=32,
        borderwidth=0, font=("Courier", 11)
    )
    style.configure(
        "CC.Treeview.Heading",
        background=SURFACE2, foreground=MUTED,
        font=("Courier", 9), relief="flat", borderwidth=0
    )
    style.map(
        "CC.Treeview",
        background=[("selected", SURFACE2)],
        foreground=[("selected", ACCENT)]
    )

    frame = ctk.CTkFrame(
        parent, fg_color=SURFACE,
        corner_radius=8, border_width=1, border_color=BORDER
    )
    tv = ttk.Treeview(
        frame, columns=columns,
        show="headings", style="CC.Treeview", selectmode="browse"
    )
    for i, col in enumerate(columns):
        tv.heading(col, text=col.upper())
        tv.column(col, width=col_widths[i] if col_widths else 140, anchor="w")

    scrollbar = ctk.CTkScrollbar(frame, command=tv.yview)
    tv.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y", pady=8)
    tv.pack(fill="both", expand=True, padx=4, pady=4)

    return frame, tv


# ── Form field ─────────────────────────────────────────────────────────────────
def form_field(parent, label, placeholder="", widget_type="entry", options=None):
    """
    Renders a label + input widget and returns the widget.
    widget_type: "entry" for CTkEntry, "option" for CTkOptionMenu.
    """
    ctk.CTkLabel(
        parent, text=label,
        font=("Courier", 9), text_color=MUTED
    ).pack(anchor="w", pady=(0, 3))

    if widget_type == "entry":
        widget = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            fg_color=BG, border_color=BORDER,
            text_color=TEXT, font=("Courier", 12), height=36
        )
    elif widget_type == "option":
        widget = ctk.CTkOptionMenu(
            parent, values=options or [],
            fg_color=BG, button_color=SURFACE2,
            button_hover_color=BORDER,
            text_color=TEXT, font=("Courier", 12)
        )

    widget.pack(fill="x", pady=(0, 12))
    return widget