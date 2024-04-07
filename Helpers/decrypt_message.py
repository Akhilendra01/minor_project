from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def load_private_key_from_pem(private_key_pem):
    """Loads an RSA private key from PEM string."""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),  # Convert string to bytes
        password=None,
        backend=default_backend()
    )
    return private_key

def decrypt_message(private_key, encrypted_message):
    """Decrypts a message using the provided private key with OAEP padding."""
    private_key=load_private_key_from_pem(private_key)
    decrypted_data = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode()
