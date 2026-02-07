import os
from dotenv import load_dotenv
from jose import jwt

# Load environment variables
load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET', 'your-super-secret-jwt-key-change-in-production-immediately')
ALGORITHM = "HS256"

print(f"Using SECRET: {JWT_SECRET}")

# Test with string sub
data_str = {"sub": "10", "exp": 1770055000}  # exp is expiration time
token_str = jwt.encode(data_str, JWT_SECRET, algorithm=ALGORITHM)
print(f"Token with string sub: {token_str}")

# Decode to check what happens
decoded_str = jwt.decode(token_str, JWT_SECRET, algorithms=[ALGORITHM])
print(f"Decoded with string sub: {decoded_str}")

# Test with int sub
data_int = {"sub": 10, "exp": 1770055000}
token_int = jwt.encode(data_int, JWT_SECRET, algorithm=ALGORITHM)
print(f"Token with int sub: {token_int}")

# Decode to check what happens
decoded_int = jwt.decode(token_int, JWT_SECRET, algorithms=[ALGORITHM])
print(f"Decoded with int sub: {decoded_int}")

# Check if both cause the same error
from jose import JWTError
try:
    result1 = jwt.decode(token_str, JWT_SECRET, algorithms=[ALGORITHM])
    print("String sub token decoded successfully")
except JWTError as e:
    print(f"Error with string sub token: {e}")

try:
    result2 = jwt.decode(token_int, JWT_SECRET, algorithms=[ALGORITHM])
    print("Integer sub token decoded successfully")
except JWTError as e:
    print(f"Error with integer sub token: {e}")