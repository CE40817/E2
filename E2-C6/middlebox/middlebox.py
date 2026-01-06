import os
import socket

LISTEN_HOST = os.environ.get("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8443"))

ORIGIN_HOST = os.environ.get("ORIGIN_HOST", "127.0.0.1")
ORIGIN_PORT = int(os.environ.get("ORIGIN_PORT", "18080"))

SCAN_BYTES = int(os.environ.get("SCAN_BYTES", "64"))
SCAN_TIMEOUT = float(os.environ.get("SCAN_TIMEOUT", "0.15"))

DEBUG = os.environ.get("DEBUG", "1") not in ("0", "false", "False", "")

def log(*a):
    if DEBUG:
        print(*a, flush=True)

def relay(a: socket.socket, b: socket.socket):
    a.settimeout(0.5)
    b.settimeout(0.5)

    a_open = True
    b_open = True

    while a_open or b_open:
        for src, dst in ((a, b), (b, a)):
            try:
                data = src.recv(4096)
                if not data:
                    if src is a:
                        a_open = False
                    else:
                        b_open = False
                    try:
                        dst.shutdown(socket.SHUT_WR)
                    except Exception:
                        pass
                    continue

                dst.sendall(data)

            except socket.timeout:
                continue
            except Exception as e:
                log("relay error:", repr(e))
                return

def handle_client(c: socket.socket, addr):
    c.settimeout(SCAN_TIMEOUT)

    first = b""
    try:
        while len(first) < SCAN_BYTES:
            chunk = c.recv(SCAN_BYTES - len(first))
            if not chunk:
                break
            first += chunk
    except Exception:
        pass

    log("accepted", addr, "first_len", len(first), "preview", first[:80])

    if b"forbidden.com" in first:
        try:
            c.sendall(b"BLOCKED\n")
        except Exception:
            pass
        try:
            c.close()
        except Exception:
            pass
        log("blocked", addr)
        return

    try:
        o = socket.create_connection((ORIGIN_HOST, ORIGIN_PORT), timeout=2.0)
    except Exception as e:
        log("origin connect failed:", (ORIGIN_HOST, ORIGIN_PORT), repr(e))
        try:
            c.sendall(b"MB_ERR\n")
        except Exception:
            pass
        try:
            c.close()
        except Exception:
            pass
        return

    try:
        if first:
            o.sendall(first)
        relay(c, o)
    finally:
        try:
            c.close()
        except Exception:
            pass
        try:
            o.close()
        except Exception:
            pass

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((LISTEN_HOST, LISTEN_PORT))
    s.listen(64)

    log("middlebox listening on", (LISTEN_HOST, LISTEN_PORT), "origin", (ORIGIN_HOST, ORIGIN_PORT))

    while True:
        c, addr = s.accept()
        handle_client(c, addr)

if __name__ == "__main__":
    main()
