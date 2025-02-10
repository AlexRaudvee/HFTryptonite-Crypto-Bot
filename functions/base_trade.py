import hashlib
import hmac
import json
import time
import requests

from config import API_KEY, API_SECRET, BASE_URL


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
    
    url = BASE_URL + "/v5/order/create"

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
        "orderLinkId": order_link_id,
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

    
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    # Generate signature
    sorted_params = dict(sorted(params.items()))
    json_params = json.dumps(sorted_params, separators=(",", ":"))
    sign_str = timestamp + API_KEY + recv_window + json_params
    print(sign_str)
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        sign_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    print(signature)
    

    params["sign"] = signature
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }

    #  "Content-Type": "application/json",
    # "X-BAPI-API-KEY": self.api_key,
    # "X-BAPI-SIGN": signature,
    # "X-BAPI-SIGN-TYPE": "2",
    # "X-BAPI-TIMESTAMP": str(timestamp),
    # "X-BAPI-RECV-WINDOW": str(recv_window),

    # Send request
    try:
        response = requests.post(
            url=url,
            headers=headers,
            data=params
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        if isinstance(e, requests.HTTPError):
            error_msg = f"HTTP Error {e.response.status_code}: {e.response.text}"
        else:
            error_msg = f"Request failed: {str(e)}"
        raise requests.RequestException(error_msg) from e
    
    pass