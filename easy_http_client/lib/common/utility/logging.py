from lib.common.utility.conditions import set_if

def log_if_not_null(obj, message):
    output = set_if(obj is None, message)
    if output is None:
        return
    
    print(message)