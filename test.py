# coding: utf-8

class Singleton(object):
    def __new__(cls):
        # 每一次实例化的时候 ，只返回这同一个_instance
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

obj1 = Singleton()
obj2 = Singleton()

obj1.attr1 = 'value'
print obj1.attr1, obj2.attr1
print obj1 is obj2