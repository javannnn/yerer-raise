import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import List, Dict, Callable, Optional
from screeninfo import get_monitors

# ── tiny styling helper ───────────────────────────────────────────────────────
def _style():
    s = ttk.Style()
    if s.theme_use() == "clam":
        s.theme_use("default")
    s.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
_style()

# ── dialogs ───────────────────────────────────────────────────────────────────

def edit_name(parent: tk.Tk, part: Dict[str, str]) -> None:
    new = simpledialog.askstring("Edit name", "New name:", initialvalue=part["name"], parent=parent)
    if new:
        part["name"] = new

def prompt_credentials() -> Dict[str, str]:
    root = tk.Tk(); root.withdraw()
    aid = simpledialog.askstring("Zoom", "Account ID:", parent=root)
    cid = simpledialog.askstring("Zoom", "Client ID:", parent=root)
    sec = simpledialog.askstring("Zoom", "Client Secret:", show="*", parent=root)
    root.destroy()
    if not all((aid, cid, sec)):
        raise ValueError("All Zoom credentials required")
    return {"account_id": aid, "client_id": cid, "client_secret": sec}

# ── speaker view (55'' TV) ────────────────────────────────────────────────────

def speaker_window(monitor_index: int) -> tk.Toplevel:
    mon = get_monitors()[monitor_index]
    win = tk.Toplevel()
    win.overrideredirect(True)           # borderless
    win.geometry(f"{mon.width}x{mon.height}+{mon.x}+{mon.y}")
    win.configure(bg="black")

    lbl = tk.Label(
        win, text="", fg="white", bg="black",
        justify="center", anchor="center"
    )
    lbl.pack(expand=True, fill="both")
    win.label = lbl           # type: ignore
    return win

def _fit_font(label: tk.Label, text: str):
    """Dynamically shrink font so text fits width (~85 %)."""
    w = label.winfo_width() or label.master.winfo_width()
    if w == 1: return  # window not realised yet
    size = int(w * 0.085)      # heuristically 8.5 % of width
    label.config(font=("Segoe UI", size, "bold"))

def update_speaker(win: tk.Toplevel, queue: List[Dict[str, str]]):
    txt = "\n".join(p["name"] for p in queue[:4]) or " "   # keep label height
    win.label.config(text=txt)
    _fit_font(win.label, txt)

# ── operator window ───────────────────────────────────────────────────────────

def operator_window(
    fetch: Callable[[], List[Dict[str, str]]],
    push : Callable[[List[Dict[str, str]]], None],
    add  : Optional[Callable[[str], None]] = None,
    refresh_repo: Optional[Callable[[], None]] = None,
) -> tk.Tk:
    root = tk.Tk(); root.title("YererRaise")

    # search box
    query = tk.StringVar()
    ttk.Entry(root, textvariable=query).pack(fill="x", padx=6, pady=(6,2))

    # list / queue
    tree = ttk.Treeview(root, show="tree", selectmode="browse")
    tree.pack(side="left", fill="both", expand=True, padx=(6,0), pady=6)
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.pack(side="left", fill="y", pady=6)
    tree.configure(yscrollcommand=vsb.set)

    queue: List[Dict[str, str]] = []

    def redraw(*_):
        tree.delete(*tree.get_children())
        q = query.get().lower()
        for p in fetch():
            if q and q not in p["name"].lower(): continue
            tag = "hand" if p in queue else ""
            tree.insert("", "end", text=("✋ " if tag else "") + p["name"], tags=(tag,))
        push(queue)
    tree.tag_configure("hand", foreground="#d35400")
    query.trace_add("write", redraw)

    # interactions
    def on_double(_):
        sel = tree.focus()
        if not sel: return
        idx = tree.index(sel)
        part = fetch()[idx]
        edit_name(root, part); redraw()
    def toggle():
        sel = tree.focus()
        if not sel: return
        part = fetch()[tree.index(sel)]
        queue.remove(part) if part in queue else queue.append(part)
        redraw()
    def clear():
        queue.clear(); redraw()
    def add_dialog():
        if not add: return
        name = simpledialog.askstring("Add participant", "Name:", parent=root)
        if name: add(name); redraw()

    tree.bind("<Double-1>", on_double)
    ttk.Button(root, text="Raise / Lower (Space)", command=toggle).pack(fill="x", padx=6, pady=(0,4))
    if add:
        ttk.Button(root, text="Add participant", command=add_dialog).pack(fill="x", padx=6, pady=(0,4))
    ttk.Button(root, text="Clear all", command=clear).pack(fill="x", padx=6, pady=(0,4))
    if refresh_repo:
        ttk.Button(root, text="Update code", command=refresh_repo).pack(fill="x", padx=6, pady=(0,4))

    root.bind("<space>", lambda e: toggle())
    root.refresh = redraw  # type: ignore
    return root
