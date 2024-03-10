import socket
from cryptography.hazmat.primitives import serialization
import helpers as hlp

def run_client(host='localhost', port=12345, key_size=2048):
  """Starts the client, performs handshake, and receives message."""

  # Generate keys
  client_private_key = hlp.generate_rsa_key_pair(key_size)

  # Client socket setup
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((host, port))

  # Send client's public key
  client_public_key_bytes = hlp.get_pem_encoded_public_key(client_private_key)
  hlp.send_data(client_socket, client_public_key_bytes)

  # Receive encrypted message
  encrypted_message = hlp.receive_data(client_socket)

  # Decrypt message
  decrypted_message = hlp.decrypt_message(client_private_key, encrypted_message)

  print(decrypted_message.decode())

  # Close socket
  client_socket.close()

run_client()
