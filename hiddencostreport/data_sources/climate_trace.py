import requests

url = "https://api.climatetrace.org/v6/assets"

response = requests.get(url)

assets = response.json()
