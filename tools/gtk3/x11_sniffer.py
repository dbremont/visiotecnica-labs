import socket
from scapy.all import *
from scapy.layers.inet import TCP

# X11 Unix socket path, usually /tmp/.X11-unix/X0
X11_SOCKET_PATH = "/tmp/.X11-unix/X0"

def parse_x11_data(data):
    # Minimal example: parse first byte = opcode
    if len(data) < 1:
        return None
    opcode = data[0]
    # Common X11 opcodes (partial)
    opcodes = {
        1: "CreateWindow",
        8: "MapWindow",
        9: "MapSubwindows",
        16: "ConfigureWindow",
        18: "DestroyWindow",
        20: "ChangeProperty",
        33: "SendEvent",
    }
    return opcodes.get(opcode, f"Unknown opcode {opcode}")

def main():
    # Create a Unix socket and bind to the X11 socket path
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(X11_SOCKET_PATH)

    print(f"Connected to X11 socket at {X11_SOCKET_PATH}")

    while True:
        data = sock.recv(1024)
        if not data:
            break
        event = parse_x11_data(data)
        if event:
            print(f"X11 Event: {event}, Raw bytes: {data.hex()}")
        else:
            print(f"Unknown or empty X11 data: {data.hex()}")

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("Permission denied: run as root or with appropriate privileges.")
    except Exception as e:
        print(f"Error: {e}")
