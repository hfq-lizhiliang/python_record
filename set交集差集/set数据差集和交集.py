
# coding: utf-8

# In[1]:

some_list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']


# In[2]:

duplicates = []
for value in some_list:
    if some_list.count(value) > 1:
        if value not in duplicates:
            duplicates.append(value)
print duplicates


# In[3]:

# 上面通过for循环处理重读数据，下面使用set来处理


# In[4]:

#交集
valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print input_set.intersection(valid)


# In[ ]:




# In[5]:

#差集
valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print input_set.difference(valid)


# In[ ]:



