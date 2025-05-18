import socket
import threading
import pyperclip

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    data = conn.recv(4096).decode("utf-8")
    print(f"[>] Received: {data}")

    with open("PCRecieved.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n\n")  # append with spacing

    pyperclip.copy(data)
    print("[✓] Data appended to PCRecieved.txt and copied to clipboard.")
    conn.close()


def start_server(host="0.0.0.0", port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[📡] Listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
