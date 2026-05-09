class OntologyParser:
    registry = {}

    @classmethod
    def register(cls, name):
        def wrapper(subclass):
            cls.registry[name] = subclass
            return subclass
        return wrapper
    
    @classmethod
    def parse(cls, name):
        if name not in cls.registry:
            raise ValueError(f"{name} not registered")
        return cls.registry[name]()