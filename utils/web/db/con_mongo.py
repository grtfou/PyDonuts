#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20130828
#  @date          20130829
#  @version       1.0
#  @brief         Connect MongoDB database by PyMongo

import sys

class ConnMongo(object):
    from pymongo import MongoClient
    from pymongo import database as DB

    ##
    #  @param       (Dict) connection setting
    #  @return      (Object) db connetction
    #  @return      (Dict) collections
    #
    def get_conn(self, conn_conf):
        """
        Opened a connection to the given database
        """
        tables = {}
        try:
            conn = self.MongoClient(conn_conf['host'], conn_conf['port'], slave_okay=True)

            db = self.DB.Database(conn, conn_conf['db'])
            db.authenticate(conn_conf['user'], conn_conf['password'])

        except:
            print("Configure: host, port, db, user, password")
            print("=====Connection fail!!=====")
            sys.stdout.flush()
            raise

        tables = {}
        for coll_name in db.collection_names():
            tables[coll_name] = db[coll_name]

        return conn, tables

if __name__ == '__main__':
    ### MongoDB test ###
    MDB_SETTING = {'host': '192.168.0.1',
                   'port' : 27017,
                   'user':'theuser',
                   'password': 'testPWD',
                   'db': 'testdb'
                  }

    my_test2 = ConnMongo()
    db, posts = my_test2.get_conn(MDB_SETTING)
    # print posts['car_color'].find_one()
    ###-MongoDB