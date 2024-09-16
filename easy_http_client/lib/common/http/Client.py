import requests
import enum
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from lib.common.utility.logging import log_if_not_null
from lib.common.utility.throw import raise_if_null_or_empty
from lib.common.utility.conditions import set_if
from lib.common.utility.nameof import AutoNameProperties
from lib.common.utility.singleton import Singleton

class HttpRequestType(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    
    def to_string(value):
        if (value == HttpRequestType.GET):
            return "GET"
        if (value == HttpRequestType.POST):
            return "POST"
        if (value == HttpRequestType.PUT):
            return "PUT"
        if (value == HttpRequestType.DELETE):
            return "DELETE"

class HttpRequest(AutoNameProperties):
    url: str
    type: HttpRequestType
    params: dict
    body: dict
    headers: dict
    proxies: dict

    def __init__(self, request: dict):
        self.url = request[HttpRequest.url__name]
        raise_if_null_or_empty(self.url)

        self.type = request[HttpRequest.type__name]
        self.type = set_if(self.type is None, HttpRequestType.GET)

        self.params = request[HttpRequest.params__name]
        self.body = request[HttpRequest.body__name]
        self.headers = request[HttpRequest.headers__name]
        self.proxies = request[HttpRequest.proxies__name]

    def __str__(self):
        print(f"[{self.type}] {self.url}")
        log_if_not_null(self.params, f"Params:\n{self.params}")
        log_if_not_null(self.body, f"Body:\n{self.body}")
        log_if_not_null(self.headers, f"Headers:\n{self.headers}")
        log_if_not_null(self.proxies, f"Proxies:\n{self.proxies}")

class HttpClient(Singleton):
    def __init__(self, baseUrl: str = ""):
        self.baseUrl = baseUrl
        pass

    def request(self, request: HttpRequest):
        return self._request(request.url, request.type, request.params, request.body, request.headers, request.proxies)

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=1, max=3),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
        reraise=True
    )
    def _request(self, url: str, request_type: HttpRequestType | str = HttpRequestType.GET, params = None, body = None, headers = None, proxies = None) -> requests.Response:
        try:
            url = self.baseUrl + url

            return requests.request(str(request_type), url, params=params, body=body, headers=headers, proxies=proxies)
        except requests.exceptions.RequestException as e:
            print(f"All retry attempts failed. Final error: {e}")
            return None
        
    def is_request_type(self, input_request_type: HttpRequestType | str, request_type: HttpRequestType):
        return input_request_type == request_type or input_request_type == HttpRequestType.to_string(request_type)
    