import json
ACCOUNTS_PATH = 'data/accounts.json'

def saveAccount(data, accounts):
    if accounts:
        accountId = len(accounts)+1001
    else:
        accountId = 1001

    accountData = {
        "id":accountId,
        "username":data["username"],
        "full name":data["full name"],
        "password":data["password"],
        "is_deleted":False,
        "is_admin":False    
    }
    accounts.append(accountData)
    with open(ACCOUNTS_PATH, 'w') as file:
            json.dump(accounts, file, indent=3)
        