import json
import socket
import threading
from aes import encrypt_text, decrypt_text

KDC_IP = "192.168.180.130"
CONTROL_PORT = 5001
BOB_HOST = "0.0.0.0"
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

            send_message(conn, {"role": "bob"})
            response = read_message(file)

            if not response or response.get("type") != "REGISTERED":
                continue

            with print_lock:
                print("[Bob] Terhubung ke kanal kontrol KDC.")

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
                                "\n[Bob] Master key berhasil diperbarui."
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
                print(f"\n[Bob] Kanal kontrol terputus: {error}")
        finally:
            if file:
                file.close()
            if conn:
                conn.close()
        threading.Event().wait(3)

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
                    "PESAN DITERIMA DARI ALICE",
                    plaintext,
                    cipher_hex
                )
            elif message.get("type") == "QUIT":
                with print_lock:
                    print("\n[Alice] Mengakhiri percakapan.")
                break
        except (OSError, ValueError, json.JSONDecodeError) as error:
            if not stop_event.is_set():
                with print_lock:
                    print(f"\n[!] Koneksi terputus: {error}")
            break

    stop_event.set()

def handle_alice(conn, addr):
    file = conn.makefile("r", encoding="utf-8")
    stop_event = threading.Event()

    try:
        message = read_message(file)
        if not message or message.get("type") != "TICKET":
            return
        with key_lock:
            key = master_key

        ticket = json.loads(
            decrypt_text(bytes.fromhex(message["data"]), key)
        )

        if (
            ticket.get("ID_A") != "Alice"
            or ticket.get("ID_B") != "Bob"
        ):
            send_message(conn, {"type": "AUTH_ERROR"})
            return

        session_key = ticket["K_S"]
        n2 = 123456789

        send_message(
            conn,
            {
                "type": "CHALLENGE",
                "data": encrypt_text(str(n2), session_key).hex()
            }
        )
        response = read_message(file)

        if not response or response.get("type") != "CHALLENGE_RESPONSE":
            return
        answer = decrypt_text(
            bytes.fromhex(response["data"]),
            session_key
        )
        if answer != str(n2 - 1):
            send_message(conn, {"type": "AUTH_ERROR"})
            return

        send_message(conn, {"type": "AUTH_OK"})
        with print_lock:
            print(f"\n[Bob] Alice terhubung dari {addr[0]}.")
            print("Ketik /quit untuk mengakhiri percakapan.")

        receiver = threading.Thread(
            target=receive_messages,
            args=(file, session_key, stop_event),
            daemon=True
        )
        receiver.start()

        while not stop_event.is_set():
            try:
                text = input("[Bob]: ")
            except (EOFError, KeyboardInterrupt):
                text = "/quit"

            if text.strip() == "/quit":
                send_message(conn, {"type": "QUIT"})
                stop_event.set()
                break

            ciphertext = encrypt_text(text, session_key)
            cipher_hex = ciphertext.hex()

            show_message(
                "PESAN TERKIRIM KE ALICE",
                text,
                cipher_hex
            )
            send_message(
                conn,
                {"type": "CHAT", "data": cipher_hex}
            )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        with print_lock:
            print(f"\n[Bob] Sesi gagal: {error}")
    finally:
        stop_event.set()
        file.close()
        conn.close()

def main():
    global master_key
    while True:
        key = input("Master key awal Bob (16 karakter): ")
        if valid_key(key):
            master_key = key
            break
        print("[!] Key harus 16 karakter ASCII yang dapat dicetak.")
    threading.Thread(
        target=control_loop,
        daemon=True
    ).start()

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((BOB_HOST, BOB_PORT))
    server.listen()

    print(f"[Bob] Menunggu koneksi pada port {BOB_PORT}...")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=handle_alice,
                args=(conn, addr),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\n[Bob] Server dihentikan.")
    finally:
        server.close()

if __name__ == "__main__":
    main()