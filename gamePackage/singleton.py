# coding: utf-8


class Singleton(object):
    __instance = None

    def __call__(cls, *args, **kwargs):
        print(cls.__instance)
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]
