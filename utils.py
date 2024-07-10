import os
import requests

def load_env_variables(env_file=".env"):
    with open(env_file) as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def getenv(key):
    return os.getenv(key)

def ntfy(desc):
    requests.post(f"https://ntfy.sh/{getenv('NTFY_CHANNEL')}", 
                                    data=f"{desc}".encode('utf-8'))
    

# Example usage
load_env_variables()