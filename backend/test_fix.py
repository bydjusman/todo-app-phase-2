import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables:")
print(f"JWT_SECRET from os.getenv: {os.getenv('JWT_SECRET', 'NOT FOUND')}")

# Import auth functions
from app.core.auth import SECRET_KEY, ALGORITHM, create_access_token, verify_token
from datetime import timedelta

print(f"\nFrom auth module:")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"ALGORITHM: {ALGORITHM}")

# Test the actual create_access_token function with a string sub
data = {"sub": "10"}  # Using string as per our fix
expires = timedelta(minutes=30)
token = create_access_token(data=data, expires_delta=expires)
print(f"\nCreated test token using create_access_token function: {token}")

# Verify the token
result = verify_token(token)
print(f"Verified token result: {result}")
if result:
    print(f"User ID from token: {result.user_id}")
    print(f"Type of user_id: {type(result.user_id)}")
else:
    print("Token verification failed")

# Also test with integer to see what happens
print("\n--- Testing with integer sub (should fail) ---")
try:
    data_int = {"sub": 10}  # Using integer
    token_int = create_access_token(data=data_int, expires_delta=expires)
    print(f"Created token with integer sub: {token_int}")

    result_int = verify_token(token_int)
    print(f"Verification result with integer sub: {result_int}")
except Exception as e:
    print(f"Error with integer sub: {e}")