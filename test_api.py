"""
API Testing Script
Use this to test the Study Bot API endpoints
"""

import requests
import json
from datetime import datetime

# API Base URL (change this to your deployed URL)
BASE_URL = "http://localhost:8000"  # Change to your Render URL after deployment

def print_response(title, response):
    """Pretty print API responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def test_health_check():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_chat(user_id="test_user_123", message="What is photosynthesis?"):
    """Test chat endpoint"""
    payload = {
        "user_id": user_id,
        "message": message
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print_response(f"Chat Request: {message}", response)
    return response.status_code == 200

def test_get_history(user_id="test_user_123"):
    """Test get history endpoint"""
    response = requests.get(f"{BASE_URL}/history/{user_id}")
    print_response(f"Get History for {user_id}", response)
    return response.status_code == 200

def test_clear_history(user_id="test_user_123"):
    """Test clear history endpoint"""
    response = requests.delete(f"{BASE_URL}/clear-history/{user_id}")
    print_response(f"Clear History for {user_id}", response)
    return response.status_code == 200

def test_stats():
    """Test stats endpoint"""
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Statistics", response)
    return response.status_code == 200

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("STUDY BOT API TESTING")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Chat - Question 1", lambda: test_chat(message="What is photosynthesis?")),
        ("Chat - Question 2", lambda: test_chat(message="Can you explain it in simpler terms?")),
        ("Chat - Question 3", lambda: test_chat(message="What are some study tips for biology?")),
        ("Get History", test_get_history),
        ("Statistics", test_stats),
        ("Clear History", test_clear_history),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "✓ PASSED" if result else "✗ FAILED"))
        except Exception as e:
            results.append((test_name, f"✗ ERROR: {str(e)}"))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results:
        print(f"{test_name}: {result}")
    
    passed = sum(1 for _, r in results if "PASSED" in r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API")
        print(f"Make sure the server is running at {BASE_URL}")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
