from pathlib import Path
import json
from screeninfo import get_monitors
import tkinter as tk
from tkinter import ttk

CFG_FILE = Path(__file__).with_name("display_config.json")


def _save(cfg: dict):
    CFG_FILE.write_text(json.dumps(cfg))


def _load() -> dict | None:
    if CFG_FILE.exists():
        return json.loads(CFG_FILE.read_text())
    return None


def choose_displays() -> tuple[int, int]:
    """
    Returns (audience_monitor_index, speaker_monitor_index).
    If a saved config exists, that is returned silently.
    """
    saved = _load()
    if saved:
        return saved["audience"], saved["speaker"]

    mons = get_monitors()
    root = tk.Tk(); root.title("Select displays")

    ttk.Label(root, text="Audience display").grid(row=0, column=0, padx=6, pady=4)
    ttk.Label(root, text="Speaker display").grid(row=1, column=0, padx=6, pady=4)

    aud = tk.StringVar(value="0")
    spk = tk.StringVar(value="0")
    for i, m in enumerate(mons):
        label = f"{i}: {m.width}×{m.height} @ {m.x},{m.y}"
        ttk.Radiobutton(root, text=label, variable=aud, value=str(i)).grid(row=0, column=i+1, sticky="w")
        ttk.Radiobutton(root, text=label, variable=spk, value=str(i)).grid(row=1, column=i+1, sticky="w")

    def done():
        a = int(aud.get()); s = int(spk.get())
        _save({"audience": a, "speaker": s})
        root.destroy()
    ttk.Button(root, text="OK", command=done).grid(row=2, column=0, columnspan=len(mons)+1, pady=6)
    root.mainloop()
    return int(aud.get()), int(spk.get())
