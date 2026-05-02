import os
from dotenv import load_dotenv
from mine_utils import MinecraftAuthorization

load_dotenv()
CLIENT_ID = str(os.getenv("CLIENT_ID"))
REDIRECT_URL = str(os.getenv("REDIRECT_URL"))

# Create and run authorization
auth = MinecraftAuthorization(CLIENT_ID, REDIRECT_URL)

if auth.authorize(timeout=300):
    credentials = auth.get_credentials()
    print(f"\nCredentials: {credentials}")
else:
    print("Authorization failed")