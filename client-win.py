import socket
import pyperclip
import keyboard
import threading
import time

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

def monitor_send_hotkey():
    global last_clipboard
    print("[⌨] Press CTRL+ALT+C to send clipboard to Linux.")
    while True:
        if keyboard.is_pressed("ctrl+alt+c"):
            current_text = pyperclip.paste()
            if current_text and current_text != last_clipboard:
                last_clipboard = current_text
                send_clipboard(current_text)
                time.sleep(1)
            else:
                print("[i] Clipboard unchanged.")
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
