#!/usr/bin/env python3
import socket
import os
import threading
import struct
import subprocess
import sys
import time

REAL_X11_SOCKET = "/tmp/.X11-unix/X0"
FAKE_X11_DISPLAY = ":99"
FAKE_X11_SOCKET = f"/tmp/.X11-unix/X99"

# Clean fake socket
os.makedirs(os.path.dirname(FAKE_X11_SOCKET), exist_ok=True)
if os.path.exists(FAKE_X11_SOCKET):
    os.remove(FAKE_X11_SOCKET)

def decode_and_log(data):
    if len(data) < 4:
        return
    major_opcode = data[0]
    minor_opcode = data[1]
    length_units = struct.unpack("=H", data[2:4])[0]
    print(f"[→] Request: opcode={major_opcode} minor={minor_opcode} length={length_units * 4} bytes")

def proxy_client_to_server(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            decode_and_log(data)
            dst.sendall(data)
    except:
        pass

def proxy_server_to_client(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        pass

def handle_client(client_sock):
    print("[*] New client connected")
    real_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    real_sock.connect(REAL_X11_SOCKET)

    # Bidirectional proxying
    threading.Thread(target=proxy_client_to_server, args=(client_sock, real_sock), daemon=True).start()
    threading.Thread(target=proxy_server_to_client, args=(real_sock, client_sock), daemon=True).start()

def start_proxy_server():
    server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_sock.bind(FAKE_X11_SOCKET)
    server_sock.listen(5)
    print(f"[+] Listening as fake X11 server on {FAKE_X11_DISPLAY}")

    def accept_loop():
        while True:
            client, _ = server_sock.accept()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()

    threading.Thread(target=accept_loop, daemon=True).start()
    return server_sock

def main():
    if len(sys.argv) < 2:
        print("Usage: ./x11trace <X11 app command...>")
        sys.exit(1)

    # Step 1: Start fake X11 server proxy
    server_sock = start_proxy_server()

    # Step 2: Launch app with DISPLAY=:99
    env = os.environ.copy()
    env["DISPLAY"] = FAKE_X11_DISPLAY

    print(f"[+] Launching: {' '.join(sys.argv[1:])}")
    proc = subprocess.Popen(sys.argv[1:], env=env)

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("[!] Interrupted, terminating child process")
        proc.terminate()
        proc.wait()

    print("[+] App exited. Shutting down proxy.")
    server_sock.close()
    if os.path.exists(FAKE_X11_SOCKET):
        os.remove(FAKE_X11_SOCKET)

if __name__ == "__main__":
    main()
