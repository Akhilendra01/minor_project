from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def load_public_key_from_pem(public_key_pem):
    """Loads an RSA public key from PEM string."""
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),  # Convert string to bytes
        backend=default_backend()
    )
    return public_key

def decrypt_with_public_key(public_key, encrypted_message):
    """Decrypts a message using the provided public key with OAEP padding."""
    decrypted_data = public_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode()
