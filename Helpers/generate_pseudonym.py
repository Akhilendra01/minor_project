import string
import random

def generate_pseudonym(length=6):
    characters = string.ascii_letters + string.digits  # includes letters (both cases) and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string