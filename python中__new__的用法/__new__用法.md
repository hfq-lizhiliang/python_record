#__init__方法

__init__方法通常用来初始化一个类实例：
```
class Person(object):

    """person"""

    def __init__(self, name, age):

        self.name = name

        self.age = age

    def __str___(self):

        return '<Person: %s(%s)>' % (self.name, self.age)

if __name__ == '__main__':

    huahua = Person('huahua', 22)

    print huahua

<__main__.Person object at 0x03196E10>

```
这里是__init__最常用的方法，实例化对象，但是并不是第一个被调用的，最先被调用的是__new__方法。

# __new__方法
__new__方法接受的参数和__init__一样，但是__init__是在类实例创建之后调用的，而__new__方法则是创建这个类实例的方法。通俗的说，__new__创建一个实例对象，返回给__init__去初始化，—__init__（self）中的self就是__new__创建返回的实例对象。因此，__new__方法必须要有返回值，__init__不需要返回值。

```
class Person(object):
    """person"""
    def __new__(cls, name, age):
        print '__new__ called'
        return super(Person, cls).__new__(cls, name, age)
    def __init__(self, name, age):
        print '__init__ called'
        self.name = name
        self.age = age
    def __str__(self):
        return '<Person: %s(%s)>' % (self.name, self.age)

if __name__ == '__main__':
    huahua = Person('huahua', 12)
    print huahua

__new__ called
__init__ called
<Person: huahua(12)>
```

__init__ 和 __new__ 最主要的区别在于：
1.__init__ 通常用于初始化一个新实例，控制这个初始化的过程，比如添加一些属性， 做一些额外的操作，发生在类实例被创建完以后。它是实例级别的方法。
2.__new__ 通常用于控制生成一个新实例的过程。它是类级别的方法。


三 __new__的作用

依照Python官方文档的说法，__new__方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。还有就是实现`自定义的metaclass`。

假如我们需要一个永远都是正数的正数类型，通过继承nt，我们可能会这样处理：
```
class PositiveInteger(int):
    def __init__(self,value):
        super(PositiveInteger, self).__init__(self, abs(value))

i = PositiveInteger(-3)
print i

-3

```

运行之后，我们发现结果并不是我们想要的那种，依旧是-3.这是因为对于int这种不可变的对象，我们只有重载塔的__new__方法才能起到自定义的作用。

```
class PositiveInteger(int):
    def __new__(cls,value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))

i = PositiveInteger(-3)
print i

3
```
上面通过重载__new__方法，我们实现了需要的功能

#四 用__new__来实现单例

利用__new__方法，来实现设计模式中的单例模式(singleton)。因为类每一次实例化后产生的过程都是通过__new__来控制的，所以通过重载__new__方法，我们 可以实现单例 。

```
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

value value
True
```
