# -*- coding: utf-8 -*-
import traceback

import pymysql


class DBHelper(object):

    def __init__(self):
        self.connection = pymysql.connect(host='localhost', port=3307, user='root', password='1qazxsw2', db='spider',
                                          charset='utf8mb4')

    def __del__(self):
        if self.connection:
            self.connection.close()

    def insert(self, item):
        try:
            sql = 'insert into news ' \
                  '(rid,tag,category,publish_time,title,content) values ' \
                  '(%s,%s,%s,%s,%s,%s) on duplicate key update ' \
                  'title=values(title),content=values(content),publish_time=values(publish_time),modified_date=now()'
            insert = (item['id'], item['tag'], item['category'], item['publish_time'], item['title'], item['content'])
            self.connection.cursor().execute(sql, insert)
            self.connection.commit()
        except Exception as e:
            print(traceback.format_exc())
            self.connection.rollback()
