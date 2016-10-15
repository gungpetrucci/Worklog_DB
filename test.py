import unittest
from peewee import *
from os import remove
from unittest.mock import patch

from worklog_DB import *






class WorklogTest(unittest.TestCase):

    def setUp(self):
        db = SqliteDatabase('worklog.db')
        db.connect()
        db.create_table(Entry, safe=True)
        Entry.create(entry_id = id_generator(),
                     employee = 'Harin',
                     date = date.today().strftime('%Y%m%d'),
                     taskname = 'Testing',
                     timespent = 10,
                     detail = 'Coding a test file for worklog'
                     )

    def test_data_entry(self):
        self.assertEqual('Harin', Entry.get(Entry.entry_id == 1).employee)
        self.assertEqual('Testing', Entry.get(Entry.entry_id == 1).taskname)
        self.assertEqual(10, Entry.get(Entry.entry_id == 1).timespent)
        self.assertIn('Coding', Entry.get(Entry.entry_id == 1).detail)

    def test_check_id_true(self):
        assert id_check(1) == True
        assert id_check('error') == 2
        assert id_check(999999) == False

    def test_id_generator(self):

        max_id = 0
        for row in Entry:
            if row.entry_id > max_id:
                max_id = row.entry_id
        assert id_generator() == max_id+1

    def test_db_exist(self):
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()


        
                                
        
