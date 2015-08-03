#!/usr/bin/env python

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

'''循环遍历

此菜谱包含：

- 遍历且更新可变序列（列表），需复制一个序列
- 遍历序列（列表），同时获取索引和值
- 同时遍历多个序列（列表）
- 依次遍历多个序列（列表），无需嵌套循环（代码可读性）

'''


# 遍历且更新可变序列（列表），需复制一个序列
seq = [1, 2, 3, 4, 5, 6]
for s in seq[:]:
    if len(seq) > 6:
        seq.insert(0, s)


# 遍历序列（列表），同时获取索引和值
#
# 内嵌函数enumerate()的参考实现：
#
#    def enumerate(sequence, start=0):
#        n = start
#        for elem in sequence:
#            yield n, elem
#            n += 1
#
# @see enumerate()
seq = [1, 2, 3, 4, 5, 6]
start_index = 1
for index, value in enumerate(seq):
    assert seq[index] == value
for index, value in enumerate(seq, start=start_index):
    assert seq[index-start_index] == value


# 同时遍历多个序列（列表）
#
# @see zip()
# @see itertools.zip_longest()
# NOTE: itertools.izip_longest() in Python 2
seq1 = [1, 2, 3, 4, 5, 6]
seq2 = ['a', 'b', 'c']

for value1, value2 in zip(seq1, seq2):
    assert value1 in seq1
    assert value2 in seq2
    assert seq1.index(value1) == seq2.index(value2)

import itertools
for value1, value2 in itertools.zip_longest(seq1, seq2):
    assert value1 in seq1
    if value2 not in seq2:
        assert value2 is None
        assert seq1.index(value1) >= len(seq2)

fillvalue = 0
for value1, value2 in itertools.zip_longest(seq1, seq2, fillvalue=fillvalue):
    assert value1 in seq1
    if value2 not in seq2:
        assert value2 == fillvalue
        assert seq1.index(value1) >= len(seq2)


# 依次遍历多个序列（列表），无需嵌套循环（代码可读性）
#
# 函数chain()的参考实现：
#
#     def chain(iterators):
#         for i in iterators:
#             yield from i
#
# @see itertools.chain()
seq1 = [1, 2, 3, 4, 5, 6]
seq2 = ['a', 'b', 'c']
for item in itertools.chain(seq1, seq2):
    assert item in seq1 or item in seq2
