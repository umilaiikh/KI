S_BOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

INV_S_BOX = [0] * 256
for _i, _v in enumerate(S_BOX):
    INV_S_BOX[_v] = _i

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def _xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF

def _mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a = _xtime(a)
        b >>= 1
    return result

def _expand_key(key):
    if len(key) != 16:
        raise ValueError("Kunci AES-128 harus tepat 16 byte.")

    words = [list(key[i:i + 4]) for i in range(0, 16, 4)]

    for i in range(4, 44):
        temp = words[i - 1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [S_BOX[x] for x in temp]
            temp[0] ^= RCON[i // 4]

        words.append([
            words[i - 4][j] ^ temp[j]
            for j in range(4)
        ])

    return [sum(words[4 * r:4 * r + 4], []) for r in range(11)]

def _add_round_key(state, round_key):
    for c in range(4):
        for r in range(4):
            state[r][c] ^= round_key[4 * c + r]

def _sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = S_BOX[state[r][c]]

def _inv_sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = INV_S_BOX[state[r][c]]

def _shift_rows(state):
    for r in range(1, 4):
        state[r] = state[r][r:] + state[r][:r]

def _inv_shift_rows(state):
    for r in range(1, 4):
        state[r] = state[r][-r:] + state[r][:-r]

def _mix_columns(state):
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = _mul(a[0], 2) ^ _mul(a[1], 3) ^ a[2] ^ a[3]
        state[1][c] = a[0] ^ _mul(a[1], 2) ^ _mul(a[2], 3) ^ a[3]
        state[2][c] = a[0] ^ a[1] ^ _mul(a[2], 2) ^ _mul(a[3], 3)
        state[3][c] = _mul(a[0], 3) ^ a[1] ^ a[2] ^ _mul(a[3], 2)

def _inv_mix_columns(state):
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = _mul(a[0], 14) ^ _mul(a[1], 11) ^ _mul(a[2], 13) ^ _mul(a[3], 9)
        state[1][c] = _mul(a[0], 9) ^ _mul(a[1], 14) ^ _mul(a[2], 11) ^ _mul(a[3], 13)
        state[2][c] = _mul(a[0], 13) ^ _mul(a[1], 9) ^ _mul(a[2], 14) ^ _mul(a[3], 11)
        state[3][c] = _mul(a[0], 11) ^ _mul(a[1], 13) ^ _mul(a[2], 9) ^ _mul(a[3], 14)

def encrypt_block(block, key):
    if len(block) != 16:
        raise ValueError("Blok harus tepat 16 byte.")

    round_keys = _expand_key(key)
    state = [[block[4 * c + r] for c in range(4)] for r in range(4)]

    _add_round_key(state, round_keys[0])

    for rnd in range(1, 10):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, round_keys[rnd])

    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, round_keys[10])

    return bytes(state[r][c] for c in range(4) for r in range(4))

def decrypt_block(block, key):
    if len(block) != 16:
        raise ValueError("Blok harus tepat 16 byte.")

    round_keys = _expand_key(key)
    state = [[block[4 * c + r] for c in range(4)] for r in range(4)]

    _add_round_key(state, round_keys[10])

    for rnd in range(9, 0, -1):
        _inv_shift_rows(state)
        _inv_sub_bytes(state)
        _add_round_key(state, round_keys[rnd])
        _inv_mix_columns(state)

    _inv_shift_rows(state)
    _inv_sub_bytes(state)
    _add_round_key(state, round_keys[0])

    return bytes(state[r][c] for c in range(4) for r in range(4))

def encrypt_text(plaintext, key_text):
    try:
        key = key_text.encode("ascii")
        data = plaintext.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("Kunci dan pesan harus menggunakan karakter ASCII.")

    if len(key) != 16:
        raise ValueError("Kunci AES-128 harus tepat 16 karakter ASCII.")

    pad_len = 16 - (len(data) % 16)
    data += bytes([pad_len]) * pad_len

    return b"".join(
        encrypt_block(data[i:i + 16], key)
        for i in range(0, len(data), 16)
    )

def decrypt_text(ciphertext, key_text):
    try:
        key = key_text.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("Kunci harus menggunakan karakter ASCII.")

    if len(key) != 16:
        raise ValueError("Kunci AES-128 harus tepat 16 karakter ASCII.")

    if not ciphertext or len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext harus terdiri dari blok 16 byte.")

    data = b"".join(
        decrypt_block(ciphertext[i:i + 16], key)
        for i in range(0, len(ciphertext), 16)
    )

    pad_len = data[-1]
    if (
        pad_len < 1
        or pad_len > 16
        or data[-pad_len:] != bytes([pad_len]) * pad_len
    ):
        raise ValueError("Padding salah: kunci atau ciphertext mungkin tidak cocok.")

    try:
        return data[:-pad_len].decode("ascii")
    except UnicodeDecodeError:
        raise ValueError("Hasil dekripsi bukan teks ASCII yang valid.")

def _self_test():
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    plain = bytes.fromhex("00112233445566778899aabbccddeeff")
    expected = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

    actual = encrypt_block(plain, key)
    assert actual == expected, f"Test enkripsi gagal: {actual.hex()}"
    assert decrypt_block(actual, key) == plain, "Test dekripsi gagal"

    print("Self-test AES-128: LULUS")

if __name__ == "__main__":
    _self_test()
    print("\n=== DEMO AES-128 MANUAL ===")
    key_text = input("Masukkan kunci AES (16 karakter ASCII): ")
    plaintext = input("Masukkan pesan ASCII: ")

    try:
        ciphertext = encrypt_text(plaintext, key_text)
        print("\nKunci:", key_text)
        print("Plaintext:", plaintext)
        print("Ciphertext hex:", ciphertext.hex())
        print("Hasil dekripsi:", decrypt_text(ciphertext, key_text))

    except ValueError as error:
        print("Kesalahan:", error)