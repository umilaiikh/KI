import json
import socket
import threading
import secrets
from aes import encrypt_text, decrypt_text

KDC_IP = "192.168.180.130"
KDC_PORT = 5000
CONTROL_PORT = 5001
BOB_IP = "192.168.180.133"
BOB_PORT = 6000

master_key = ""
key_lock = threading.Lock()
print_lock = threading.Lock()

def valid_key(key):
    return (
        len(key) == 16
        and key.isascii()
        and all(32 <= ord(c) <= 126 for c in key)
    )

def send_message(conn, data, lock=None):
    payload = (json.dumps(data) + "\n").encode("utf-8")
    if lock:
        with lock:
            conn.sendall(payload)
    else:
        conn.sendall(payload)

def read_message(file):
    line = file.readline()
    return json.loads(line) if line else None

def show_message(title, plaintext, ciphertext):
    with print_lock:
        print()
        print("=" * 45)
        print(title)
        print(f"Plaintext  : {plaintext}")
        print(f"Ciphertext : {ciphertext}")
        print("=" * 45)

def control_loop():
    global master_key
    while True:
        conn = None
        file = None
        try:
            conn = socket.create_connection(
                (KDC_IP, CONTROL_PORT),
                timeout=10
            )
            conn.settimeout(None)
            file = conn.makefile("r", encoding="utf-8")

            send_message(conn, {"role": "alice"})
            response = read_message(file)

            if not response or response.get("type") != "REGISTERED":
                continue
            with print_lock:
                print("[Alice] Terhubung ke kanal kontrol KDC.")

            while True:
                message = read_message(file)
                if message is None:
                    break
                if message.get("type") == "KEY_UPDATE":
                    try:
                        with key_lock:
                            old_key = master_key
                        encrypted = bytes.fromhex(
                            message["encrypted_key"]
                        )
                        new_key = decrypt_text(encrypted, old_key)
                        if not valid_key(new_key):
                            raise ValueError("Key tidak valid.")
                        with key_lock:
                            master_key = new_key
                        send_message(
                            conn,
                            {
                                "type": "KEY_UPDATE_ACK",
                                "status": "OK"
                            }
                        )
                        with print_lock:
                            print(
                                "\n[Alice] Master key berhasil diperbarui."
                            )
                    except (ValueError, KeyError, TypeError):
                        send_message(
                            conn,
                            {
                                "type": "KEY_UPDATE_ACK",
                                "status": "ERROR"
                            }
                        )

        except (OSError, ValueError, json.JSONDecodeError) as error:
            with print_lock:
                print(f"\n[Alice] Kanal kontrol terputus: {error}")

        finally:
            if file:
                file.close()
            if conn:
                conn.close()
        threading.Event().wait(3)

def request_session():
    with key_lock:
        key = master_key

    nonce = secrets.token_hex(8)
    conn = socket.create_connection((KDC_IP, KDC_PORT), timeout=10)
    file = conn.makefile("r", encoding="utf-8")

    try:
        send_message(
            conn,
            {
                "type": "REQUEST_SESSION",
                "ID_A": "Alice",
                "ID_B": "Bob",
                "N1": nonce
            }
        )
        response = read_message(file)
    finally:
        file.close()
        conn.close()

    if not response or response.get("type") != "SESSION_RESPONSE":
        raise ValueError("Respons KDC tidak valid.")

    data = json.loads(
        decrypt_text(bytes.fromhex(response["data"]), key)
    )

    if (
        data.get("ID_A") != "Alice"
        or data.get("ID_B") != "Bob"
        or data.get("N1") != nonce
    ):
        raise ValueError("Validasi respons KDC gagal.")
    return data["K_S"], data["TICKET_B"]

def receive_messages(file, session_key, stop_event):
    while not stop_event.is_set():
        try:
            message = read_message(file)
            if message is None:
                break
            if message.get("type") == "CHAT":
                cipher_hex = message["data"]
                plaintext = decrypt_text(
                    bytes.fromhex(cipher_hex),
                    session_key
                )
                show_message(
                    "PESAN DITERIMA DARI BOB",
                    plaintext,
                    cipher_hex
                )
            elif message.get("type") == "QUIT":
                with print_lock:
                    print("\n[Bob] Mengakhiri percakapan.")
                break
        except (OSError, ValueError, json.JSONDecodeError) as error:
            if not stop_event.is_set():
                with print_lock:
                    print(f"\n[!] Koneksi terputus: {error}")
            break
    stop_event.set()


def chat():
    session_key, ticket = request_session()
    conn = socket.create_connection((BOB_IP, BOB_PORT), timeout=10)
    conn.settimeout(None)
    file = conn.makefile("r", encoding="utf-8")
    stop_event = threading.Event()

    try:
        send_message(
            conn,
            {"type": "TICKET", "data": ticket}
        )

        challenge = read_message(file)

        if not challenge or challenge.get("type") != "CHALLENGE":
            raise ValueError("Challenge Bob tidak valid.")

        n2 = int(
            decrypt_text(
                bytes.fromhex(challenge["data"]),
                session_key
            )
        )

        send_message(
            conn,
            {
                "type": "CHALLENGE_RESPONSE",
                "data": encrypt_text(
                    str(n2 - 1),
                    session_key
                ).hex()
            }
        )

        result = read_message(file)

        if not result or result.get("type") != "AUTH_OK":
            raise ValueError("Autentikasi Alice gagal.")

        print("\n[Alice] Terhubung dengan Bob.")
        print("Ketik /quit untuk mengakhiri percakapan.")

        receiver = threading.Thread(
            target=receive_messages,
            args=(file, session_key, stop_event),
            daemon=True
        )
        receiver.start()

        while not stop_event.is_set():
            try:
                text = input("[Alice]: ")
            except (EOFError, KeyboardInterrupt):
                text = "/quit"

            if text.strip() == "/quit":
                send_message(conn, {"type": "QUIT"})
                stop_event.set()
                break

            ciphertext = encrypt_text(text, session_key)
            cipher_hex = ciphertext.hex()

            show_message(
                "PESAN TERKIRIM KE BOB",
                text,
                cipher_hex
            )
            send_message(
                conn,
                {"type": "CHAT", "data": cipher_hex}
            )
    finally:
        stop_event.set()
        conn.close()

def main():
    global master_key

    while True:
        key = input("Master key awal Alice (16 karakter): ")
        if valid_key(key):
            master_key = key
            break
        print("[!] Key harus 16 karakter ASCII yang dapat dicetak.")

    threading.Thread(
        target=control_loop,
        daemon=True
    ).start()

    while True:
        print("\nMENU ALICE")
        print("1. Mulai sesi dengan Bob")
        print("2. Keluar")

        choice = input("Pilih menu: ").strip()
        if choice == "1":
            try:
                chat()
            except (OSError, ValueError, json.JSONDecodeError) as error:
                print(f"[!] Sesi gagal: {error}")
        elif choice == "2":
            break
        else:
            print("[!] Pilihan tidak valid.")

if __name__ == "__main__":
    main()