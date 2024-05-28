import secrets

def generate_jwt_secret_key(length=32):
    # Generate a secure random string of bytes
    secret_key = secrets.token_urlsafe(length)
    return secret_key

# Generate a JWT secret key
jwt_secret_key = generate_jwt_secret_key()
print("Your secure JWT secret key is:", jwt_secret_key)
