import socket
import pyperclip
import keyboard
import time

SERVER_IP = "192.168.20.103"  # Replace with your Linux IP
SERVER_PORT = 65432

last_clipboard = ""

def send_clipboard(text):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(text.encode("utf-8"))
        print("[✓] Clipboard content sent.")
    except Exception as e:
        print(f"[!] Failed to send: {e}")

def monitor_hotkey():
    global last_clipboard
    print("[⌨] Press CTRL+ALT+C to send clipboard to Linux laptop.")
    while True:
        if keyboard.is_pressed("ctrl+alt+c"):
            current_text = pyperclip.paste()
            if current_text and current_text != last_clipboard:
                last_clipboard = current_text
                send_clipboard(current_text)
                time.sleep(1)  # prevent repeat sending
            else:
                print("[i] Clipboard has not changed.")
                time.sleep(1)

if __name__ == "__main__":
    monitor_hotkey()
