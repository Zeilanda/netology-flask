import requests

data = requests.post('http://127.0.0.1:5000', json={'a': 'b'},)
print(data.status_code)
print(data.text)
