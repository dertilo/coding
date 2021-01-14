from functools import wraps


class Clazz:
    @staticmethod
    def fun(x):
        return x


def fun(x):
    return x


def some_decorator(f):
    @wraps(f)
    def fun(*args):
        return f(*args)

    return fun


class DecoratedStaticMethod:
    @staticmethod
    @some_decorator
    def fun(x):
        return x


class StaticMethod:
    @staticmethod
    def fun(x):
        return x + "what"


class ClazzWithClassmethod:
    @classmethod
    def fun(cls, x):
        return x


class ClazzDecoratedClassmethod:
    @classmethod
    @some_decorator
    def fun(cls, x):
        return x
