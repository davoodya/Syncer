import socket
import threading
import pyperclip
import keyboard
import time
import os
import shutil
import tkinter as tk
from tkinter import filedialog

WINDOWS_CLIENT_IP = "192.168.1.103"
WINDOWS_RECEIVE_PORT = 65433

def handle_client(conn, addr):
    first_bytes = conn.recv(5)

    if first_bytes == b"FILE\n":
        # Step 1: دریافت نام فایل
        filename = b""
        while not filename.endswith(b"\n"):
            filename += conn.recv(1)
        filename = filename.decode().strip()

        # Step 2: ساخت دایرکتوری مقصد
        os.makedirs("PC_Received", exist_ok=True)
        save_path = os.path.join("PC_Received", filename)

        # Step 3: ذخیره فایل در دیسک
        with open(save_path, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
        print(f"[💾] File received from Windows and saved to {save_path}")

    else:
        # اگر متن ساده بود
        data = first_bytes + conn.recv(4096)
        try:
            decoded = data.decode("utf-8")
        except:
            decoded = "[!] Could not decode clipboard content."
        print(f"[⇧] Received from Windows: {decoded}")
        with open("PCRecieved.txt", "a", encoding="utf-8") as f:
            f.write(decoded + "\n\n")
        pyperclip.copy(decoded)
        print("[✓] Data written to PCRecieved.txt and copied to clipboard.")

    conn.close()

def start_receive_server(port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[📡] Listening for Windows clipboard on port {port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def send_clipboard_to_windows():
    data = pyperclip.paste()
    if not data.strip():
        print("[!] Clipboard is empty. Nothing to send.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WINDOWS_CLIENT_IP, WINDOWS_RECEIVE_PORT))
            s.sendall(data.encode("utf-8"))
        print("[✓] Sent clipboard to Windows.")
    except Exception as e:
        print(f"[!] Could not send to Windows: {e}")

def send_file_to_windows(file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WINDOWS_CLIENT_IP, WINDOWS_RECEIVE_PORT))

            # ارسال هدر برای شناسایی نوع داده (فایل)
            s.sendall(b"FILE\n")

            # ارسال نام فایل
            file_name = os.path.basename(file_path)
            s.sendall(f"{file_name}\n".encode())

            # ارسال محتوای فایل
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    s.sendall(data)

        print(f"[✓] File {file_name} sent to Windows.")
    except Exception as e:
        print(f"[!] Could not send file to Windows: {e}")

def send_directory_to_windows(directory_path):
    try:
        # ایجاد آرشیو از دایرکتوری
        base_name = os.path.basename(directory_path)
        archive_path = f"/tmp/{base_name}_archive.zip"
        shutil.make_archive(archive_path.replace('.zip', ''), 'zip', directory_path)

        # ارسال آرشیو
        send_file_to_windows(archive_path)

        # حذف آرشیو موقت
        os.remove(archive_path)
        print(f"[✓] Directory {base_name} sent as archive to Windows.")
    except Exception as e:
        print(f"[!] Could not send directory to Windows: {e}")
        if os.path.exists(archive_path):
            os.remove(archive_path)

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select files to send to Windows")
    return file_paths

def select_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(title="Select directory to send to Windows")
    return dir_path

def monitor_send_hotkeys():
    print("[⌨] Hotkeys:")
    print("  - CTRL+SHIFT+V: Send clipboard to Windows")
    print("  - CTRL+ALT+Y: Select and send files to Windows")
    print("  - CTRL+ALT+U: Select and send directory to Windows")

    while True:
        try:
            if keyboard.is_pressed("ctrl+shift+v"):
                send_clipboard_to_windows()
                time.sleep(1.5)
            elif keyboard.is_pressed("ctrl+alt+y"):
                file_paths = select_files()
                if file_paths:
                    for file_path in file_paths:
                        if os.path.isfile(file_path):
                            send_file_to_windows(file_path)
                            time.sleep(0.5)  # تأخیر کوتاه بین ارسال فایل‌ها
                time.sleep(1.5)
            elif keyboard.is_pressed("ctrl+alt+u"):
                dir_path = select_directory()
                if dir_path and os.path.isdir(dir_path):
                    send_directory_to_windows(dir_path)
                time.sleep(1.5)
        except Exception as e:
            print(f"[!] Hotkey error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=start_receive_server, daemon=True).start()
    monitor_send_hotkeys()
