import hashlib

SECRET_SALT = "agaxtur2025"  

def generate_user_token(phone_number: str) -> str:
    # Remove espaços, sinais, etc.
    normalized = ''.join(filter(str.isdigit, phone_number))
    # Gera hash SHA-256 (string hex de 64 caracteres)
    token = hashlib.sha256(f"{normalized}{SECRET_SALT}".encode()).hexdigest()
    return token
