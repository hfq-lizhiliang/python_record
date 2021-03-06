
**原文**  [深刻理解Python中的元类(metaclass)](http://blog.jobbole.com/21351/)
#type 动态的创建类

type有一种完全不同的能力，它也能动态的创建类。type可以接受一个类的描述作为参数，然后返回一个类。

常见的创建类的方法：
```
class MyShinyClass(object):
	pass

```

type也可以这样工作：
`type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)`

```
MyShinyClass = type('MyShinyClass', (), {}) #返回一个类对象
```

type可以接受一个字典来为类定义属性
```
class Foo(object):
	bar = True
```
可以翻译为：
Foo = type('Foo', (), {'bar':True})

当然，你也可以想这个类继承：
```
class FooChild(Foo):
	pass
```

type可以写成这样：
```
FooChild = type('FooChild', (Foo,), {})
```

你希望为你的类增加方法啊，只需要定义一个有着恰当签名的函数并将其作为属性赋值就可以了。


	def echo_bar(self):
		print self.bar
	
	FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
	
	hasattr(Foo, 'echo_bar')
	False
	
	hasattr(FooChild, 'echo_bar')
	True


你可以看到，在Python中，类也是对象，你可以动态的创建类。这就是当你使用关键字class时Python在幕后做的事情，而这就是通过元类来实现的。


# 什么是元类
元类就是用来创建类的"东西"。元类就是用来创建类的类。

python中的所有东西都是对象，包含整数、字符串、函数以及类等。它们全部都是对象，而且它们都是从一个类创建而来。

	age = 35

	age.__class__

	int

---

	name = 'hehe'

	name.__class__

	str

---

	def foo():
	    pass

	foo.__class__

	function

---

	class Bar(object):

   		pass

	b = Bar()

	b.__class__

	__main__.Bar


对于任何一个__class__的__class__属性又是什么？
  
	age.__class__.__class__
	type

	foo.__class__.__class__
	type

	b.__class__.__class__
	type


因此，元类就是python的类工厂。

# __metaclass__属性
你可以在写一个类的时候为期添加__metaclass__属性
```
class Foo(object):
	__metaclass__ = something
```

如果这样做，Python就会用元类来创建类Foo。你首先写下class Foo(object)，但是类对象Foo还没有在内存中创建。Python会在类的定义中寻找__metaclass__属性，如果找到了，python就会用它来创建类Foo.如果没有找到，就会用内奸的type来创建这个类。

```
class Foo(Bar):
	pass
```

参考上线的代码，Python做了如下操作：
>Foo中有__metaclass__这个属性吗？如果是，python会在内存中通过__metaclass__创建一个名字为Foo的类对象。如果Python中没有找到__metaclass__，他会继续在Bar(父类)中寻找__metaclass__属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到__metaclass__，它就会在模块层次中去寻找__metaclass__，并尝试做同样的操作。如果还是找不到__metaclass__,Python就会用内置的type来创建这个类对象。


>现在的问题就是，你可以在__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。


# 自定义元类

元类的主要目的就是为了当创建类时能够自动地改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类。所以，我们这里就先以一个简单的函数作为例子开始。

	# 元类会自动将你通常传给‘type’的参数作为自己的参数传入

	def upper_attr(future_class_name, future_class_parents, future_class_attr):
	    '''
		返回一个类对象，将属性都转为大写形式
		future_class_name       类名
		future_class_parents	父类名
		future_class_attr		属性（dict）
		'''
	
	    print 'future_class_name:%s, future_class_parents:%s, future_class_attr:%s' % (future_class_name, future_class_parents, future_class_attr)
	    #  选择所有不以'__'开头的属性
	    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
	
	    # 将它们转为大写形式
	    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
	
	    # 通过'type'来做类对象的创建
	    return type(future_class_name, future_class_parents, uppercase_attr)
	
	
	__metaclass__ = upper_attr  # 这会作用到这个模块中的所有类
	
	
	class Foo(object):
	    # 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
	    bar = 'bip'
	
	
	print hasattr(Foo, 'bar')
	f = Foo()
	print f.bar

	#输出：
	True
	bip


## 现在用一个真正的clss来当做元类

	```
	# 请记住，'type'实际上是一个类，就像'str'和'int'一样
	# 所以，你可以从type继承
	class UpperAttrMetaClass(type):
	    # __new__ 是在__init__之前被调用的特殊方法
	    # __new__是用来创建对象并返回之的方法
	    # 而__init__只是用来将传入的参数初始化给对象
	    # 你很少用到__new__，除非你希望能够控制对象的创建
	    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
	    # 如果你希望的话，你也可以在__init__中做些事情
	    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
	    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
	        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
	        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
	        return type(future_class_name, future_class_parents, uppercase_attr)
	```

但是，这种方式其实不是OOP。我们直接调用了type，而且我们没有改写父类的__new__方法。现在让我们这样去处理:

	class UpperAttrMetaclass(type):
	    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
	        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
	        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
	 
	        # 复用type.__new__方法
	        # 这就是基本的OOP编程，没什么魔法
	        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)

