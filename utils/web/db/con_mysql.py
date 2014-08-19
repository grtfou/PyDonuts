#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130828
#  @date          20130829
#  @version       1.0
#  @brief         Connect MySQL database by SqlAlchemy.

import sys

class ConnMysql(object):
    import sqlalchemy
    from sqlalchemy.exc import SQLAlchemyError

    ##
    #  @param       (Dict) connection setting
    #  @return      (Object) engine
    #  @return      (Object) connetction
    #  @return      (Object) tables
    #
    def get_conn(self, conn_conf):
        """
        Opened a connection to the given database
        """
        tables = {}
        try:
            connection_str = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
                                conn_conf['driver'], conn_conf['user'],
                                conn_conf['password'], conn_conf['host'],
                                conn_conf['db'], conn_conf['encoding'])

            conf_tables = conn_conf['tables']
        except:
            print("Configure: driver, user, password, host, db, encoding")
            print("=====Connection fail!!=====")
            raise

        try:
            engine = self.sqlalchemy.create_engine(connection_str, strategy='threadlocal',
                                                              pool_recycle=600)
            connection = engine.contextual_connect()

            for tag, table_name in conf_tables.iteritems():
                metadata = self.sqlalchemy.MetaData()
                metadata.bind = engine
                table = self.sqlalchemy.Table(table_name, metadata, autoload=True)
                tables[tag] = table

            return engine, connection, tables
        except self.SQLAlchemyError, detail:
            err_msg = "Error: unable to open connection to {0} on {1}.".format(
                        conn_conf['db'], conn_conf['host'])
            print(err_msg)
            sys.stdout.flush()

    ##
    #  @param       (Dict) engines
    #  @return      (String) text
    #
    def close_conn(self, engines):
        """
        Closed given database connection
        """
        try:
            for engine_name in engines:
                engines[engine_name].contextual_connect().close()
                engines[engine_name].dispose()
                del engines[engine_name]
        except:
            pass

if __name__ == '__main__':
    ### MySql test ###
    from sqlalchemy.sql import *
    MYSQL_SETTING = {'driver': "mysql",
                     'host': "192.168.0.1",
                     'encoding': "utf8",
                     'user': "theuser",
                     'password': "testPWD",
                     'db': "testdb",
                     'tables': {'keywords': 'keywords',
                                'contents': 'contents'}
                    }

    my_test = ConnMysql()
    engine, conn, tables = my_test.get_conn(MYSQL_SETTING)
    # print conn.execute(select([tables['keywords'].c.hash])).fetchone()
    ###-MySql
