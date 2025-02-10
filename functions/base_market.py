import hmac
import hashlib
import requests
from urllib.parse import urlencode

from config_ import API_SECRET, BASE_URL

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


def get_bybit_server_time() -> dict:
    """
    Retrieve the current server time from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/time` endpoint
    to fetch the current server time in both seconds and nanoseconds.

    Parameters
    ---
        None

    Returns
    ---
        dict: A dictionary containing the server time information. The structure includes:
            - 'retCode' (int): API response code (0 indicates success).
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains 'timeSecond' (epoch time in seconds) and
              'timeNano' (epoch time in nanoseconds).

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 HTTP status code.
        requests.RequestException: For issues like network connectivity problems,
            invalid URL, or timeout.

    Example
    ---
        >>> try:
        ...     server_time = get_bybit_server_time()
        ...     print(f"Server time (seconds): {server_time['result']['timeSecond']}")
        ... except requests.HTTPError as e:
        ...     print(f"HTTP error occurred: {e}")
        ... except requests.RequestException as e:
        ...     print(f"Request error occurred: {e}")
    """
    
    url = BASE_URL + "/v5/market/time"
    
    response = requests.get(url=url)
    response.raise_for_status()  # Raise exception for non-200 status codes
    return response.json()


def get_kline(category: str, symbol: str, interval: str, start: int = None, end: int = None, limit: int = 200) -> dict:
    """
    Retrieve kline (candlestick) data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/kline` endpoint
    to fetch historical candlestick data for the specified trading pair.

    Parameters
    ---
        category (str): Product category. Valid values: "spot", "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        interval (str): Kline interval. Supported values: 1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M.
        start (int, optional): Start timestamp in milliseconds. Defaults to None.
        end (int, optional): End timestamp in milliseconds. Defaults to None.
        limit (int, optional): Maximum number of records to return. Defaults to 200.

    Returns
    ---
        dict: A dictionary containing the kline data. Structure includes:
            - 'retCode' (int): API response code (0 indicates success).
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): The product category.
                - 'symbol' (str): The trading pair.
                - 'list' (list): List of kline entries. Each entry is an array with:
                    [0] Start time (ms timestamp),
                    [1] Open price,
                    [2] High price,
                    [3] Low price,
                    [4] Close price,
                    [5] Volume,
                    [6] Turnover.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 HTTP status code.
        requests.RequestException: For issues like network connectivity problems,
            invalid URL, or timeout.

    Example
    ---
        >>> try:
        ...     kline_data = get_kline(category='linear', symbol='BTCUSDT', interval='15')
        ...     print(f"First kline open price: {kline_data['result']['list'][0][1]}")
        ... except requests.HTTPError as e:
        ...     print(f"HTTP error occurred: {e}")
        ... except requests.RequestException as e:
        ...     print(f"Request error occurred: {e}")
    """
    
    url = BASE_URL + "/v5/market/kline"
    
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit
    }
    
    params['sign'] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status() 
    return response.json()


def get_mark_price_kline(category: str, symbol: str, interval: str, start: int = None, end: int = None, limit: int = 200) -> dict: 
    """
    Retrieve mark price kline data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/mark-price-kline` endpoint
    to fetch historical mark price candlestick data for the specified trading pair.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        interval (str): Kline interval. Supported values: 1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M.
        start (int, optional): Start timestamp in milliseconds. Defaults to None.
        end (int, optional): End timestamp in milliseconds. Defaults to None.
        limit (int, optional): Maximum number of records to return. Defaults to 200.

    Returns
    ---
        dict: A dictionary containing the mark price kline data. Structure includes:
            - 'retCode' (int): API response code (0 indicates success).
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): The product category.
                - 'symbol' (str): The trading pair.
                - 'list' (list): List of kline entries. Each entry is an array with:
                    [0] Start time (ms timestamp),
                    [1] Open mark price,
                    [2] High mark price,
                    [3] Low mark price,
                    [4] Close mark price.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 HTTP status code.
        requests.RequestException: For network issues, invalid URL, or timeout.

    Example
    ---
        >>> try:
        ...     data = get_mark_price_kline(category='linear', symbol='BTCUSDT', interval='60')
        ...     print(f"First mark price: {data['result']['list'][0][4]}")
        ... except requests.HTTPError as e:
        ...     print(f"HTTP error: {e}")
    """
    
    url = BASE_URL + "/v5/market/mark-price-kline"
    
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit
    }
    
    params['sign'] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()
    
    
