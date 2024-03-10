from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

def load_key_from_file(filename):
    with open(filename, 'rb') as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

def encrypt_message(message, public_key):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

# Alice's side
alice_private_key, alice_public_key = generate_key_pair()
save_key_to_file(alice_private_key, 'alice_private_key.pem')
print("Alice's private key saved to alice_private_key.pem")
alice_public_key_bytes = alice_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Bob's side
bob_private_key, bob_public_key = generate_key_pair()
save_key_to_file(bob_private_key, 'bob_private_key.pem')
print("Bob's private key saved to bob_private_key.pem")
bob_public_key_bytes = bob_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Message exchange
message_from_alice = "Hello Bob, this is Alice!"
print("Message from Alice:", message_from_alice)
encrypted_message_from_alice = encrypt_message(message_from_alice, bob_public_key)
print("Encrypted message from Alice sent to Bob.")

# Bob decrypts the message
decrypted_message_from_alice = decrypt_message(encrypted_message_from_alice, bob_private_key)
print("Decrypted message from Alice:", decrypted_message_from_alice)

# Bob responds to Alice
message_from_bob = "Hello Alice, nice to meet you!"
print("Message from Bob:", message_from_bob)
encrypted_message_from_bob = encrypt_message(message_from_bob, alice_public_key)
print("Encrypted message from Bob sent to Alice.")

# Alice decrypts the message
decrypted_message_from_bob = decrypt_message(encrypted_message_from_bob, alice_private_key)
print("Decrypted message from Bob:", decrypted_message_from_bob)
