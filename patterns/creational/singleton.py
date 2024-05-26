import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not isinstance(cls._instance, cls):
                cls._instance = super().__new__(cls)
                
        return cls._instance
