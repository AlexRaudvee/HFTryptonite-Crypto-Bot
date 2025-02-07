import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from config_ import API_KEY, API_SECRET, BASE_URL

def generate_signature(params, secret):
    """
    Generate the HMAC SHA256 signature required by Bybit.
    The parameters must be sorted alphabetically.
    """
    # Sort the parameters by key
    sorted_params = sorted(params.items())
    # Build the query string from sorted parameters
    query_string = urlencode(sorted_params)
    # Create HMAC SHA256 signature
    signature = hmac.new(secret.encode('utf-8'),
                         query_string.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    return signature

def get_wallet_balance():
    """
    Retrieve your wallet balance using the private endpoint.
    Endpoint: GET /v5/account/wallet-balance
    """
    endpoint = '/v5/account/wallet-balance'
    url = BASE_URL + endpoint

    # Create the parameters. The timestamp should be in milliseconds.
    params = {
        "api_key": API_KEY,
        "timestamp": int(time.time() * 1000), 
        "accountType": "UNIFIED",
    }
    
    # Generate the signature using your secret key and add it to the parameters.
    params['sign'] = generate_signature(params, API_SECRET)
    
    # Make the GET request to the endpoint with the parameters.
    response = requests.get(url, params=params)
    
    # Parse the response as JSON.
    return response.json()

if __name__ == "__main__":
    balance_info = get_wallet_balance()
    print("Wallet Balance Info:")
    print(balance_info["result"]["list"][0]["totalMarginBalance"])
