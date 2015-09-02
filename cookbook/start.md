# 入门
Python 3.4.3+

## 参考资料

- Why I Love Python (2001)
- [Think Python: How to Think Like a Computer Scientist](http://www.greenteapress.com/thinkpython/html/index.html) (适合无编程经验者)
- [Python 3 官方文档](https://docs.python.org/3/) ([中文翻译](http://python.usyiyi.cn/python_343/tutorial/))
- Python Cookbook, 3rd Edition (2013) [中文版](http://python3-cookbook.readthedocs.org/zh_CN/latest/)

## 代码编辑器

- Notepad++ (Windows)

编码方式: 无BOM`UTF-8`.

## Hello World

```python
#!/usr/bin/env python3

print('Hello World')
```

Python 2.7:

```python
#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function

print('Hello World')
```

## 定义变量

```python
i = 1           # 整数 int
type(i).__name__ == 'int'

i = 0xff        # 十六进制整数 int
type(i).__name__ == 'int'

i = 's'         # 字符串 str (utf-8编码)
type(i).__name__ == 'str'

i = "a, 's'"    # 带单引号的字符串 str (utf-8编码)
type(i).__name__ == 'str'

i = 'a, "s"'    # 带双引号的字符串 str (utf-8编码)
type(i).__name__ == 'str'

i = 1.0         # 浮点数 float
type(i).__name__ == 'float'

i = 1.23e9      # 科学计数法浮点数 float
type(i).__name__ == 'float'

i = b'abc'      # 二进制 bytes
type(i).__name__ == 'bytes'

i = True        # 布尔值 真
i = False       # 布尔值 假
type(i).__name__ == 'bool'

i = None        # None
type(i).__name__ == 'NoneType'


# 布尔值判断
if a
if a == True      # Bad!!!
if a is True      # Worse!!!


# 判断是否是None
if a is None
if a is not None
if not a is None  # Bad!!!


# 判断字符串是否为空
if s
if len(s)        # Bad!!!
if len(s) != 0   # Worse!!!
if not len(s)    # Worse!!!


# 多重赋值 （列表、元组、字符串、文件、迭代器、产生器）
a = (1, 2, 3, 4, 5, 6)
a1, a2, a3, a4, a5, a6 = a
assert a1 == 1
assert a2 == 2
assert a3 == 3
assert a4 == 4
assert a5 == 5
assert a6 == 6

# 忽略部分赋值
_, b, *c = record
assert b == 2
assert c == (3, 4, 5, 6)

# 赋值变量过少异常
try:
    v1, v2, v3 = a
except ValueError as err:
    assert str(err) == 'too many values to unpack (expected 3)'

# 赋值变量过多异常
try:
    v1, v2, v3, v4, v5, v6, v7, v8 = a
except ValueError as err:
    assert str(err) == 'need more than 6 values to unpack'
```

## 控制流

```python
# if 语句
if a == 1:
    print('a == 1')
elif a == 2:
    print('a == 2')
else:
    print('a != 1 and a != 2')


# while 语句
i = 0
while i<10:
    print(i)
    i += 1


# for 语句
for i in range(3):
    print(i)
```

## 数据结构

```python
# 列表
i = [1, 2, 3, 4, 5, 6]
type(i).__name__ == 'list'
assert len(i) == 6
assert i[0] == 1
assert i[-1] == 6
assert i[1:3] == [2, 3]
assert i[1:] == [2, 3, 4, 5, 6]
assert i[:3] == [1, 2, 3]
assert i[::2] == [2]
assert i[:] == [1, 2, 3, 4, 5, 6]  # 复制列表
assert 1 in i and 0 not in i  # 判断是否含有某值
i.append(7)
del i[6]
i.sort()  # 进行原址排序

a = [x for x in 'abracadabra' if x not in 'abc']  # 列表表达式
assert a == ['r', 'd', 'r']


# 元组
i = (1, 2, 3, 4, 5, 6)
type(i).__name__ == 'tuple'
assert len(i) == 6
assert i[0] == 1
assert i[-1] == 6
assert i[1:3] == (2, 3)
assert i[1:] == (2, 3, 4, 5, 6)
assert i[:3] == (1, 2, 3)
assert i[::2] == (2,)
assert 1 in i and 0 not in i  # 判断是否含有某值

a = [x for x in 'abracadabra' if x not in 'abc']  # 元组表达式
assert a == ('r', 'd', 'r')


# 判断序列（列表、元组）是否为空
if seq
if len(seq)        # Bad!!!
if len(seq) != 0   # Worse!!!
if not len(seq)    # Worse!!!


# 遍历序列（列表，元组）
seq = [1, 2, 3, 4, 5, 6]
for s in seq:
    pass


# 字典
i = {'a': 1, 'b': 2}
type(i).__name__ == 'dict'
assert len(i) == 2
assert i['a'] == 1


# 遍历字典
i = {'a': 1, 'b': 2}
for key in i:
    pass

for key, value in i.items(): # Python 2: i.iteritems()
    pass


# 集合
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
assert basket == {'orange', 'banana', 'pear', 'apple'}
assert 'orange' in basket  # 判断是否含有某值

a = set('abracadabra') 
b = set('alacazam')
assert a == {'a', 'r', 'b', 'c', 'd'}
a - b   # letters in a but not in b
a | b   # letters in either a or b
a & b   # letters in both a and b
a ^ b   # letters in a or b but not both

a = {x for x in 'abracadabra' if x not in 'abc'}  # 集合表达式
assert a == {'r', 'd'}
```

## 定义函数

```python
def f(a):
    return a

type(f).__name__ == 'function'
```

## 面向对象 (OOP)

```python
class A(object):
    '''A class.

    # Built-in Class Attributes:
    - __name__   : string name of class
    - __doc__    : documentation string
    - __bases__  : tuple of class's base classes
    - __slots__  : list of attribute names (reduce memory)

    # Built-in Instance Attributes:
    - __doc__    : documentation string
    - __class__  : class for instance
    - __module__ : module where class is defined

    # Built-in Methods:
    - __init__() : constructor
    - __str__()  : string representation, str(obj)
    - __len__()  : length, len(obj)
    '''

    # Python does not provide any internal mechanism track how many instances
    # of a class have been created or to keep tabs on what they are. The best
    # way is to keep track of the number of instances using a class attribute.
    num_of_instances = 0

    def __init__(self, a1=None, a2=None):
        A.num_of_instances += 1
        self.public_instance_attribute = a1
        self.private_instance_attribute = a2

    def public_instance_method(self):
        return (A.num_of_instances,
                self.publuc_instance_attribute,
                self.private_instance_attribute)

    def _private_instance_method(self):
        pass

    @staticmethod
    def static_method():
        return A.num_of_instances

    @classmethod
    def class_method(cls):
        return cls.__name__


class B(A):
    '''Subclass of A.
    '''

    def __init__(self, b, a1=None, a2=None):
        super(B, self).__init__(a1, a2)
        self.b = b

    def public_instance_method(self):
        print('Override method of {0}'.format(self.__class__.__bases__[0]))

    def new_method(self):
        print('New method without inheritance from {0}'
                .format(self.__class__.__bases__[0]))


assert isinstance(A(), A)
assert issubclass(B, A)
type(A).__name__ = 'type'
type(A()).__name__ = 'A'
```

## 终端打印

```python
print('stdout')                   # 打印到标准输出流(stdout)

import sys
print('stderr', file=sys.stderr)  # 打印到标准错误流(stderr)
```

## 文件

```python
# 文本文件
#
# 文件是一个Context Manager (with语句)
#
# try:
#     f = open('filename', 'r', encoding='utf-8')
# except OSError as err:
#     import sys
#     print(err, file=sys.stderr)
# try:
#     for line in f:
#         print(line)
# except OSError as err:
#     import sys
#     print(err, file=sys.stderr)
# finally:
#     f.close()
#
try:
    with open('filename', 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
except OSError as err:
    import sys
    print(err, file=sys.stderr)
```
