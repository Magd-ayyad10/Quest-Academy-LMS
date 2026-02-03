import requests

def test_teacher_login():
    url = "http://localhost:8000/api/auth/teacher/login"
    data = {
        "username": "teacher@questacademy.com",
        "password": "password123"
    }
    try:
        response = requests.post(url, data=data) # default is form-urlencoded
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_teacher_login()
