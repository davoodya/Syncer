import sys
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
import tkinter as tk
from tkinter import filedialog # used for asking files for sending to linux server

SERVER_IP = "192.168.1.102"  # Linux IP

SERVER_PORT = 65432 # Linux Port should be the same as server side in start_receive_server()
# Note: Ports should be same in both server and client sides

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

""" send file in clipboard(Step 1: get file path from clipboard) """
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

""" send file in clipboard(Step 2: send clipboard file to linux server) """
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

""" this function used for open File Selction Windows and sending selected files to linux server """
def send_files_to_linux():
    root = tk.Tk()
    root.withdraw()  # مخفی‌سازی پنجره اصلی
    file_paths = filedialog.askopenfilenames(title="Select files to send to Linux")

    for file_path in file_paths:
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()

            file_name = os.path.basename(file_path)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            sock.sendall(b"FILE\n")
            sock.sendall(f"{file_name}\n".encode())
            sock.sendall(file_data)
            sock.close()
            print(f"[✓] Sent {file_name} to Linux.")
        except Exception as e:
            print(f"[!] Failed to send {file_path}: {e}")


def monitor_send_hotkey():
    global last_clipboard
    print("[⌨] Hotkeys:")
    print("  - CTRL+ALT+C: Send clipboard to Linux")
    print("  - CTRL+ALT+SHIFT+F: Select and send files to Linux")
    print("  - CTRL+ALT+SHIFT+U(Under Develop): Select and send directory to Linux")

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

        # Send a Clipboard file to Linux
        elif keyboard.is_pressed('ctrl+shift+alt+c'):
            print("Detected CTRL+SHIFT+ALT+C — Sending clipboard file to Linux...")
            file_path = get_clipboard_file_path()
            if file_path:
                send_file_to_linux(file_path)
            else:
                print("No file found in clipboard.")
            time.sleep(1)

        # Sending some files to linux server
        elif keyboard.is_pressed("ctrl+alt+shift+f"):
            print("🔍 File selection triggered...")
            send_files_to_linux()
            time.sleep(1)


def receive_from_linux():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", CLIENT_RECEIVE_PORT))
    server.listen(1)
    print(f"[📥] Waiting for clipboard or files from Linux on port {CLIENT_RECEIVE_PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[🔗] Connection established from {addr}")


        first_bytes = conn.recv(5)
        # If Data is File
        if first_bytes == b"FILE\n":
            filename = b""
            while not filename.endswith(b"\n"):
                filename += conn.recv(1)
            filename = filename.decode().strip()

            os.makedirs("Linux_Received", exist_ok=True)
            save_path = os.path.join("Linux_Received", filename)

            with open(save_path, "wb") as f:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)

            print(f"[💾] File received from Linux and saved to {save_path}")
        else:
            # If Data is Text
            data = first_bytes + conn.recv(4096)
            decoded = data.decode("utf-8")
            with open("LinuxReceived.txt", "a", encoding="utf-8") as f:
                f.write(decoded + "\n\n")
            pyperclip.copy(decoded)
            print("[✓] Text saved and copied to clipboard.")

        conn.close()


if __name__ == "__main__":
    threading.Thread(target=monitor_send_hotkey, daemon=True).start()
    receive_from_linux()





