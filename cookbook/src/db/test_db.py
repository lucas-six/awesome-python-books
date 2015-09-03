#!/usr/bin/env python3

# Copyright (c) 2015 xjzhou <xiangjiang3602008@163.com>
# Copyright (c) 2015 Li Yun <leven.cn@gmail.com>
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

'''测试数据库 - MySQL

'''

import sys

import mysql

import db


def test_mysql(func, **args):
    '''测试用例：MySQL数据库操作
    '''
    uid = '123'
    user_name = 'user name'

    try:
        with func(func, args) as conn:
            # 创建表
            conn.execute('CREATE TABLE user(user_id varchar(36), user_name varchar(128))')

            # 新增数据
            conn.execute('INSERT INTO user VALUES(?, ?)', (uid, user_name))

            # 查询数据
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user')
            result = cursor.fetchall()
            print(result)
            
            # 删除数据
            conn.execute('DELETE FROM user WHERE user_id=?', (uid,))
    except sqlite3.OperationalError as err:
        print(err, file=sys.stderr)


if __name__ == '__main__':
    # MySQL
    #arg = ('localhost', 3306, 'test_db', 'admin', '111111')
    #test_mysql(mysql.connector.connect, *arg)
    #test_mysql(db.mysql_connection, *arg)
