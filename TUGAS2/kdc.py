import json
import socket
import threading
import secrets
import string
from queue import Queue, Empty
from aes import encrypt_text, decrypt_text

HOST = "0.0.0.0"
KDC_PORT = 5000
CONTROL_PORT = 5001
master_keys = {}
clients = {}
key_lock = threading.Lock()
client_lock = threading.Lock()

def valid_key(key):
    return len(key) == 16 and key.isascii() and all(32 <= ord(c) <= 126 for c in key)

def send_message(conn, data, lock=None):
    message = (json.dumps(data) + "\n").encode("utf-8")
    if lock:
        with lock:
            conn.sendall(message)
    else:
        conn.sendall(message)

def read_message(file):
    line = file.readline()
    return json.loads(line) if line else None

def handle_control(conn, addr):
    file = conn.makefile("r", encoding="utf-8")
    role = None
    try:
        registration = read_message(file)
        if not registration:
            return
        role = registration.get("role", "").lower()
        if role not in ("alice", "bob"):
            return
        client_info = {"conn": conn, "pending": None, "send_lock": threading.Lock()}
        with client_lock:
            old = clients.get(role)
            clients[role] = client_info
        if old:
            try:
                old["conn"].close()
            except OSError:
                pass
        send_message(conn, {"type": "REGISTERED"}, client_info["send_lock"])
        while True:
            message = read_message(file)
            if message is None:
                break
            if message.get("type") == "KEY_UPDATE_ACK":
                with client_lock:
                    current = clients.get(role)
                    pending = current.get("pending") if current and current["conn"] is conn else None
                if pending:
                    pending.put(message.get("status") == "OK")
    except (OSError, ValueError, json.JSONDecodeError):
        pass
    finally:
        if role:
            with client_lock:
                current = clients.get(role)
                if current and current["conn"] is conn:
                    del clients[role]
        try:
            file.close()
        except OSError:
            pass
        conn.close()

def control_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, CONTROL_PORT))
    server.listen()
    print(f"[KDC] Control aktif pada port {CONTROL_PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_control, args=(conn, addr), daemon=True).start()

def change_master_key(role):
    key_name = f"{role}_master_key"
    with key_lock:
        old_key = master_keys[key_name]
    with client_lock:
        client = clients.get(role)
        if client is None:
            print(f"[!] {role.title()} belum terhubung.")
            return
        if client["pending"] is not None:
            print("[!] Pembaruan key sedang berlangsung.")
            return
        pending = Queue(maxsize=1)
        client["pending"] = pending
    new_key = input(f"Master key baru {role.title()} (16 karakter): ")
    if not valid_key(new_key):
        print("[!] Key harus 16 karakter ASCII yang dapat dicetak.")
        with client_lock:
            client["pending"] = None
        return
    try:
        encrypted_key = encrypt_text(new_key, old_key)
        send_message(client["conn"], {"type": "KEY_UPDATE", "encrypted_key": encrypted_key.hex()}, client["send_lock"])
        confirmed = pending.get(timeout=10)
        if confirmed:
            with key_lock:
                master_keys[key_name] = new_key
            print(f"[OK] Master key {role.title()} berhasil diperbarui.")
        else:
            print("[!] Klien menolak pembaruan key.")
    except (OSError, ValueError, Empty) as error:
        print(f"[!] Pembaruan gagal: {error}")
    finally:
        with client_lock:
            if clients.get(role) is client:
                client["pending"] = None

def generate_session_key():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(16))

def handle_request(conn):
    file = conn.makefile("r", encoding="utf-8")
    try:
        request = read_message(file)
        if not request or request.get("type") != "REQUEST_SESSION":
            send_message(conn, {"type": "ERROR"})
            return
        if request.get("ID_A") != "Alice" or request.get("ID_B") != "Bob":
            send_message(conn, {"type": "ERROR"})
            return
        nonce = request.get("N1")
        if not isinstance(nonce, str):
            send_message(conn, {"type": "ERROR"})
            return
        with key_lock:
            alice_key = master_keys["alice_master_key"]
            bob_key = master_keys["bob_master_key"]
        session_key = generate_session_key()
        ticket = {"ID_A": "Alice", "ID_B": "Bob", "K_S": session_key}
        ticket_b = encrypt_text(json.dumps(ticket), bob_key)
        response = {"ID_A": "Alice", "ID_B": "Bob", "N1": nonce, "K_S": session_key, "TICKET_B": ticket_b.hex()}
        encrypted_response = encrypt_text(json.dumps(response), alice_key)
        send_message(conn, {"type": "SESSION_RESPONSE", "data": encrypted_response.hex()})
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"[KDC] Permintaan gagal: {error}")
    finally:
        file.close()
        conn.close()

def kdc_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, KDC_PORT))
    server.listen()
    print(f"[KDC] Server aktif pada port {KDC_PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_request, args=(conn,), daemon=True).start()

def main():
    print("Inisialisasi Master Key")
    for role in ("alice", "bob"):
        while True:
            key = input(f"Master key {role.title()} (16 karakter ASCII): ")
            if valid_key(key):
                master_keys[f"{role}_master_key"] = key
                break
            print("[!] Masukkan tepat 16 karakter ASCII yang dapat dicetak.")
    threading.Thread(target=control_server, daemon=True).start()
    threading.Thread(target=kdc_server, daemon=True).start()
    while True:
        print("\nMENU KDC")
        print("1. Ganti master key Alice")
        print("2. Ganti master key Bob")
        print("3. Status koneksi")
        print("4. Keluar")
        choice = input("Pilih: ").strip()
        if choice == "1":
            change_master_key("alice")
        elif choice == "2":
            change_master_key("bob")
        elif choice == "3":
            with client_lock:
                print("Alice:", "Terhubung" if "alice" in clients else "Belum terhubung")
                print("Bob:", "Terhubung" if "bob" in clients else "Belum terhubung")
        elif choice == "4":
            break
        else:
            print("[!] Pilihan tidak valid.")

if __name__ == "__main__":
    main()