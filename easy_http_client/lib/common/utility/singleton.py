class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class UseSingleton:
    def __init__(self, singleton_class):
        self.singleton_class = singleton_class
        self._instance = None

    def __get__(self, obj, objtype=None):
        if self._instance is None:
            self._instance = self.singleton_class()
        return self._instance

class ConfigManager(Singleton):
    def __init__(self):
        self.config = {}
    
    def set_config(self, key, value):
        self.config[key] = value
    
    def get_config(self, key):
        return self.config.get(key)

class MyClass:
    config_manager = UseSingleton(ConfigManager)

# Esempio di utilizzo
if __name__ == "__main__":
    # Accesso alla proprietà statica singleton
    MyClass.config_manager.set_config("API_KEY", "12345")
    
    # Creazione di istanze multiple di MyClass
    obj1 = MyClass()
    obj2 = MyClass()
    
    # Verifica che la proprietà sia condivisa tra tutte le istanze e la classe
    print(MyClass.config_manager.get_config("API_KEY"))  # Output: 12345
    print(obj1.config_manager.get_config("API_KEY"))    # Output: 12345
    print(obj2.config_manager.get_config("API_KEY"))    # Output: 12345
    
    # Modifica della configurazione attraverso un'istanza
    obj1.config_manager.set_config("DEBUG", True)
    
    # Verifica che la modifica sia visibile ovunque
    print(MyClass.config_manager.get_config("DEBUG"))   # Output: True
    print(obj2.config_manager.get_config("DEBUG"))      # Output: True
    
    # Verifica che tutte le istanze si riferiscano allo stesso oggetto
    print(MyClass.config_manager is obj1.config_manager is obj2.config_manager)  # Output: True