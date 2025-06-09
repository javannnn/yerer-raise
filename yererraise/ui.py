import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import List, Dict


def edit_name(root: tk.Tk, participant: Dict[str, str]):
    new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=participant['name'], parent=root)
    if new_name:
        participant['name'] = new_name


def create_speaker_window() -> tk.Toplevel:
    window = tk.Toplevel()
    window.title("Speaker View")
    window.geometry("400x300")
    label = tk.Label(window, text="", font=("Helvetica", 24))
    label.pack(expand=True)
    window.label = label  # type: ignore
    return window


def update_speaker_window(window: tk.Toplevel, hands: List[Dict[str, str]]):
    text = "\n".join(p['name'] for p in hands)
    window.label.config(text=text)


def create_main_window(participants: List[Dict[str, str]], update_callback):
    root = tk.Tk()
    root.title("YererRaise")
    listbox = tk.Listbox(root, width=40)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    hands = []

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for p in participants:
            prefix = "✋ " if p in hands else ""
            listbox.insert(tk.END, f"{prefix}{p['name']}")

    def on_double_click(event):
        index = listbox.curselection()
        if not index:
            return
        participant = participants[index[0]]
        edit_name(root, participant)
        refresh_listbox()
        update_callback(hands)

    def toggle_hand():
        index = listbox.curselection()
        if not index:
            messagebox.showinfo("Select", "Select a participant first")
            return
        participant = participants[index[0]]
        if participant in hands:
            hands.remove(participant)
        else:
            hands.append(participant)
        refresh_listbox()
        update_callback(hands)

    listbox.bind("<Double-1>", on_double_click)
    btn_toggle = tk.Button(root, text="Raise/Lower Hand", command=toggle_hand)
    btn_toggle.pack(fill=tk.X)

    refresh_listbox()
    return root

