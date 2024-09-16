from typing import Any
import inspect
import sys

def raise_member(member: Any):
    # Ottieni informazioni sul frame chiamante
    frame = sys._getframe(1)
    
    # Ottieni il nome della variabile se non fornito
    member_name = [name for name, value in frame.f_locals.items() if value is member][0]
    
    # Ottieni informazioni sulla riga di codice
    file_name = frame.f_code.co_filename
    line_number = frame.f_lineno
    
    # Ottieni il contesto della chiamata (le righe di codice intorno alla chiamata)
    context_lines = inspect.getframeinfo(frame).code_context
    
    # Costruisci il messaggio di errore
    error_message = f"ValueError: '{member_name}' è None\n"
    error_message += f"File: {file_name}, Linea: {line_number}\n"
    if context_lines:
        error_message += "Contesto:\n"
        error_message += "".join(context_lines)
    
    # Ottieni informazioni sullo stack
    stack_info = inspect.stack()[1:]
    if stack_info:
        error_message += "\nStack Trace:\n"
        for frame_info in stack_info:
            error_message += f"  File '{frame_info.filename}', linea {frame_info.lineno}, in {frame_info.function}\n"
            if frame_info.code_context:
                error_message += f"    {frame_info.code_context[0].strip()}\n"
    
    raise ValueError(error_message)

def raise_if_null(member: Any):
    if member is None:
        raise_member(member)

def raise_if_null_or_empty(member: str):
    if member is None or member == "":
        raise_member(member)