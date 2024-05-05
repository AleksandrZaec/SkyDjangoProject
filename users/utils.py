import string
import random

def generate_random_code():
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_letters, k=5)) + random.choice(string.ascii_uppercase)
    code = ''.join(random.sample(digits + letters, len(digits + letters)))
    return code



