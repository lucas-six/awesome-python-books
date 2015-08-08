#!/usr/bin/env python3

# Copyright (c) 2014-2015 Li Yun <leven.cn@gmail.com>
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''Function - 函数

此菜谱包含：

- 函数参数的默认值只计算一次
- 带默认参数的函数
- 从字典、元组或列表中获取函数参数
- 带可变长参数的函数

'''


def f(a, L=[]):
    '''函数参数的默认值只计算一次
    '''
    L.append(a)
    return L

assert f(1) == [1]
assert f(2) == [1 , 2]
assert f(3) == [1, 2, 3]


def func_default_value(arg, L=None):
    '''带默认参数的函数

    由于函数参数的默认值只计算一次,如果有默认值的参数是可改变对象，应该按照此函数定义
    '''
    if L is None:
        L = []
    L.append(arg)
    return L

assert func_default_value(1) == [1]
assert func_default_value(2) == [2]
assert func_default_value(3) == [3]


def func_unpack_args(arg1, arg2):
    '''从字典、元组或列表中获取函数参数

    对于字典：

        mydict = {'arg1': 1, 'arg2': 2}
        func_unpack_args(**mydict)

    对于元组或列表：

        mytuple = ("a", "b")
        func_unpack_args(*mytuple)

    '''
    pass


def func_vargs(arg, other='o', *vargs, **args):
    '''带可变长参数的函数

    1. <code>*vargs</code>参数位置必须在 <code>**args</code>之前.

    2. 任何在<code>*vargs</code>参数A之后的均为关键字参数（不可按参数顺序）

    '''
    # 所有<code>vargs</code>参数都映射为元组(tuple)
    for param in vargs:
        # handle `*vargs`
        pass

    # 所有<code>args</code>参数都映射为有序字典(OrderedDict)
    for key, value in args.items():
        # handle `**args`
        pass


def f(x:int, y:int) -> int:
    '''Function Annotations (Python 3 Only)

    The Python interpreter does not attach any semantic meaning to the attached
    annotations. They are not type checks, nor do they make Python behave any
    differently than it did before. However, they might give useful hints to
    others reading the source code about what you had in mind. Third-party
    tools and frameworks might also attach semantic meaning to the annotations.

    Although you can attach any kind of object to a function as an annotation
    (e.g., numbers, strings, instances, etc.), classes or strings often seem to
    make the most sense.

    Function annotations are merely stored in a function’s `__annotations__`
    attribute.
    '''
    return x + y
