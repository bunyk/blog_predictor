import sqlite3
import os

from util import data_file

class Persistence(object):

    def execute(self, *args):
        # print 'execute(%s)' % ', '.join(map(repr, args))
        return self.con.execute(*args)

    def create_db(self, dbfile):
        self.con = sqlite3.connect(
            data_file(dbfile) if dbfile != ':memory:' else dbfile,
        )
        self.execute(
            'create table if not exists '
            'fc(feature, category, count, unique(feature, category))'
        )
        self.execute('create table if not exists '
            'cc(category primary key, count) '
        )

    def fcount(self, feature, category):
        ''' Count feature occurences in category '''
        res = self.execute(
            'select count from fc where feature=? and category=?',
            (feature, category)
        ).fetchone()
        return float(res[0]) if res else 0 

    def incf(self, feature, category):
        ''' Increment counter of pairs feature / category '''
        count = self.fcount(feature, category)
        if count == 0:
            self.execute('insert into fc values (?, ?, 1)',
                (feature, category)
            )
        else:
            self.execute('update fc set count=? '
                'where feature=? and category=?',
                (count + 1, feature, category)
            )

    def incc(self, category):
        ''' Increment category usages '''
        count = self.catcount(category)
        if count == 0:
            self.execute('insert into cc values (?, 1)', (category,))
        else:
            self.execute('update cc set count=? where category=?',
                (count + 1, category)
            )

    def catcount(self, category):
        ''' Get count of samples in category '''
        res = self.execute('select count from cc '
            'where category=?', (category,)
        ).fetchone()
        return float(res[0]) if res else 0

    def categories(self):
        res = self.execute('select category from cc')
        return (d[0] for d in res)

    def totalcount(self):
        ''' Total count of samples in database '''
        res = self.execute('select sum(count) from cc').fetchone()
        return res[0] if res else 0

    def commit(self):
        # print 'commit()'
        self.con.commit()
