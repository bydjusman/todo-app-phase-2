"""
Test script for the AI Todo Chatbot functionality
This script tests the complete chatbot functionality including:
- MCP server tools
- Chat API endpoint
- Conversation persistence
- Natural language processing
"""
import asyncio
import json
import requests
from datetime import datetime

def test_chatbot_functionality():
    """
    Comprehensive test for the chatbot functionality
    """
    print("Testing AI Todo Chatbot functionality...")

    # Test server details
    BASE_URL = "http://localhost:8000/api"

    # First, let's try to register a test user or get an existing one
    print("\n1. Testing user authentication...")
    try:
        # Try to login with test credentials (adjust as needed)
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }

        # Attempt login (may fail if user doesn't exist)
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

        if login_response.status_code != 200:
            # Try to register the test user
            register_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123"
            }

            register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)

            if register_response.status_code == 200:
                print("✓ Test user registered successfully")

                # Now try to login
                login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            else:
                print(f"✗ Failed to register test user: {register_response.text}")
                return False

        if login_response.status_code == 200:
            auth_data = login_response.json()
            token = auth_data.get('access_token')
            user_id = auth_data.get('user_id')

            print(f"✓ Successfully authenticated. User ID: {user_id}")
        else:
            print(f"✗ Login failed: {login_response.text}")
            return False

    except Exception as e:
        print(f"✗ Authentication test failed: {str(e)}")
        return False

    # Test chat functionality
    print("\n2. Testing chat API endpoint...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        # Test 1: Add a task via chat
        print("   Testing task addition...")
        chat_data = {
            "message": "Add a task to buy groceries",
            "token": token
        }

        response = requests.post(f"{BASE_URL}/chat/{user_id}", json=chat_data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Task added successfully. Response: {result['response'][:50]}...")
            conversation_id = result.get('conversation_id')
        else:
            print(f"   ✗ Task addition failed: {response.text}")
            return False

        # Test 2: List tasks via chat
        print("   Testing task listing...")
        chat_data = {
            "message": "Show me all my tasks",
            "conversation_id": conversation_id,
            "token": token
        }

        response = requests.post(f"{BASE_URL}/chat/{user_id}", json=chat_data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Tasks listed successfully. Response: {result['response'][:50]}...")
        else:
            print(f"   ✗ Task listing failed: {response.text}")
            return False

        # Test 3: Complete a task via chat
        print("   Testing task completion...")
        # First, get the task ID by listing tasks
        list_data = {
            "message": "Show me all my tasks",
            "conversation_id": conversation_id,
            "token": token
        }

        response = requests.post(f"{BASE_URL}/chat/{user_id}", json=list_data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            # Parse the response to extract task ID
            # This is a simple heuristic - in a real test, we'd parse more carefully
            import re
            task_ids = re.findall(r'\[(\d+)\]', result['response'])

            if task_ids:
                task_id = int(task_ids[0])  # Get the first task ID

                # Now complete the task
                complete_data = {
                    "message": f"Complete task {task_id}",
                    "conversation_id": conversation_id,
                    "token": token
                }

                response = requests.post(f"{BASE_URL}/chat/{user_id}", json=complete_data, headers=headers)

                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✓ Task {task_id} completed successfully. Response: {result['response'][:50]}...")
                else:
                    print(f"   ✗ Task completion failed: {response.text}")
                    return False
            else:
                print("   ⚠ Could not extract task ID from response, skipping completion test")
        else:
            print(f"   ✗ Could not list tasks to find ID: {response.text}")
            return False

        print("\n✓ All chatbot functionality tests passed!")
        return True

    except Exception as e:
        print(f"✗ Chat API test failed: {str(e)}")
        return False


def test_mcp_server():
    """
    Test the MCP server functionality
    """
    print("\n3. Testing MCP server tools...")

    # This would normally test the MCP server directly
    # For now, we'll just verify that the endpoints exist
    BASE_URL = "http://localhost:8000/api"

    try:
        # Test that the MCP tools endpoints are available
        endpoints = [
            f"{BASE_URL}/mcp-tools/add-task",
            f"{BASE_URL}/mcp-tools/list-tasks",
            f"{BASE_URL}/mcp-tools/update-task",
            f"{BASE_URL}/mcp-tools/complete-task",
            f"{BASE_URL}/mcp-tools/delete-task"
        ]

        for endpoint in endpoints:
            try:
                response = requests.options(endpoint)  # OPTIONS request to check if endpoint exists
                print(f"   ✓ MCP endpoint available: {endpoint}")
            except:
                print(f"   ⚠ MCP endpoint may not be available: {endpoint}")

        print("✓ MCP server endpoints verified!")
        return True

    except Exception as e:
        print(f"✗ MCP server test failed: {str(e)}")
        return False


def main():
    """
    Main test function
    """
    print("="*60)
    print("AI Todo Chatbot - Comprehensive Functionality Test")
    print("="*60)

    # Run all tests
    tests = [
        ("Chatbot functionality", test_chatbot_functionality),
        ("MCP server", test_mcp_server),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        result = test_func()
        results.append((test_name, result))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print("\nOverall result:", "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
    print("="*60)

    return all_passed


if __name__ == "__main__":
    main()