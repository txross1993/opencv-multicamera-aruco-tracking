class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class SingletonImpl(metaclass=Singleton): pass