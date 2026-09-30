import socket
import threading
from des import encrypt, decrypt

DES_KEY = "133457799BBCDFF1"
PORT = 5000

def receive_messages(sock):
    buffer = ""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[Connection closed by Device A]")
                break
            buffer += data.decode("utf-8")
            while "\n" in buffer:
                ciphertext, buffer = buffer.split("\n", 1)

                if ciphertext.strip():
                    plaintext = decrypt(ciphertext, DES_KEY)
                    print("\n----------------------------------------")
                    print("Ciphertext received:")
                    print(ciphertext)
                    print()
                    print("Decrypted message:")
                    print(plaintext)
                    print("----------------------------------------")
                    print("Enter message: ", end="", flush=True)

        except Exception as e:
            print("\n[Receive error:", e, "]")
            break
def main():
    print("========================================")
    print("          DES SECURE CHAT")
    print("             DEVICE B")
    print("========================================")
    print()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("0.0.0.0", PORT))
    server.listen(1)

    print("Waiting for Device A...")
    conn, addr = server.accept()

    print()
    print("Device A connected:", addr)
    print("Type /exit to close the connection.")
    print()

    receiver = threading.Thread(
        target=receive_messages,
        args=(conn,),
        daemon=True
    )
    receiver.start()

    try:
        while True:
            message = input("Enter message: ")
            if message == "/exit":
                break
            if not message.strip():
                continue
            ciphertext = encrypt(message, DES_KEY)

            print()
            print("Plaintext:")
            print(message)
            print()
            print("Ciphertext:")
            print(ciphertext)
            print()
            print("[Ciphertext sent]")
            print()

            conn.sendall((ciphertext + "\n").encode("utf-8"))
    except Exception as e:
        print()
        print("Error:", e)
    finally:
        conn.close()
        server.close()
        print()
        print("Connection closed.")

if __name__ == "__main__":
    main()
