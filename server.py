import socket
from cryptography.hazmat.primitives import serialization
import helpers as hlp

def run_server(host='localhost', port=12345, key_size=2048):
  """Starts the server, performs handshake, and sends message."""

  # Generate keys
  server_private_key = hlp.generate_rsa_key_pair(key_size)

  # Server socket setup
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)

  # Accept client connection
  client_socket, address = server_socket.accept()

  # Receive client's public key
  client_public_key_bytes = hlp.receive_data(client_socket)
  client_public_key = serialization.load_pem_public_key(client_public_key_bytes)

  # Encrypt a message
  encrypted_message = hlp.encrypt_message(client_public_key, b'Handshake successfull')

  # Send encrypted message
  hlp.send_data(client_socket, encrypted_message)

  # Close sockets
  client_socket.close()
  server_socket.close()

run_server()