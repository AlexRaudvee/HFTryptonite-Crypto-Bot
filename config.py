import hmac
import hashlib
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