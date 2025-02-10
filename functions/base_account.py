import hmac
import json
import time
import uuid
import hashlib
import requests

from requests import Response
from urllib.parse import urlencode
from config import API_KEY, API_SECRET, BASE_URL

httpClient=requests.Session()
recv_window=str(5000)

def HTTP_Request(endpoint: str, method: str, params: dict) -> Response:
    global time_stamp
    
    time_stamp=str(int(time.time() * 10 ** 3))
    
    if method == 'POST':
        signature=genSignature(json.dumps(params))
    elif method == "GET":
        signature=genSignature(urlencode(params))
    else: 
        raise ConnectionAbortedError(f"""Couldn't execute request, check for Method Correctness\n 
                                     method: {method}""")
        
    headers = {
        'X-BAPI-API-KEY': API_KEY,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    
    if(method=="POST"):
        response = httpClient.request(method, BASE_URL+endpoint, headers=headers, data=json.dumps(params))
    elif(method=="GET"):
        response = httpClient.request(method, BASE_URL+endpoint+"?"+urlencode(params), headers=headers)
    else: 
        raise ConnectionAbortedError(f"""Couldn't execute request, check for Method Correctness\n 
                                     method: {method}""")
        
    return response


def genSignature(params: str) -> str:
    param_str= str(time_stamp) + API_KEY + recv_window + params
    hash = hmac.new(bytes(API_SECRET, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature


def get_wallet_balance(account_type: str, coin: str = None) -> dict: 
    
    endpoint = "/v5/account/wallet-balance"
    
    params = {
        "accountType": account_type,
        "coin": coin
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_transferale_amount(coin_name: str) -> dict:
    
    endpoint = "/v5/account/withdrawal"
    
    params = {
        "coinName": coin_name
    }    
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_borrow_history(currency: str = None, start_time: int = None,
                       end_time: int = None, limit: int = None, 
                       cursor: str = None) -> dict:
    
    endpoint = "/v5/account/borrow-history"
    
    params = {
        "currency": currency,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def replay_library(coin: str) -> dict:
    
    endpoint = "/v5/account/quick-repayment"
    
    params = {
        "coin": coin
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_collateral_coin(coin: str, collateral_switch: str) -> dict:
    
    endpoint = "/v5/account/set-collateral-switch"
    
    params = {
        "coin": coin,
        "collateralSwitch": collateral_switch
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def batch_set_collateral_coin(request: list[dict]) -> dict: 
    
    endpoint = "/v5/account/set-collateral-switch-batch"
    
    params = {
        "request": request
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_collateral_info(currency: str) -> dict:
    
    endpoint = "/v5/account/collateral-info"
    
    params = {
        "currency": currency
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_coin_greeks(base_coin: str) -> dict:
    
    endpoint = "/v5/asset/coin-greeks"
    
    params = {
        "baseCoin": base_coin
    }

    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_fee_rate(category: str, symbol: str = None, base_coin: str = None) -> dict:
    
    endpoint = "/v5/account/fee-rate"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_account_info() -> dict:
    
    endpoint = "/v5/account/info"
    params = {}
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_DCP_info() -> dict:
    
    endpoint = "/v5/account/query-dcp-info"
    params = {}
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_transaction_log_UTA(account_type: str = None, category: str = None, currency: str = None,
                        base_coin: str = None, type: str = None, start_time: int = None, 
                        end_time: int = None, limit: int = None, cursor: str = None) -> dict:
    
    endpoint = "/v5/account/transaction-log"
    
    params = {
        "accountType": account_type,
        "category": category,
        "currency": currency,
        "baseCoin": base_coin,
        "type": type,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_transaction_log_classic(currency: str = None, base_coin: str = None, 
                                type: str = None, start_time: int = None, 
                                end_time: int = None, limit: int = None, cursor: str = None) -> dict:
    
    endpoint = '/v5/account/contract-transaction-log'
    
    params = {
        "currency": currency,
        "baseCoin": base_coin,
        "type": type,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_group_id() -> dict: 
    
    endpoint = '/v5/account/smp-group'
    params = {}
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_margin_mode(set_margin_mode: str) -> dict:
    
    endpoint = '/v5/account/set-margin-mode'
    
    params = {
        "setMarginMode": set_margin_mode
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def set_spot_hedging(set_hedging_mode: str) -> dict:
    
    endpoint = '/v5/account/set-hedging-mode'
    
    params = {
        "setHedgingMode": set_hedging_mode
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def set_mmp(base_coin: str, window: str, frozen_period: str, 
            qty_limit: str, delta_limit: str) -> dict:
    
    endpoint = "/v5/account/mmp-modify"
    
    params = {
        "baseCoin": base_coin,
        "window": window,
        "frozenPeriod": frozen_period,
        "qtyLimit": qty_limit,
        "deltaLimit": delta_limit
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def reset_mmp(base_coin: str) -> dict:
    
    endpoint = "/v5/account/mmp-reset"
    
    params = {
        "baseCoin": base_coin
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_mmp_state(base_coin: str) -> dict:
    
    endpoint = "/v5/account/mmp-state"
    
    params = {
        "baseCoin": base_coin
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()

