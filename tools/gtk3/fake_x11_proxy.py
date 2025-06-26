import socket
import os
import select
import threading
import shutil

# Real X11 display
REAL_X11_SOCKET = "/tmp/.X11-unix/X0"
# Fake display socket
FAKE_X11_SOCKET = "/tmp/.X11-unix/X99"

# Ensure the directory exists
os.makedirs("/tmp/.X11-unix", exist_ok=True)

# Clean up any existing socket
if os.path.exists(FAKE_X11_SOCKET):
    os.remove(FAKE_X11_SOCKET)

def proxy_data(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        pass
    finally:
        try: src.shutdown(socket.SHUT_RD)
        except: pass
        try: dst.shutdown(socket.SHUT_WR)
        except: pass

def handle_client(client_sock):
    # Connect to the real X server

    print("Handling new client connection")

    real_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    real_sock.connect(REAL_X11_SOCKET)

    # Start proxying in both directions
    threading.Thread(target=proxy_data, args=(client_sock, real_sock)).start()
    threading.Thread(target=proxy_data, args=(real_sock, client_sock)).start()

# Create fake X11 socket
server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_sock.bind(FAKE_X11_SOCKET)
server_sock.listen(5)

print(f"Fake X11 server listening on {FAKE_X11_SOCKET}")
try:
    while True:
        client, _ = server_sock.accept()
        threading.Thread(target=handle_client, args=(client,)).start()
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    server_sock.close()
    os.remove(FAKE_X11_SOCKET)
