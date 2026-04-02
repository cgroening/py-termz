"""
termz.util.singleton
====================

Provides a metaclass implementation of the Singleton design pattern.

This module defines a `Singleton` metaclass, which ensures that a class has only
one instance throughout the lifetime of the application.

Usage example:

```
class SomeClass(metaclass=Singleton):
    def __init__(self):
        ...
```

Once defined with this metaclass, all instantiations of `SomeClass` will return
the same object.

Features:

- Enforces a single instance per class.
- Accessible instance via the `instance` property.

"""

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

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

    @property
    def instance(self):
        return self._instance
