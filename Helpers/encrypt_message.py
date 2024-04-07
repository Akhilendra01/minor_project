from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def load_public_key(public_key_str):
    """Loads an RSA public key from PEM string."""
    public_key = serialization.load_pem_public_key(
        public_key_str.encode(),
        backend=default_backend()
    )
    return public_key

def encrypt_message(public_key, message):
    """Encrypts a message using the provided public key with OAEP padding."""
    public_key=load_public_key(public_key)
    encrypted_data = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data
