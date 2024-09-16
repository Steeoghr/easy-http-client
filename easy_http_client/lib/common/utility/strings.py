def join_strings(*args, separator=''):
    """
    Unisce una serie di stringhe utilizzando un separatore opzionale.
    Accetta sia un array di stringhe che argomenti separati.

    Args:
    *args: Un array di stringhe o stringhe separate come argomenti.
    separator (str, optional): Il separatore da usare tra le stringhe. Default è una stringa vuota.

    Returns:
    str: La stringa risultante dall'unione delle stringhe di input.

    Note:
    - Le stringhe vuote e None vengono ignorati.
    - Se non vengono fornite stringhe valide, viene restituita una stringa vuota.
    """
    # Gestisce sia il caso di un singolo array che argomenti multipli
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        strings = args[0]
    else:
        strings = args

    # Filtra le stringhe vuote e None
    valid_strings = [str(s) for s in strings if s is not None and str(s).strip()]
    
    # Unisce le stringhe valide con il separatore
    return separator.join(valid_strings)





# Esempi di utilizzo
if __name__ == "__main__":
    # Esempio con array di stringhe
    array_input = ["Hello", "World", "Python"]
    print(join_strings(array_input, separator=" "))  # Output: 'Hello World Python'
    print(join_strings("Hello", "World"))  # Output: HelloWorld
    print(join_strings("Hello", "World", separator=" "))  # Output: Hello World
    print(join_strings("A", "B", "C", separator=", "))  # Output: A, B, C
    print(join_strings("One", "", "Two", "Three", separator="-"))  # Output: One-Two-Three
    print(join_strings("Start", None, "End", separator=" "))  # Output: Start End
    print(join_strings())  # Output: (stringa vuota)
    print(join_strings("Single"))  # Output: Single
    print(join_strings("  Leading", "Trailing  ", "  Both  ", separator="|"))  # Output: Leading|Trailing|Both