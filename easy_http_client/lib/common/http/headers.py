from enum import Enum
from typing import Dict

class ContentType(Enum):
    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"
    TEXT = "text/plain"
    HTML = "text/html"
    XML = "application/xml"

class HeadersUtility:
    @staticmethod
    def apply_content_type(headers: Dict[str, str], content_type: ContentType) -> Dict[str, str]:
        """
        Applica il Content-Type specificato agli headers.
        """
        headers["Content-Type"] = content_type.value
        return headers

    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        """
        Restituisce un set di headers di default anonimi.
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "DNT": "1"
        }

    @staticmethod
    def merge_headers(*dicts: Dict[str, str]) -> Dict[str, str]:
        """
        Unisce più dizionari di headers, dando priorità agli ultimi.
        """
        result = {}
        for dictionary in dicts:
            result.update(dictionary)
        return result

# Esempio di utilizzo
if __name__ == "__main__":
    # Ottenere headers di default
    default_headers = HeadersUtility.get_default_headers()
    print("Headers di default:")
    print(default_headers)

    # Applicare un content type
    json_headers = HeadersUtility.apply_content_type(default_headers.copy(), ContentType.JSON)
    print("\nHeaders con Content-Type JSON:")
    print(json_headers)

    # Merge di headers
    custom_headers = {"Authorization": "Bearer TOKEN123", "X-Custom-Header": "Value"}
    merged_headers = HeadersUtility.merge_headers(default_headers, custom_headers)
    print("\nHeaders dopo il merge:")
    print(merged_headers)