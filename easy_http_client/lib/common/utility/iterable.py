from typing import Callable, Iterable, List, TypeVar, Union, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from itertools import groupby
from lib.common.utility.generic import T

R = TypeVar('R')

def map(iterable: Iterable[T], 
                  func: Callable[[T], R], 
                  chunk_size: int = 1000,
                  max_workers: int = None,
                  use_threading: bool = False,
                  handle_exceptions: bool = False) -> List[R]:
    """
    Una funzione map ottimizzata che applica una funzione a ogni elemento di un iterable.

    Args:
    iterable (Iterable[T]): L'iterable di input.
    func (Callable[[T], R]): La funzione da applicare a ogni elemento.
    chunk_size (int): Dimensione dei chunk per l'elaborazione in batch.
    max_workers (int): Numero massimo di worker per l'elaborazione parallela.
    use_threading (bool): Se True, usa ThreadPoolExecutor per l'elaborazione parallela.
    handle_exceptions (bool): Se True, gestisce le eccezioni senza interrompere l'elaborazione.

    Returns:
    List[R]: Una lista contenente i risultati dell'applicazione della funzione.

    Raises:
    Exception: Rilancia qualsiasi eccezione se handle_exceptions è False.
    """
    def process_chunk(chunk: List[T]) -> List[R]:
        if handle_exceptions:
            return [func(item) if (result := safe_apply(func, item))[0] else result[1] for item in chunk]
        return [func(item) for item in chunk]

    def safe_apply(f: Callable[[T], R], x: T) -> Union[Tuple[bool, R], Tuple[bool, Exception]]:
        try:
            return True, f(x)
        except Exception as e:
            return False, e

    # Ottimizzazione per input di piccole dimensioni
    if not use_threading or (hasattr(iterable, '__len__') and len(iterable) <= chunk_size):
        return process_chunk(list(iterable))

    # Elaborazione in parallelo per input di grandi dimensioni
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for chunk in iter(lambda: list(itertools.islice(iterable, chunk_size)), []):
            futures.append(executor.submit(process_chunk, chunk))
        
        for future in as_completed(futures):
            results.extend(future.result())

    return results





def group_by(items: List[T], key_func: Callable[[T], Any]) -> Dict[Any, List[T]]:
    """
    Perform an optimized group by operation on a list of items.

    :param items: List of items to group
    :param key_func: Lambda function to extract the grouping key from each item
    :return: Dictionary with keys as group identifiers and values as lists of items in each group
    """
    # Sort the items based on the key function
    sorted_items = sorted(items, key=key_func)
    
    # Use itertools.groupby for efficient grouping
    return {k: list(g) for k, g in groupby(sorted_items, key=key_func)}



def where(items: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """
    Perform an optimized 'where' operation on a list of items.

    :param items: List of items to filter
    :param predicate: Lambda function that returns True for items to keep
    :return: List of items that satisfy the predicate
    """
    return list(filter(predicate, items))


OrderKey = Union[Callable[[T], Any], Tuple[Callable[[T], Any], bool]]

def order_by(items: List[T], *key_funcs: OrderKey) -> List[T]:
    """
    Perform an optimized 'order by' operation on a list of items.

    :param items: List of items to sort
    :param key_funcs: One or more lambda functions to extract sorting keys.
                      Each key can be a simple lambda or a tuple (lambda, reverse)
                      where reverse is a boolean indicating descending order.
    :return: Sorted list of items
    """
    if not key_funcs:
        return sorted(items)

    def create_key_func(key_funcs):
        def key_func(item):
            return tuple(
                (key(item) if not isinstance(key, tuple) else
                 (key[0](item) if not key[1] else _invert(key[0](item))))
                for key in key_funcs
            )
        return key_func

    def _invert(obj):
        if isinstance(obj, (int, float)):
            return -obj
        if isinstance(obj, str):
            return ''.join(chr(255 - ord(c)) for c in obj)
        raise TypeError(f"Cannot invert type {type(obj)}")

    return sorted(items, key=create_key_func(key_funcs))