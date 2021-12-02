import base64
import datetime
import hashlib
import hmac
import json
import time

import requests

import keys
import urls


def get_all_trades_for_account(url=urls.MY_TRADES_URL, api_key=keys.gemini_api_key,
                               api_secret=keys.gemini_api_secret):
    account_info = get_account_info()

    created_date = account_info['account']["created"]

    all_trades = []

    trades_from_query = get_500_trades_since_timestamp(created_date, url=url, api_key=api_key, api_secret=api_secret)
    all_trades += trades_from_query

    # reasoning: 500 trades is a the max per call
    # so if call has 500 trades,
    # there is a high chance there is more trades to query
    while len(trades_from_query) == 500:
        latest_timestamp = all_trades[0]['timestampms']
        trades_from_query = get_500_trades_since_timestamp(latest_timestamp + 1, url, api_key, api_secret)
        all_trades = trades_from_query + all_trades

    return all_trades


def get_account_info(url=urls.MY_ACCOUNT_URL, api_key=keys.gemini_api_key,
                     api_secret=keys.gemini_api_secret):
    # create payload
    payload_nonce = create_nonce();
    payload = {"request": "/v1/account", "nonce": payload_nonce}
    # encode payload
    encoded_payload, signature = encode_payload_and_sign(payload, api_secret)

    gemini_header = create_gemini_header(api_key, encoded_payload, signature)

    response = requests.post(url, headers=gemini_header)

    account = response.json()

    return account


def get_latest_500_trades_from_gemini(url=urls.MY_TRADES_URL, api_key=keys.gemini_api_key,
                                      api_secret=keys.gemini_api_secret):
    # create payload
    payload_nonce = create_nonce();
    payload = {"request": "/v1/mytrades", "nonce": payload_nonce, "limit_trades": 500}  # 500 is max

    # encode payload
    encoded_payload, signature = encode_payload_and_sign(payload, api_secret)

    gemini_header = create_gemini_header(api_key, encoded_payload, signature)

    response = requests.post(url, headers=gemini_header)

    trades = response.json()

    return trades


def get_500_trades_since_timestamp(timestamp, url=urls.MY_TRADES_URL, api_key=keys.gemini_api_key,
                                   api_secret=keys.gemini_api_secret):
    # create payload
    payload_nonce = create_nonce();
    payload = {"request": "/v1/mytrades", "nonce": payload_nonce, "limit_trades": 500,
               "timestamp": timestamp}  # 500 is max

    # encode payload
    encoded_payload, signature = encode_payload_and_sign(payload, api_secret)

    gemini_header = create_gemini_header(api_key, encoded_payload, signature)

    response = requests.post(url, headers=gemini_header)

    trades = response.json()

    return trades


def create_nonce():
    t = datetime.datetime.now()
    return str(int(time.mktime(t.timetuple()) * 1000))


def encode_payload_and_sign(payload, api_secret_key):
    encoded_secret = api_secret_key.encode()
    encoded_payload = json.dumps(payload).encode()
    payload_as_b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(encoded_secret, payload_as_b64, hashlib.sha384).hexdigest()
    return payload_as_b64, signature


def create_gemini_header(api_key, encoded_payload, signature):
    request_headers = {
        'Content-Type': "text/plain",
        'Content-Length': "0",
        'X-GEMINI-APIKEY': api_key,
        'X-GEMINI-PAYLOAD': encoded_payload,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
    }

    return request_headers
