import requests

url = "http://localhost:8000"
username = "qxnam"
password = "1234"
token = ""

def get_token():
    response = requests.post(f"{url}/auth/token", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def create_user():
    response = requests.post(f"{url}/auth/register", json={
        "username": username,
        "password": password,
    })
    if response.status_code == 400:
        print("User already exists.")
    elif response.status_code == 201:
        print("User created.")
    else:
        print("Failed to create user:", response.text)

def submit_solution(solution, headers):
    response = requests.post(f"{url}/answer", json=solution, headers=headers)
    if response.status_code == 200:
        print("Solution submitted successfully.")
    else:
        print("Failed to submit solution:", response.text)

token = get_token()
if not token:
    create_user()
    token = get_token()
    
headers = {"Authorization": f"Bearer {token}"}
solution = {
    "question_id": 1,
    "answer": "This is a test answer."
}
submit_solution(solution, headers)
