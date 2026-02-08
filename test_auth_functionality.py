import requests
import json

# Base URL for the backend
BASE_URL = "http://localhost:8000"

def test_signup_login():
    print("Testing Signup and Login functionality...")
    
    # Test data with unique username
    import time
    unique_id = str(int(time.time()))
    signup_data = {
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123"
    }
    
    print(f"\n1. Testing Signup with username: {signup_data['username']}...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("[SUCCESS] Signup successful!")
            user_data = response.json()
            print(f"  User created: {user_data['username']} (ID: {user_data['id']})")
        elif response.status_code == 400 and "already registered" in response.text:
            print("[INFO] User already exists, continuing with login test...")
        else:
            print(f"[ERROR] Signup failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Signup error: {e}")
        return False
    
    print(f"\n2. Testing Login with username: {signup_data['username']}...")
    login_data = {
        "username": signup_data['username'],
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=login_data  # Using form data for OAuth2PasswordRequestForm
        )
        if response.status_code == 200:
            print("[SUCCESS] Login successful!")
            token_data = response.json()
            print(f"  Access token received (length: {len(token_data['access_token'])})")
            return True
        else:
            print(f"[ERROR] Login failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return False

if __name__ == "__main__":
    success = test_signup_login()
    if success:
        print("\n[SUCCESS] All tests passed! Signup and login are working correctly.")
    else:
        print("\n[ERROR] Some tests failed. Please check the backend configuration.")