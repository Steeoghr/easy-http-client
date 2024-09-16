import threading
from functools import wraps

class Lock:
    def __init__(self):
        self._lock = threading.Lock()

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

# Esempio di utilizzo come context manager
LOCK = Lock()







# Examples

def critical_section():
    with LOCK:
        print("Questa sezione è in esecuzione in mutua esclusione")
        # Operazioni critiche qui

# Esempio di utilizzo come decoratore
@LOCK
def critical_method():
    print("Questo metodo intero è in esecuzione in mutua esclusione")
    # Operazioni critiche qui

# Esempio di utilizzo in un ambiente multi-thread
import time
from concurrent.futures import ThreadPoolExecutor

shared_resource = 0

@LOCK
def increment_resource():
    global shared_resource
    local_value = shared_resource
    time.sleep(0.1)  # Simula un'operazione che richiede tempo
    shared_resource = local_value + 1

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
            executor.submit(increment_resource)

    print(f"Valore finale della risorsa condivisa: {shared_resource}")

if __name__ == "__main__":
    critical_section()
    critical_method()
    main()