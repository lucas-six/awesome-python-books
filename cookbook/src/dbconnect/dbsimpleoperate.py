#!/usr/bin/env python3

# Copyright (c) 2014-2015 xjzhou <xiangjiang3602008@163.com>
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

'''python  mysql sqlite3 connect

Including:

- create table
- add data
- query data
- update data
- delete data


@since Python 3.4.3
'''

from contextlib import contextmanager
import sqlite3
import  mysql.connector

#datebase type you choose
use_database='mysql'

#config for sqlite
sqliteconfig ={'path':'/usr/local/test.db'}

#config for mysql
mysqlconfig={
    'host':'127.0.0.1',
    'user':'root',
    'password':'123456',
    'port':3306,
    'database':'databasename',
    'charset':'utf8'
}

@contextmanager
def getsqliteconn():
    conn=sqlite3.connect(sqliteconfig['path'])
    cursor=conn.cursor()
    try:
        yield cursor
    except Exception as e :
        conn.rollback()
        print(e)
    else :
        conn.commit()
    finally:
        cursor.close()
        conn.close()

@contextmanager
def getmysqlconn():
    conn=mysql.connector.connect(**mysqlconfig)
    mycursor=conn.cursor()
    try:
        yield mycursor
    except mysql.connector.Error as e :
        conn.rollback()
        print(e)
    else :
        conn.commit()
    finally:
        mycursor.close()
        conn.close()

def getConn():
    if use_database =='mysql':
        conn= getmysqlconn()
    else :
        conn = getsqliteconn()
    return conn

def createtable(sql):
    with getConn() as c:
        c.execute(sql)

def save(sql,data):
    with getConn() as c:
        c.execute(sql,data)

def fetchall(sql):
    with getConn() as c:
        c.execute(sql)
        result = c.fetchall()
    return result

def query(sql,data):
    with getConn() as c:
        c.execute(sql,data)
        result=c.fetchall()
        return result

def update(sql,data):
    with getConn() as c:
        c.execute(sql,data)

def delete(sql,data):
    with getConn() as c:
        c.execute(sql,data)