你可能已经注意到了有个额外的参数upperattr_metaclass，这并没有什么特别的。类方法的第一个参数总是表示当前的实例，就像在普通的类方法中的self参数一样。当然了，为了清晰起见，这里的名字我起的比较长。但是就像self一样，所有的参数都有它们的传统名称。因此，在真实的产品代码中一个元类应该是像这样的：

	class UpperAttrMetaclass(type):
	    def __new__(cls, name, bases, dct):
	        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
	        uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
	        return type.__new__(cls, name, bases, uppercase_attr)

如果使用super方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从type继承）

	class UpperAttrMetaclass(type):
	    def __new__(cls, name, bases, dct):
	        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
	        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
	        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

就是这样，除此之外，关于元类真的没有别的可说的了。使用到元类的代码比较复杂，这背后的原因倒并不是因为元类本身，而是因为你通常会使用元类去做一些晦涩的事情，依赖于自省，控制继承等等。确实，用元类来搞些“黑暗魔法”是特别有用的，因而会搞出些复杂的东西来。但就元类本身而言，它们其实是很简单的：

1)   拦截类的创建

2)   修改类

3)   返回修改之后的类


# 为什么要用metaclass类而不是函数？
由于__metaclass__可以接受任何可调用的对象，那为何还要使用类呢，因为很显然使用类会更加复杂啊？这里有好几个原因：

1）  意图会更加清晰。当你读到UpperAttrMetaclass(type)时，你知道接下来要发生什么。

2） 你可以使用OOP编程。元类可以从元类中继承而来，改写父类的方法。元类甚至还可以使用元类。

3）  你可以把代码组织的更好。当你使用元类的时候肯定不会是像我上面举的这种简单场景，通常都是针对比较复杂的问题。将多个方法归总到一个类中会很有帮助，也会使得代码更容易阅读。

4） 你可以使用__new__, __init__以及__call__这样的特殊方法。它们能帮你处理不同的任务。就算通常你可以把所有的东西都在__new__里处理掉，有些人还是觉得用__init__更舒服些。

5） 哇哦，这东西的名字是metaclass，肯定非善类，我要小心！

#究竟为什么要使用元类？

现在回到我们的大主题上来，究竟是为什么你会去使用这样一种容易出错且晦涩的特性？好吧，一般来说，你根本就用不上它：
>“元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。”  —— Python界的领袖 Tim Peters

元类的主要用途是创建API。一个典型的例子是Django ORM。它允许你像这样定义：
	class Person(models.Model):
	    name = models.CharField(max_length=30)
	    age = models.IntegerField()

但是如果你像这样做的话：
	guy  = Person(name='bob', age='35')
	print guy.age

这并不会返回一个IntegerField对象，而是会返回一个int，甚至可以直接从数据库中取出数据。这是有可能的，因为models.Model定义了__metaclass__， 并且使用了一些魔法能够将你刚刚定义的简单的Person类转变成对数据库的一个复杂hook。Django框架将这些看起来很复杂的东西通过暴露出一个简单的使用元类的API将其化简，通过这个API重新创建代码，在背后完成真正的工作。

结语

首先，你知道了类其实是能够创建出类实例的对象。好吧，事实上，类本身也是实例，当然，它们是元类的实例。

	>>>class Foo(object): pass
	>>> id(Foo)
	142630324
Python中的一切都是对象，它们要么是类的实例，要么是元类的实例，除了type。type实际上是它自己的元类，在纯Python环境中这可不是你能够做到的，这是通过在实现层面耍一些小手段做到的。其次，元类是很复杂的。对于非常简单的类，你可能不希望通过使用元类来对类做修改。