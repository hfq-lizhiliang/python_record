
# coding: utf-8

# In[2]:

a = ['a','b','c','d','e','f','g','h']


# In[3]:

print a[:4] #前四个


# In[4]:

print a[-4:] #后四个


# In[5]:

print a[3:-3] #第四个到倒数第四个


# 当切片是从头开始的话，下标0可以省略  a[:3] = a[0:3]

# 分片中使用负数对于从后往前的操作很方便。负数的绝对值就是相对于末尾数据的偏移量。所有的形式对于新手而言也都是清晰的。

# In[6]:

a[:]


# In[7]:

a[:5]


# In[8]:

a[:-1]


# In[9]:

a[4:]


# In[10]:

a[-3:]


# In[11]:

a[2:5]


# In[12]:

a[2:-1]


# In[14]:

a[-3:-1]


# 分片机制将自动处理超出集合边界的下标的取值，这也使得建立一个最大长度的输入序列更加的容易。

# In[15]:

a[:20]


# In[16]:

a[-20:]


# 对比起来，直接索引到与上边相同的下标会引发一个异常

# In[17]:

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


# In[18]:

a[8]


# In[19]:

a[:8]


# 对比a[8]和a[:8]的计算结果，发现a[8]数组下标越界了，而a[:8]正常，发生这个异常的原因就在于分片机制下数字是指相对于开始位置的offset（偏移量），而单纯的使用下标的话还是需要遵守列表的访问规则的。

# In[ ]:




# 分片不会改变原始的数据，返回的仍然是一个列表。而原来的列表的值并不会发生变化，对返回的列表进行操作不会影响到原来的列表的值。

# In[20]:

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


# In[21]:

b = a[4:]


# In[22]:

b #原值


# In[23]:

b[1] = 99


# In[24]:

b #后值


# In[25]:

a #切片前


# In[26]:

a[2:7] = [99,22,14]


# In[27]:

a


# 对比上面的赋值结果，发现a在切片赋值后，分片的赋值将会替换切片范围内的空间，切片的赋值长度不必与切片范围一致，就如上面的例子，切片的范围a[2:7]比赋值[99,22,14]的范围大，赋值替换了切片的范围.

# In[28]:

b = a[:]


# In[29]:

b


# 对比上面的结果，如果省略开头索引和结尾索引，就会获得原始列表的拷贝版本。

# In[33]:

b = a


# In[34]:

print 'Before:',a


# In[35]:

a[:] = [101,102,103]


# In[37]:

print 'After:',a


# 当为列表赋值的时候省去开头和结尾下标的时候，将会用这个引用来替换整个列表的内容，而不是创建一个新的列表。同时，引用了这个列表的列表的相关内容，也会跟着发生变化。

# In[ ]:




# In[ ]:



