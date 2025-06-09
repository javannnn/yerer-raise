import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import List, Dict, Callable, Optional


def edit_name(root: tk.Tk, participant: Dict[str, str]):
    new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=participant['name'], parent=root)
    if new_name:
        participant['name'] = new_name


def create_speaker_window() -> tk.Toplevel:
    """Create the full-screen speaker display window."""
    window = tk.Toplevel()
    window.title("Speaker View")
    window.geometry("600x400")
    label = tk.Label(window, text="", font=("Helvetica", 32))
    label.pack(expand=True)
    window.label = label  # type: ignore
    return window


def update_speaker_window(window: tk.Toplevel, hands: List[Dict[str, str]]):
    """Update the speaker view with the queue of raised hands."""
    text = "\n".join(p['name'] for p in hands)
    window.label.config(text=text)


def prompt_credentials() -> Dict[str, str]:
    """Prompt the user for Zoom API credentials."""
    root = tk.Tk()
    root.withdraw()

    account_id = simpledialog.askstring("Zoom Credentials", "Account ID:", parent=root)
    client_id = simpledialog.askstring("Zoom Credentials", "Client ID:", parent=root)
    client_secret = simpledialog.askstring(
        "Zoom Credentials",
        "Client Secret:",
        parent=root,
        show="*",
    )

    root.destroy()

    if not account_id or not client_id or not client_secret:
        messagebox.showerror("Error", "All credential fields are required")
        raise ValueError("Missing Zoom credentials")

    return {
        "account_id": account_id,
        "client_id": client_id,
        "client_secret": client_secret,
    }


def create_main_window(
    get_participants: Callable[[], List[Dict[str, str]]],
    update_callback: Callable[[List[Dict[str, str]]], None],
    add_participant: Optional[Callable[[str], None]] = None,
):
    root = tk.Tk()
    root.title("YererRaise")

    search_var = tk.StringVar()
    entry_search = tk.Entry(root, textvariable=search_var)
    entry_search.pack(fill=tk.X)

    listbox = tk.Listbox(root, width=40)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    hands: List[Dict[str, str]] = []

    def refresh_listbox(*_):
        listbox.delete(0, tk.END)
        search = search_var.get().lower()
        for p in get_participants():
            if search and search not in p['name'].lower():
                continue
            prefix = "✋ " if p in hands else ""
            listbox.insert(tk.END, f"{prefix}{p['name']}")

    def on_double_click(event):
        index = listbox.curselection()
        if not index:
            return
        participant = get_participants()[index[0]]
        edit_name(root, participant)
        refresh_listbox()
        update_callback(hands)

    def toggle_hand():
        index = listbox.curselection()
        if not index:
            messagebox.showinfo("Select", "Select a participant first")
            return
        participant = get_participants()[index[0]]
        if participant in hands:
            hands.remove(participant)
        else:
            hands.append(participant)
        refresh_listbox()
        update_callback(hands)

    def add_participant_dialog():
        if not add_participant:
            return
        name = simpledialog.askstring("Add Participant", "Name:", parent=root)
        if name:
            add_participant(name)
            refresh_listbox()

    listbox.bind("<Double-1>", on_double_click)
    btn_toggle = tk.Button(root, text="Raise/Lower Hand", command=toggle_hand)
    btn_toggle.pack(fill=tk.X)
    if add_participant:
        btn_add = tk.Button(root, text="Add Participant", command=add_participant_dialog)
        btn_add.pack(fill=tk.X)

    btn_clear = tk.Button(root, text="Clear All", command=lambda: (hands.clear(), refresh_listbox(), update_callback(hands)))
    btn_clear.pack(fill=tk.X)

    search_var.trace_add('write', refresh_listbox)

    refresh_listbox()
    root.refresh_listbox = refresh_listbox  # type: ignore
    return root

