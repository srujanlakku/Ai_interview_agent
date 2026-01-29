
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_signup():
    print("Testing Signup...")
    payload = {
        "email": "lakkusrujan@gmail.com",
        "full_name": "Srujan",
        "password": "Srujan@123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("Signup Successful")
            return True
        elif response.status_code == 409:
            print("User already exists (Duplicate)")
            return True # Technically not a system failure, just state
        else:
            print("Signup Failed")
            return False
    except Exception as e:
        print(f"Signup Exception: {e}")
        return False

def test_login():
    print("\nTesting Login...")
    payload = {
        "email": "lakkusrujan@gmail.com",
        "password": "Srujan@123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("Login Successful")
            return True
        else:
            print("Login Failed")
            return False
    except Exception as e:
        print(f"Login Exception: {e}")
        return False

if __name__ == "__main__":
    signup_success = test_signup()
    login_success = test_login()
