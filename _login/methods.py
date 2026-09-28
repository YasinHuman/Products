from datetime import datetime, timedelta
from uuid import uuid4
import json
ACCOUNTS_PATH = 'data/accounts.json'

def generateToken(userId, accounts):
    token = f'{uuid4()}-{uuid4()}'
    expiration = datetime.utcnow() + timedelta(hours=1)

    for account in accounts:
        if account["id"] == userId:
            account["token"] = token
            account["token_expiration"] = expiration.isoformat()
            break
        
    with open(ACCOUNTS_PATH, 'w') as file:
        json.dump(accounts, file, indent=3)

    return {"token (expires in 1 hour)": token}