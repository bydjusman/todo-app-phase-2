import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables:")
print(f"JWT_SECRET from os.getenv: {os.getenv('JWT_SECRET', 'NOT FOUND')}")

# Import auth functions
from app.core.auth import SECRET_KEY, ALGORITHM
print(f"\nFrom auth module:")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"ALGORITHM: {ALGORITHM}")

# Test token creation and verification with more debugging
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# Create a test token manually to see if it works
to_encode = {"sub": 10}
expire = datetime.utcnow() + timedelta(minutes=30)
to_encode.update({"exp": expire})

print(f"\nEncoding data: {to_encode}")
print(f"Using SECRET_KEY: {SECRET_KEY}")

encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print(f"Encoded token: {encoded_token}")

# Try to decode it manually
try:
    decoded_payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded payload: {decoded_payload}")
except JWTError as e:
    print(f"JWTError during decoding: {e}")
    import traceback
    traceback.print_exc()

# Now test with the function from auth module
from app.core.auth import verify_token
result = verify_token(encoded_token)
print(f"verify_token result: {result}")