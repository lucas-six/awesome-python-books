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

'''Database - SQLite3, MySQL

Including:

- 自定义SQLite3连接上下文管理器
- 自定义MySQL连接上下文管理器

@since Python 3.4.3
'''

from contextlib import contextmanager
import sqlite3
import mysql


@contextmanager
def sqlite3_connection(path):
    '''自定义SQLite3连接上下文管理器

    @param path path to the SQLite3 database file
    '''
    conn = None
    try:
        conn = sqlite3.connect(path)
        yield conn
    except Exception as e :
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.commit()
            conn.close()


@contextmanager
def mysql_connection(host, port=3306, db_name='', charset='utf-8', user_name='', password=''):
    '''自定义MySQL连接上下文管理器

    @param host host of MySQL server
    @param port port of MySQL server
    @param db_name database name
    @param charset charset of database
    @param user_name user name of the database
    @param password password of the database
    '''
    conn = None
    config = {
        'host': host,
        'port': port,
        'database': db_name,
        'charset': charset,
        'user': user_name,
        'password': password
    }
    
    try:
        conn = mysql.connector.connect(**config)
        yield conn
    except Exception as e :
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.commit()
            conn.close(
