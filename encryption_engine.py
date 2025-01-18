
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
import base64

def generate_ecc_keys():
    """Generate ECC public-private key pair."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_data(public_key, data):
    """Encrypt intellectual property using ECC."""
    shared_key = public_key.public_numbers().encode_point()
    derived_key = HKDF(
        algorithm=SHA256(),
        length=32,
        salt=None,
        info=b"Nathan Andrew Smith IP Encryption"
    ).derive(shared_key)

    encrypted_data = "".join(
        chr((ord(char) + derived_key[i % len(derived_key)]) % 256)
        for i, char in enumerate(data)
    )
    return base64.b64encode(encrypted_data.encode()).decode()

def save_encrypted_file(encrypted_data, author, filename="encrypted_ip.txt"):
    """Save encrypted intellectual property with metadata."""
    metadata = f"Author: {author}\nEncryption Date: 2025-01-18\n"
    with open(filename, "w") as file:
        file.write(metadata)
        file.write(f"Encrypted Data:\n{encrypted_data}")

# Example Usage
if __name__ == "__main__":
    private_key, public_key = generate_ecc_keys()
    intellectual_property = "This is the code by Nathan Andrew Smith."
    encrypted_data = encrypt_data(public_key, intellectual_property)
    save_encrypted_file(encrypted_data, "Nathan Andrew Smith")
