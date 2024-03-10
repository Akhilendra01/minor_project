from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import string
import random

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def private_key_to_text(private_key):
    private_key_text = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key_text.decode()

def public_key_to_text(public_key):
    public_key_text = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_text.decode()

def send_data(sock, data):
  """Sends data through the provided socket."""
  sock.sendall(data)

def receive_data(sock, buffer_size=2048):
  """Receives data from the provided socket with a buffer size."""
  return sock.recv(buffer_size)

def encrypt_message(public_key, message):
  """Encrypts a message using the provided public key with OAEP padding."""
  return public_key.encrypt(
      message,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )

def decrypt_message(private_key, encrypted_message):
  """Decrypts a message using the provided private key with OAEP padding."""
  return private_key.decrypt(
      encrypted_message,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )

def generate_pseudonym(length=6):
    characters = string.ascii_letters + string.digits  # includes letters (both cases) and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string