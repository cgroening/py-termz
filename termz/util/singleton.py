class Singleton(type):
    """
    Metaclass for the singleton pattern.

    Ensures that a class has only one instance and provides global access to it.

    Attributes
    ----------
    _instance : object or None
        The single instance of the class, or None if not yet created.

    Examples
    --------
    >>> class SomeClass(metaclass=Singleton):
    ...     def __init__(self):
    ...         pass
    """

    _instance = None

    def __call__(cls, *args, **kwargs):  # pyright: ignore[reportAny, reportUnknownParameterType, reportMissingParameterType]
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)  # pyright: ignore[reportAny]
        return cls._instance  # pyright: ignore[reportAny]

    @property
    def instance(self):
        return self._instance
