from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def load_private_key_from_pem(private_key_pem):
    """Loads an RSA private key from PEM string."""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),  # Convert string to bytes
        password=None,  # No password for this example
        backend=default_backend()
    )
    return private_key

def encrypt_with_private_key(private_key, message):
    """Encrypts a message using the provided private key with OAEP padding."""
    encrypted_data = private_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data
