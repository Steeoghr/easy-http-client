import requests
import enum
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from lib.common.http.request import HttpRequest

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


class HttpClient:
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
    def _request(self, url: str, request_type: HttpRequestType, params = None, body = None, headers = None, proxies = None) -> requests.Response:
        try:
            url = self.baseUrl + url
            if self.is_request_type(request_type, HttpRequestType.GET):
                response = requests.get(url, params=params, headers=headers, proxies=proxies)
            elif self.is_request_type(request_type, HttpRequestType.POST):
                response = requests.post(url, json=body, params=params, headers=headers, proxies=proxies)
            elif self.is_request_type(request_type, HttpRequestType.PUT):
                response = requests.put(url, json=body, params=params, headers=headers, proxies=proxies)
            elif self.is_request_type(request_type, HttpRequestType.DELETE):
                response = requests.delete(url, params=params, headers=headers, proxies=proxies)
            else:
                return None

            return response
        except requests.exceptions.RequestException as e:
            print(f"All retry attempts failed. Final error: {e}")
            return None
        
    def is_request_type(self, input_request_type: HttpRequestType | str, request_type: HttpRequestType):
        return input_request_type == request_type or input_request_type == HttpRequestType.to_string(request_type)
    