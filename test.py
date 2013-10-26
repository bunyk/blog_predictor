import unittest


class TestPersistence(unittest.TestCase):
    def setUp(self):
        from model import Persistence
        self.persistence = Persistence()
        self.persistence.create_db('test.db')
        self.persistence.commit()

    def test_empty_feature_count(self):
        self.assertEquals(self.persistence.fcount('viagra', 'spam'), 0)

    def test_increment_feature_count(self):
        self.persistence.incf('viagra', 'spam')
        self.assertEquals(self.persistence.fcount('viagra', 'spam'), 1)

    def test_empty_cat_count(self):
        self.assertEquals(self.persistence.catcount('spam'), 0)

    def test_increment_cat_count(self):
        self.persistence.incc('spam')
        self.assertEquals(self.persistence.catcount('spam'), 1)

    def tearDown(self):
        self.persistence.con.rollback()

if __name__ == '__main__':
    unittest.main()


