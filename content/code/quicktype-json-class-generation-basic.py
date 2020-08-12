import requests

data = requests.get('https://s2k7tnzlhrpw.statuspage.io/api/v2/status.json').json()
status = data['status']['description']
updated_at = data['page']['updated_at']
print(f"Status: {status}\nUpdated at: {updated_at}")
