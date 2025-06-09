import threading, time, subprocess
from pathlib import Path
from typing import List, Dict, Optional
from tkinter import messagebox
from .zoom_client import ZoomClient
from .config       import load_config
from .display      import choose_displays
from .ui           import (
    operator_window, speaker_window, update_speaker,
    prompt_credentials
)

POLL_INTERVAL = 10  # seconds

class YererRaiseApp:
    def __init__(self, meeting_id: Optional[str] = None):
        # pick monitors -------------------------------------------------------
        self.aud_idx, self.spk_idx = choose_displays()

        self.meeting_id = meeting_id
        self.zoom: Optional[ZoomClient] = None
        if meeting_id:
            try:
                cfg = load_config()
            except FileNotFoundError:
                cfg = prompt_credentials()
            self.zoom = ZoomClient(cfg)

        self.participants: List[Dict[str,str]] = []
        self.speaker = speaker_window(self.spk_idx)
        self.root    = operator_window(
            self._get_participants,
            lambda q: update_speaker(self.speaker, q),
            add = self._add_manual,
            refresh_repo = self._git_pull
        )
        self.root.after(100, self.root.refresh)  # initial draw
        self._start_polling()
        self.root.mainloop()

    # ── operator helpers ────────────────────────────────────────────────────
    def _git_pull(self) -> None:
        try:
            subprocess.check_call(["git", "pull"], cwd=Path(__file__).resolve().parent.parent)
            messagebox.showinfo("Update", "Code updated – restart app to apply.")
        except Exception as exc:
            messagebox.showerror("Update failed", str(exc))

    def _add_manual(self, name: str) -> None:
        self.participants.append({"name": name})
        self.root.refresh()

    def _get_participants(self) -> List[Dict[str,str]]:
        return self.participants

    # ── polling Zoom every N seconds ───────────────────────────────────────
    def _poll_zoom(self):
        while True:
            if self.zoom and self.meeting_id:
                try:
                    self.participants = self.zoom.participants(self.meeting_id)
                    self.root.after(0, self.root.refresh)
                except Exception as exc:
                    print("Zoom polling failed:", exc)
            time.sleep(POLL_INTERVAL)

    def _start_polling(self):
        if self.zoom:
            threading.Thread(target=self._poll_zoom, daemon=True).start()

# ── CLI entrypoint ──────────────────────────────────────────────────────────
def main():
    import argparse, sys
    parser = argparse.ArgumentParser(description="YererRaise")
    parser.add_argument("meeting_id", nargs="?", help="Zoom Meeting ID (empty=manual mode)")
    args = parser.parse_args()
    try:
        YererRaiseApp(args.meeting_id)
    except Exception as exc:
        print("Fatal:", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()
