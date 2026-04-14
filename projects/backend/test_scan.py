import requests

url = "http://localhost:8000/api/scan"
data = {
    "wallet_address": "TEST_WALLET",
}
files = {
    "file": ("test.teal", "# pragma version 8\nint 1\nreturn")
}

try:
    response = requests.post(url, data=data, files=files)
    print(f"Status: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
