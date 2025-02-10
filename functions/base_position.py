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


def get_position_info(category: str, symbol: str = None, 
                      base_coin: str = None, settle_coin: str = None,
                      limit: int = None, cursor: str = None) -> dict:
    
    endpoint = "/v5/position/list"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "settleCoin": settle_coin,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_leverage(category: str, symbol: str, buy_leverage: str, sell_leverage: str) -> dict:
     
    endpoint = "/v5/position/set-leverage"
    
    params = {
        "category": category,
        "symbol": symbol,
        "buyLeverage": buy_leverage,
        "sellLeverage": sell_leverage,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def switch_cross_isolated_margin(category: str, symbol: str, trade_mode: int, 
                                 buy_leverage: str, sell_leverage: str) -> dict:
    
    endpoint = "/v5/position/switch-isolated"
    
    params = {
        "category": category,
        "symbol": symbol,
        "tradeMode": trade_mode,
        "buyLeverage": buy_leverage,
        "sellLeverage": sell_leverage,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def switch_position_mode(category: str, mode: int, symbol: str, coin: str = None) -> dict:
    
    endpoint = "/v5/position/switch-mode"
    
    params = {
        "category": category,
        "mode": mode,
        "symbol": symbol,
        "coin": coin,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def set_trading_stop(category: str, symbol: str, tpsl_mode: str, position_idx: int, 
                     take_profit: str = None, stop_loss: str = None, 
                     trailing_stop: str = None, tp_trigger_by: str = None, 
                     sl_trigger_by: str = None, active_price: str = None,
                     tp_size: str = None, sl_size: str = None, 
                     tp_limit_price: str = None, sl_limit_price: str = None,
                     tp_order_type: str = None, sl_order_type: str = None) -> dict:
    
    endpoint = "/v5/position/trading-stop"
    
    params = {
        "category": category,
        "symbol": symbol,
        "tpslMode": tpsl_mode,
        "positionIdx": position_idx,
        "takeProfit": take_profit,
        "stopLoss": stop_loss,
        "trailingStop": trailing_stop,
        "tpTriggerBy": tp_trigger_by,
        "slTriggerBy": sl_trigger_by,
        "activePrice": active_price,
        "tpSize": tp_size,
        "slSize": sl_size,
        "tpLimitPrice": tp_limit_price,
        "slLimitPrice": sl_limit_price,
        "tpOrderType": tp_order_type,
        "slOrderType": sl_order_type,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def set_auto_add_margin(category: str, symbol: str, auto_add_margin: int, position_idx: int) -> dict:
    
    endpoint = "/v5/position/set-auto-add-margin"
    
    params = {
        "category": category,
        "symbol": symbol,
        "autoAddMargin": auto_add_margin,
        "positionIdx": position_idx,
    } 
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def add_or_reduce_margin(category: str, symbol: str, margin: str, position_idx: int) -> dict:
    
    endpoint = "/v5/position/add-margin"
    
    params = {
        "category": category,
        "symbol": symbol,
        "margin": margin,
        "positionIdx": position_idx,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_closed_pnL(category: str, symbol: str = None, start_time: int = None,
                   end_time: int = None, limit: int = None, cursor: str = None) -> dict:
    
    
    endpoint = "/v5/position/closed-pnl"
    
    params = {
        "category": category,
        "symbol": symbol,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def move_position(from_uid: str, to_uid: str, list: list[dict]) -> dict:
    
    endpoint = "/v5/position/move-positions"
    
    params = {
        "fromUid": from_uid,
        "toUid": to_uid,
        "list": list,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_move_position_history(category: str, symbol: str, start_time: int, end_time: int,
                              status: str = None, block_trade_id: str = None, limit: str = None,
                              cursor: str = None) -> dict:
    
    endpoint = "/v5/position/move-history"
    
    params = {
        "category": category,
        "symbol": symbol,
        "startTime": start_time,
        "endTime": end_time,
        "status": status,
        "blockTradeId": block_trade_id,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def confirm_new_risk_limit(category: str, symbol: str) -> dict:
    
    endpoint = "/v5/position/confirm-pending-mmr"
    
    params = {
        "category": category,
        "symbol": symbol,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_tp_sl_mode(category: str, symbol: str, tp_sl_mode: str) -> dict:
    
    endpoint = "/v5/position/set-tpsl-mode"
    
    params = {
        "category": category,
        "symbol": symbol,
        "tpSlMode": tp_sl_mode,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_risk_limit(category: str, symbol: str, risk_id: str, positon_idx: str = None) -> dict:
    
    endpoint = "/v5/position/set-risk-limit"
    
    params = {
        "category": category,
        "symbol": symbol,
        "riskId": risk_id,
        "positionIdx": positon_idx,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()