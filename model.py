import sqlite3
import os

from util import data_file

class Persistence(object):
    def create_db(self, dbfile):
        self.con = sqlite3.connect(data_file(dbfile))
        self.con.execute('create table if not exists fc(feature, category, count)')
        self.con.execute('create table if not exists cc(category, count)')

    def fcount(self, feature, category):
        ''' Count feature occurences in category '''
        res = self.con.execute(
            'select count from fc where feature="%s" and category="%s"' % (
                feature, category
            )
        ).fetchone()
        return float(res[0]) if res else 0 

    def incf(self, feature, category):
        ''' Increment counter of pairs feature / category '''
        count = self.fcount(feature, category)
        if count == 0:
            self.con.execute('insert into fc values '
                '("%s", "%s", 1)' % (feature, category)
            )
        else:
            self.con.execute('update fc set count=%d '
                'where feature="%s" and category="%s"' % (
                count + 1, feature, category
                )
            )

    def incc(self, category):
        ''' Increment category usages '''
        count = self.catcount(category)
        if count == 0:
            self.con.execute('insert into cc values ("%s", 1)' % category)
        else:
            self.con.execute('update cc set count=%d where category="%s"' % (
                count + 1, category
            ))

    def catcount(self, category):
        ''' Get count of samples in category '''
        res = self.con.execute('select count from cc '
            'where category="%s"' % category
        ).fetchone()
        return float(res[0]) if res else 0

    def totalcount(self):
        ''' Total count of samples in database '''

    def commit(self):
        self.con.commit()

