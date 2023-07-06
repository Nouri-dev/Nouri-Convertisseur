import functools


class CachedProperty:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, '_cached_properties'):
            instance._cached_properties = {}
        if self.func.__name__ not in instance._cached_properties:
            instance._cached_properties[self.func.__name__] = self.func(instance)
        return instance._cached_properties[self.func.__name__]

    def __set_name__(self, owner, name):
        self.name = name

    def __call__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
        return self