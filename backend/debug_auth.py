import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables:")
print(f"JWT_SECRET from os.getenv: {os.getenv('JWT_SECRET', 'NOT FOUND')}")
print(f"SECRET_KEY from os.getenv: {os.getenv('SECRET_KEY', 'NOT FOUND')}")

# Test importing the auth module and checking its SECRET_KEY
from app.core.auth import SECRET_KEY, ALGORITHM
print(f"\nFrom auth module:")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"ALGORITHM: {ALGORITHM}")

# Test token creation and verification
from app.core.auth import create_access_token, verify_token
from datetime import timedelta

# Create a test token
data = {"sub": 10}
expires = timedelta(minutes=30)
token = create_access_token(data=data, expires_delta=expires)
print(f"\nCreated test token: {token}")

# Verify the token
result = verify_token(token)
print(f"Verified token result: {result}")
if result:
    print(f"User ID from token: {result.user_id}")
else:
    print("Token verification failed")