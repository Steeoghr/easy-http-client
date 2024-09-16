import os
import json
import enum
from typing import List
from lib.common.utility.throw import raise_error
from app.http import HttpRequestsHandler

JSON_ENV_KEY = 'REQUESTS'

def parse_requests():
    json_requests = os.environ.get(JSON_ENV_KEY)

    try:
        if json_requests is None:
            raise_error("Unavailable requests")
        
        return json.loads(json_requests)
    except Exception as e:
        print(f"An error occurred parsing requests: {e}")
        return

def elab_requests():
    requests: List[dict] = parse_requests()
    for request in requests:
        HttpRequestsHandler.handle(request)

if __name__ == "__main__":
    elab_requests()