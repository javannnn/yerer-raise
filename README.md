# YererRaise

Modern hand-raising assistant for Yerer Congregation hybrid meetings.

**What does it do?**
- Fetches live participants from your Zoom meeting (Business plan required)
- Lets you edit names for clarity and accuracy
- Manual “raised hand” icon to notify the speaker
- Instantly displays who’s raising their hand on a dedicated speaker screen
- Built for the real-world needs of Jehovah’s Witnesses meetings

## Features

- Slick, intuitive Windows interface
- Live Zoom participant fetch via API
- Editable names, manual hand-raise/highlight
- Multi-screen support (audience, speaker)
- Fast, simple, and congregation-friendly
- Works without Zoom by manually adding participants
- Search/filter participants and maintain a queue of raised hands

## Why?

Because Zoom doesn’t let you track hands automatically, and the Kingdom Hall deserves better than sticky notes and chaos.

## Tech Stack

- Python (Tkinter/PySide)
- Zoom Dashboard API
- Multi-monitor support

## Setup

### Linux
1. Register your Zoom app on the [Zoom Marketplace](https://marketplace.zoom.us/)




2. Install the package with `pip install .`
3. Run the app with `yererraise MEETING_ID` to use the Zoom integration or omit `MEETING_ID` to manage participants manually. Enter your Zoom credentials when prompted.
4. Plug in your screen setup and start the meeting. Use the `Update` button at any time to pull the latest version.

### Windows
1. Install [Python](https://www.python.org/) and clone this repository.
2. Install dependencies with `pip install -r requirements.txt` and `pip install pyinstaller`.
3. Double‑click `build_exe.bat` (or run it from a command prompt) to generate `dist\YererRaise.exe`.
4. Run `YererRaise.exe` to start the app. You can also install with `pip install .` and launch via the `yererraise` command.




2. Install the package with `pip install .` or build a standalone executable using `pyinstaller --onefile -n YererRaise yererraise/app.py`.
3. Run the app with `yererraise MEETING_ID` to use the Zoom integration or omit `MEETING_ID` to manage participants manually. Enter your Zoom credentials when prompted.
4. Plug in your screen setup
5. Start the meeting and watch the magic. Use the search box to quickly filter participants, toggle hand-raise status, and clear the queue at any time. The `Update` button pulls the latest version from this repository.


2. Run the app with `python -m yererraise.app MEETING_ID` to use the Zoom integration or omit `MEETING_ID` to manage participants manually. Enter your Zoom credentials when prompted.
3. Plug in your screen setup
4. Start the meeting and watch the magic. Use the search box to quickly filter participants, toggle hand-raise status, and clear the queue at any time.

2. Copy `yererraise/config.sample.json` to `yererraise/config.json` and paste your OAuth credentials
3. Plug in your screen setup
4. Run the app with `python -m yererraise.app MEETING_ID`
5. Start the meeting and watch the magic





## Contributing

Ideas, issues, and PRs welcome. No drama, just Kingdom Hall efficiency.

---

*Developed for Yerer Congregation, but share the love!*

