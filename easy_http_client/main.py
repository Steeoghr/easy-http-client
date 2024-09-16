import os
import json
from lib.common.http.request import HttpRequest
from lib.common.http.Client import HttpClient, HttpRequestType
from lib.common.utility.throw import raise_if_null_or_empty
from lib.common.utility.conditions import set_if

JSON_ENV_KEY = 'REQUESTS'

json_requests = os.environ.get(JSON_ENV_KEY)

if json_requests is None:
    exit()

requests_to_execute = {}

try:
    requests_to_execute = json.loads(json_requests)
except Exception as e:
    error = f"An error occurred parsing requests: {e}"
    raise ValueError(e)

http_client = HttpClient()

for request in requests_to_execute:
    url = request["url"]
    type = request["type"]

    raise_if_null_or_empty(url)
    type = set_if(type is None, HttpRequestType.GET)

    httpRequest = HttpRequest(url, type, request["params"], request["body"], request["headers"], request["proxies"])
    response = http_client.request(httpRequest)
    print(httpRequest)
    if response is not None:
        print(f"Response with:\n[{response.status_code}]\n{response.text}")