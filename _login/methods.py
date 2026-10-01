from datetime import datetime, timedelta
from uuid import uuid4
import json
ACCOUNTS_PATH = 'data/accounts.json'

def generateToken():
    token = f'{uuid4()}-{uuid4()}'
    expiration = datetime.utcnow() + timedelta(hours=1)
    return token, expiration

def saveToken(userId, token, expiration, accounts):
    for account in accounts:
        if account["id"] == userId:
            account["token"] = token
            account["token_expiration"] = expiration.isoformat()
            break
        
    with open(ACCOUNTS_PATH, 'w') as file:
        json.dump(accounts, file, indent=3)

    return {"Login successful, your token is token (expires in 1 hour)": token}