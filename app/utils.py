import hashlib

# Парольді хэштеу функциясы (қауіпсіздік үшін)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Енгізілген парольді дерекқордағы хэшпен салыстыру
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password