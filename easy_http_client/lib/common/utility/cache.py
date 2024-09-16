

class Cache:
    _data = {}

    def set(self, key, value):
        self._data[key] = value
    
    def get(self, key):
        if key in self._data:
            return self._data[key]
        return None