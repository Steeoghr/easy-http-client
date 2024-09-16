import requests
from lib.common.http.Client import HttpRequestType
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=1, max=3),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
    reraise=True
)
def make_proxy_request(url, headers, proxies):
    return requests.get(url, headers=headers, proxies=proxies, timeout=(5, 360))

def handle_proxy_request(url, proxies, headers = None):
    try:
        print(f"Starting proxy request on {url}")
        response = make_proxy_request(url, headers, proxies)
        print(f"Get response status {response.status_code} from {url}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"All retry attempts failed. Final error: {e}")
        return None

def handle_request(url, headers = None):
    print(f"Start request on {url}")
    # Fai una richiesta GET alla pagina web
    response = requests.get(url, headers=headers)
    print(f"Get response status {response.status_code} from {url}")
    return response

def get_html_response(response: requests.Response | None):
    print("Parse html response")
    scrap = response.text
    if scrap is None:
        return None
    html = BeautifulSoup(scrap, "html.parser")
    return html

def handle_html_request(url, headers):
    response = handle_request(url, headers)
    # Verifica se la richiesta è andata a buon fine
    if response.status_code == 200:
        return get_html_response(response)
    else:
        raise ValueError(f"An error occurred on request to {url}: {response.status_code}")
        # print(f"Errore nella richiesta: {response.status_code}")
        # return None