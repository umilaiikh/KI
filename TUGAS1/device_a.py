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
                print("\n[Connection closed by Device B]")
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
    print("             DEVICE A")
    print("========================================")
    print()

    device_b_ip = input("Enter Device B IP address: ").strip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((device_b_ip, PORT))
        print()
        print("Connected to Device B.")
        print("Type /exit to close the connection.")
        print()
        receiver = threading.Thread(
            target=receive_messages,
            args=(sock,),
            daemon=True
        )
        receiver.start()

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
            sock.sendall((ciphertext + "\n").encode("utf-8"))

    except ConnectionRefusedError:
        print()
        print("Connection refused.")
        print("Make sure Device B is running and the IP address is correct.")
    except TimeoutError:
        print()
        print("Connection timed out.")
    except Exception as e:
        print()
        print("Error:", e)
    finally:
        sock.close()
        print()
        print("Connection closed.")

if __name__ == "__main__":
    main()