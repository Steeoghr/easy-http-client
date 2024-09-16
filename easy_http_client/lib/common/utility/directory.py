import os

def join_paths(*dirs):
    """
    Unisce un numero variabile di percorsi.
    
    Args:
    *dirs: Un numero variabile di stringhe rappresentanti i percorsi da unire.
    
    Returns:
    str: Il percorso unito.
    
    Raises:
    ValueError: Se non viene fornito alcun argomento.
    """
    if not dirs:
        raise ValueError("Almeno un percorso deve essere fornito")
    return os.path.join(*dirs)

def get_script_dir(file):
    return os.path.dirname(os.path.abspath(file))