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

'''Formatting - 格式化字符串

此菜谱包含：

- int类型格式化字符串
- float类型格式化字符串

'''


def int_format():
    '''int类型格式化字符串

    @see format()
    @see bin()
    @see hex()
    @see oct()
    '''
    i = 2

    # 二进制 '0b'
    assert bin(i) == '0b10' == format(i, '#b')  # 前缀
    assert format(i, 'b') == '10'               # 转十进制字符串
    assert format(i, '08b') == '00000010'       # 填充
    assert format(i, '#010b') == '0b00000010'   # 前缀及填充

    # 十六进制 '0x'
    assert hex(i) == '0x2' == format(i, '#x')   # 前缀
    assert format(i, 'x') == '2'                # 转十进制字符串
    assert format(i, '02x') == '02'             # 填充
    assert format(i, '#04x') == '0x02'          # 前缀及填充

    # 八进制 '0o'
    assert oct(i) == '0o2' == format(i, '#o')   # 前缀，Python 2: oct(i) == '02'
    assert format(i, 'o') == '2'                # 转十进制字符串
    assert format(i, '03o') == '002'            # 填充
    assert format(i, '#05o') == '0o002'         # 前缀及填充


def float_format():
    '''float类型格式化字符串
    
    @see format()
    '''
    f = 12345.678

    assert format(f, '0.2f') == '12345.68'      # 两位小数精度
    assert format(f, '>10.2f') == '  12345.68'  # 右对齐
    assert format(f, '<10.2f') == '12345.68  '  # 左对齐
    assert format(f, '^10.2f') == ' 12345.68 '  # 居中对齐
    assert format(f, ',') == '12,345.678'       # 千位分隔符
    assert format(f, '0,.2f') == '12,345.68'    # 千位分隔符加两位小数精度
    assert format(f, 'e') == '1.234568e+04'     # 科学计数法
    assert format(f, '0.2E') == '1.23E+04'      # 科学计数法（两位小数精度）


int_format()
float_format()
