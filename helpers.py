from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def generate_rsa_key_pair(key_size=2048):
  """Generates an RSA key pair with the specified key size."""
  return rsa.generate_private_key(
      public_exponent=65537,
      key_size=key_size
  )

def get_pem_encoded_public_key(private_key):
  """Returns the PEM-encoded public key from a private key."""
  return private_key.public_key().public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )

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
