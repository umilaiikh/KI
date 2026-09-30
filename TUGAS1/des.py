IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]
SHIFT = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]
S_BOX = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]
def permute(bits, table):
    return [bits[i - 1] for i in table]

def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)]

def left_shift(bits, count):
    return bits[count:] + bits[:count]

def hex_to_bits(hex_string):
    return [
        int(bit)
        for char in hex_string
        for bit in f"{int(char, 16):04b}"
    ]

def bits_to_hex(bits):
    result = ""
    for i in range(0, len(bits), 4):
        value = (bits[i] << 3) | (bits[i + 1] << 2) | (bits[i + 2] << 1) | bits[i + 3]
        result += f"{value:X}"
    return result

def generate_subkeys(key_hex):
    key_bits = hex_to_bits(key_hex)
    if len(key_bits) != 64:
        raise ValueError("DES key harus terdiri dari 16 karakter hexadecimal.")
    key_bits = permute(key_bits, PC1)

    left = key_bits[:28]
    right = key_bits[28:]
    subkeys = []

    for shift in SHIFT:
        left = left_shift(left, shift)
        right = left_shift(right, shift)
        
        combined = left + right
        subkey = permute(combined, PC2)

        subkeys.append(subkey)

    return subkeys

def sbox_substitution(bits):
    result = []
    for i in range(8):
        block = bits[i * 6:(i + 1) * 6]
        row = (block[0] << 1) | block[5]
        column = (
            (block[1] << 3)
            | (block[2] << 2)
            | (block[3] << 1)
            | block[4]
        )
        value = S_BOX[i][row][column]
        result.extend([
            (value >> 3) & 1,
            (value >> 2) & 1,
            (value >> 1) & 1,
            value & 1
        ])

    return result

def feistel(right, subkey):
    expanded = permute(right, E)
    xored = xor_bits(expanded, subkey)
    substituted = sbox_substitution(xored)
    return permute(substituted, P)


def des_block(block_hex, key_hex, decrypt=False):
    block_bits = hex_to_bits(block_hex)
    if len(block_bits) != 64:
        raise ValueError("DES block harus terdiri dari 16 karakter hexadecimal.")
    subkeys = generate_subkeys(key_hex)

    if decrypt:
        subkeys = subkeys[::-1]
    block_bits = permute(block_bits, IP)

    left = block_bits[:32]
    right = block_bits[32:]

    for subkey in subkeys:
        new_left = right
        new_right = xor_bits(left, feistel(right, subkey))

        left = new_left
        right = new_right
    combined = right + left
    result = permute(combined, FP)
    return bits_to_hex(result)

def encrypt_block(block_hex, key_hex):
    return des_block(block_hex, key_hex, decrypt=False)

def decrypt_block(block_hex, key_hex):
    return des_block(block_hex, key_hex, decrypt=True)

def add_padding(data):
    padding_length = 8 - (len(data) % 8)

    if padding_length == 0:
        padding_length = 8
    return data + bytes([padding_length]) * padding_length

def remove_padding(data):
    if not data:
        raise ValueError("Data kosong.")
    padding_length = data[-1]

    if padding_length < 1 or padding_length > 8:
        raise ValueError("Padding tidak valid.")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Padding tidak valid.")
    return data[:-padding_length]

def encrypt(message, key_hex):
    data = message.encode("utf-8")
    data = add_padding(data)

    ciphertext = ""

    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        block_hex = block.hex().upper()
        encrypted_block = encrypt_block(block_hex, key_hex)
        ciphertext += encrypted_block
    return ciphertext

def decrypt(ciphertext, key_hex):
    ciphertext = ciphertext.strip()
    
    if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext DES tidak valid.")
    decrypted_data = bytearray()

    for i in range(0, len(ciphertext), 16):
        block_hex = ciphertext[i:i + 16]
        decrypted_block = decrypt_block(block_hex, key_hex)
        decrypted_data.extend(bytes.fromhex(decrypted_block))
    decrypted_data = remove_padding(bytes(decrypted_data))

    return decrypted_data.decode("utf-8")


if __name__ == "__main__":
    key = "133457799BBCDFF1"
    plaintext = "0123456789ABCDEF"

    print("========================================")
    print("          DES IMPLEMENTATION TEST")
    print("========================================")
    print()

    print("Key       :", key)
    print("Plaintext :", plaintext)

    ciphertext = encrypt_block(plaintext, key)

    print("Ciphertext:", ciphertext)

    decrypted = decrypt_block(ciphertext, key)

    print("Decrypted :", decrypted)

    print()

    if ciphertext == "85E813540F0AB405" and decrypted == plaintext:
        print("DES TEST BERHASIL")
    else:
        print("DES TEST GAGAL")