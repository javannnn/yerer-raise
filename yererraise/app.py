import threading
import time
from typing import List, Dict


from typing import Optional

from .zoom_client import ZoomClient
from .config import load_config
from .ui import (
    create_main_window,
    create_speaker_window,
    update_speaker_window,
    prompt_credentials,
)


class YererRaiseApp:
    def __init__(self, meeting_id: Optional[str] = None):
        """Initialize the application.

        If ``meeting_id`` is provided, Zoom integration will be enabled and the
        user will be asked for credentials if a config file is not found.
        Otherwise the app runs in manual mode.
        """

        self.meeting_id = meeting_id
        self.zoom: Optional[ZoomClient] = None
        if self.meeting_id:
            try:
                config = load_config()
            except FileNotFoundError:
                config = prompt_credentials()
            self.zoom = ZoomClient(config)


from .zoom_client import ZoomClient
from .ui import create_main_window, create_speaker_window, update_speaker_window


class YererRaiseApp:
    def __init__(self, meeting_id: str):
        self.meeting_id = meeting_id
        self.zoom = ZoomClient()

        self.participants: List[Dict[str, str]] = []
        self.root = None
        self.speaker_window = None


    def add_participant(self, name: str):
        """Add a participant manually."""
        self.participants.append({"name": name})
        if self.root:
            self.root.after(0, self.root.refresh_listbox)

    def fetch_participants(self):
        if not self.zoom or not self.meeting_id:
            return

    def fetch_participants(self):

        try:
            self.participants = self.zoom.get_meeting_participants(self.meeting_id)
        except Exception as e:
            print(f"Failed to fetch participants: {e}")

    def start_polling(self):

        if not self.zoom or not self.meeting_id:
            return

        def poll():
            while True:
                self.fetch_participants()
                if self.root:
                    self.root.after(0, self.root.refresh_listbox)
                time.sleep(10)


        def poll():
            while True:
                self.fetch_participants()
                time.sleep(10)

        t = threading.Thread(target=poll, daemon=True)
        t.start()

    def run(self):
        self.fetch_participants()
        self.speaker_window = create_speaker_window()

        def update_callback(hands):
            update_speaker_window(self.speaker_window, hands)


        self.root = create_main_window(
            lambda: self.participants,
            update_callback,
            add_participant=self.add_participant,
        )
        self.root.refresh_listbox()

        self.root = create_main_window(self.participants, update_callback)

        self.start_polling()
        self.root.mainloop()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="YererRaise")

    parser.add_argument(
        "meeting_id",
        nargs="?",
        help="Zoom meeting ID (omit to manage participants manually)",
    )

    parser.add_argument("meeting_id", help="Zoom meeting ID")

    args = parser.parse_args()

    app = YererRaiseApp(args.meeting_id)
    app.run()


if __name__ == "__main__":
    main()

