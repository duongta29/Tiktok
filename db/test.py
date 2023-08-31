import json
with open ("db/account.json", "r") as f:
        # account = json.loads(f)
        account = f.read()
        n = json.loads(account)
print(n)