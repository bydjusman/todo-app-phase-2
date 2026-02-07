#!/usr/bin/env python3
"""
Simple test script to check if backend auth endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_register():
    """Test register endpoint"""
    print("\nTesting register endpoint...")
    try:
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test1234",
            "confirm_password": "test1234"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 400]  # 400 if user already exists
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test login endpoint"""
    print("\nTesting login endpoint...")
    try:
        data = {
            "username": "testuser",
            "password": "test1234"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=data,  # form-encoded
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 401]  # 401 if wrong credentials
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Auth Test Script")
    print("=" * 50)
    
    health_ok = test_health()
    if not health_ok:
        print("\n❌ Health check failed! Backend server might not be running.")
        print("Start backend with: cd backend && python -m uvicorn app.main:app --reload")
        exit(1)
    
    register_ok = test_register()
    login_ok = test_login()
    
    print("\n" + "=" * 50)
    if health_ok and register_ok and login_ok:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    print("=" * 50)
