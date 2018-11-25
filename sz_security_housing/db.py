import pymysql
import pymysql.cursors
import json
from sz_security_housing.settings import MYSQL as sqlConnConfig

class Mysql(object):
    _conn = None
    _cursor = None

    def __init__(self):
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()
    
    def __getConn(self):
        if self._conn is None:
            conn = pymysql.Connect(
                host = sqlConnConfig["host"],
                port = sqlConnConfig["port"],
                user = sqlConnConfig["user"],
                password = sqlConnConfig["password"],
                db = sqlConnConfig["db"],
                charset = sqlConnConfig["charset"]
            )
        return conn

    def getAll(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)

        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False

        return result

    def insertOne(self, sql, value):
        self._cursor.execute(sql,value)
        return self.__getInsertId()
    
    def insertMany(self,sql,values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql,values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("select last_insert_id()")
        result = self._cursor.fetchall()
        return result[0][0]
 
    def __query(self,sql,param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        return count

    def update(self,sql,param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)
 
    def delete(self,sql,param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)
 
    def end(self,option='commit'):
        """
        @summary: 结束事务
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()