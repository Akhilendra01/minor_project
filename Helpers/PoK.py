import hashlib

class ProofOfKnowledge:
    def __init__(self):
        pass

    def generate_proof(self, secret_key, public_key):
        proof_data = f"{secret_key}{public_key}"
        return hashlib.sha256(proof_data.encode()).hexdigest()

    def verify_proof(self, proof, secret_key, public_key):
        expected_proof = self.generate_proof(secret_key, public_key)
        return proof == expected_proof
