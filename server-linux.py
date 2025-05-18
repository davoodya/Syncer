import socket
import threading
import pyperclip
import keyboard
import time

WINDOWS_CLIENT_IP = "192.168.20.100"  # آدرس IP ویندوز
WINDOWS_RECEIVE_PORT = 65433  # پورتی که ویندوز گوش می‌دهد

def handle_client(conn, addr):
    data = conn.recv(4096).decode("utf-8")
    print(f"[⇧] Received from Windows: {data}")
    with open("PCRecieved.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n\n")
    pyperclip.copy(data)
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

def monitor_send_hotkey():
    print("[⌨] Press CTRL+SHIFT+V to send clipboard to Windows.")
    while True:
        try:
            if keyboard.is_pressed("ctrl+shift+v"):
                send_clipboard_to_windows()
                time.sleep(1.5)
        except Exception as e:
            print(f"[!] Hotkey error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=start_receive_server, daemon=True).start()
    monitor_send_hotkey()
