


# ShadowLoggerX

**ShadowLoggerX** is a stealthy Python-based keylogger that records user keystrokes **per application**, along with active window context and timestamps. Designed for educational and ethical use only — use it in your **own systems**, virtual machines, or labs for **self-monitoring**, productivity tracking, or research.

---

## Disclaimer

> ShadowLoggerX is **NOT** malware.  
> It does **NOT** exfiltrate data, does **NOT** persist silently, and is **NOT** intended for unethical purposes.  
> This tool is for **learning**, **self-analysis**, and **educational penetration testing** in a **controlled environment** only.  
> The developer is not responsible for any misuse.

---

## Features

- ✅ Logs every keystroke typed
- ✅ Groups logs by **active application window**
- ✅ Timestamps every window context switch
- ✅ Saves logs to a **daily `.log` file**
- ✅ Takes a **screenshot when ESC is pressed** (for context capture)
- ✅ Stealthy folder names: logs are saved in `AppData/Windows Update` for minimal visibility

---

## File Structure

```plaintext
AppData/
├── Windows Update/
│   ├── 2025-06-16.log        ← Daily log file
├── ShadowLogs/
│   ├── screenshot_20250616_153522_exit.png ← Screenshot at session end


## Log Format

```plaintext
╔════════════════════════════════════════════════════════════════════════════╗
║                        [ SESSION STARTED: 2025-06-16 15:20:01 ]           ║
╚════════════════════════════════════════════════════════════════════════════╝

⏺️ [chrome.exe - YouTube - Google Chrome - 15:20:05]
hello this is a test

⏺️ [notepad.exe - notes.txt - Notepad - 15:20:10]
some notes written here

╔════════════════════════════════════════════════════════════════════════════╗
║                        [ SESSION ENDED: 2025-06-16 15:25:45 ]             ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## How to Run

### Prerequisites

* Python 3.x installed
* Install required modules:

```bash
pip install pyautogui pynput psutil pywin32
```

---

### Running the Logger

```bash
python shadowloggerx.py
```

* The script will start immediately.
* Logs will be stored in:

  ```
  %APPDATA%\Windows Update\<yyyy-mm-dd>.log
  ```
* Press `ESC` key to stop and take a screenshot.

---

## Ethical Use

ShadowLoggerX is **not a remote logger**, it does not upload, send, or transmit any data. If you want to add features like:

* Automatic ZIP compression
* Remote email upload
* Registry persistence

...do so responsibly and clearly indicate them.


