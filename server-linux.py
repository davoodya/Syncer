import socket
import threading
import pyperclip
import keyboard
import time
import os  # OS library used for saving files operations


WINDOWS_CLIENT_IP = "192.168.20.100"  # Enter Windows IP
WINDOWS_RECEIVE_PORT = 65433  # Windows Port Listener
# Note: define allow firewall rule in Windows => wf.msc => inbound rules for above port


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
