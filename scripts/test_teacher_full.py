import requests
import json

def test_teacher_flow():
    # 1. Register
    reg_url = "http://localhost:8000/api/auth/teacher/register"
    reg_data = {
        "username": "MasterTeacher",
        "email": "teacher@questacademy.com",
        "password": "password123"
    }
    print("Attempting Register...")
    try:
        res = requests.post(reg_url, json=reg_data)
        print(f"Register Status: {res.status_code}")
        print(f"Register Response: {res.text}")
    except Exception as e:
        print(f"Register Error: {e}")

    # 2. Login
    login_url = "http://localhost:8000/api/auth/teacher/login"
    login_data = {
        "username": "teacher@questacademy.com",
        "password": "password123"
    }
    print("\nAttempting Login...")
    try:
        res = requests.post(login_url, data=login_data)
        print(f"Login Status: {res.status_code}")
        if res.status_code == 200:
            print("Login SUCCESS!")
            print(f"Token: {res.json().get('access_token')[:20]}...")
        else:
            print(f"Login Failed: {res.text}")
    except Exception as e:
        print(f"Login Error: {e}")

if __name__ == "__main__":
    test_teacher_flow()
