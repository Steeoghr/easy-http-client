class NameProperty:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return self.name

class AutoNameProperties:
    @classmethod
    def __init_subclass__(cls):
        for name, value in cls.__annotations__.items():
            if not name.startswith('__'):
                setattr(cls, f"{name.upper()}_NAME", NameProperty(name))
                setattr(cls, f"{name}__name", NameProperty(name))

    @classmethod
    def get_property_names(cls):
        return {name: value.name for name, value in cls.__dict__.items() if isinstance(value, NameProperty)}

# Esempio di utilizzo
class HttpRequest(AutoNameProperties):
    url: str
    params: dict
    headers: dict
    
    def __init__(self, url: str, params: dict, headers: dict):
        self.url = url
        self.params = params
        self.headers = headers

# Test (da eseguire solo se il file viene eseguito direttamente)
if __name__ == "__main__":
    print(HttpRequest.URL_NAME)        # Dovrebbe stampare: url
    print(HttpRequest.PARAMS_NAME)     # Dovrebbe stampare: params
    print(HttpRequest.HEADERS_NAME)    # Dovrebbe stampare: headers

    print(HttpRequest.url__name)       # Dovrebbe stampare: url
    print(HttpRequest.params__name)    # Dovrebbe stampare: params
    print(HttpRequest.headers__name)   # Dovrebbe stampare: headers

    request = HttpRequest("https://example.com", {"key": "value"}, {"Content-Type": "application/json"})
    print(request.url)                 # Dovrebbe stampare: https://example.com
    print(request.params)              # Dovrebbe stampare: {'key': 'value'}
    print(request.headers)             # Dovrebbe stampare: {'Content-Type': 'application/json'}

    # Stampare tutti i nomi delle proprietà
    print(HttpRequest.get_property_names())

    # Verifica che le costanti siano accessibili anche dalle istanze
    print(request.URL_NAME)            # Dovrebbe stampare: url
    print(request.url__name)           # Dovrebbe stampare: url