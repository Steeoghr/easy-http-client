
from lib.common.http.Client import HttpClient, HttpRequest
from lib.common.utility.singleton import UseSingleton

class HttpRequestsHandler:
    http_client: HttpClient = UseSingleton(HttpClient)
    def handle(request: HttpRequest):
        httpRequest = HttpRequest(request)
        response = HttpRequestsHandler.http_client.request(httpRequest)
        print(httpRequest)
        if response is not None:
            print(f"Response with:\n[{response.status_code}]\n{response.text}")