def get_index_price_kline(category: str, symbol: str, interval: str, start: int = None, end: int = None, limit: int = 200) -> dict: 
    """
    Retrieve index price kline data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/index-price-kline` endpoint
    to fetch historical index price candlestick data for the specified trading pair.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        interval (str): Kline interval. Supported values: 1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M.
        start (int, optional): Start timestamp in milliseconds. Defaults to None.
        end (int, optional): End timestamp in milliseconds. Defaults to None.
        limit (int, optional): Maximum number of records to return. Defaults to 200.

    Returns
    ---
        dict: A dictionary containing the index price kline data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains category, symbol, and list of kline entries with:
                [0] Timestamp, [1-4] Open/High/Low/Close index prices.

    Raises
    ---
        requests.HTTPError: For non-200 responses.
        requests.RequestException: For request-related errors.

    Example
    ---
        >>> try:
        ...     data = get_index_price_kline(category='linear', symbol='ETHUSDT', interval='D')
        ...     print(f"Daily index prices: {len(data['result']['list'])} entries")
        ... except requests.RequestException as e:
        ...     print(f"Error: {e}")
    """
    
    url = BASE_URL + "/v5/market/index-price-kline"
    
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit
    }
    
    params['sign'] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_premium_index_price_kline(category: str, symbol: str, interval: str, start: int = None, end: int = None, limit: int = 200) -> dict: 
    """
    Retrieve premium index price kline data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/premium-index-price-kline` endpoint
    to fetch historical premium index price candlestick data for the specified trading pair.

    Parameters
    ---
        category (str): Product category. Valid values: "linear".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        interval (str): Kline interval. Supported values: 1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M.
        start (int, optional): Start timestamp in milliseconds. Defaults to None.
        end (int, optional): End timestamp in milliseconds. Defaults to None.
        limit (int, optional): Maximum number of records. Defaults to 200.

    Returns
    ---
        dict: Dictionary with premium index price klines. Structure includes:
            - 'retCode' (int): Response status code.
            - 'retMsg' (str): Response message.
            - 'result' (dict): Contains premium index price data points with timestamps.

    Raises
    ---
        requests.HTTPError: For unsuccessful API responses.
        requests.RequestException: For request failures.

    Example
    ---
        >>> try:
        ...     premium_data = get_premium_index_price_kline(category='linear', symbol='BTCUSDT', interval='60')
        ...     print(f"Premium index values: {premium_data['result']['list']}")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e.response.status_code}")
    """
    
    url = BASE_URL + "/v5/market/premium-index-price-kline"
    
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit
    }
    
    params['sign'] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_instruments_info(category: str, symbol: str, base_coin: str, status: str = None, limit: int = 500, cursor: str = None) -> dict:
    """
    Retrieve instrument information from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/instruments-info` endpoint
    to fetch detailed information about trading instruments.

    Parameters
    ---
        category (str): Product category. Valid values: "spot", "linear", "inverse", "option".
        symbol (str): Specific instrument symbol to filter by.
        base_coin (str): Base coin to filter instruments (e.g., "BTC").
        status (str, optional): Filter by instrument status. Valid values: "Trading", "Settling".
        limit (int, optional): Maximum number of results. Defaults to 500.
        cursor (str, optional): Pagination cursor for next page.

    Returns
    ---
        dict: Dictionary containing instrument details. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): Response message.
            - 'result' (dict): Contains 'category', 'list' of instruments with details like
              symbol, contract type, fees, and settlement status.

    Raises
    ---
        requests.HTTPError: For non-200 status codes.
        requests.RequestException: For request errors.

    Example
    ---
        >>> try:
        ...     instruments = get_instruments_info(category='spot', symbol='BTCUSDT', base_coin='BTC')
        ...     print(f"Found {len(instruments['result']['list'])} instruments")
        ... except requests.RequestException as e:
        ...     print(f"Request failed: {e}")
    """
    
    url = BASE_URL + "/v5/market/instruments-info"
    
    params = {
        "category": category,
        "symbol": symbol,
        "status": status,
        "baseCoin": base_coin,
        "limit": limit,
        "cursor": cursor
    }
    
    params['sign'] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_orderbook(category: str, symbol: str, limit: int = None) -> dict:
    """
    Retrieve order book data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/orderbook` endpoint
    to fetch the current order book (market depth) for the specified trading pair.

    Parameters
    ---
        category (str): Product category. Valid values: "spot", "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        limit (int, optional): Number of price points to return. Valid values: 1-200. Defaults to None.

    Returns
    ---
        dict: A dictionary containing order book data. Structure includes:
            - 'retCode' (int): API response code (0 indicates success).
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 's' (str): Symbol.
                - 'b' (list): Bid prices with quantities ([price, quantity]).
                - 'a' (list): Ask prices with quantities ([price, quantity]).
                - 'ts' (int): Timestamp of the response.
                - 'u' (int): Order book update ID.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 HTTP status code.
        requests.RequestException: For network issues, invalid URL, or timeout.

    Example
    ---
        >>> try:
        ...     orderbook = get_orderbook(category='spot', symbol='BTCUSDT')
        ...     print(f"Best bid: {orderbook['result']['b'][0][0]}")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e.response.status_code}")
    """

    url = BASE_URL + "/v5/market/orderbook"
    
    params = {
        "category": category,
        "symbol": symbol,
        "limit": limit
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_tickers(category: str, symbol: str, base_coin: str = None, exp_date: str = None) -> dict:
    """
    Retrieve market tickers from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/tickers` endpoint
    to fetch real-time market data for the specified trading instruments.

    Parameters
    ---
        category (str): Product category. Valid values: "spot", "linear", "inverse", "option".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        base_coin (str, optional): Base coin for filtering options. Required for options category.
        exp_date (str, optional): Expiration date for options (YYYY-MM-DD). Required for options.

    Returns
    ---
        dict: A dictionary containing ticker data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): Product category.
                - 'list' (list): Ticker data including last price, 24h volume, bid/ask prices.

    Raises
    ---
        requests.HTTPError: For non-200 responses.
        requests.RequestException: For request-related errors.

    Example
    ---
        >>> try:
        ...     tickers = get_tickers(category='spot', symbol='BTCUSDT')
        ...     print(f"24h volume: {tickers['result']['list'][0]['volume24h']}")
        ... except requests.RequestException as e:
        ...     print(f"Error: {e}")
    """

    url = BASE_URL + "/v5/market/tickers"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "expDate": exp_date
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()

def get_funding_rate_history(category: str, symbol: str, start_time: int = None, end_time: int = None, limit: int = None) -> dict:
    """
    Retrieve historical funding rates from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/funding/history` endpoint
    to fetch historical funding rate data for perpetual contracts.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        start_time (int, optional): Start timestamp in milliseconds.
        end_time (int, optional): End timestamp in milliseconds.
        limit (int, optional): Number of results to return. Max 200.

    Returns
    ---
        dict: A dictionary containing funding rate history. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): Product category.
                - 'list' (list): Funding rate records with timestamps and rates.

    Raises
    ---
        requests.HTTPError: For unsuccessful API responses.
        requests.RequestException: For request failures.

    Example
    ---
        >>> try:
        ...     funding = get_funding_rate_history(category='linear', symbol='BTCUSDT')
        ...     print(f"Last funding rate: {funding['result']['list'][0]['fundingRate']}")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e}")
    """

    url = BASE_URL + "/v5/market/funding/history"
    
    params = {
        "category": category,
        "symbol": symbol,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_public_recent_trading_history(category: str, symbol: str, base_coin: str = None, option_type: str = None, limit: int = None) -> dict:
    """
    Retrieve recent trading history from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/recent-trade` endpoint
    to fetch recent executed trades for the specified instrument.

    Parameters
    ---
        category (str): Product category. Valid values: "spot", "linear", "inverse", "option".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        base_coin (str, optional): Base coin for options filtering.
        option_type (str, optional): Option type (Call/Put). Valid values: "Call", "Put".
        limit (int, optional): Number of trades to return. Max 1000.

    Returns
    ---
        dict: A dictionary containing recent trades. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): Product category.
                - 'list' (list): Trade entries with price, quantity, and timestamp.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 status code.
        requests.RequestException: For network or request errors.

    Example
    ---
        >>> try:
        ...     trades = get_public_recent_trading_history(category='spot', symbol='ETHUSDT')
        ...     print(f"Most recent trade price: {trades['result']['list'][0]['price']}")
        ... except requests.RequestException as e:
        ...     print(f"Error fetching trades: {e}")
    """

    url = BASE_URL + "/v5/market/recent-trade"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "optionType": option_type,
        "limit": limit
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_open_interest(category: str, symbol: str, interval_time: str, start_time: int = None, end_time: int = None, limit: int = None, cursor: str = None) -> dict:
    """
    Retrieve open interest data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/open-interest` endpoint
    to fetch historical open interest data for derivatives contracts.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        interval_time (str): Data interval. Valid values: "5min", "15min", "30min", "1h", "4h", "1d".
        start_time (int, optional): Start timestamp in milliseconds.
        end_time (int, optional): End timestamp in milliseconds.
        limit (int, optional): Number of results to return. Max 200.
        cursor (str, optional): Pagination cursor.

    Returns
    ---
        dict: A dictionary containing open interest data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains:
                - 'category' (str): Product category.
                - 'symbol' (str): Trading pair.
                - 'list' (list): Open interest values with timestamps.

    Raises
    ---
        requests.HTTPError: For non-200 status codes.
        requests.RequestException: For request-related issues.

    Example
    ---
        >>> try:
        ...     oi_data = get_open_interest(category='linear', symbol='BTCUSDT', interval_time='1h')
        ...     print(f"Open interest trend: {len(oi_data['result']['list'])} data points")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e}")
    """
    
    url = BASE_URL + "/v5/market/open-interest"
    
    params = {
        "category": category,
        "symbol": symbol,
        "intervalTime": interval_time,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_historical_volatility(category: str, base_coin: str = None, period: int = None, start_time: int = None, end_time: int = None) -> dict:
    """
    Retrieve historical volatility data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/historical-volatility` endpoint
    to fetch volatility data for cryptocurrency options.

    Parameters
    ---
        category (str): Product category. Valid values: "option".
        base_coin (str, optional): Base coin (e.g., "BTC").
        period (int, optional): Period for volatility calculation in days.
        start_time (int, optional): Start timestamp in milliseconds.
        end_time (int, optional): End timestamp in milliseconds.

    Returns
    ---
        dict: A dictionary containing volatility data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains volatility values and timestamps.

    Raises
    ---
        requests.HTTPError: For unsuccessful API responses.
        requests.RequestException: For request failures.

    Example
    ---
        >>> try:
        ...     volatility = get_historical_volatility(category='option', base_coin='BTC')
        ...     print(f"Volatility data points: {len(volatility['result']['data'])}")
        ... except requests.RequestException as e:
        ...     print(f"Error: {e}")
    """
    
    url = BASE_URL + "/v5/market/historical-volatility"
    
    params = {
        "category": category,
        "baseCoin": base_coin,
        "period": period,
        "startTime": start_time,
        "endTime": end_time
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_insurance(coin: str = None) -> dict:
    """
    Retrieve insurance fund data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/insurance` endpoint
    to fetch information about the exchange's insurance fund.

    Parameters
    ---
        coin (str, optional): Coin to filter insurance fund data (e.g., "BTC").

    Returns
    ---
        dict: A dictionary containing insurance fund details. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains insurance fund balances and update times.

    Raises
    ---
        requests.HTTPError: For non-200 responses.
        requests.RequestException: For request errors.

    Example
    ---
        >>> try:
        ...     insurance = get_insurance(coin='BTC')
        ...     print(f"BTC insurance balance: {insurance['result']['list'][0]['balance']}")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e}")
    """

    url = BASE_URL + "/v5/market/insurance"
    
    params = {
        "coin": coin
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_risk_limit(category: str, symbol: str = None, cursor: str = None) -> dict:
    """
    Retrieve risk limit information from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/risk-limit` endpoint
    to fetch risk limit parameters for derivative contracts.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str, optional): Specific contract symbol to filter by.
        cursor (str, optional): Pagination cursor for large datasets.

    Returns
    ---
        dict: A dictionary containing risk limit data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains risk limit tiers and maintenance margins.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 status code.
        requests.RequestException: For network or request issues.

    Example
    ---
        >>> try:
        ...     risk_limits = get_risk_limit(category='linear', symbol='BTCUSDT')
        ...     print(f"Risk limit tiers: {len(risk_limits['result']['list'])}")
        ... except requests.RequestException as e:
        ...     print(f"Error: {e}")
    """

    url = BASE_URL + "/v5/market/risk-limit"
    
    params = {
        "category": category,
        "symbol": symbol,
        "cursor": cursor
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_delivery_price(category: str, symbol: str = None, base_coin: str = None, limit: int = None, cursor: str = None) -> dict:
    """
    Retrieve delivery price data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/delivery-price` endpoint
    to fetch settlement prices for expired contracts.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str, optional): Specific contract symbol to filter by.
        base_coin (str, optional): Base coin for filtering.
        limit (int, optional): Number of results to return. Max 200.
        cursor (str, optional): Pagination cursor.

    Returns
    ---
        dict: A dictionary containing delivery prices. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains delivery prices and settlement times.

    Raises
    ---
        requests.HTTPError: For unsuccessful API responses.
        requests.RequestException: For request-related errors.

    Example
    ---
        >>> try:
        ...     delivery = get_delivery_price(category='linear', symbol='BTCUSDT')
        ...     print(f"Delivery price: {delivery['result']['list'][0]['deliveryPrice']}")
        ... except requests.HTTPError as e:
        ...     print(f"API error: {e}")
    """

    url = BASE_URL + "/v5/market/delivery-price"
    
    params = {
        "category": category,
        "symbol": symbol,
        "baseCoin": base_coin,
        "limit": limit,
        "cursor": cursor
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()


def get_long_short_ratio(category: str, symbol: str, period: str, start_time: str = None, end_time: str = None, limit: int = None, cursor: str = None) -> dict: 
    """
    Retrieve long/short ratio data from the Bybit API.

    This function sends a GET request to the Bybit API's `/v5/market/account-ratio` endpoint
    to fetch historical long/short position ratios.

    Parameters
    ---
        category (str): Product category. Valid values: "linear", "inverse".
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        period (str): Data period. Valid values: "5min", "15min", "30min", "1h", "1d".
        start_time (str, optional): Start timestamp in milliseconds.
        end_time (str, optional): End timestamp in milliseconds.
        limit (int, optional): Number of results to return. Max 500.
        cursor (str, optional): Pagination cursor.

    Returns
    ---
        dict: A dictionary containing ratio data. Structure includes:
            - 'retCode' (int): API response code.
            - 'retMsg' (str): API response message.
            - 'result' (dict): Contains long/short ratios with timestamps.

    Raises
    ---
        requests.HTTPError: If the API returns a non-200 status code.
        requests.RequestException: For network or request issues.

    Example
    ---
        >>> try:
        ...     ratio_data = get_long_short_ratio(category='linear', symbol='BTCUSDT', period='1h')
        ...     print(f"Latest ratio: {ratio_data['result']['list'][0]['longShortRatio']}")
        ... except requests.RequestException as e:
        ...     print(f"Error: {e}")
    """
    
    url = BASE_URL + "/v5/market/account-ratio"
    
    params = {
        "category": category,
        "symbol": symbol,
        "period": period,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
        "cursor": cursor
    }
    
    params["sign"] = generate_signature(params, API_SECRET)
    
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response.json()