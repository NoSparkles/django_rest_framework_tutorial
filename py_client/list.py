import requests

auth_endpoint = 'http://127.0.0.1:8000/api/auth/'

auth_response = get_response = requests.post(auth_endpoint, json={'username': 'robertas', 'password': 'robertas'})

print(auth_response.json())

if auth_response.status_code == 200:
  token = auth_response.json()['token']
  headers = {
    'Authorization': f'Bearer {token}'
  }

endpoint = 'http://127.0.0.1:8000/api/products/'

get_response = requests.get(endpoint, headers=headers)

print(get_response.json())