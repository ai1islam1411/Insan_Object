## Insan Form


class cached_class_property:
    """Descriptor decorator implementing a class-level, read-only property,
    which caches its results on the class(es) on which it operates.

    Inheritance is supported, insofar as the descriptor is never hidden by its cache;
    rather, it stores values under its access name with added underscores. For example,
    when wrapping getters named "choices", "choices_" or "_choices", each class's result
    is stored on the class at "_choices_"; decoration of a getter named "_choices_"
    would raise an exception."""

    class AliasConflict(ValueError):
        pass

    def __init__(self, func):
        self.__func__ = func
        self.__cache_name__ = "_{}_".format(func.__name__.strip("_"))
        if self.__cache_name__ == func.__name__:
            raise self.AliasConflict(self.__cache_name__)

    def __get__(self, instance, cls=None):
        if cls is None:
            cls = type(instance)

        try:
            return vars(cls)[self.__cache_name__]
        except KeyError:
            result = self.__func__(cls)
            setattr(cls, self.__cache_name__, result)
            return result
