import requests
import concurrent.futures
from typing import List, Dict

def fetch_proxy_list() -> List[Dict[str, str]]:
    """Fetch a list of proxies from a public API."""
    url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [{"ip": proxy["ip"], "port": proxy["port"], "protocol": proxy['protocols'][0]} for proxy in data["data"]]
    except requests.RequestException as e:
        print(f"Errore nel recupero della lista dei proxy: {e}")
        return []

def validate_proxy(proxy: Dict[str, str]) -> Dict[str, str]:
    """Validate a single proxy by making a test request."""
    proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
    # print(f"Validate proxy {proxy_url}")
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
        response.raise_for_status()
        # print("Proxy valid")
        return {"proxy": proxy_url, "status": "valid"}
    except requests.RequestException:
        # print("Proxy invalid")
        return {"proxy": proxy_url, "status": "invalid"}

def get_valid_proxies() -> List[str]:
    """Fetch and validate a list of proxies."""
    proxy_list = fetch_proxy_list()
    valid_proxies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(validate_proxy, proxy): proxy for proxy in proxy_list}
        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result["status"] == "valid":
                valid_proxies.append(result["proxy"])

    return valid_proxies

if __name__ == "__main__":
    valid_proxies = get_valid_proxies()
    print(f"Proxy validi trovati: {len(valid_proxies)}")
    for proxy in valid_proxies:
        print(proxy)