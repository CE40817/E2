import os
import secrets
import socket

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "18080"))
FLAG = os.environ.get("FLAG", f"CTF{{FRONTING_{secrets.token_hex(4).upper()}}}")

def handle(c):
    data = b""
    c.settimeout(2.0)
    try:
        while True:
            chunk = c.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\n\n" in data or len(data) > 8192:
                break
    except Exception:
        pass

    text = data.decode(errors="replace")
    host = ""
    for line in text.splitlines():
        if line.lower().startswith("host:"):
            host = line.split(":", 1)[1].strip()
            break

    if host == "forbidden.com":
        body = "OK\n" + FLAG + "\n"
    else:
        body = "PUBLIC\n"

    try:
        c.sendall(body.encode())
    except Exception:
        pass
    c.close()

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(32)
    while True:
        c, _ = s.accept()
        handle(c)

if __name__ == "__main__":
    main()
