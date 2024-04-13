from platform import system

platform = system().lower()

if platform == "windows":
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
    from Cryptodome.Random import get_random_bytes
elif platform == "linux":
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
else:
    raise Exception(f"Unknown platform {platform}")

from hashlib import sha3_256


def encrypt(plaintext: str, key: str) -> bytes:
    key = sha3_256(key.encode()).digest()

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    encrypted_data = iv + ciphertext

    return encrypted_data


def decrypt(ciphertext: bytes, key: str) -> str:
    key = sha3_256(key.encode()).digest()

    iv = ciphertext[: AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext[AES.block_size :]), AES.block_size)

    return decrypted_data.decode()
