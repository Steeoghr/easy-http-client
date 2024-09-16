import concurrent.futures
from typing import Iterable, Callable, Any
import time

def parallel_foreach(iterable: Iterable[Any], 
                     action: Callable[[Any], Any], 
                     max_workers: int = None, 
                     timeout: float = None,
                     show_progress: bool = False) -> list:
    """
    Esegue un'azione in parallelo su ogni elemento di un iterable.

    :param iterable: Una collezione di elementi su cui eseguire l'azione.
    :param action: La funzione da eseguire su ogni elemento.
    :param max_workers: Il numero massimo di thread da utilizzare. Se None, usa il default di ThreadPoolExecutor.
    :param timeout: Il tempo massimo (in secondi) da attendere per il completamento di tutti i task.
    :param show_progress: Se True, mostra una barra di avanzamento.
    :return: Una lista contenente i risultati dell'azione su ogni elemento.
    """
    results = []
    total_items = len(iterable) if hasattr(iterable, '__len__') else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(action, item): item for item in iterable}
        
        if show_progress and total_items:
            print(f"0/{total_items} completati", end='\r')

        completed = 0
        for future in concurrent.futures.as_completed(future_to_item):
            try:
                result = future.result(timeout=timeout)
                results.append(result)
                completed += 1
                if show_progress and total_items:
                    print(f"{completed}/{total_items} completati", end='\r')
            except concurrent.futures.TimeoutError:
                print(f"L'operazione su {future_to_item[future]} è andata in timeout")
            except Exception as exc:
                print(f"L'operazione su {future_to_item[future]} ha generato un'eccezione: {exc}")

    if show_progress and total_items:
        print(f"{total_items}/{total_items} completati")

    return results

# Esempio di utilizzo
if __name__ == "__main__":
    def process_item(item):
        time.sleep(1)  # Simula un'operazione che richiede tempo
        return item * 2

    items = list(range(10))
    
    results = parallel_foreach(items, process_item, max_workers=3, show_progress=True)
    print("Risultati:", results)