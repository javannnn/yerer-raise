import threading
import time
from typing import List, Dict

from .zoom_client import ZoomClient
from .config import load_config
from .ui import (
    create_main_window,
    create_speaker_window,
    update_speaker_window,
    prompt_credentials,
)


class YererRaiseApp:
    def __init__(self, meeting_id: str):
        self.meeting_id = meeting_id
        try:
            config = load_config()
        except FileNotFoundError:
            config = prompt_credentials()
        self.zoom = ZoomClient(config)
        self.participants: List[Dict[str, str]] = []
        self.root = None
        self.speaker_window = None

    def fetch_participants(self):
        try:
            self.participants = self.zoom.get_meeting_participants(self.meeting_id)
        except Exception as e:
            print(f"Failed to fetch participants: {e}")

    def start_polling(self):
        def poll():
            while True:
                self.fetch_participants()
                if self.root:
                    self.root.after(0, self.root.refresh_listbox)
                time.sleep(10)
        t = threading.Thread(target=poll, daemon=True)
        t.start()

    def run(self):
        self.fetch_participants()
        self.speaker_window = create_speaker_window()

        def update_callback(hands):
            update_speaker_window(self.speaker_window, hands)

        self.root = create_main_window(lambda: self.participants, update_callback)
        self.root.refresh_listbox()
        self.start_polling()
        self.root.mainloop()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="YererRaise")
    parser.add_argument("meeting_id", help="Zoom meeting ID")
    args = parser.parse_args()

    app = YererRaiseApp(args.meeting_id)
    app.run()


if __name__ == "__main__":
    main()

