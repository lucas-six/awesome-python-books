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

'''Test python  connect mysql sqlite3 

'''
from  dbsimpleoperate import createtable,save,fetchall,delete,update
import  uuid

if __name__=='__main__':
    #test mysql connect db operate
    #test for create table
    sql=("""create table user(user_id varchar(36), user_name varchar(128)) """)
    createtable(sql)

    #test for add
    sql='insert into user values(%s,%s)'
    id=str(uuid.uuid1())
    data=(id,'name')
    save(sql,data)

    #test for query
    sql='select * from user'
    result = fetchall(sql)
    for r in result :
        print(r)

    #test for update
    sql ='update user set user_name=%s where user_id =%s'
    data=('myname',id)
    update(sql,data)

    #test for delete
    sql ="delete from user where user_id = '%s'" %id
    delete(sql,'')


    #test sqlite3 connect db operate

    #test for create table
    sql=("""create table user(user_id varchar(36), user_name varchar(128)) """)
    createtable(sql)

    #test for add
    sql='insert into user values(?,?)'
    id=str(uuid.uuid1())
    data=(id,'name')
    save(sql,data)

    #test for query
    sql='select * from user'
    result = fetchall(sql)
    for r in result :
        print(r)

    #test for update
    sql ='update user set user_name=? where user_id =?'
    data=('myname',id)
    update(sql,data)

    #test for delete
    sql ="delete from user where user_id = '%s'" %id
    delete(sql,'')

