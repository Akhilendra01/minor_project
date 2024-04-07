import Helpers

def generate_data():
    name=Helpers.generate_pseudonym()
    private_key, public_key=Helpers.generate_rsa_key_pair()
    private_key=Helpers.private_key_to_text(private_key)
    public_key=Helpers.public_key_to_text(public_key)
    return {
        "name": name,
        "private_key": private_key,
        "public_key": public_key
    }