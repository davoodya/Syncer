import socket
import pyperclip
import keyboard
import threading
import time
import ctypes
from ctypes import wintypes
import win32clipboard
import win32con
import win32com.client
import os

SERVER_IP = "192.168.20.103"  # Linux IP
SERVER_PORT = 65432
CLIENT_RECEIVE_PORT = 65433  # for incoming data from Linux

last_clipboard = ""

def send_clipboard(text):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(text.encode("utf-8"))
        print("[✓] Sent clipboard to Linux.")
    except Exception as e:
        print(f"[!] Send failed: {e}")


def get_clipboard_file_path():
    try:
        shell = win32com.client.Dispatch("Shell.Application")
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32con.CF_HDROP)
        win32clipboard.CloseClipboard()
        if data:
            return list(data)[0]  # only first file
    except Exception:
        return None

def send_file_to_linux(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    file_name = os.path.basename(file_path)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.sendall(b"FILE\n")  # tell server it’s a file
        sock.sendall(f"{file_name}\n".encode())
        sock.sendall(file_data)
    finally:
        sock.close()


def monitor_send_hotkey():
    global last_clipboard
    print("[⌨] Press CTRL+ALT+C to send clipboard to Linux.")
    while True:
        # Send clipboard contents
        if keyboard.is_pressed("ctrl+alt+c"):
            current_text = pyperclip.paste()
            if current_text and current_text != last_clipboard:
                last_clipboard = current_text
                send_clipboard(current_text)
                time.sleep(1)
            else:
                print("[i] Clipboard unchanged.")
                time.sleep(1)

        # Send Clipboard file to Linux
        elif keyboard.is_pressed('ctrl+shift+alt+c'):
            print("Detected CTRL+SHIFT+ALT+C — Sending clipboard file to Linux...")
            file_path = get_clipboard_file_path()
            if file_path:
                send_file_to_linux(file_path)
            else:
                print("No file found in clipboard.")
            time.sleep(1)


def receive_from_linux():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", CLIENT_RECEIVE_PORT))
    server.listen(1)
    print(f"[📥] Waiting for clipboard from Linux on port {CLIENT_RECEIVE_PORT}")

    while True:
        conn, addr = server.accept()
        data = conn.recv(4096).decode("utf-8")
        print(f"[⇩] Received clipboard from Linux: {data}")

        with open("LinuxReceived.txt", "a", encoding="utf-8") as f:
            f.write(data + "\n\n")

        pyperclip.copy(data)
        print("[✓] Saved to LinuxReceived.txt and copied to clipboard.")
        conn.close()

if __name__ == "__main__":
    threading.Thread(target=monitor_send_hotkey, daemon=True).start()
    receive_from_linux()
