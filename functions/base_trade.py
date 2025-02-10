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


def place_order(category: str, symbol: str, side: str, order_type: str, qty: str, 
                is_leverage: int = None, market_unit: str = None,
                price: str = None, trigger_direction: int = None, 
                order_filter: str = None, trigger_price: str = None,
                triggered_by: str = None, order_iv: str = None, 
                time_in_force: str = None, position_idx: int = None,
                order_link_id: str = None, take_profit: str = None, 
                stop_loss: str = None, tp_trigger_by: str = None, 
                sl_triggered_by: str = None, reduce_only: bool = None,
                close_on_trigger: bool = None, smp_type: str = None, 
                mmp: bool = None, tp_sl_mode: str = None, 
                tp_limit_price: str = None, sl_limit_price: str = None,
                tp_order_type: str = None, sl_order_type: str = None) -> dict:
    
    endpoint = "/v5/order/create"

    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": order_type,
        "qty": qty,
        "isLeverage": is_leverage,
        "marketUnit": market_unit,
        "price": price,
        "triggerDirection": trigger_direction,
        "orderFilter": order_filter,
        "triggerPrice": trigger_price,
        "triggeredBy": triggered_by,
        "orderIV": order_iv,
        "timeInForce": time_in_force,
        "positionIdx": position_idx,
        "orderLinkId": uuid.uuid4().hex,
        "takeProfit": take_profit,
        "stopLoss": stop_loss,
        "tpTriggeredBy": tp_trigger_by,
        "slTriggeredBy": sl_triggered_by,
        "reduceOnly": reduce_only,
        "closeOnTrigger": close_on_trigger,
        "smpType": smp_type,
        "mmp": mmp,
        "tpSlMode": tp_sl_mode,
        "tpLimitPrice": tp_limit_price,
        "slLimitPrice": sl_limit_price,
        "tpOrderType": tp_order_type,
        "slOrderType": sl_order_type
    }

    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)

    return response.json()


def amend_order(category: str, symbol: str, 
               order_id: str = None, order_link_id: str = None,
               order_iv: str = None, trigger_price: str = None, 
               qty: str = None, price: str = None, 
               tpsl_mode: str = None, take_profit: str = None,
               stop_loss: str = None, tp_trigger_by: str = None, 
               sl_trigger_by: str = None, trigger_by: str = None, 
               tp_limit_price: str = None, sl_limit_price: str = None) -> dict:
    
    endpoint = "/v5/order/amend"
    
    params = {
        "category": category,
        "symbol": symbol,
        "orderId": order_id,
        "orderLinkId": uuid.uuid64().hex,
        "orderIV": order_iv,
        "triggerPrice": trigger_price,
        "qty": qty,
        "price": price,
        "tpslMode": tpsl_mode,
        "takeProfit": take_profit,
        "stopLoss": stop_loss,
        "tpTriggerBy": tp_trigger_by,
        "slTriggerBy": sl_trigger_by,
        "triggerBy": trigger_by,
        "tpLimitPrice": tp_limit_price,
        "slLimitPrice": sl_limit_price,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def cancel_order(category: str, symbol: str, 
                 order_id: str = None, order_link_id: str = None, 
                 order_filter: str = None) -> dict:
    
    endpoint = "/v5/order/cancel"
    
    params = {
        "category": category,
        "symbol": symbol,
        "orderId": order_id,
        "orderLinkId": uuid.uuid64().hex,
        "orderFilter": order_filter,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_open_and_closed_orders(category: str, symbol: str = None, 
                               base_coin: str = None, settle_coin: str = None, 
                               order_id: str = None, order_link_id: str = None, 
                               open_only: int = None, order_filter: str = None, 
                               limit: int = None, cursor: str = None) -> dict:
    
    endpoint = "/v5/order/realtime"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "settleCoin": settle_coin,
        "orderId": order_id,
        "orderLinkId": uuid.uuid64().hex,
        "openOnly": open_only,
        "orderFilter": order_filter,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()
    
    
def cancel_all_orders(category: str, symbol: str = None, 
                      base_coin: str = None, settle_coin: str = None, 
                      order_filter: str = None, stop_order_type: str = None) -> dict:
    
    endpoint = "/v5/order/cancel-all"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "settleCoin": settle_coin,
        "orderFilter": order_filter,
        "stopOrderType": stop_order_type,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_order_history(category: str, symbol: str = None,
                      base_coin: str = None, settle_coin: str = None, 
                      order_id: str = None, order_link_id: str = None, 
                      order_filter: str = None, order_status: str = None,
                      start_time: int = None, end_time: int = None, 
                      limit: int = None, cursor: str = None) -> dict:
    
    endpoint = "/v5/order/history"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "settleCoin": settle_coin,
        "orderId": order_id,
        "orderLinkId": uuid.uuid64().hex,
        "orderFilter": order_filter,
        "orderStatus": order_status,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor,
    }
    
        
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def get_trade_history(category: str, symbol: str = None,
                      base_coin: str = None, order_id: str = None, 
                      order_link_id: str = None, start_time: int = None, 
                      end_time: int = None, exec_type: str = None, 
                      limit: int = None, cursor: str = None) -> dict:
    
    endpoint = "/v5/execution/list"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "orderId": order_id,
        "orderLinkId": uuid.uuid64().hex,
        "startTime": start_time,
        "endTime": end_time,
        "execType": exec_type,
        "limit": limit,
        "cursor": cursor,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def batch_place_order(category: str, request: list[dict]) -> dict:
    
    endpoint = "/v5/order/create-batch"
    
    params = {
        "category": category,
        "request": request,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def batch_amend_order(category: str, request: list[dict]) -> dict:
    
    endpoint = "/v5/order/amend-batch"
    
    params = {
        "category": category,
        "request": request,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def batch_cancel_order(category: str, request: list[dict]) -> dict:
    
    endpoint = "/v5/order/cancel-batch"
    
    params = {
        "category": category,
        "request": request,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()


def get_borrow_quota_spot(category: str, symbol: str, side: str) -> dict:
    
    endpoint = "/v5/order/spot-borrow-check"
    
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="GET", params=params)
    
    return response.json()


def set_DCP(time_window: int, product: str = "OPTIONS") -> dict:
    
    endpoint = "/v5/order/disconnected-cancel-all"
    
    params = {
        "time_window": time_window,
        "product": product,
    }
    
    params = dict(sorted(params.items()))
    response: Response = HTTP_Request(endpoint=endpoint, method="POST", params=params)
    
    return response.json()