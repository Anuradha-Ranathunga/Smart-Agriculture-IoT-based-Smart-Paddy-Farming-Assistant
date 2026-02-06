import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:5000"

def test_endpoints():
    print("Testing IoT endpoints...")
    
    # Test getting all IoT data
    try:
        response = requests.get(f"{BASE_URL}/iot-data")
        print(f"IoT Data Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing IoT data endpoint: {e}")
    
    # Test getting a specific field
    try:
        response = requests.get(f"{BASE_URL}/iot-data/temperature")
        print(f"Temperature Field Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing temperature field endpoint: {e}")
    
    # Test getting threshold
    try:
        response = requests.get(f"{BASE_URL}/threshold")
        print(f"Threshold Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing threshold endpoint: {e}")

if __name__ == "__main__":
    test_endpoints()