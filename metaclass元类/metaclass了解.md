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

幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类（我知道，某些名字里带有‘class’的东西并不需要是一个class，画画图理解下，这很有帮助）。所以，我们这里就先以一个简单的函数作为例子开始。

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