from basic.exceptions import ExcelNotLoadError


class Decorator:

    @staticmethod
    def singleton(cls):
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return get_instance

    @staticmethod
    def check_load(func):
        def wrapper(self, *args, **kwargs):
            if not self._load:
                raise ExcelNotLoadError()
            return func(self, *args, **kwargs)

        return wrapper
