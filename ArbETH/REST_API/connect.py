from os import getcwd
import json
import requests


tokenlist_location = f"{getcwd()}/REST_API/1inchtokens.json"

# Get token list
r = requests.get("https://api.1inch.exchange/v1.1/tokens")
assert(r.status_code == 200), f"Failed request with code {r.status_code}. Is the URL correct?"

with open(tokenlist_location, "w") as json_file:
    json.dump(r.json(), json_file, indent = 4, sort_keys=True)

# After getting token list, select a range of tokens

